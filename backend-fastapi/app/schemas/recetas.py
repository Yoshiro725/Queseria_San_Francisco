from pydantic import BaseModel
from typing import List, Optional

class InsumoRecetaCreate(BaseModel):
    insumo_id: str  # ✅ El frontend envía strings
    nombre_insumo: Optional[str] = None
    cantidad: float
    unidad: str

class RecetaCreate(BaseModel):
    producto_id: str  # ✅ El frontend envía strings
    rendimiento: float
    unidad_rendimiento: str
    observaciones: str
    insumos: List[InsumoRecetaCreate]
    estado: bool = True

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