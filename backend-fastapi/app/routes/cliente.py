from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from beanie import Link

from app.models.cliente import Cliente
from app.models.ciudad import Ciudad
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# ===============================
# Listar todos los clientes
# ===============================
@router.get("/", response_model=List[ClienteRead])
async def listar_clientes():
    clientes = await Cliente.find_all().to_list()
    return [
        ClienteRead(
            **cliente.dict(),
            _id=str(cliente.id),
            ciudad_id=str(cliente.ciudad_id.id) if cliente.ciudad_id else None
        )
        for cliente in clientes
    ]


# ===============================
# Agregar un cliente
# ===============================
@router.post("/", response_model=ClienteRead)
async def agregar_cliente(cliente: ClienteCreate):
    nuevo_cliente = Cliente(**cliente.model_dump())
    await nuevo_cliente.insert()
    return ClienteRead(
        **nuevo_cliente.dict(),
        _id=str(nuevo_cliente.id),
        ciudad_id=str(nuevo_cliente.ciudad_id.id) if nuevo_cliente.ciudad_id else None
    )


# ===============================
# Actualizar un cliente
# ===============================
@router.put("/{cliente_id}", response_model=ClienteRead)
async def actualizar_cliente(cliente_id: str, datos: ClienteUpdate):
    cliente = await Cliente.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    await cliente.set(datos.model_dump(exclude_unset=True))
    
    return ClienteRead(
        **cliente.dict(),
        _id=str(cliente.id),
        ciudad_id=str(cliente.ciudad_id.id) if cliente.ciudad_id else None
    )


# ===============================
# Eliminar un cliente
# ===============================
@router.delete("/{cliente_id}")
async def eliminar_cliente(cliente_id: str):
    cliente = await Cliente.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    await cliente.delete()
    return {"mensaje": "Cliente eliminado correctamente"}
