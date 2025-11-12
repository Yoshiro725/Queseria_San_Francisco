from fastapi import APIRouter, HTTPException
from typing import List
from app.models.recetas import Receta

router = APIRouter(prefix="/recetas", tags=["Recetas"])

# Crear una receta
@router.post("/", response_model=Receta)
async def create_receta(receta: Receta):
    await receta.insert()
    return receta

# Listar todas las recetas
@router.get("/", response_model=List[Receta])
async def list_recetas():
    recetas = await Receta.find_all().to_list()
    return recetas

# Obtener receta por ID
@router.get("/{receta_id}", response_model=Receta)
async def get_receta(receta_id: str):
    receta = await Receta.get(receta_id)
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

# Actualizar receta
@router.put("/{receta_id}", response_model=Receta)
async def update_receta(receta_id: str, receta_data: Receta):
    receta = await Receta.get(receta_id)
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    await receta.update({"$set": receta_data.dict(exclude_unset=True)})
    return receta

# Eliminar receta
@router.delete("/{receta_id}")
async def delete_receta(receta_id: str):
    receta = await Receta.get(receta_id)
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    await receta.delete()
    return {"message": "Receta eliminada correctamente"}
