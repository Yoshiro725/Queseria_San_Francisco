from fastapi import APIRouter, HTTPException
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteRead
from app.models.clientes import Cliente
from app.service.clientes import create_cliente, get_cliente, update_cliente, delete_cliente, list_clientes

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteRead)
async def create_cliente_endpoint(cliente: ClienteCreate):
    cliente_doc = Cliente(**cliente.dict())
    return await create_cliente(cliente_doc)

@router.get("/", response_model=list[ClienteRead])
async def list_clientes_endpoint():
    return await list_clientes()

@router.get("/{cliente_id}", response_model=ClienteRead)
async def get_cliente_endpoint(cliente_id: str):
    cliente = await get_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteRead)
async def update_cliente_endpoint(cliente_id: str, cliente: ClienteUpdate):
    updated_cliente = await update_cliente(cliente_id, cliente.dict(exclude_unset=True))
    if not updated_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return updated_cliente

@router.delete("/{cliente_id}")
async def delete_cliente_endpoint(cliente_id: str):
    deleted = await delete_cliente(cliente_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"mensaje": "Cliente eliminado correctamente"}
