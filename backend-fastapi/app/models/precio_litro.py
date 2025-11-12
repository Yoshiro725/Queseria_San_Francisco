# models/precios_litro.py
from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime

class PrecioLitro(Document):
    anno: int
    semana: int
    fec_ini: datetime
    fec_fin: datetime
    precio: float

class PrecioLitroResponse(BaseModel):
    id: str = Field(..., alias="_id")
    anno: int
    semana: int
    fec_ini: datetime
    fec_fin: datetime
    precio: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
