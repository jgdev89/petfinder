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

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/registro", response_model=schemas.UsuarioResponse)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    password_hash = pwd_context.hash(usuario.password)
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=password_hash,
        telefono=usuario.telefono
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()
    if not usuario or not pwd_context.verify(form_data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    token = crear_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me/perfil", response_model=schemas.UsuarioResponse)
def mi_perfil(usuario_actual: models.Usuario = Depends(get_usuario_actual)):
    return usuario_actual

@router.get("/me/mascotas", response_model=list[schemas.MascotaResponse])
def mis_mascotas(db: Session = Depends(get_db), usuario_actual: models.Usuario = Depends(get_usuario_actual)):
    return db.query(models.Mascota)\
        .options(joinedload(models.Mascota.imagenes))\
        .filter(models.Mascota.usuario_id == usuario_actual.id)\
        .order_by(models.Mascota.fecha_publicacion.desc())\
        .all()

@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/solicitar-reseteo")
def solicitar_reseteo(datos: schemas.SolicitarReseteo, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == datos.email).first()
    if not usuario:
        return {"mensaje": "Si el email existe, recibirás un enlace en breve."}

    # Invalidar tokens anteriores
    db.query(models.TokenReseteo).filter(
        models.TokenReseteo.usuario_id == usuario.id,
        models.TokenReseteo.usado == False
    ).update({"usado": True})
    db.commit()

    # Generar token y guardarlo
    token = secrets.token_urlsafe(32)
    expira = datetime.utcnow() + timedelta(hours=1)
    nuevo_token = models.TokenReseteo(
        usuario_id=usuario.id,
        token=token,
        expira=expira
    )
    db.add(nuevo_token)
    db.commit()

    # Enviar email
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    enlace = f"{frontend_url}/resetear-password?token={token}"

    mensaje = Mail(
        from_email=os.getenv("EMAIL_REMITENTE"),
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
        raise HTTPException(status_code=500, detail="Error al enviar el email")

    return {"mensaje": "Si el email existe, recibirás un enlace en breve."}

@router.post("/resetear-password")
def resetear_password(datos: schemas.ResetearPassword, db: Session = Depends(get_db)):
    token_db = db.query(models.TokenReseteo).filter(
        models.TokenReseteo.token == datos.token,
        models.TokenReseteo.usado == False,
        models.TokenReseteo.expira > datetime.utcnow()
    ).first()

    if not token_db:
        raise HTTPException(status_code=400, detail="El enlace no es válido o ha caducado.")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == token_db.usuario_id).first()
    usuario.password = pwd_context.hash(datos.nueva_password)
    token_db.usado = True
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente."}