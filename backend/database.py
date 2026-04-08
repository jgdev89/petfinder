from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de conexión a la base de datos
# os.getenv() lee la variable de entorno DATABASE_URL si existe (definida en docker-compose.yml)
# Si no existe (por ejemplo en local sin Docker), usa el valor por defecto
# Formato: driver://usuario:contraseña@host:puerto/nombre_bd
# "db" es el nombre del servicio MySQL en Docker Compose, no localhost
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://petfinder_user:petfinder_pass@db:3306/petfinder")

# Crea el motor de conexión a la BD
# Es el objeto central de SQLAlchemy — gestiona el pool de conexiones
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones: cada sesión es una "conversación" con la BD
# autocommit=False → los cambios no se guardan solos, hay que hacer commit() explícito
# autoflush=False  → no sincroniza automáticamente los objetos pendientes antes de cada query
# bind=engine      → asocia las sesiones a nuestro motor de conexión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredan todos los modelos (tablas)
# SQLAlchemy la usa para registrar y relacionar los modelos entre sí
Base = declarative_base()

# Función generadora que provee una sesión de BD a cada endpoint que la necesite
# Se usa como dependencia en FastAPI: def mi_endpoint(db: Session = Depends(get_db))
def get_db():
    db = SessionLocal()  # Abre una nueva sesión
    try:
        yield db          # Cede la sesión al endpoint (aquí se ejecuta la lógica)
    finally:
        db.close()        # Se ejecuta siempre al terminar, tanto si hubo error como si no