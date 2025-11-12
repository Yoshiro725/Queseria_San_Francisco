# routes/ventas.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.ventas import Venta, VentaResponse

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/", response_model=VentaResponse)
async def create_venta(v: Venta):
    doc = await v.insert()
    return VentaResponse(
        id=str(doc.id),
        fecha_venta=doc.fecha_venta,
        total=doc.total,
        IVA=doc.IVA,
        cliente_id=str(doc.cliente_id.id),
        detalle=doc.detalle
    )

@router.get("/", response_model=List[VentaResponse])
async def list_ventas():
    ventas = await Venta.find_all().to_list()
    return [
        VentaResponse(
            id=str(v.id),
            fecha_venta=v.fecha_venta,
            total=v.total,
            IVA=v.IVA,
            cliente_id=str(v.cliente_id.id),
            detalle=v.detalle
        )
        for v in ventas
    ]

@router.put("/{venta_id}", response_model=VentaResponse)
async def update_venta(venta_id: str, data: Venta):
    v = await Venta.get(venta_id)
    if not v:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    await v.update({"$set": data.dict(exclude_unset=True)})
    v = await Venta.get(venta_id)
    return VentaResponse(
        id=str(v.id),
        fecha_venta=v.fecha_venta,
        total=v.total,
        IVA=v.IVA,
        cliente_id=str(v.cliente_id.id),
        detalle=v.detalle
    )

@router.delete("/{venta_id}")
async def delete_venta(venta_id: str):
    v = await Venta.get(venta_id)
    if not v:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    await v.delete()
    return {"message": "Venta eliminada"}
