# models/inventario_productos.py
from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.productos_lacteos import ProductoLacteo

class InventarioProducto(Document):
    producto_id: Link[ProductoLacteo]
    fecha_entrada: datetime
    cantidad_disponible: float
    costo_unitario: float
    ubicacion: str

class InventarioProductoResponse(BaseModel):
    id: str = Field(..., alias="_id")
    producto_id: str
    fecha_entrada: datetime
    cantidad_disponible: float
    costo_unitario: float
    ubicacion: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
