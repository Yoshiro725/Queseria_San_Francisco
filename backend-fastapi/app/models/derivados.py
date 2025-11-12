from pydantic import BaseModel, Field
from typing import Optional

class Derivado(BaseModel):
    id: Optional[str] = Field(alias="_id")
    receta_origen_id: str
    nombre_derivado: str
    cantidad_generada: float
    unidad: str
