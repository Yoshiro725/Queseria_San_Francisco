from beanie import Document


class Ciudad(Document):
    nombre: str
    estado: str

    class Settings:
        name = "ciudades"  # Nombre de la colección en MongoDB
