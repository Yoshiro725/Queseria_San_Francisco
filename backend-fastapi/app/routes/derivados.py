# routes/derivados.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.derivados import Derivado, DerivadoResponse
from app.models.productos_lacteos import ProductoLacteo

router = APIRouter(prefix="/derivados", tags=["Derivados"])

@router.post("/", response_model=DerivadoResponse)
async def create_derivado(d: Derivado):
    doc = await d.insert()
    return DerivadoResponse(
        id=str(doc.id),
        receta_origen_id=str(doc.receta_origen_id.id),
        nombre_derivado=doc.nombre_derivado,
        cantidad_generada=doc.cantidad_generada,
        unidad=doc.unidad
    )

@router.get("/", response_model=List[DerivadoResponse])
async def list_derivados():
    derivados = await Derivado.find_all().to_list()
    return [
        DerivadoResponse(
            id=str(d.id),
            receta_origen_id=str(d.receta_origen_id.id),
            nombre_derivado=d.nombre_derivado,
            cantidad_generada=d.cantidad_generada,
            unidad=d.unidad
        )
        for d in derivados
    ]

@router.put("/{derivado_id}", response_model=DerivadoResponse)
async def update_derivado(derivado_id: str, data: Derivado):
    d = await Derivado.get(derivado_id)
    if not d:
        raise HTTPException(status_code=404, detail="Derivado no encontrado")
    await d.update({"$set": data.dict(exclude_unset=True)})
    d = await Derivado.get(derivado_id)
    return DerivadoResponse(
        id=str(d.id),
        receta_origen_id=str(d.receta_origen_id.id),
        nombre_derivado=d.nombre_derivado,
        cantidad_generada=d.cantidad_generada,
        unidad=d.unidad
    )

@router.delete("/{derivado_id}")
async def delete_derivado(derivado_id: str):
    d = await Derivado.get(derivado_id)
    if not d:
        raise HTTPException(status_code=404, detail="Derivado no encontrado")
    await d.delete()
    return {"message": "Derivado eliminado"}
