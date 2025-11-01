from app.models.clientes import Cliente

async def create_cliente(cliente_data):
    await cliente_data.insert()
    return cliente_data

async def get_cliente(cliente_id: str):
    return await Cliente.get(cliente_id)

async def update_cliente(cliente_id: str, update_data: dict):
    cliente = await Cliente.get(cliente_id)
    if cliente:
        await cliente.set(update_data)
    return cliente

async def delete_cliente(cliente_id: str):
    cliente = await Cliente.get(cliente_id)
    if cliente:
        await cliente.delete()
    return cliente

async def list_clientes():
    return await Cliente.find_all().to_list()
