from beanie import Document
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return {
            "type": "any",
            "json_schema": {
                "type": "string",
                "pattern": "^[a-f\\d]{24}$"
            }
        }

class DetalleVenta(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)
    precioVenta: float = Field(..., gt=0)
    nombre_producto: Optional[str] = None

    @field_validator('producto_id', mode='before')
    @classmethod
    def validate_producto_id(cls, v):
        """Convierte ObjectId a string"""
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v is not None else ""

class Venta(Document):
    fecha_venta: datetime = Field(default_factory=datetime.utcnow)
    total: float = Field(..., gt=0)
    IVA: float = Field(..., ge=0)
    cliente_id: str
    detalle: List[DetalleVenta] = Field(..., min_items=1)

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True
    )

    class Settings:
        name = "ventas"

class VentaCreate(BaseModel):
    fecha_venta: datetime
    total: float = Field(..., gt=0)
    IVA: float = Field(..., ge=0)
    cliente_id: str
    detalle: List[DetalleVenta] = Field(..., min_items=1)

class VentaResponse(BaseModel):
    id: str
    fecha_venta: datetime
    total: float
    IVA: float
    cliente_id: str
    detalle: List[DetalleVenta]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )