from beanie import Document
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from bson import ObjectId

# ✅ IMPLEMENTACIÓN CORRECTA para Pydantic v2
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _info):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str) and ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

class InsumoReceta(BaseModel):
    insumo_id: PyObjectId
    cantidad: float
    unidad: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class Receta(Document):
    producto_id: PyObjectId
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