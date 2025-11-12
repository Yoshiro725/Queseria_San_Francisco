# routes/denominaciones.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.denominacion import Denominacion, DenominacionResponse

router = APIRouter(prefix="/denominaciones", tags=["Denominaciones"])

@router.post("/", response_model=DenominacionResponse)
async def create_denominacion(d: Denominacion):
    doc = await d.insert()
    return DenominacionResponse(id=str(doc.id), nominal=d.nominal)

@router.get("/", response_model=List[DenominacionResponse])
async def list_denominaciones():
    denoms = await Denominacion.find_all().to_list()
    return [DenominacionResponse(id=str(d.id), nominal=d.nominal) for d in denoms]

@router.put("/{denominacion_id}", response_model=DenominacionResponse)
async def update_denominacion(denominacion_id: str, data: Denominacion):
    d = await Denominacion.get(denominacion_id)
    if not d:
        raise HTTPException(status_code=404, detail="Denominación no encontrada")
    await d.update({"$set": data.dict(exclude_unset=True)})
    d = await Denominacion.get(denominacion_id)
    return DenominacionResponse(id=str(d.id), nominal=d.nominal)

@router.delete("/{denominacion_id}")
async def delete_denominacion(denominacion_id: str):
    d = await Denominacion.get(denominacion_id)
    if not d:
        raise HTTPException(status_code=404, detail="Denominación no encontrada")
    await d.delete()
    return {"message": "Denominación eliminada"}
