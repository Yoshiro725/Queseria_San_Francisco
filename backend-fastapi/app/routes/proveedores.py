from fastapi import APIRouter, HTTPException
from app.models.proveedores import Proveedor

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

@router.post("/", response_model=Proveedor)
async def create_proveedor(proveedor: Proveedor):
    await proveedor.insert()
    return proveedor

@router.get("/", response_model=list[Proveedor])
async def list_proveedores():
    proveedores = await Proveedor.find_all().to_list()
    return proveedores

@router.get("/{proveedor_id}", response_model=Proveedor)
async def get_proveedor(proveedor_id: str):
    proveedor = await Proveedor.get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.put("/{proveedor_id}", response_model=Proveedor)
async def update_proveedor(proveedor_id: str, update_data: dict):
    proveedor = await Proveedor.get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    await proveedor.set(update_data)
    return proveedor

@router.delete("/{proveedor_id}")
async def delete_proveedor(proveedor_id: str):
    proveedor = await Proveedor.get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    await proveedor.delete()
    return {"detail": "Proveedor eliminado"}
