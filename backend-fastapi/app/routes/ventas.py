from fastapi import APIRouter, HTTPException
from app.schemas.ventas import VentaCreate, VentaUpdate, VentaRead
from app.models.ventas import Venta
from app.service.ventas import create_venta, get_venta, update_venta, delete_venta, list_ventas

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/", response_model=VentaRead)
async def create_venta_endpoint(venta: VentaCreate):
    venta_doc = Venta(**venta.dict())
    return await create_venta(venta_doc)

@router.get("/", response_model=list[VentaRead])
async def list_ventas_endpoint():
    return await list_ventas()

@router.get("/{venta_id}", response_model=VentaRead)
async def get_venta_endpoint(venta_id: str):
    venta = await get_venta(venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.put("/{venta_id}", response_model=VentaRead)
async def update_venta_endpoint(venta_id: str, venta: VentaUpdate):
    updated_venta = await update_venta(venta_id, venta.dict(exclude_unset=True))
    if not updated_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return updated_venta

@router.delete("/{venta_id}")
async def delete_venta_endpoint(venta_id: str):
    deleted = await delete_venta(venta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return {"mensaje": "Venta eliminada correctamente"}
