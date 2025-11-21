from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from bson import ObjectId
from datetime import datetime
from app.db.database import get_database

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.get("/")
async def list_ventas():
    try:
        print("🔍 Iniciando list_ventas...")
        db = get_database()
        ventas_collection = db.ventas
        clientes_collection = db.clientes
        productos_collection = db.productos_lacteos
        
        # Obtener todas las ventas
        ventas = await ventas_collection.find().to_list(length=None)
        print(f"📦 Se encontraron {len(ventas)} ventas")
        
        # Convertir manualmente todos los ObjectId a string
        ventas_json = []
        for venta in ventas:
            # Obtener información del cliente
            cliente_id = venta.get("cliente_id")
            nombre_cliente = "Cliente no encontrado"
            
            if cliente_id:
                try:
                    cliente = await clientes_collection.find_one({"_id": ObjectId(cliente_id)})
                    nombre_cliente = cliente.get("nombre_cliente", "Cliente no encontrado") if cliente else "Cliente no encontrado"
                except:
                    nombre_cliente = "Cliente no encontrado"
            
            venta_dict = {
                "id": str(venta["_id"]),
                "fecha_venta": venta.get("fecha_venta", datetime.utcnow()).isoformat(),
                "total": venta.get("total", 0),
                "IVA": venta.get("IVA", 0),
                "cliente_id": str(venta.get("cliente_id", "")),
                "cliente_nombre": nombre_cliente,  # ✅ NUEVO CAMPO
                "detalle": []
            }
            
            # Procesar detalle con nombres de productos
            for detalle in venta.get("detalle", []):
                producto_id = detalle.get("producto_id")
                nombre_producto = "Producto no encontrado"
                
                if producto_id:
                    try:
                        producto = await productos_collection.find_one({"_id": ObjectId(producto_id)})
                        nombre_producto = producto.get("desc_queso", "Producto no encontrado") if producto else "Producto no encontrado"
                    except:
                        nombre_producto = "Producto no encontrado"
                
                detalle_dict = {
                    "producto_id": str(detalle.get("producto_id", "")),
                    "cantidad": detalle.get("cantidad", 0),
                    "precioVenta": detalle.get("precioVenta", 0),
                    "nombre_producto": nombre_producto,  # ✅ NUEVO CAMPO
                    "subtotal": detalle.get("cantidad", 0) * detalle.get("precioVenta", 0)  # ✅ CALCULAR SUBTOTAL
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