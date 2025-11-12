# models/reportes_produccion.py
from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime

class ReporteProduccion(Document):
    fecha_inicio: datetime
    fecha_fin: datetime
    total_producido: float
    observaciones: str

class ReporteProduccionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    fecha_inicio: datetime
    fecha_fin: datetime
    total_producido: float
    observaciones: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
