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