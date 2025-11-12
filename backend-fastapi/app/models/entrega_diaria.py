from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EntregaDiaria(BaseModel):
    id: Optional[str] = Field(alias="_id")
    proveedor_id: str
    fecha: datetime
    cantidad: float
