from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.db.database import get_database
from app.models.recetas import Receta
from app.schemas.recetas import RecetaResponse, RecetaCreate

router = APIRouter(prefix="/recetas", tags=["Recetas"])

# ✅ FUNCIÓN CONVERT_MONGO_TO_RESPONSE CORREGIDA
async def convert_mongo_to_response(receta_data: dict) -> RecetaResponse:
    try:
        print("🔄 Convirtiendo receta a respuesta:", receta_data)
        
        if not receta_data:
            raise ValueError("Datos de receta vacíos")
        
        database = get_database()
        
        # Convertir _id a string
        receta_id = str(receta_data["_id"])
        
        # Convertir producto_id a string
        producto_id = str(receta_data["producto_id"])
        
        # Obtener nombre del producto
        producto = await database.productos_lacteos.find_one({"_id": receta_data["producto_id"]})
        nombre_producto = producto.get("desc_queso", "Producto sin nombre") if producto else "Producto no encontrado"
        
        # Procesar insumos
        insumos_con_nombre = []
        for insumo_data in receta_data.get("insumos", []):
            insumo_id = str(insumo_data["insumo_id"])
            
            # Obtener nombre del insumo
            insumo = await database.insumos.find_one({"_id": insumo_data["insumo_id"]})
            nombre_insumo = insumo.get("nombre_insumo", "Insumo sin nombre") if insumo else "Insumo no encontrado"
            
            insumos_con_nombre.append({
                "insumo_id": insumo_id,
                "nombre_insumo": nombre_insumo,
                "cantidad": insumo_data["cantidad"],
                "unidad": insumo_data["unidad"]
            })
        
        response_data = RecetaResponse(
            id=receta_id,
            producto_id=producto_id,
            nombre_producto=nombre_producto,
            rendimiento=receta_data["rendimiento"],
            unidad_rendimiento=receta_data["unidad_rendimiento"],
            observaciones=receta_data["observaciones"],
            estado=receta_data.get("estado", True),
            insumos=insumos_con_nombre
        )
        
        print("✅ Respuesta convertida exitosamente")
        return response_data
        
    except Exception as e:
        print(f"❌ Error en convert_mongo_to_response: {e}")
        import traceback
        traceback.print_exc()
        raise

@router.get("/", response_model=List[RecetaResponse])
async def list_recetas():
    try:
        database = get_database()
        
        # Obtener todas las recetas
        recetas = await database.recetas.find().to_list(length=None)
        
        # Obtener todos los productos para mapeo
        productos = await database.productos_lacteos.find().to_list(length=None)
        producto_map = {}
        for p in productos:
            producto_map[str(p["_id"])] = p.get("desc_queso") or p.get("nombre", "Sin nombre")
        
        # Obtener todos los insumos para mapeo
        insumos = await database.insumos.find().to_list(length=None)
        insumo_map = {str(i["_id"]): i.get("nombre_insumo", "Sin nombre") for i in insumos}
        
        recetas_response = []
        for receta_data in recetas:
            try:
                # Manejar producto_id
                producto_id = receta_data["producto_id"]
                if isinstance(producto_id, ObjectId):
                    producto_id_str = str(producto_id)
                else:
                    producto_id_str = producto_id
                
                nombre_producto = producto_map.get(producto_id_str, "Producto no encontrado")
                
                # ✅ CORRECIÓN: Convertir insumo_id de ObjectId a string
                insumos_mejorados = []
                for insumo in receta_data.get("insumos", []):
                    # Convertir insumo_id a string
                    insumo_id = insumo["insumo_id"]
                    if isinstance(insumo_id, ObjectId):
                        insumo_id_str = str(insumo_id)
                    else:
                        insumo_id_str = insumo_id
                    
                    nombre_insumo = insumo_map.get(insumo_id_str, "Insumo no encontrado")
                    
                    insumos_mejorados.append({
                        "insumo_id": insumo_id_str,  # ✅ Ahora es string
                        "nombre_insumo": nombre_insumo,
                        "cantidad": insumo["cantidad"],
                        "unidad": insumo["unidad"]
                    })
                
                receta_response = RecetaResponse(
                    id=str(receta_data["_id"]),
                    producto_id=producto_id_str,
                    nombre_producto=nombre_producto,
                    rendimiento=receta_data["rendimiento"],
                    unidad_rendimiento=receta_data["unidad_rendimiento"],
                    observaciones=receta_data["observaciones"],
                    estado=receta_data.get("estado", True),
                    insumos=insumos_mejorados  # ✅ Con insumo_id como string
                )
                recetas_response.append(receta_response)
                
            except Exception as e:
                print(f"Error procesando receta {receta_data.get('_id')}: {e}")
                continue
                
        return recetas_response
        
    except Exception as e:
        print(f"Error general al obtener recetas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/", response_model=RecetaResponse)
async def create_receta(receta_data: RecetaCreate):
    try:
        print("📥 Datos recibidos para crear receta:", receta_data.dict())
        
        # ✅ CONVERTIR MANUALMENTE strings a ObjectId para MongoDB
        receta_dict = receta_data.dict()
        
        # Los IDs vienen como strings del frontend, pero MongoDB necesita ObjectId
        from bson import ObjectId
        
        # Crear un nuevo dict con ObjectId
        mongo_data = {
            "producto_id": ObjectId(receta_dict["producto_id"]),
            "rendimiento": receta_dict["rendimiento"],
            "unidad_rendimiento": receta_dict["unidad_rendimiento"],
            "observaciones": receta_dict["observaciones"],
            "estado": receta_dict["estado"],
            "insumos": [
                {
                    "insumo_id": ObjectId(insumo["insumo_id"]),
                    "cantidad": insumo["cantidad"],
                    "unidad": insumo["unidad"]
                }
                for insumo in receta_dict["insumos"]
            ]
        }
        
        print("📤 Creando receta en MongoDB:", mongo_data)
        
        # ✅ Usar insert_one directamente para evitar problemas de Beanie
        database = get_database()
        result = await database.recetas.insert_one(mongo_data)
        
        print("✅ Receta creada exitosamente:", result.inserted_id)
        
        # Obtener la receta recién creada
        receta_creada = await database.recetas.find_one({"_id": result.inserted_id})
        
        if not receta_creada:
            raise HTTPException(status_code=500, detail="No se pudo recuperar la receta creada")
            
        return await convert_mongo_to_response(receta_creada)
        
    except Exception as e:
        print(f"❌ Error creando receta: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al crear receta: {str(e)}")

@router.get("/{receta_id}", response_model=RecetaResponse)
async def get_receta(receta_id: str):
    if not ObjectId.is_valid(receta_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    try:
        database = get_database()
        receta_data = await database.recetas.find_one({"_id": ObjectId(receta_id)})
        if receta_data is None:
            raise HTTPException(status_code=404, detail="Receta no encontrada")
        
        return await convert_mongo_to_response(receta_data)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error obteniendo receta: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/{receta_id}", response_model=RecetaResponse)
async def update_receta(receta_id: str, receta_data: RecetaCreate):
    if not ObjectId.is_valid(receta_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    receta = await Receta.get(receta_id)
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    update_data = receta_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(receta, key, value)
    
    await receta.save()
    
    updated_data = {
        "_id": receta.id,
        "producto_id": receta.producto_id,
        "rendimiento": receta.rendimiento,
        "unidad_rendimiento": receta.unidad_rendimiento,
        "observaciones": receta.observaciones,
        "estado": receta.estado,
        "insumos": receta.insumos
    }
    
    return await convert_mongo_to_response(updated_data)

@router.patch("/{receta_id}/estado")
async def cambiar_estado_receta(receta_id: str, estado: bool):
    if not ObjectId.is_valid(receta_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    receta = await Receta.get(receta_id)
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    receta.estado = estado
    await receta.save()
    return {"message": "Estado actualizado", "estado": estado}

@router.delete("/{receta_id}")
async def delete_receta(receta_id: str):
    if not ObjectId.is_valid(receta_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    receta = await Receta.get(receta_id)
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    await receta.delete()
    return {"message": "Receta eliminada correctamente"}