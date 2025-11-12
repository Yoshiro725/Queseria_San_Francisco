from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReporteProduccion(BaseModel):
    id: Optional[str] = Field(alias="_id")
    fecha_inicio: datetime
    fecha_fin: datetime
    total_producido: float
    observaciones: str
