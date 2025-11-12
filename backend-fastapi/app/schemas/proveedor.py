from pydantic import BaseModel, Field
from typing import Optional

class ProveedorBase(BaseModel):
    nombre: str
    estado: str
    domicilio: str
    ciudad_id: str

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre: Optional[str]
    estado: Optional[str]
    domicilio: Optional[str]
    ciudad_id: Optional[str]

class ProveedorRead(ProveedorBase):
    id: str = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
