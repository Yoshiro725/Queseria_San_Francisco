from beanie import Document

class Produccion(Document):
    producto_id: str
    cantidad: float
    fecha: str

    class Settings:
        name = "producciones"
