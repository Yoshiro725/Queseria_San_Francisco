# models/distribucion_pagos.py
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.models.proveedor import Proveedor

class DistribucionPago(Document):
    proveedor_id: Link[Proveedor]
    anno: int
    semana: int
    denominacion: int
    cantidad: int

class DistribucionPagoResponse(BaseModel):
    id: str = Field(..., alias="_id")
    proveedor_id: str
    anno: int
    semana: int
    denominacion: int
    cantidad: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
