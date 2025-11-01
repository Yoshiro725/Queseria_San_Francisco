from beanie import Document

class Denominacion(Document):
    nombre: str
    descripcion: str | None = None

    class Settings:
        name = "denominaciones"
