from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PrecioLitro(BaseModel):
    id: Optional[str] = Field(alias="_id")
    anno: int
    semana: int
    fec_ini: datetime
    fec_fin: datetime
    precio: float
