# Router de mascotas — gestiona todos los endpoints relacionados con publicaciones
# de mascotas perdidas o encontradas.

from auth import get_usuario_actual
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models, schemas
import requests  # Para llamar a la API de Nominatim y obtener coordenadas
from typing import Optional

router = APIRouter(prefix="/mascotas", tags=["mascotas"])


def geocodificar(localidad: str, provincia: str) -> tuple[str, str] | None:
    """
    Convierte una localidad y provincia en coordenadas geográficas
    usando la API gratuita de Nominatim (OpenStreetMap).
    Devuelve una tupla (latitud, longitud) como strings, o None si falla.
    """
    query = f"{localidad}, {provincia}, España"
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    # Nominatim requiere un User-Agent identificativo para no ser bloqueado
    headers = {"User-Agent": "PetFinder-TFG/1.0"}

    try:
        respuesta = requests.get(url, params=params, headers=headers, timeout=5)
        datos = respuesta.json()
        if datos:
            return datos[0]["lat"], datos[0]["lon"]
    except Exception:
        # Si falla la geocodificación, simplemente no guardamos coordenadas
        pass

    return None


# ─── POST /mascotas/ — Crear nueva publicación ──────────────────────────────────
@router.post("/", response_model=schemas.MascotaResponse)
def crear_mascota(
    mascota: schemas.MascotaCreate,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(get_usuario_actual)
):
    # Convertimos el schema a diccionario para poder modificarlo
    datos = mascota.model_dump()

    # Intentamos geocodificar la localidad y provincia
    # Si falla, latitud y longitud quedan como None en la BD
    coords = geocodificar(datos["localidad"], datos["provincia"])
    if coords:
        datos["latitud"], datos["longitud"] = coords

    # Creamos el objeto mascota con los datos del formulario + el ID del usuario
    nueva_mascota = models.Mascota(**datos, usuario_id=usuario_actual.id)
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota


# ─── GET /mascotas/ — Listar mascotas con filtros opcionales ────────────────────
@router.get("/", response_model=list[schemas.MascotaResponse])
def listar_mascotas(
    tipo: Optional[str] = None,
    especie: Optional[str] = None,
    provincia: Optional[str] = None,
    nombre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Empezamos con una query sobre toda la tabla mascotas
    query = db.query(models.Mascota)

    # Aplicamos los filtros solo si tienen valor (si el usuario los ha seleccionado)
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

    # joinedload carga las imágenes de cada mascota en la misma consulta SQL
    # evitando el problema N+1 (una query por cada mascota)
    return query.options(joinedload(models.Mascota.imagenes)).all()


# ─── GET /mascotas/{id} — Obtener una mascota por ID ───────────────────────────
@router.get("/{mascota_id}", response_model=schemas.MascotaResponse)
def obtener_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = (
        db.query(models.Mascota)
        .options(joinedload(models.Mascota.imagenes))
        .filter(models.Mascota.id == mascota_id)
        .first()
    )
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota


# ─── PATCH /mascotas/{id}/resolver — Marcar caso como resuelto ─────────────────
@router.patch("/{mascota_id}/resolver")
def resolver_caso(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Cambiamos el estado a "resuelto" y guardamos
    mascota.estado = "resuelto"
    db.commit()
    return {"message": "Caso marcado como resuelto"}


# ─── PUT /mascotas/{id} — Editar una mascota existente ─────────────────────────
@router.put("/{mascota_id}", response_model=schemas.MascotaResponse)
def editar_mascota(
    mascota_id: int,
    datos: schemas.MascotaCreate,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(get_usuario_actual)
):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Solo el dueño puede editar su propia publicación
    if mascota.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta mascota")

    # Convertimos el schema a diccionario
    datos_dict = datos.model_dump()

    # Si la localidad o provincia han cambiado, volvemos a geocodificar
    if datos_dict["localidad"] != mascota.localidad or datos_dict["provincia"] != mascota.provincia:
        coords = geocodificar(datos_dict["localidad"], datos_dict["provincia"])
        if coords:
            datos_dict["latitud"], datos_dict["longitud"] = coords

    # Actualizamos cada campo de la mascota con los nuevos valores
    for campo, valor in datos_dict.items():
        setattr(mascota, campo, valor)

    db.commit()
    db.refresh(mascota)
    return mascota


# ─── DELETE /mascotas/{id} — Eliminar una mascota ──────────────────────────────
@router.delete("/{mascota_id}")
def eliminar_mascota(
    mascota_id: int,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(get_usuario_actual)
):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Solo el dueño puede eliminar su propia publicación
    if mascota.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta mascota")

    db.delete(mascota)
    db.commit()
    return {"message": "Mascota eliminada correctamente"}