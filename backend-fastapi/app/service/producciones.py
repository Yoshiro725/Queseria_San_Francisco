from app.models.produccion import Produccion

async def create_produccion(produccion_data):
    await produccion_data.insert()
    return produccion_data

async def get_produccion(produccion_id: str):
    return await Produccion.get(produccion_id)

async def update_produccion(produccion_id: str, update_data: dict):
    produccion = await Produccion.get(produccion_id)
    if produccion:
        await produccion.set(update_data)
    return produccion

async def delete_produccion(produccion_id: str):
    produccion = await Produccion.get(produccion_id)
    if produccion:
        await produccion.delete()
    return produccion

async def list_producciones():
    return await Produccion.find_all().to_list()
