from beanie import Document

class Derivado(Document):
    nombre: str
    tipo: str
    descripcion: str | None = None

    class Settings:
        name = "derivados"
