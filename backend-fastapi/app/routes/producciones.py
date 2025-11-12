from fastapi import APIRouter, HTTPException
from app.schemas.produccion import ProduccionCreate, ProduccionUpdate, ProduccionRead
from app.models.produccion import Produccion
from app.service.producciones import create_produccion, get_produccion, update_produccion, delete_produccion, list_producciones

router = APIRouter(prefix="/producciones", tags=["Producciones"])

@router.post("/", response_model=ProduccionRead)
async def create_produccion_endpoint(produccion: ProduccionCreate):
    produccion_doc = Produccion(**produccion.dict())
    return await create_produccion(produccion_doc)

@router.get("/", response_model=list[ProduccionRead])
async def list_producciones_endpoint():
    return await list_producciones()

@router.get("/{produccion_id}", response_model=ProduccionRead)
async def get_produccion_endpoint(produccion_id: str):
    produccion = await get_produccion(produccion_id)
    if not produccion:
        raise HTTPException(status_code=404, detail="Producción no encontrada")
    return produccion

@router.put("/{produccion_id}", response_model=ProduccionRead)
async def update_produccion_endpoint(produccion_id: str, produccion: ProduccionUpdate):
    updated_produccion = await update_produccion(produccion_id, produccion.dict(exclude_unset=True))
    if not updated_produccion:
        raise HTTPException(status_code=404, detail="Producción no encontrada")
    return updated_produccion

@router.delete("/{produccion_id}")
async def delete_produccion_endpoint(produccion_id: str):
    deleted = await delete_produccion(produccion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producción no encontrada")
    return {"mensaje": "Producción eliminada correctamente"}
