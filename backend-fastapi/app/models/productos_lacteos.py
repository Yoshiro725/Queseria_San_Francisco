from beanie import Document

class ProductoLacteo(Document):
    nombre: str
    tipo: str
    descripcion: str | None = None

    class Settings:
        name = "productos_lacteos"
