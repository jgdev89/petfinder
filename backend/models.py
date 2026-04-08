# Importamos todos los tipos de columna que vamos a usar en los modelos
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship  # Para definir relaciones entre tablas
from sqlalchemy.sql import func          # Para funciones SQL como NOW()
from database import Base               # Clase base de la que heredan todos los modelos

# ─── TABLA: usuarios ────────────────────────────────────────────────────────────
class Usuario(Base):
    __tablename__ = "usuarios"

    id             = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String(100), nullable=False)
    email          = Column(String(255), unique=True, nullable=False)  # Único: no pueden repetirse
    password       = Column(String(255), nullable=False)               # Guardado con bcrypt, nunca en plano
    telefono       = Column(String(20))                                # Opcional (no tiene nullable=False)
    fecha_registro = Column(DateTime, default=func.now())              # Se rellena automáticamente al crear

    # Relación uno a muchos: un usuario puede tener varias mascotas publicadas
    # back_populates conecta esta relación con la del modelo Mascota
    mascotas = relationship("Mascota", back_populates="usuario")


# ─── TABLA: mascotas ────────────────────────────────────────────────────────────
class Mascota(Base):
    __tablename__ = "mascotas"

    id          = Column(Integer, primary_key=True, index=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Clave foránea → usuarios.id

    # Enum: solo acepta estos dos valores exactos a nivel de BD
    tipo        = Column(Enum("perdida", "encontrada"), nullable=False)

    nombre      = Column(String(100))           # Opcional: la mascota puede no tener nombre conocido
    especie     = Column(String(50), nullable=False)
    raza        = Column(String(100))
    color       = Column(String(100))
    descripcion = Column(Text)                  # Text permite textos largos, String tiene límite

    provincia   = Column(String(100), nullable=False)
    localidad   = Column(String(100), nullable=False)

    fecha_suceso     = Column(Date, nullable=False)                     # Solo fecha, sin hora
    estado           = Column(Enum("activo", "resuelto"), default="activo")
    fecha_publicacion = Column(DateTime, default=func.now())

    # Relación inversa con Usuario (muchos a uno)
    usuario  = relationship("Usuario", back_populates="mascotas")

    # Relación uno a muchos con Imagen: una mascota puede tener varias fotos
    imagenes = relationship("Imagen", back_populates="mascota")


# ─── TABLA: imagenes ────────────────────────────────────────────────────────────
class Imagen(Base):
    __tablename__ = "imagenes"

    id         = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)  # A qué mascota pertenece
    url        = Column(String(500), nullable=False)   # Ruta del archivo en /uploads/
    es_principal = Column(Boolean, default=False)      # Marca cuál es la foto principal de la publicación
    fecha_subida = Column(DateTime, default=func.now())

    # Relación inversa con Mascota
    mascota = relationship("Mascota", back_populates="imagenes")


# ─── TABLA: mensajes ────────────────────────────────────────────────────────────
class Mensaje(Base):
    __tablename__ = "mensajes"

    id              = Column(Integer, primary_key=True, index=True)

    # Dos claves foráneas al mismo modelo (Usuario): remitente y destinatario
    remitente_id    = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    destinatario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Opcional: el mensaje puede o no estar vinculado a una mascota concreta
    mascota_id  = Column(Integer, ForeignKey("mascotas.id"))

    asunto      = Column(String(200), nullable=False)
    contenido   = Column(Text, nullable=False)
    leido       = Column(Boolean, default=False)   # Para marcar mensajes no leídos
    fecha_envio = Column(DateTime, default=func.now())


# ─── TABLA: tokens_reseteo ──────────────────────────────────────────────────────
class TokenReseteo(Base):
    __tablename__ = "tokens_reseteo"

    id         = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    token      = Column(String(255), unique=True, nullable=False)  # Token único generado al pedir reseteo
    expira     = Column(DateTime, nullable=False)   # Fecha límite: el token caduca pasado ese momento
    usado      = Column(Boolean, default=False)     # Evita que el mismo token se use dos veces