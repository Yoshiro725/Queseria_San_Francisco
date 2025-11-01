from beanie import Document

class Venta(Document):
    cliente_id: str
    producto_id: str
    cantidad: float
    total: float
    fecha: str

    class Settings:
        name = "ventas"
