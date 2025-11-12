from pydantic import BaseModel, Field
from typing import Optional

class Denominacion(BaseModel):
    id: Optional[str] = Field(alias="_id")
    nominal: int
