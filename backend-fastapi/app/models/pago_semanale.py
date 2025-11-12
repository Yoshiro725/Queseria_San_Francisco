from pydantic import BaseModel, Field
from typing import Optional

class PagoSemanal(BaseModel):
    id: Optional[str] = Field(alias="_id")
    proveedor_id: str
    anno: int
    semana: int
    importe: float
    cantidad: float
