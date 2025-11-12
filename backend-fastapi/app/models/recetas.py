from pydantic import BaseModel, Field
from typing import Optional, List

class RecetaInsumo(BaseModel):
    insumo_id: str
    cantidad: float
    unidad: str

class Receta(BaseModel):
    id: Optional[str] = Field(alias="_id")
    producto_id: str
    rendimiento: float
    unidad_rendimiento: str
    observaciones: Optional[str]
    insumos: List[RecetaInsumo]
