# routes/entregas_diarias.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.entrega_diaria import EntregaDiaria, EntregaDiariaResponse

router = APIRouter(prefix="/entregas_diarias", tags=["Entregas Diarias"])

@router.post("/", response_model=EntregaDiariaResponse)
async def create_entrega(e: EntregaDiaria):
    doc = await e.insert()
    return EntregaDiariaResponse(
        id=str(doc.id),
        proveedor_id=str(doc.proveedor_id.id),
        fecha=doc.fecha,
        cantidad=doc.cantidad
    )

@router.get("/", response_model=List[EntregaDiariaResponse])
async def list_entregas():
    entregas = await EntregaDiaria.find_all().to_list()
    return [
        EntregaDiariaResponse(
            id=str(e.id),
            proveedor_id=str(e.proveedor_id.id),
            fecha=e.fecha,
            cantidad=e.cantidad
        )
        for e in entregas
    ]

@router.put("/{entrega_id}", response_model=EntregaDiariaResponse)
async def update_entrega(entrega_id: str, data: EntregaDiaria):
    e = await EntregaDiaria.get(entrega_id)
    if not e:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    await e.update({"$set": data.dict(exclude_unset=True)})
    e = await EntregaDiaria.get(entrega_id)
    return EntregaDiariaResponse(
        id=str(e.id),
        proveedor_id=str(e.proveedor_id.id),
        fecha=e.fecha,
        cantidad=e.cantidad
    )

@router.delete("/{entrega_id}")
async def delete_entrega(entrega_id: str):
    e = await EntregaDiaria.get(entrega_id)
    if not e:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    await e.delete()
    return {"message": "Entrega eliminada"}
