from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DetalleVenta(BaseModel):
    producto_id: str
    cantidad: int
    precioVenta: float

class VentaBase(BaseModel):
    fecha_venta: datetime
    total: float
    IVA: float
    cliente_id: str
    detalle: List[DetalleVenta]

class VentaCreate(VentaBase):
    pass

class VentaUpdate(BaseModel):
    total: Optional[float]
    IVA: Optional[float]
    cliente_id: Optional[str]
    detalle: Optional[List[DetalleVenta]]

class VentaRead(VentaBase):
    id: str = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
