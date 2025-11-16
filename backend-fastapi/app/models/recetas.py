from beanie import Document
from pydantic import BaseModel, ConfigDict
from typing import List
from bson import ObjectId

class InsumoReceta(BaseModel):
    insumo_id: str  # ← STRING simple
    cantidad: float
    unidad: str

class Receta(Document):
    producto_id: str  # ← STRING simple
    rendimiento: float
    unidad_rendimiento: str = "kg"
    observaciones: str = ""
    insumos: List[InsumoReceta]
    estado: bool = True

    class Settings:
        name = "recetas"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )