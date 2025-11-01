from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Ciudad
from app.core.config import settings

db_client = None

async def init_db():
    global db_client
    db_client = AsyncIOMotorClient(settings.mongo_url)
    database = db_client[settings.mongo_db]

    # Inicializar Beanie con todos los modelos
    await init_beanie(database=database, document_models=[Ciudad])
    print("✅ Conexión a MongoDB establecida y Beanie inicializado")
