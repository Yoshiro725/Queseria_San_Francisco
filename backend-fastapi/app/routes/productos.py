from fastapi import APIRouter, HTTPException
from app.models.productos_lacteos import ProductoLacteo


router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoLacteo)
async def create_producto(producto: ProductoLacteo):
    await producto.insert()
    return producto

@router.get("/", response_model=list[ProductoLacteo])
async def list_productos():
    productos = await ProductoLacteo.find_all().to_list()
    return productos

@router.get("/{producto_id}", response_model=ProductoLacteo)
async def get_producto(producto_id: str):
    producto = await ProductoLacteo.get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoLacteo)
async def update_producto(producto_id: str, update_data: dict):
    producto = await ProductoLacteo.get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    await producto.set(update_data)
    return producto

@router.delete("/{producto_id}")
async def delete_producto(producto_id: str):
    producto = await ProductoLacteo.get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    await producto.delete()
    return {"detail": "Producto eliminado"}
