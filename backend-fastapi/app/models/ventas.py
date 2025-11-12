from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class DetalleVenta(BaseModel):
    producto_id: Any
    cantidad: int
    precioVenta: Optional[float] = None

class Venta(Document):
    fecha_venta: datetime = Field(default_factory=datetime.utcnow)
    total: float = 0
    IVA: float = 0
    cliente_id: Optional[Any] = None  # ✅ ahora puede faltar
    detalle: List[DetalleVenta] = Field(default_factory=list)

    class Settings:
        name = "ventas"


# ✅ Agregamos VentaResponse al final
class VentaResponse(BaseModel):
    id: str
    fecha_venta: datetime
    total: float
    IVA: float
    cliente_id: Optional[Any]
    detalle: List[dict]

    class Config:
        from_attributes = True  # equivale a orm_mode en Pydantic v1
