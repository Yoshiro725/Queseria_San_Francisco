from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.db.database import get_database

router = APIRouter(prefix="/insumos", tags=["Insumos"])

@router.get("/", response_model=List[dict])
async def list_insumos():
    try:
        database = get_database()
        insumos_cursor = database.insumos.find()
        insumos_list = await insumos_cursor.to_list(length=None)
        
        insumos_response = []
        for insumo in insumos_list:
            insumos_response.append({
                "id": str(insumo["_id"]),
                "nombre_insumo": insumo.get("nombre_insumo", ""),
                "unidad": insumo.get("unidad", ""),
                "stock_actual": insumo.get("stock_actual", 0),
                "stock_minimo": insumo.get("stock_minimo", 0),
                "costo_unitario": insumo.get("costo_unitario", 0)
            })
        
        return insumos_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{insumo_id}")
async def get_insumo(insumo_id: str):
    try:
        if not ObjectId.is_valid(insumo_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        database = get_database()
        insumo = await database.insumos.find_one({"_id": ObjectId(insumo_id)})
        
        if insumo is None:
            raise HTTPException(status_code=404, detail="Insumo no encontrado")
        
        return {
            "id": str(insumo["_id"]),
            "nombre_insumo": insumo.get("nombre_insumo", ""),
            "unidad": insumo.get("unidad", ""),
            "stock_actual": insumo.get("stock_actual", 0),
            "stock_minimo": insumo.get("stock_minimo", 0),
            "costo_unitario": insumo.get("costo_unitario", 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ✅ NUEVO ENDPOINT PARA ACTUALIZAR INSUMO
@router.put("/{insumo_id}")
async def update_insumo(insumo_id: str, update_data: dict):
    try:
        if not ObjectId.is_valid(insumo_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        database = get_database()
        
        # Verificar que el insumo existe
        insumo = await database.insumos.find_one({"_id": ObjectId(insumo_id)})
        if insumo is None:
            raise HTTPException(status_code=404, detail="Insumo no encontrado")
        
        # Campos permitidos para actualizar
        allowed_fields = ["stock_actual", "stock_minimo", "costo_unitario", "nombre_insumo", "unidad"]
        update_fields = {k: v for k, v in update_data.items() if k in allowed_fields}
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No hay campos válidos para actualizar")
        
        # Actualizar en la base de datos
        result = await database.insumos.update_one(
            {"_id": ObjectId(insumo_id)},
            {"$set": update_fields}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el insumo")
        
        # Obtener el insumo actualizado
        insumo_actualizado = await database.insumos.find_one({"_id": ObjectId(insumo_id)})
        
        return {
            "id": str(insumo_actualizado["_id"]),
            "nombre_insumo": insumo_actualizado.get("nombre_insumo", ""),
            "unidad": insumo_actualizado.get("unidad", ""),
            "stock_actual": insumo_actualizado.get("stock_actual", 0),
            "stock_minimo": insumo_actualizado.get("stock_minimo", 0),
            "costo_unitario": insumo_actualizado.get("costo_unitario", 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ✅ ENDPOINT ALTERNATIVO SOLO PARA ACTUALIZAR STOCK
@router.patch("/{insumo_id}/stock")
async def update_stock_insumo(insumo_id: str, stock_data: dict):
    try:
        if not ObjectId.is_valid(insumo_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        database = get_database()
        
        # Verificar que el insumo existe
        insumo = await database.insumos.find_one({"_id": ObjectId(insumo_id)})
        if insumo is None:
            raise HTTPException(status_code=404, detail="Insumo no encontrado")
        
        # Actualizar solo stock_actual
        nuevo_stock = stock_data.get("stock_actual")
        if nuevo_stock is None:
            raise HTTPException(status_code=400, detail="Se requiere stock_actual")
        
        result = await database.insumos.update_one(
            {"_id": ObjectId(insumo_id)},
            {"$set": {"stock_actual": nuevo_stock}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el stock")
        
        return {"message": "Stock actualizado correctamente", "nuevo_stock": nuevo_stock}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")