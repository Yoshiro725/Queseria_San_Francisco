# routes/distribucion_pagos.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.distribucion_pago import DistribucionPago, DistribucionPagoResponse

router = APIRouter(prefix="/distribucion_pagos", tags=["Distribución Pagos"])

@router.post("/", response_model=DistribucionPagoResponse)
async def create_distribucion(d: DistribucionPago):
    doc = await d.insert()
    return DistribucionPagoResponse(
        id=str(doc.id),
        proveedor_id=str(doc.proveedor_id.id),
        anno=doc.anno,
        semana=doc.semana,
        denominacion=doc.denominacion,
        cantidad=doc.cantidad
    )

@router.get("/", response_model=List[DistribucionPagoResponse])
async def list_distribuciones():
    distribs = await DistribucionPago.find_all().to_list()
    return [
        DistribucionPagoResponse(
            id=str(d.id),
            proveedor_id=str(d.proveedor_id.id),
            anno=d.anno,
            semana=d.semana,
            denominacion=d.denominacion,
            cantidad=d.cantidad
        )
        for d in distribs
    ]

@router.put("/{distribucion_id}", response_model=DistribucionPagoResponse)
async def update_distribucion(distribucion_id: str, data: DistribucionPago):
    d = await DistribucionPago.get(distribucion_id)
    if not d:
        raise HTTPException(status_code=404, detail="Distribución no encontrada")
    await d.update({"$set": data.dict(exclude_unset=True)})
    d = await DistribucionPago.get(distribucion_id)
    return DistribucionPagoResponse(
        id=str(d.id),
        proveedor_id=str(d.proveedor_id.id),
        anno=d.anno,
        semana=d.semana,
        denominacion=d.denominacion,
        cantidad=d.cantidad
    )

@router.delete("/{distribucion_id}")
async def delete_distribucion(distribucion_id: str):
    d = await DistribucionPago.get(distribucion_id)
    if not d:
        raise HTTPException(status_code=404, detail="Distribución no encontrada")
    await d.delete()
    return {"message": "Distribución eliminada"}
