from beanie import Document

class PrecioLitro(Document):
    producto_id: str
    precio: float
    fecha: str

    class Settings:
        name = "precios_litro"
