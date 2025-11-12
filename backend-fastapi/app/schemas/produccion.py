from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class InsumoConsumido(BaseModel):
    insumo_id: str
    cantidad: float

class ProduccionBase(BaseModel):
    receta_id: str
    fecha_produccion: datetime
    cantidad_producida: float
    unidad: str
    observaciones: Optional[str]
    insumos_consumidos: List[InsumoConsumido]

class ProduccionCreate(ProduccionBase):
    pass

class ProduccionUpdate(BaseModel):
    cantidad_producida: Optional[float]
    unidad: Optional[str]
    observaciones: Optional[str]
    insumos_consumidos: Optional[List[InsumoConsumido]]

class ProduccionRead(ProduccionBase):
    id: str = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
