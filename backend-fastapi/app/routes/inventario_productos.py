# routes/inventario_productos.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.inventario_productos import InventarioProducto, InventarioProductoResponse
from app.models.productos_lacteos import ProductoLacteo

router = APIRouter(prefix="/inventario_productos", tags=["Inventario Productos"])

@router.post("/", response_model=InventarioProductoResponse)
async def create_inventario(inv: InventarioProducto):
    doc = await inv.insert()
    return InventarioProductoResponse(
        id=str(doc.id),
        producto_id=str(doc.producto_id.id),
        fecha_entrada=doc.fecha_entrada,
        cantidad_disponible=doc.cantidad_disponible,
        costo_unitario=doc.costo_unitario,
        ubicacion=doc.ubicacion
    )

@router.get("/", response_model=List[InventarioProductoResponse])
async def list_inventario():
    inventarios = await InventarioProducto.find_all().to_list()
    return [
        InventarioProductoResponse(
            id=str(i.id),
            producto_id=str(i.producto_id.id),
            fecha_entrada=i.fecha_entrada,
            cantidad_disponible=i.cantidad_disponible,
            costo_unitario=i.costo_unitario,
            ubicacion=i.ubicacion
        )
        for i in inventarios
    ]

@router.put("/{inv_id}", response_model=InventarioProductoResponse)
async def update_inventario(inv_id: str, data: InventarioProducto):
    inv = await InventarioProducto.get(inv_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    await inv.update({"$set": data.dict(exclude_unset=True)})
    inv = await InventarioProducto.get(inv_id)
    return InventarioProductoResponse(
        id=str(inv.id),
        producto_id=str(inv.producto_id.id),
        fecha_entrada=inv.fecha_entrada,
        cantidad_disponible=inv.cantidad_disponible,
        costo_unitario=inv.costo_unitario,
        ubicacion=inv.ubicacion
    )

@router.delete("/{inv_id}")
async def delete_inventario(inv_id: str):
    inv = await InventarioProducto.get(inv_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    await inv.delete()
    return {"message": "Inventario eliminado"}
