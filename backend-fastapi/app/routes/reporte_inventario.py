# routes/reportes_inventario.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.reporte_inventario import ReporteInventario, ReporteInventarioResponse

router = APIRouter(prefix="/reportes_inventario", tags=["Reportes Inventario"])

@router.post("/", response_model=ReporteInventarioResponse)
async def create_reporte(r: ReporteInventario):
    doc = await r.insert()
    return ReporteInventarioResponse(
        id=str(doc.id),
        fecha=doc.fecha,
        tipo=doc.tipo,
        descripcion=doc.descripcion
    )

@router.get("/", response_model=List[ReporteInventarioResponse])
async def list_reportes():
    reportes = await ReporteInventario.find_all().to_list()
    return [
        ReporteInventarioResponse(
            id=str(r.id),
            fecha=r.fecha,
            tipo=r.tipo,
            descripcion=r.descripcion
        ) for r in reportes
    ]

@router.put("/{reporte_id}", response_model=ReporteInventarioResponse)
async def update_reporte(reporte_id: str, data: ReporteInventario):
    r = await ReporteInventario.get(reporte_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    await r.update({"$set": data.dict(exclude_unset=True)})
    r = await ReporteInventario.get(reporte_id)
    return ReporteInventarioResponse(
        id=str(r.id),
        fecha=r.fecha,
        tipo=r.tipo,
        descripcion=r.descripcion
    )

@router.delete("/{reporte_id}")
async def delete_reporte(reporte_id: str):
    r = await ReporteInventario.get(reporte_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    await r.delete()
    return {"message": "Reporte eliminado"}
