from beanie import Document

class CategoriaInsumo(Document):
    nombre: str
    descripcion: str | None = None

    class Settings:
        name = "categorias_insumo"