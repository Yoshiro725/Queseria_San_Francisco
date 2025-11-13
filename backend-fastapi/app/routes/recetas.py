from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.db.database import get_database
from app.models.recetas import Receta
from app.models.insumos import Insumo
from app.models.productos_lacteos import ProductoLacteo
from app.schemas.recetas import RecetaResponse, RecetaCreate

router = APIRouter(prefix="/recetas", tags=["Recetas"])

# === ENDPOINTS PRINCIPALES ===

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
                # Manejar producto_id (puede ser ObjectId o string)
                producto_id = receta_data["producto_id"]
                if isinstance(producto_id, ObjectId):
                    producto_id_str = str(producto_id)
                else:
                    producto_id_str = producto_id
                
                nombre_producto = producto_map.get(producto_id_str, "Producto no encontrado")
                
                # Mejorar insumos
                insumos_mejorados = []
                for insumo in receta_data.get("insumos", []):
                    # Manejar insumo_id (puede ser ObjectId o string)
                    insumo_id = insumo["insumo_id"]
                    if isinstance(insumo_id, ObjectId):
                        insumo_id_str = str(insumo_id)
                    else:
                        insumo_id_str = insumo_id
                    
                    nombre_insumo = insumo_map.get(insumo_id_str, "Insumo no encontrado")
                    
                    insumos_mejorados.append({
                        "insumo_id": insumo_id_str,
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
                    insumos=insumos_mejorados
                )
                recetas_response.append(receta_response)
                
            except Exception as e:
                print(f"Error procesando receta {receta_data.get('_id')}: {e}")
                continue
                
        return recetas_response
        
    except Exception as e:
        print(f"Error general al obtener recetas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
# === ENDPOINTS DE DEBUG ===

@router.get("/debug/productos")
async def debug_productos():
    try:
        database = get_database()
        productos = await database.productos_lacteos.find().to_list(length=None)
        return [
            {
                "id": str(p["_id"]),
                "desc_queso": p.get("desc_queso", "Sin nombre"),
                "precio": p.get("precio", 0)
            }
            for p in productos
        ]
    except Exception as e:
        return {"error": str(e)}

@router.get("/debug/insumos")
async def debug_insumos():
    try:
        database = get_database()
        insumos = await database.insumos.find().to_list(length=None)
        return [
            {
                "id": str(i["_id"]),
                "nombre_insumo": i.get("nombre_insumo", "Sin nombre"),
                "unidad": i.get("unidad", "Sin unidad")
            }
            for i in insumos
        ]
    except Exception as e:
        return {"error": str(e)}

@router.get("/debug/recetas-raw")
async def debug_recetas_raw():
    try:
        database = get_database()
        recetas = await database.recetas.find().to_list(length=None)
        return [
            {
                "id": str(r["_id"]),
                "producto_id": str(r.get("producto_id", "")),
                "rendimiento": r.get("rendimiento", 0),
                "insumos": [
                    {
                        "insumo_id": str(insumo.get("insumo_id", "")),
                        "cantidad": insumo.get("cantidad", 0),
                        "unidad": insumo.get("unidad", "")
                    }
                    for insumo in r.get("insumos", [])
                ]
            }
            for r in recetas
        ]
    except Exception as e:
        return {"error": str(e)}

# === FUNCIONES AUXILIARES ===

async def convert_mongo_to_response(receta_data: dict) -> RecetaResponse:
    try:
        receta_id = str(receta_data.get("_id", ""))
        
        producto_id = str(receta_data.get("producto_id", ""))
        
        nombre_producto = "Producto no encontrado"
        if producto_id and ObjectId.is_valid(producto_id):
            try:
                producto = await ProductoLacteo.get(producto_id)
                if producto and hasattr(producto, 'desc_queso'):
                    nombre_producto = producto.desc_queso
            except Exception as e:
                print(f"Error obteniendo producto {producto_id}: {e}")
        
        insumos_con_nombre = []
        for insumo_data in receta_data.get("insumos", []):
            try:
                insumo_id = str(insumo_data.get("insumo_id", ""))
                
                nombre_insumo = "Insumo no encontrado"
                if insumo_id and ObjectId.is_valid(insumo_id):
                    try:
                        insumo = await Insumo.get(insumo_id)
                        if insumo and hasattr(insumo, 'nombre_insumo'):
                            nombre_insumo = insumo.nombre_insumo
                    except Exception as e:
                        print(f"Error obteniendo insumo {insumo_id}: {e}")
                
                insumos_con_nombre.append({
                    "insumo_id": insumo_id,
                    "nombre_insumo": nombre_insumo,
                    "cantidad": insumo_data.get("cantidad", 0.0),
                    "unidad": insumo_data.get("unidad", "unidad")
                })
            except Exception as e:
                print(f"Error procesando insumo: {e}")
                continue
        
        return RecetaResponse(
            id=receta_id,
            producto_id=producto_id,
            nombre_producto=nombre_producto,
            rendimiento=receta_data.get("rendimiento", 0.0),
            unidad_rendimiento=receta_data.get("unidad_rendimiento", "kg"),
            observaciones=receta_data.get("observaciones", ""),
            estado=receta_data.get("estado", True),
            insumos=insumos_con_nombre
        )
        
    except Exception as e:
        print(f"Error grave en convert_mongo_to_response: {e}")
        return RecetaResponse(
            id=str(receta_data.get("_id", "")),
            producto_id=str(receta_data.get("producto_id", "")),
            nombre_producto="Error al cargar",
            rendimiento=receta_data.get("rendimiento", 0.0),
            unidad_rendimiento=receta_data.get("unidad_rendimiento", "kg"),
            observaciones=receta_data.get("observaciones", ""),
            estado=receta_data.get("estado", True),
            insumos=[]
        )

# === RESTO DE ENDPOINTS ===

@router.post("/", response_model=RecetaResponse)
async def create_receta(receta: RecetaCreate):
    try:
        receta_dict = receta.dict()
        
        receta_dict["producto_id"] = ObjectId(receta_dict["producto_id"])
        for insumo in receta_dict["insumos"]:
            insumo["insumo_id"] = ObjectId(insumo["insumo_id"])
        
        nueva_receta = Receta(**receta_dict)
        await nueva_receta.insert()
        
        receta_data = {
            "_id": nueva_receta.id,
            "producto_id": nueva_receta.producto_id,
            "rendimiento": nueva_receta.rendimiento,
            "unidad_rendimiento": nueva_receta.unidad_rendimiento,
            "observaciones": nueva_receta.observaciones,
            "estado": nueva_receta.estado,
            "insumos": nueva_receta.insumos
        }
        
        return await convert_mongo_to_response(receta_data)
        
    except Exception as e:
        print(f"Error creando receta: {e}")
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