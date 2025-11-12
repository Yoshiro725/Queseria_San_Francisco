# models/pagos_semanales.py
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.models.proveedor import Proveedor

class PagoSemanal(Document):
    proveedor_id: Link[Proveedor]
    anno: int
    semana: int
    importe: float
    cantidad: float

class PagoSemanalResponse(BaseModel):
    id: str = Field(..., alias="_id")
    proveedor_id: str
    anno: int
    semana: int
    importe: float
    cantidad: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
