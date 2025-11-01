from app.models.proveedores import Proveedor

async def create_proveedor(proveedor_data: Proveedor):
    await proveedor_data.insert()
    return proveedor_data

async def get_proveedor(proveedor_id: str):
    return await Proveedor.get(proveedor_id)

async def update_proveedor(proveedor_id: str, update_data: dict):
    proveedor = await Proveedor.get(proveedor_id)
    if proveedor:
        await proveedor.set(update_data)
    return proveedor

async def delete_proveedor(proveedor_id: str):
    proveedor = await Proveedor.get(proveedor_id)
    if proveedor:
        await proveedor.delete()
    return proveedor

async def list_proveedores():
    return await Proveedor.find_all().to_list()
