from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional

class ProductoLacteo(Document):
    desc_queso: Optional[str] = "Desconocido"
    precio: Optional[float] = 0.0
    totalInventario: int = 0

    class Settings:
        name = "productos_lacteos"
