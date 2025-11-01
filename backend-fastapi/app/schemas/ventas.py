from pydantic import BaseModel
from datetime import datetime

class VentaCreate(BaseModel):
    cliente_id: str
    producto_id: str
    cantidad: int
    total: float

class VentaUpdate(BaseModel):
    cliente_id: str | None = None
    producto_id: str | None = None
    cantidad: int | None = None
    total: float | None = None

class VentaRead(BaseModel):
    id: str
    cliente_id: str
    producto_id: str
    cantidad: int
    total: float
    fecha: datetime
