# models/derivados.py
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.models.productos_lacteos import ProductoLacteo

class Derivado(Document):
    receta_origen_id: Link[ProductoLacteo]
    nombre_derivado: str
    cantidad_generada: float
    unidad: str

class DerivadoResponse(BaseModel):
    id: str = Field(..., alias="_id")
    receta_origen_id: str
    nombre_derivado: str
    cantidad_generada: float
    unidad: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
