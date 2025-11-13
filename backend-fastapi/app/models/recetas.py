from beanie import Document
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from bson import ObjectId

# Solución más simple - usar str y dejar que Beanie maneje la conversión
class InsumoReceta(BaseModel):
    insumo_id: str  # Simple string
    cantidad: float
    unidad: str

class Receta(Document):
    producto_id: str  # Simple string
    rendimiento: float
    unidad_rendimiento: str = "kg"
    observaciones: str = ""
    insumos: List[InsumoReceta]
    estado: bool = True

    class Settings:
        name = "recetas"

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True
    )