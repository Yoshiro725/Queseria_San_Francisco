from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReporteInventario(BaseModel):
    id: Optional[str] = Field(alias="_id")
    fecha: datetime
    tipo: str
    descripcion: str
