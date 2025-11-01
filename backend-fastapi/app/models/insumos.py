from beanie import Document

class Insumo(Document):
    nombre: str
    cantidad: float
    unidad: str

    class Settings:
        name = "insumos"
