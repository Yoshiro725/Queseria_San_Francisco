# routes/movimientos_insumo.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.movimientos_insumo import MovimientoInsumo, MovimientoInsumoResponse
from app.models.insumos import Insumo

router = APIRouter(prefix="/movimientos_insumo", tags=["Movimientos de Insumos"])

@router.post("/", response_model=MovimientoInsumoResponse)
async def create_movimiento(mov: MovimientoInsumo):
    doc = await mov.insert()
    return MovimientoInsumoResponse(
        id=str(doc.id),
        insumo_id=str(doc.insumo_id.id),
        fecha=doc.fecha,
        tipo_mov=doc.tipo_mov,
        cantidad=doc.cantidad,
        descripcion=doc.descripcion
    )

@router.get("/", response_model=List[MovimientoInsumoResponse])
async def list_movimientos():
    movimientos = await MovimientoInsumo.find_all().to_list()
    return [
        MovimientoInsumoResponse(
            id=str(m.id),
            insumo_id=str(m.insumo_id.id),
            fecha=m.fecha,
            tipo_mov=m.tipo_mov,
            cantidad=m.cantidad,
            descripcion=m.descripcion
        )
        for m in movimientos
    ]

@router.put("/{mov_id}", response_model=MovimientoInsumoResponse)
async def update_movimiento(mov_id: str, data: MovimientoInsumo):
    mov = await MovimientoInsumo.get(mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    await mov.update({"$set": data.dict(exclude_unset=True)})
    mov = await MovimientoInsumo.get(mov_id)
    return MovimientoInsumoResponse(
        id=str(mov.id),
        insumo_id=str(mov.insumo_id.id),
        fecha=mov.fecha,
        tipo_mov=mov.tipo_mov,
        cantidad=mov.cantidad,
        descripcion=mov.descripcion
    )

@router.delete("/{mov_id}")
async def delete_movimiento(mov_id: str):
    mov = await MovimientoInsumo.get(mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    await mov.delete()
    return {"message": "Movimiento eliminado"}
