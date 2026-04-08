import os
import secrets
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi.security import OAuth2PasswordRequestForm
from auth import crear_token, get_usuario_actual
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models, schemas
from passlib.context import CryptContext

# Router con prefijo /usuarios — todos los endpoints de este archivo empiezan por /usuarios
router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# Contexto de hashing para contraseñas
# bcrypt es el algoritmo — internamente genera un salt aleatorio en cada hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─── REGISTRO ────────────────────────────────────────────────────────────────

@router.post("/registro", response_model=schemas.UsuarioResponse)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Comprobamos si ya existe un usuario con ese email antes de crearlo
    existe = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Nunca guardamos la contraseña en plano — la hasheamos con bcrypt
    password_hash = pwd_context.hash(usuario.password)

    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=password_hash,
        telefono=usuario.telefono
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  # Recarga el objeto desde la BD para obtener el id generado
    return nuevo_usuario


# ─── LOGIN ────────────────────────────────────────────────────────────────────

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm espera los campos "username" y "password" en el body
    # Usamos "username" como campo de email (convención de OAuth2)
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()

    # Verificamos que el usuario existe Y que la contraseña coincide con el hash
    # Ambas comprobaciones en el mismo if para no revelar si el email existe o no
    if not usuario or not pwd_context.verify(form_data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    # Generamos el JWT con el id del usuario como "subject" del token
    token = crear_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}


# ─── PERFIL DEL USUARIO AUTENTICADO ──────────────────────────────────────────

@router.get("/me/perfil", response_model=schemas.UsuarioResponse)
def mi_perfil(usuario_actual: models.Usuario = Depends(get_usuario_actual)):
    # get_usuario_actual lee el JWT de la cabecera y devuelve el usuario de la BD
    # Si el token no es válido o ha expirado, lanza un 401 automáticamente
    return usuario_actual


# ─── MASCOTAS DEL USUARIO AUTENTICADO ────────────────────────────────────────

@router.get("/me/mascotas", response_model=list[schemas.MascotaResponse])
def mis_mascotas(db: Session = Depends(get_db), usuario_actual: models.Usuario = Depends(get_usuario_actual)):
    return (
        db.query(models.Mascota)                                      # Consulta a la tabla Mascota
        .options(joinedload(models.Mascota.imagenes))                 # Carga las imágenes asociadas en el mismo query (evita N+1)
        .filter(models.Mascota.usuario_id == usuario_actual.id)       # Solo las mascotas del usuario logueado
        .order_by(models.Mascota.fecha_publicacion.desc())            # Ordenadas de más reciente a más antigua
        .all()                                                        # Ejecuta la query y devuelve lista
)


# ─── OBTENER USUARIO POR ID (público) ────────────────────────────────────────

@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# ─── SOLICITAR RESETEO DE CONTRASEÑA ─────────────────────────────────────────

@router.post("/solicitar-reseteo")
def solicitar_reseteo(datos: schemas.SolicitarReseteo, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == datos.email).first()

    # Si el email no existe, devolvemos el mismo mensaje que si existe
    # Esto evita el "email enumeration" — que alguien pueda saber qué emails están registrados
    if not usuario:
        return {"mensaje": "Si el email existe, recibirás un enlace en breve."}

    # Invalidamos cualquier token de reseteo anterior que no se haya usado
    # Así solo puede haber un enlace válido activo a la vez
    db.query(models.TokenReseteo).filter(
        models.TokenReseteo.usuario_id == usuario.id,
        models.TokenReseteo.usado == False
    ).update({"usado": True})
    db.commit()

    # Generamos un token criptográficamente seguro (32 bytes = 43 caracteres en base64url)
    token = secrets.token_urlsafe(32)
    expira = datetime.utcnow() + timedelta(hours=1)  # Caduca en 1 hora

    nuevo_token = models.TokenReseteo(
        usuario_id=usuario.id,
        token=token,
        expira=expira
    )
    db.add(nuevo_token)
    db.commit()

    # Construimos el enlace que recibirá el usuario por email
    # El token va como query param: /resetear-password?token=xxxx
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    enlace = f"{frontend_url}/resetear-password?token={token}"

    mensaje = Mail(
        from_email=os.getenv("EMAIL_REMITENTE"),   # Remitente definido en variables de entorno
        to_emails=usuario.email,
        subject="Recuperar contraseña - PetFinder",
        html_content=f"""
            <h2>Recuperar contraseña</h2>
            <p>Hola {usuario.nombre}, hemos recibido una solicitud para restablecer tu contraseña.</p>
            <p><a href="{enlace}">Haz clic aquí para crear una nueva contraseña</a></p>
            <p>El enlace caduca en 1 hora. Si no solicitaste esto, ignora este email.</p>
        """
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(mensaje)
    except Exception as e:
        # Si SendGrid falla, lanzamos un 500 — el token ya está guardado pero el email no llegó
        raise HTTPException(status_code=500, detail="Error al enviar el email")

    return {"mensaje": "Si el email existe, recibirás un enlace en breve."}


# ─── RESETEAR CONTRASEÑA ──────────────────────────────────────────────────────

@router.post("/resetear-password")
def resetear_password(datos: schemas.ResetearPassword, db: Session = Depends(get_db)):
    # Buscamos el token en la BD comprobando tres condiciones a la vez:
    # 1. Que el token coincida exactamente
    # 2. Que no haya sido usado ya
    # 3. Que no haya expirado
    token_db = db.query(models.TokenReseteo).filter(
        models.TokenReseteo.token == datos.token,
        models.TokenReseteo.usado == False,
        models.TokenReseteo.expira > datetime.utcnow()
    ).first()

    if not token_db:
        raise HTTPException(status_code=400, detail="El enlace no es válido o ha caducado.")

    # Actualizamos la contraseña del usuario con el nuevo hash
    usuario = db.query(models.Usuario).filter(models.Usuario.id == token_db.usuario_id).first()
    usuario.password = pwd_context.hash(datos.nueva_password)

    # Marcamos el token como usado para que no pueda reutilizarse
    token_db.usado = True
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente."}