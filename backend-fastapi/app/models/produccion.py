from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class InsumoConsumido(BaseModel):
    insumo_id: str
    cantidad: float

class Produccion(BaseModel):
    id: Optional[str] = Field(alias="_id")
    receta_id: str
    fecha_produccion: datetime
    cantidad_producida: float
    unidad: str
    observaciones: Optional[str]
    insumos_consumidos: List[InsumoConsumido]
