from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from bson import ObjectId
from datetime import datetime
from app.db.database import get_database  # ✅ Importación correcta

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.get("/")
async def list_ventas():
    try:
        print("🔍 Iniciando list_ventas...")
        db = get_database()
        ventas_collection = db.ventas
        
        # Obtener todas las ventas
        ventas = await ventas_collection.find().to_list(length=None)
        print(f"📦 Se encontraron {len(ventas)} ventas")
        
        # Convertir manualmente todos los ObjectId a string
        ventas_json = []
        for venta in ventas:
            venta_dict = {
                "id": str(venta["_id"]),
                "fecha_venta": venta.get("fecha_venta", datetime.utcnow()).isoformat(),
                "total": venta.get("total", 0),
                "IVA": venta.get("IVA", 0),
                "cliente_id": str(venta.get("cliente_id", "")),
                "detalle": []
            }
            
            # Procesar detalle
            for detalle in venta.get("detalle", []):
                detalle_dict = {
                    "producto_id": str(detalle.get("producto_id", "")),
                    "cantidad": detalle.get("cantidad", 0),
                    "precioVenta": detalle.get("precioVenta", 0)
                }
                venta_dict["detalle"].append(detalle_dict)
            
            ventas_json.append(venta_dict)
        
        print("✅ Lista de ventas procesada correctamente")
        return ventas_json
        
    except Exception as e:
        print(f"❌ Error crítico en list_ventas: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al obtener ventas: {str(e)}")

@router.post("/")
async def create_venta(venta_data: Dict[str, Any]):
    try:
        print("📤 Creando nueva venta...")
        db = get_database()
        ventas_collection = db.ventas
        productos_collection = db.productos_lacteos
        
        # Validar stock de productos
        for detalle in venta_data.get("detalle", []):
            producto_id = detalle.get("producto_id")
            cantidad = detalle.get("cantidad", 0)
            
            # Buscar producto
            producto = await productos_collection.find_one({"_id": ObjectId(producto_id)})
            if not producto:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Producto con ID {producto_id} no encontrado"
                )
            
            # Validar stock
            stock_actual = producto.get("totalInventario", 0)
            if stock_actual < cantidad:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuficiente para {producto.get('desc_queso', 'Producto')}. Disponible: {stock_actual}, Solicitado: {cantidad}"
                )
        
        # Preparar datos para MongoDB
        venta_mongo = {
            "fecha_venta": datetime.utcnow(),
            "total": venta_data.get("total", 0),
            "IVA": venta_data.get("IVA", 0),
            "cliente_id": ObjectId(venta_data.get("cliente_id", "")),
            "detalle": [
                {
                    "producto_id": ObjectId(detalle.get("producto_id", "")),
                    "cantidad": detalle.get("cantidad", 0),
                    "precioVenta": detalle.get("precioVenta", 0)
                }
                for detalle in venta_data.get("detalle", [])
            ]
        }
        
        # Insertar venta
        result = await ventas_collection.insert_one(venta_mongo)
        
        # Actualizar inventario de productos
        for detalle in venta_data.get("detalle", []):
            await productos_collection.update_one(
                {"_id": ObjectId(detalle.get("producto_id", ""))},
                {"$inc": {"totalInventario": -detalle.get("cantidad", 0)}}
            )
        
        # Obtener venta creada
        venta_creada = await ventas_collection.find_one({"_id": result.inserted_id})
        
        # Preparar respuesta
        response_venta = {
            "id": str(venta_creada["_id"]),
            "fecha_venta": venta_creada.get("fecha_venta", datetime.utcnow()).isoformat(),
            "total": venta_creada.get("total", 0),
            "IVA": venta_creada.get("IVA", 0),
            "cliente_id": str(venta_creada.get("cliente_id", "")),
            "detalle": [
                {
                    "producto_id": str(detalle.get("producto_id", "")),
                    "cantidad": detalle.get("cantidad", 0),
                    "precioVenta": detalle.get("precioVenta", 0)
                }
                for detalle in venta_creada.get("detalle", [])
            ]
        }
        
        print("✅ Venta creada correctamente")
        return response_venta
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en create_venta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear venta: {str(e)}")

@router.get("/{venta_id}")
async def get_venta(venta_id: str):
    try:
        db = get_database()
        ventas_collection = db.ventas
        
        venta = await ventas_collection.find_one({"_id": ObjectId(venta_id)})
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        
        # Preparar respuesta
        response_venta = {
            "id": str(venta["_id"]),
            "fecha_venta": venta.get("fecha_venta", datetime.utcnow()).isoformat(),
            "total": venta.get("total", 0),
            "IVA": venta.get("IVA", 0),
            "cliente_id": str(venta.get("cliente_id", "")),
            "detalle": [
                {
                    "producto_id": str(detalle.get("producto_id", "")),
                    "cantidad": detalle.get("cantidad", 0),
                    "precioVenta": detalle.get("precioVenta", 0)
                }
                for detalle in venta.get("detalle", [])
            ]
        }
        
        return response_venta
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en get_venta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener venta: {str(e)}")