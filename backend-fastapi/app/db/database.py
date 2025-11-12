from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

# Importa tus modelos
from app.models.ciudad import Ciudad
from app.models.proveedor import Proveedor
from app.models.cliente import Cliente

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    database = client[settings.DB_NAME]

    await init_beanie(
        database=database,
        document_models=[
            Ciudad,
            Proveedor,
            Cliente
        ],
    )
