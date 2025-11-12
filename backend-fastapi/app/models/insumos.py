from pydantic import BaseModel, Field
from typing import Optional

class Insumo(BaseModel):
    id: Optional[str] = Field(alias="_id")
    nombre_insumo: str
    unidad: str
    categoria_id: str
    stock_actual: float
    stock_minimo: float
    costo_unitario: float
