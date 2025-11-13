from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class InsumoRecetaResponse(BaseModel):
    insumo_id: str
    nombre_insumo: Optional[str] = None
    cantidad: float
    unidad: str

class RecetaResponse(BaseModel):
    id: str
    producto_id: str
    nombre_producto: Optional[str] = None
    rendimiento: float
    unidad_rendimiento: str
    observaciones: str
    insumos: List[InsumoRecetaResponse]
    estado: bool

class RecetaCreate(BaseModel):
    producto_id: str
    rendimiento: float
    unidad_rendimiento: str
    observaciones: str
    insumos: List[InsumoRecetaResponse]
    estado: bool = True