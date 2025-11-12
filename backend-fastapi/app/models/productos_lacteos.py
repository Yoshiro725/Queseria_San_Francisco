from pydantic import BaseModel, Field
from typing import Optional

class ProductoLacteo(BaseModel):
    id: Optional[str] = Field(alias="_id")
    desc_queso: str
    precio: float
    totalInventario: float

