from pydantic import BaseModel

class ProveedorCreate(BaseModel):
    nombre: str
    contacto: str
    telefono: str

class ProveedorUpdate(BaseModel):
    nombre: str | None = None
    contacto: str | None = None
    telefono: str | None = None

class ProveedorResponse(BaseModel):
    id: str
    nombre: str
    contacto: str
    telefono: str

    class Config:
        orm_mode = True
