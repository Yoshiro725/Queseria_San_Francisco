from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.db.database import get_database

router = APIRouter(prefix="/productos", tags=["ProductosLacteos"])

@router.post("/", response_model=dict)
async def create_producto(producto_data: dict):
    try:
        database = get_database()
        
        # Datos para nuevo producto
        nuevo_producto = {
            "desc_queso": producto_data.get("desc_queso", ""),
            "precio": producto_data.get("precio", 0),
            "totalInventario": 0  # Siempre empieza en 0
        }
        
        result = await database.productos_lacteos.insert_one(nuevo_producto)
        
        return {
            "id": str(result.inserted_id),
            "desc_queso": nuevo_producto["desc_queso"],
            "precio": nuevo_producto["precio"],
            "totalInventario": nuevo_producto["totalInventario"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando producto: {str(e)}")

@router.get("/", response_model=List[dict])
async def list_productos():
    try:
        database = get_database()
        productos_cursor = database.productos_lacteos.find()
        productos_list = await productos_cursor.to_list(length=None)
        
        productos_response = []
        for producto in productos_list:
            # Usar 'desc_queso' si existe, sino 'nombre'
            nombre_producto = producto.get("desc_queso") or producto.get("nombre", "Sin nombre")
            
            productos_response.append({
                "id": str(producto["_id"]),
                "desc_queso": nombre_producto,
                "precio": producto.get("precio", 0),
                "totalInventario": producto.get("totalInventario", 0)
            })
        
        return productos_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ✅ NUEVO ENDPOINT PARA ACTUALIZAR PRODUCTO
@router.put("/{producto_id}")
async def update_producto(producto_id: str, update_data: dict):
    try:
        if not ObjectId.is_valid(producto_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        database = get_database()
        
        # Verificar que el producto existe
        producto = await database.productos_lacteos.find_one({"_id": ObjectId(producto_id)})
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Campos permitidos para actualizar
        allowed_fields = ["totalInventario", "precio", "desc_queso"]
        update_fields = {k: v for k, v in update_data.items() if k in allowed_fields}
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No hay campos válidos para actualizar")
        
        # Actualizar en la base de datos
        result = await database.productos_lacteos.update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": update_fields}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el producto")
        
        # Obtener el producto actualizado
        producto_actualizado = await database.productos_lacteos.find_one({"_id": ObjectId(producto_id)})
        
        nombre_producto = producto_actualizado.get("desc_queso") or producto_actualizado.get("nombre", "Sin nombre")
        
        return {
            "id": str(producto_actualizado["_id"]),
            "desc_queso": nombre_producto,
            "precio": producto_actualizado.get("precio", 0),
            "totalInventario": producto_actualizado.get("totalInventario", 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ✅ ENDPOINT ESPECÍFICO PARA ACTUALIZAR INVENTARIO
@router.patch("/{producto_id}/inventario")
async def update_inventario_producto(producto_id: str, inventario_data: dict):
    try:
        if not ObjectId.is_valid(producto_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        database = get_database()
        
        # Verificar que el producto existe
        producto = await database.productos_lacteos.find_one({"_id": ObjectId(producto_id)})
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Actualizar inventario
        cantidad = inventario_data.get("cantidad")
        if cantidad is None:
            raise HTTPException(status_code=400, detail="Se requiere cantidad")
        
        result = await database.productos_lacteos.update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": {"totalInventario": cantidad}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el inventario")
        
        return {"message": "Inventario actualizado correctamente", "nuevo_inventario": cantidad}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ✅ ENDPOINT PARA OBTENER UN PRODUCTO POR ID
@router.get("/{producto_id}")
async def get_producto(producto_id: str):
    try:
        if not ObjectId.is_valid(producto_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        database = get_database()
        producto = await database.productos_lacteos.find_one({"_id": ObjectId(producto_id)})
        
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        nombre_producto = producto.get("desc_queso") or producto.get("nombre", "Sin nombre")
        
        return {
            "id": str(producto["_id"]),
            "desc_queso": nombre_producto,
            "precio": producto.get("precio", 0),
            "totalInventario": producto.get("totalInventario", 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")