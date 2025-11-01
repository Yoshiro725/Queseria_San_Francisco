from app.models.productos_lacteos import ProductoLacteo

async def create_producto(producto_data: ProductoLacteo):
    await producto_data.insert()
    return producto_data

async def get_producto(producto_id: str):
    return await ProductoLacteo.get(producto_id)

async def update_producto(producto_id: str, update_data: dict):
    producto = await ProductoLacteo.get(producto_id)
    if producto:
        await producto.set(update_data)
    return producto

async def delete_producto(producto_id: str):
    producto = await ProductoLacteo.get(producto_id)
    if producto:
        await producto.delete()
    return producto

async def list_productos():
    return await ProductoLacteo.find_all().to_list()
