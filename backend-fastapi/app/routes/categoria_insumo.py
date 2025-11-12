# routes/categorias_insumo.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.categorias_insumo import CategoriaInsumo, CategoriaInsumoResponse

router = APIRouter(prefix="/categorias_insumo", tags=["Categorias de Insumo"])

@router.post("/", response_model=CategoriaInsumoResponse)
async def create_categoria(cat: CategoriaInsumo):
    doc = await cat.insert()
    return CategoriaInsumoResponse(id=str(doc.id), nombre_categoria=doc.nombre_categoria)

@router.get("/", response_model=List[CategoriaInsumoResponse])
async def list_categorias():
    cats = await CategoriaInsumo.find_all().to_list()
    return [CategoriaInsumoResponse(id=str(c.id), nombre_categoria=c.nombre_categoria) for c in cats]

@router.put("/{cat_id}", response_model=CategoriaInsumoResponse)
async def update_categoria(cat_id: str, data: CategoriaInsumo):
    cat = await CategoriaInsumo.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    await cat.update({"$set": data.dict(exclude_unset=True)})
    cat = await CategoriaInsumo.get(cat_id)
    return CategoriaInsumoResponse(id=str(cat.id), nombre_categoria=cat.nombre_categoria)

@router.delete("/{cat_id}")
async def delete_categoria(cat_id: str):
    cat = await CategoriaInsumo.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    await cat.delete()
    return {"message": "Categoría eliminada"}
