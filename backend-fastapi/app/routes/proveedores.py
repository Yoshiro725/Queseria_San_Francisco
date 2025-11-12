from fastapi import APIRouter, HTTPException
from typing import List
from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorCreate, ProveedorRead, ProveedorUpdate

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

@router.get("/", response_model=List[ProveedorRead])
async def listar_proveedores():
    proveedores = await Proveedor.find_all().to_list()
    return proveedores

@router.post("/", response_model=ProveedorRead)
async def agregar_proveedor(proveedor: ProveedorCreate):
    nuevo_proveedor = Proveedor(**proveedor.model_dump())
    await nuevo_proveedor.insert()
    return nuevo_proveedor

@router.put("/{proveedor_id}", response_model=ProveedorRead)
async def actualizar_proveedor(proveedor_id: str, datos: ProveedorUpdate):
    proveedor = await Proveedor.get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    await proveedor.set(datos.model_dump(exclude_unset=True))
    return proveedor

@router.delete("/{proveedor_id}")
async def eliminar_proveedor(proveedor_id: str):
    proveedor = await Proveedor.get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    await proveedor.delete()
    return {"mensaje": "Proveedor eliminado correctamente"}
