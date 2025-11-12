# models/denominaciones.py
from beanie import Document
from pydantic import BaseModel, Field

class Denominacion(Document):
    nominal: int

class DenominacionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    nominal: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
