# models/reportes_inventario.py
from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime

class ReporteInventario(Document):
    fecha: datetime
    tipo: str
    descripcion: str

class ReporteInventarioResponse(BaseModel):
    id: str = Field(..., alias="_id")
    fecha: datetime
    tipo: str
    descripcion: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
