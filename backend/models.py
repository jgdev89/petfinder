from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    telefono = Column(String(20))
    fecha_registro = Column(DateTime, default=func.now())

    mascotas = relationship("Mascota", back_populates="usuario")


class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(Enum("perdida", "encontrada"), nullable=False)
    nombre = Column(String(100))
    especie = Column(String(50), nullable=False)
    raza = Column(String(100))
    color = Column(String(100))
    descripcion = Column(Text)
    provincia = Column(String(100), nullable=False)
    localidad = Column(String(100), nullable=False)
    fecha_suceso = Column(Date, nullable=False)
    estado = Column(Enum("activo", "resuelto"), default="activo")
    fecha_publicacion = Column(DateTime, default=func.now())

    usuario = relationship("Usuario", back_populates="mascotas")
    imagenes = relationship("Imagen", back_populates="mascota")


class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    url = Column(String(500), nullable=False)
    es_principal = Column(Boolean, default=False)
    fecha_subida = Column(DateTime, default=func.now())

    mascota = relationship("Mascota", back_populates="imagenes")


class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    remitente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    destinatario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    asunto = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    leido = Column(Boolean, default=False)
    fecha_envio = Column(DateTime, default=func.now())

class TokenReseteo(Base):
    __tablename__ = "tokens_reseteo"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expira = Column(DateTime, nullable=False)
    usado = Column(Boolean, default=False)