# routes/pagos_semanales.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.pago_semanales import PagoSemanal, PagoSemanalResponse

router = APIRouter(prefix="/pagos_semanales", tags=["Pagos Semanales"])

@router.post("/", response_model=PagoSemanalResponse)
async def create_pago(p: PagoSemanal):
    doc = await p.insert()
    return PagoSemanalResponse(
        id=str(doc.id),
        proveedor_id=str(doc.proveedor_id.id),
        anno=doc.anno,
        semana=doc.semana,
        importe=doc.importe,
        cantidad=doc.cantidad
    )

@router.get("/", response_model=List[PagoSemanalResponse])
async def list_pagos():
    pagos = await PagoSemanal.find_all().to_list()
    return [
        PagoSemanalResponse(
            id=str(p.id),
            proveedor_id=str(p.proveedor_id.id),
            anno=p.anno,
            semana=p.semana,
            importe=p.importe,
            cantidad=p.cantidad
        )
        for p in pagos
    ]

@router.put("/{pago_id}", response_model=PagoSemanalResponse)
async def update_pago(pago_id: str, data: PagoSemanal):
    p = await PagoSemanal.get(pago_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    await p.update({"$set": data.dict(exclude_unset=True)})
    p = await PagoSemanal.get(pago_id)
    return PagoSemanalResponse(
        id=str(p.id),
        proveedor_id=str(p.proveedor_id.id),
        anno=p.anno,
        semana=p.semana,
        importe=p.importe,
        cantidad=p.cantidad
    )

@router.delete("/{pago_id}")
async def delete_pago(pago_id: str):
    p = await PagoSemanal.get(pago_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    await p.delete()
    return {"message": "Pago eliminado"}
