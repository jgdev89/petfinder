from datetime import datetime, timedelta
from jose import JWTError, jwt                            # python-jose: librería para crear y verificar JWT
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer         # Esquema de seguridad Bearer token
from sqlalchemy.orm import Session
from database import get_db
import models

# Clave secreta para firmar los tokens — en producción debería ser larga, aleatoria y guardada en variable de entorno
SECRET_KEY = "petfinder_secret_key_cambiar_en_produccion"

# Algoritmo de firma del JWT (HMAC con SHA-256, el más común)
ALGORITHM = "HS256"

# Tiempo de expiración del token: 24 horas
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Le dice a FastAPI dónde está el endpoint de login para obtener el token
# Los endpoints protegidos usarán esto para extraer el token del header: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")


def crear_token(data: dict):
    to_encode = data.copy()

    # Calculamos la fecha exacta de expiración y la añadimos al payload del token
    # "exp" es un campo estándar de JWT que python-jose verifica automáticamente
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Firmamos y codificamos el token con la clave secreta
    # El resultado es un string: header.payload.firma (Base64)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Dependencia que protege los endpoints — se usa así en los routers:
# def mi_endpoint(usuario = Depends(get_usuario_actual))
def get_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    # Preparamos el error que devolveremos en cualquier caso de fallo
    # Usamos el mismo error genérico siempre para no dar pistas sobre qué falló exactamente
    credenciales_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},  # Cabecera estándar que indica al cliente cómo autenticarse
    )

    try:
        # Decodificamos y verificamos el token (firma + expiración)
        # Si el token está manipulado o expirado, lanza JWTError automáticamente
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # "sub" (subject) es el campo estándar JWT donde guardamos el ID del usuario
        usuario_id: int = payload.get("sub")
        if usuario_id is None:
            raise credenciales_error

    except JWTError:
        raise credenciales_error

    # Buscamos el usuario en la BD para confirmar que sigue existiendo
    # Un token válido no garantiza que el usuario no haya sido eliminado desde que se emitió
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise credenciales_error

    # Devolvemos el objeto usuario completo — estará disponible en el endpoint protegido
    return usuario