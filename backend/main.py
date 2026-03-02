from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine
import models
from routers import usuarios, mascotas, mensajes, imagenes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PetFinder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir imágenes como archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(usuarios.router)
app.include_router(mascotas.router)
app.include_router(mensajes.router)
app.include_router(imagenes.router)

@app.get("/")
def root():
    return {"message": "PetFinder API funcionando"}