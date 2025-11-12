from pydantic import BaseModel, Field
from typing import Optional

class CiudadBase(BaseModel):
    nom_ciudad: str
    estado: str

class CiudadCreate(CiudadBase):
    pass

class CiudadUpdate(BaseModel):
    nom_ciudad: Optional[str]
    estado: Optional[str]

class CiudadRead(CiudadBase):
    id: str = Field(alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
