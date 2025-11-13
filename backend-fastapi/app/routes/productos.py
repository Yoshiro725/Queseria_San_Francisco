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