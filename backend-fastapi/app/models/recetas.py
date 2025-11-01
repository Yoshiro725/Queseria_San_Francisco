from beanie import Document

class Receta(Document):
    nombre: str
    ingredientes: list[str]

    class Settings:
        name = "recetas"
