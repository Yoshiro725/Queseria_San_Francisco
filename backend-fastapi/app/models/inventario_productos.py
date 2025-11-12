from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class InventarioProducto(BaseModel):
    id: Optional[str] = Field(alias="_id")
    producto_id: str
    fecha_entrada: datetime
    cantidad_disponible: float
    costo_unitario: float
    ubicacion: str
