from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# --- Usuarios ---

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    telefono: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]
    fecha_registro: datetime

    class Config:
        from_attributes = True


# --- Mascotas ---

class MascotaCreate(BaseModel):
    tipo: str
    nombre: Optional[str] = None
    especie: str
    raza: Optional[str] = None
    color: Optional[str] = None
    descripcion: Optional[str] = None
    provincia: str
    localidad: str
    fecha_suceso: date

class MascotaResponse(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    nombre: Optional[str]
    especie: str
    raza: Optional[str]
    color: Optional[str]
    descripcion: Optional[str]
    provincia: str
    localidad: str
    fecha_suceso: date
    estado: str
    fecha_publicacion: datetime

    class Config:
        from_attributes = True


# --- Mensajes ---

# Lo que envía el frontend al crear un mensaje.
# Solo necesita el contenido y a qué mascota y destinatario va dirigido.
class MensajeCreate(BaseModel):
    destinatario_id: int
    mascota_id: Optional[int] = None
    asunto: str
    contenido: str

# Lo que devuelve el backend al consultar mensajes.
# Incluye todos los campos más los generados automáticamente (id, fecha, leido).
class MensajeResponse(BaseModel):
    id: int
    remitente_id: int
    destinatario_id: int
    mascota_id: Optional[int]
    asunto: str
    contenido: str
    leido: bool
    fecha_envio: datetime

    class Config:
        from_attributes = True