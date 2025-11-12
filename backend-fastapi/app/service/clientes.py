from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate
from bson import ObjectId

async def create_cliente(cliente: ClienteCreate):
    cliente_obj = Cliente(**cliente.dict())
    await cliente_obj.insert()
    # Convertir los campos a string para evitar errores de serialización
    cliente_obj.id = str(cliente_obj.id)
    if hasattr(cliente_obj, "ciudad_id") and not isinstance(cliente_obj.ciudad_id, str):
        cliente_obj.ciudad_id = str(cliente_obj.ciudad_id.id)
    return cliente_obj
