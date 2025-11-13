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