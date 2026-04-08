# Importaciones de FastAPI y sus utilidades
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine
import models

# Importamos todos los routers (cada uno gestiona una parte de la API)
from routers import usuarios, mascotas, mensajes, imagenes

# Crea todas las tablas en la BD si no existen todavía
# Usa los modelos definidos en models.py como referencia
models.Base.metadata.create_all(bind=engine)

# Instancia principal de la aplicación FastAPI
app = FastAPI(title="PetFinder API")

# Configuración de CORS (Cross-Origin Resource Sharing)
# Necesario porque el frontend (puerto 5173) y el backend (puerto 8000) son orígenes distintos
# Sin esto, el navegador bloquearía las peticiones del frontend al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la carpeta "uploads" como ruta estática
# Las imágenes subidas serán accesibles en: http://localhost:8000/uploads/nombre.jpg
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Registramos cada router en la app
# Cada uno añade sus propios endpoints con su prefijo y lógica
app.include_router(usuarios.router)
app.include_router(mascotas.router)
app.include_router(mensajes.router)
app.include_router(imagenes.router)

# Endpoint raíz — sirve para comprobar que la API está levantada
@app.get("/")
def root():
    return {"message": "PetFinder API funcionando"}