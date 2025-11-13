from beanie import Document
from pydantic import Field, ConfigDict
from typing import Optional
from bson import ObjectId

class Insumo(Document):
    nombre_insumo: str
    unidad: str
    categoria_id: str  # Mantener como string
    stock_actual: float
    stock_minimo: float
    costo_unitario: float

    class Settings:
        name = "insumos"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    # Método para manejar la carga desde MongoDB
    @classmethod
    def from_mongo(cls, data: dict):
        if data is not None:
            # Convertir categoria_id de ObjectId a string si es necesario
            if 'categoria_id' in data and isinstance(data['categoria_id'], ObjectId):
                data['categoria_id'] = str(data['categoria_id'])
        return cls(**data)