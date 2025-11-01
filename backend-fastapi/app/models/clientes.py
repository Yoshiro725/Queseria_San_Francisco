from beanie import Document

class Cliente(Document):
    nombre: str
    correo: str
    telefono: str

    class Settings:
        name = "clientes"  # Nombre de la colección en MongoDB

