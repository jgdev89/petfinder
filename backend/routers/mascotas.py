from auth import get_usuario_actual
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models, schemas
from typing import Optional

router = APIRouter(prefix="/mascotas", tags=["mascotas"])

@router.post("/", response_model=schemas.MascotaResponse)
def crear_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(get_db), usuario_actual: models.Usuario = Depends(get_usuario_actual)):
    nueva_mascota = models.Mascota(**mascota.model_dump(), usuario_id=usuario_actual.id)
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota

@router.get("/", response_model=list[schemas.MascotaResponse])
def listar_mascotas(
    tipo: Optional[str] = None,
    especie: Optional[str] = None,
    provincia: Optional[str] = None,
    nombre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Mascota)
    if tipo:
        query = query.filter(models.Mascota.tipo == tipo)
    if especie:
        query = query.filter(models.Mascota.especie == especie)
    if provincia:
        query = query.filter(models.Mascota.provincia == provincia)
    # ilike hace la búsqueda sin distinguir mayúsculas/minúsculas.
    # El % antes y después significa "cualquier cosa antes y después del texto".
    # Así "lei" encuentra "Leia", "LEI", "pleiades", etc.
    if nombre:
        query = query.filter(models.Mascota.nombre.ilike(f"%{nombre}%"))
    return query.options(joinedload(models.Mascota.imagenes)).all()

@router.get("/{mascota_id}", response_model=schemas.MascotaResponse)
def obtener_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota)\
    .options(joinedload(models.Mascota.imagenes))\
    .filter(models.Mascota.id == mascota_id)\
    .first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

@router.patch("/{mascota_id}/resolver")
def resolver_caso(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    mascota.estado = "resuelto"
    db.commit()
    return {"message": "Caso marcado como resuelto"}

@router.put("/{mascota_id}", response_model=schemas.MascotaResponse)
def editar_mascota(mascota_id: int, datos: schemas.MascotaCreate, db: Session = Depends(get_db), usuario_actual: models.Usuario = Depends(get_usuario_actual)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    if mascota.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta mascota")
    for campo, valor in datos.model_dump().items():
        setattr(mascota, campo, valor)
    db.commit()
    db.refresh(mascota)
    return mascota

@router.delete("/{mascota_id}")
def eliminar_mascota(mascota_id: int, db: Session = Depends(get_db), usuario_actual: models.Usuario = Depends(get_usuario_actual)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    if mascota.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta mascota")
    db.delete(mascota)
    db.commit()
    return {"message": "Mascota eliminada correctamente"}