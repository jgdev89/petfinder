import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(prefix="/imagenes", tags=["imagenes"])

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/mascota/{mascota_id}")
async def subir_imagen(
    mascota_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa JPG, PNG o WEBP")

    contenido = await file.read()
    if len(contenido) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="La imagen no puede superar 5MB")

    extension = file.filename.split(".")[-1].lower()
    nombre_archivo = f"{uuid.uuid4()}.{extension}"
    ruta_disco = os.path.join(UPLOAD_DIR, nombre_archivo)

    with open(ruta_disco, "wb") as f:
        f.write(contenido)

    # La primera imagen subida será la principal
    num_imagenes = db.query(models.Imagen).filter(models.Imagen.mascota_id == mascota_id).count()
    es_principal = num_imagenes == 0

    nueva_imagen = models.Imagen(
        mascota_id=mascota_id,
        url=f"/uploads/{nombre_archivo}",
        es_principal=es_principal
    )
    db.add(nueva_imagen)
    db.commit()
    db.refresh(nueva_imagen)

    return {
        "id": nueva_imagen.id,
        "url": nueva_imagen.url,
        "es_principal": nueva_imagen.es_principal
    }


@router.get("/mascota/{mascota_id}")
def listar_imagenes(mascota_id: int, db: Session = Depends(get_db)):
    return db.query(models.Imagen)\
        .filter(models.Imagen.mascota_id == mascota_id)\
        .order_by(models.Imagen.es_principal.desc())\
        .all()


@router.delete("/{imagen_id}")
def eliminar_imagen(imagen_id: int, db: Session = Depends(get_db)):
    imagen = db.query(models.Imagen).filter(models.Imagen.id == imagen_id).first()
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    # Borrar archivo del disco
    ruta_disco = imagen.url.lstrip("/")
    if os.path.exists(ruta_disco):
        os.remove(ruta_disco)

    db.delete(imagen)
    db.commit()
    return {"detail": "Imagen eliminada"}