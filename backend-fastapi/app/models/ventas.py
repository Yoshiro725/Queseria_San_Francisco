from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class DetalleVenta(BaseModel):
    producto_id: str
    cantidad: int
    precioVenta: float

class Venta(BaseModel):
    id: Optional[str] = Field(alias="_id")
    fecha_venta: datetime
    total: float
    IVA: float
    cliente_id: str
    detalle: List[DetalleVenta]
