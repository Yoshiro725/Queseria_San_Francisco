from pydantic import BaseModel

class ClienteCreate(BaseModel):
    nombre: str
    correo: str | None = None
    telefono: str | None = None

class ClienteUpdate(BaseModel):
    nombre: str | None = None
    correo: str | None = None
    telefono: str | None = None

class ClienteRead(BaseModel):
    id: str
    nombre: str
    correo: str | None
    telefono: str | None
