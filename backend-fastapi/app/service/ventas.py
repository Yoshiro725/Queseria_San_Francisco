from app.models.ventas import Venta

async def create_venta(venta_data):
    await venta_data.insert()
    return venta_data

async def get_venta(venta_id: str):
    return await Venta.get(venta_id)

async def update_venta(venta_id: str, update_data: dict):
    venta = await Venta.get(venta_id)
    if venta:
        await venta.set(update_data)
    return venta

async def delete_venta(venta_id: str):
    venta = await Venta.get(venta_id)
    if venta:
        await venta.delete()
    return venta

async def list_ventas():
    return await Venta.find_all().to_list()
