from pydantic import BaseModel, Field
from typing import Optional

class ProductoBase(BaseModel):
    desc_queso: str
    precio: float
    totalInventario: float

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    desc_queso: Optional[str]
    precio: Optional[float]
    totalInventario: Optional[float]

class ProductoRead(ProductoBase):
    id: str = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
