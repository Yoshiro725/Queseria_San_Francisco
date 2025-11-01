from beanie import Document

class InventarioProducto(Document):
    producto_id: str
    cantidad: float

    class Settings:
        name = "inventario_productos"
