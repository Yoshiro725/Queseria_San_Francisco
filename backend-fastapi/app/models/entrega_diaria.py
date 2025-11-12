# models/entregas_diarias.py
from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.proveedor import Proveedor

class EntregaDiaria(Document):
    proveedor_id: Link[Proveedor]
    fecha: datetime
    cantidad: float

class EntregaDiariaResponse(BaseModel):
    id: str = Field(..., alias="_id")
    proveedor_id: str
    fecha: datetime
    cantidad: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
