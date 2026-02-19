from fastapi import FastAPI
from database import engine
import models
from routers import usuarios

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PetFinder API")

app.include_router(usuarios.router)

@app.get("/")
def root():
    return {"message": "PetFinder API funcionando"}