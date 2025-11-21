from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

# Variables globales para acceso directo
client = None
database = None

# Importa tus modelos
from app.models.ciudad import Ciudad
from app.models.proveedor import Proveedor
from app.models.cliente import Cliente
from app.models.recetas import Receta
from app.models.productos_lacteos import ProductoLacteo
from app.models.insumos import Insumo
from app.models.ventas import Venta, VentaResponse, DetalleVenta

async def init_db():
    global client, database
    
    client = AsyncIOMotorClient(settings.MONGO_URI)
    database = client[settings.DB_NAME]

    await init_beanie(
        database=database,
        document_models=[
            Ciudad,
            Proveedor,
            Cliente,
            Receta,
            ProductoLacteo, 
            Insumo,
            Venta
        ],
    )

# Función para obtener la base de datos desde otros módulos
def get_database():
    if database is None:
        raise RuntimeError("La base de datos no ha sido inicializada. Llama a init_db() primero.")
    return database

# Función para obtener el cliente MongoDB
def get_client():
    if client is None:
        raise RuntimeError("El cliente MongoDB no ha sido inicializado. Llama a init_db() primero.")
    return client