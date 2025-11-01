from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre: str
    tipo: str
    descripcion: str | None = None

class ProductoUpdate(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    descripcion: str | None = None

class ProductoResponse(BaseModel):
    id: str
    nombre: str
    tipo: str
    descripcion: str | None = None

    class Config:
        orm_mode = True
