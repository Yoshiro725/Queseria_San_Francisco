from fastapi import APIRouter, HTTPException
from typing import List
from app.models.productos_lacteos import ProductoLacteo
from app.schemas.producto_lacteo import ProductoCreate, ProductoRead, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=List[ProductoRead])
async def listar_productos():
    productos = await ProductoLacteo.find_all().to_list()
    return productos

@router.post("/", response_model=ProductoRead)
async def crear_producto(producto: ProductoCreate):
    nuevo_producto = ProductoLacteo(**producto.model_dump())
    await nuevo_producto.insert()
    return nuevo_producto

@router.get("/{producto_id}", response_model=ProductoRead)
async def obtener_producto(producto_id: str):
    producto = await ProductoLacteo.get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoRead)
async def actualizar_producto(producto_id: str, datos: ProductoUpdate):
    producto = await ProductoLacteo.get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    await producto.set(datos.model_dump(exclude_unset=True))
    return producto

@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: str):
    producto = await ProductoLacteo.get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    await producto.delete()
    return {"mensaje": "Producto eliminado correctamente"}
