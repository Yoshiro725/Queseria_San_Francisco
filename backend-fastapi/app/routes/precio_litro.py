# routes/precios_litro.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.precio_litro import PrecioLitro, PrecioLitroResponse

router = APIRouter(prefix="/precios_litro", tags=["Precio Litro"])

@router.post("/", response_model=PrecioLitroResponse)
async def create_precio(p: PrecioLitro):
    doc = await p.insert()
    return PrecioLitroResponse(id=str(doc.id), **p.dict())

@router.get("/", response_model=List[PrecioLitroResponse])
async def list_precios():
    precios = await PrecioLitro.find_all().to_list()
    return [PrecioLitroResponse(id=str(p.id), **p.dict()) for p in precios]

@router.put("/{precio_id}", response_model=PrecioLitroResponse)
async def update_precio(precio_id: str, data: PrecioLitro):
    p = await PrecioLitro.get(precio_id)
    if not p:
        raise HTTPException(status_code=404, detail="Precio no encontrado")
    await p.update({"$set": data.dict(exclude_unset=True)})
    p = await PrecioLitro.get(precio_id)
    return PrecioLitroResponse(id=str(p.id), **p.dict())

@router.delete("/{precio_id}")
async def delete_precio(precio_id: str):
    p = await PrecioLitro.get(precio_id)
    if not p:
        raise HTTPException(status_code=404, detail="Precio no encontrado")
    await p.delete()
    return {"message": "Precio eliminado"}
