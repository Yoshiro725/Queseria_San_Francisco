from beanie import Document, Link
from pydantic import BaseModel
from typing import List
from app.models.productos_lacteos import ProductoLacteo
from app.models.insumos import Insumo

class InsumoReceta(BaseModel):
    insumo_id: Link[Insumo]
    cantidad: float
    unidad: str

class Receta(Document):
    producto_id: Link[ProductoLacteo]  # Relación con productos lácteos
    rendimiento: float
    unidad_rendimiento: str
    observaciones: str
    insumos: List[InsumoReceta]
