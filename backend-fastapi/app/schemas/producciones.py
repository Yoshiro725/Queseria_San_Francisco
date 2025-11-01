from pydantic import BaseModel
from datetime import datetime

class ProduccionCreate(BaseModel):
    producto_id: str
    cantidad: int

class ProduccionUpdate(BaseModel):
    producto_id: str | None = None
    cantidad: int | None = None

class ProduccionRead(BaseModel):
    id: str
    producto_id: str
    cantidad: int
    fecha: datetime
