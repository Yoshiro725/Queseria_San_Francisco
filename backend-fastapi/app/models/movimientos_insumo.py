# models/movimientos_insumo.py
from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.insumos import Insumo

class MovimientoInsumo(Document):
    insumo_id: Link[Insumo]
    fecha: datetime
    tipo_mov: str
    cantidad: float
    descripcion: str

class MovimientoInsumoResponse(BaseModel):
    id: str = Field(..., alias="_id")
    insumo_id: str
    fecha: datetime
    tipo_mov: str
    cantidad: float
    descripcion: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
