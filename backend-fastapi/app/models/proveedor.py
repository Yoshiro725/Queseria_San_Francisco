from beanie import Document, Link
from pydantic import Field
from app.models.ciudad import Ciudad

class Proveedor(Document):
    nombre: str = Field(..., description="Nombre del proveedor")
    estado: str = Field(..., description="Estado (A=activo, I=inactivo)")
    domicilio: str = Field(..., description="Dirección completa")
    ciudad_id: Link[Ciudad]  # Relación con Ciudad

    class Settings:
        name = "proveedores"
