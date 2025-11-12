from pydantic import BaseModel, Field
from typing import Optional

class DistribucionPago(BaseModel):
    id: Optional[str] = Field(alias="_id")
    proveedor_id: str
    anno: int
    semana: int
    denominacion: int
    cantidad: int
