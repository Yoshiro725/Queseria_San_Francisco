from beanie import Document

class Proveedor(Document):
    nombre: str
    correo: str | None = None
    telefono: str | None = None

    class Settings:
        name = "proveedores"
