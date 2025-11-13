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

@router.get("/productos")
async def list_productos():
    try:
        from app.models.productos_lacteos import ProductoLacteo
        
        # ✅ OBTENER PRODUCTOS REALES
        productos = await ProductoLacteo.find_all().to_list()
        
        productos_convertidos = []
        for producto in productos:
            productos_convertidos.append({
                "id": str(producto.id),
                "nombre": producto.desc_queso,
                "precio": producto.precio,
                "inventario": producto.totalInventario
            })
        
        return productos_convertidos
        
    except Exception as e:
        print(f"❌ Error en GET /productos: {str(e)}")
        return {"error": str(e)}


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
