from pydantic import BaseModel, Field
from typing import Optional

class CategoriaInsumo(BaseModel):
    id: Optional[str] = Field(alias="_id")
    nombre_categoria: str
