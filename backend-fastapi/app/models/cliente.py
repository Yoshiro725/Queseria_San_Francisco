from beanie import Document
from pydantic import Field

class Cliente(Document):
    nombre_cliente: str
    RFC_cliente: str
    domicilio: str
    ciudad_id: str = Field(default=None)

    class Settings:
        name = "clientes"
