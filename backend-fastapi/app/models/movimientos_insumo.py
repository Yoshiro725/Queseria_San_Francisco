from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MovimientoInsumo(BaseModel):
    id: Optional[str] = Field(alias="_id")
    insumo_id: str
    fecha: datetime
    tipo_mov: str
    cantidad: float
    descripcion: str
