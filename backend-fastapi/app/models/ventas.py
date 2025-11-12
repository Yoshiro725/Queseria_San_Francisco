# models/ventas.py
from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from app.models.cliente import Cliente
from app.models.productos_lacteos import ProductoLacteo

class VentaDetalle(BaseModel):
    producto_id: Link[ProductoLacteo]
    cantidad: float
    precioVenta: float

class Venta(Document):
    fecha_venta: datetime
    total: float
    IVA: float
    cliente_id: Link[Cliente]
    detalle: List[VentaDetalle]

class VentaResponse(BaseModel):
    id: str = Field(..., alias="_id")
    fecha_venta: datetime
    total: float
    IVA: float
    cliente_id: str
    detalle: List[VentaDetalle]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
