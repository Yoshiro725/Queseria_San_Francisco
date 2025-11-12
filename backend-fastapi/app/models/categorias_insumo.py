# models/categorias_insumo.py
from beanie import Document
from pydantic import BaseModel, Field

class CategoriaInsumo(Document):
    nombre_categoria: str

class CategoriaInsumoResponse(BaseModel):
    id: str = Field(..., alias="_id")
    nombre_categoria: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
