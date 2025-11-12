# routes/reportes_produccion.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.reporte_produccion import ReporteProduccion, ReporteProduccionResponse

router = APIRouter(prefix="/reportes_produccion", tags=["Reportes Producción"])

@router.post("/", response_model=ReporteProduccionResponse)
async def create_reporte(r: ReporteProduccion):
    doc = await r.insert()
    return ReporteProduccionResponse(
        id=str(doc.id),
        fecha_inicio=doc.fecha_inicio,
        fecha_fin=doc.fecha_fin,
        total_producido=doc.total_producido,
        observaciones=doc.observaciones
    )

@router.get("/", response_model=List[ReporteProduccionResponse])
async def list_reportes():
    reportes = await ReporteProduccion.find_all().to_list()
    return [
        ReporteProduccionResponse(
            id=str(r.id),
            fecha_inicio=r.fecha_inicio,
            fecha_fin=r.fecha_fin,
            total_producido=r.total_producido,
            observaciones=r.observaciones
        ) for r in reportes
    ]

@router.put("/{reporte_id}", response_model=ReporteProduccionResponse)
async def update_reporte(reporte_id: str, data: ReporteProduccion):
    r = await ReporteProduccion.get(reporte_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    await r.update({"$set": data.dict(exclude_unset=True)})
    r = await ReporteProduccion.get(reporte_id)
    return ReporteProduccionResponse(
        id=str(r.id),
        fecha_inicio=r.fecha_inicio,
        fecha_fin=r.fecha_fin,
        total_producido=r.total_producido,
        observaciones=r.observaciones
    )

@router.delete("/{reporte_id}")
async def delete_reporte(reporte_id: str):
    r = await ReporteProduccion.get(reporte_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    await r.delete()
    return {"message": "Reporte eliminado"}
