from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Mensaje, Usuario
from schemas import MensajeCreate, MensajeResponse
from auth import get_usuario_actual
from typing import List

router = APIRouter(prefix="/mensajes", tags=["mensajes"])


# Envía un mensaje nuevo.
# Requiere autenticación — el remitente es el usuario logueado.
@router.post("/", response_model=MensajeResponse)
def enviar_mensaje(
    mensaje: MensajeCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)
):
    # Comprobamos que el destinatario existe.
    destinatario = db.query(Usuario).filter(Usuario.id == mensaje.destinatario_id).first()
    if not destinatario:
        raise HTTPException(status_code=404, detail="Destinatario no encontrado")

    # No permitimos que un usuario se envíe mensajes a sí mismo.
    if mensaje.destinatario_id == usuario_actual.id:
        raise HTTPException(status_code=400, detail="No puedes enviarte un mensaje a ti mismo")

    nuevo_mensaje = Mensaje(
        remitente_id=usuario_actual.id,
        destinatario_id=mensaje.destinatario_id,
        mascota_id=mensaje.mascota_id,
        asunto=mensaje.asunto,
        contenido=mensaje.contenido
    )
    db.add(nuevo_mensaje)
    db.commit()
    db.refresh(nuevo_mensaje)
    return nuevo_mensaje


# Devuelve los mensajes recibidos por el usuario logueado.
@router.get("/recibidos", response_model=List[MensajeResponse])
def mensajes_recibidos(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)
):
    mensajes = db.query(Mensaje).filter(
        Mensaje.destinatario_id == usuario_actual.id
    ).order_by(Mensaje.fecha_envio.desc()).all()
    return mensajes


# Marca un mensaje como leído.
# Solo el destinatario puede marcarlo.
@router.patch("/{mensaje_id}/leido", response_model=MensajeResponse)
def marcar_leido(
    mensaje_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)
):
    mensaje = db.query(Mensaje).filter(Mensaje.id == mensaje_id).first()
    if not mensaje:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    if mensaje.destinatario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para marcar este mensaje")

    mensaje.leido = True
    db.commit()
    db.refresh(mensaje)
    return mensaje