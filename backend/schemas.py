from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# Los schemas definen la "forma" de los datos que entran y salen de la API.
# Son distintos de los modelos (models.py) — los modelos representan tablas en BD,
# los schemas representan qué datos se exponen o se aceptan por HTTP.


# --- Usuarios ---

# Schema para CREAR un usuario (datos que manda el frontend al registrarse)
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr        # EmailStr valida automáticamente que sea un email válido
    password: str          # Llega en plano, se hashea en el router antes de guardar
    telefono: Optional[str] = None  # Campo opcional, si no se manda vale None

# Schema para DEVOLVER un usuario (datos que la API envía al frontend)
# Nótese que NO incluye password — nunca se devuelve al cliente
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]
    fecha_registro: datetime

    class Config:
        from_attributes = True  # Permite crear este schema desde un objeto SQLAlchemy directamente


# --- Mascotas ---

# Schema para CREAR una publicación de mascota
class MascotaCreate(BaseModel):
    tipo: str              # "perdida" o "encontrada"
    nombre: Optional[str] = None
    especie: str           # "perro", "gato", etc.
    raza: Optional[str] = None
    color: Optional[str] = None
    descripcion: Optional[str] = None
    provincia: str
    localidad: str
    fecha_suceso: date     # Solo fecha, sin hora

# Schema para DEVOLVER una imagen asociada a una mascota
class ImagenResponse(BaseModel):
    id: int
    url: str               # Ruta relativa: /uploads/nombre.jpg
    es_principal: bool     # Indica si es la foto de portada de la publicación

    class Config:
        from_attributes = True

# Schema para DEVOLVER una mascota completa (incluye sus imágenes anidadas)
class MascotaResponse(BaseModel):
    id: int
    usuario_id: int        # Quién publicó la mascota
    tipo: str
    nombre: Optional[str]
    especie: str
    raza: Optional[str]
    color: Optional[str]
    descripcion: Optional[str]
    provincia: str
    localidad: str
    fecha_suceso: date
    estado: str            # "activa", "resuelta", etc.
    fecha_publicacion: datetime
    imagenes: list[ImagenResponse] = []  # Lista de fotos asociadas (puede estar vacía)

    class Config:
        from_attributes = True


# --- Mensajes ---

# Schema para ENVIAR un mensaje a otro usuario
class MensajeCreate(BaseModel):
    destinatario_id: int
    mascota_id: Optional[int] = None  # Puede ir asociado a una publicación concreta o no
    asunto: str
    contenido: str

# Schema para DEVOLVER un mensaje (incluye metadatos como remitente y fecha)
class MensajeResponse(BaseModel):
    id: int
    remitente_id: int
    destinatario_id: int
    mascota_id: Optional[int]
    asunto: str
    contenido: str
    leido: bool            # Para marcar mensajes como leídos/no leídos
    fecha_envio: datetime

    class Config:
        from_attributes = True


# --- Reseteo de contraseña ---

# Schema para el paso 1: el usuario manda su email para recibir el enlace
class SolicitarReseteo(BaseModel):
    email: EmailStr

# Schema para el paso 2: el usuario manda el token del email + su nueva contraseña
class ResetearPassword(BaseModel):
    token: str             # Token único generado al solicitar el reseteo (llega por URL desde el email)
    nueva_password: str