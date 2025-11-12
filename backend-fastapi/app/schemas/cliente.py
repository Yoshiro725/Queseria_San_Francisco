from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from beanie import Link
from app.models.ciudad import Ciudad  # importa tu modelo de ciudad si usas Link

# Modelo base
class ClienteBase(BaseModel):
    nombre_cliente: str
    RFC_cliente: str
    domicilio: str
    ciudad_id: str  # Se mantiene como string para devolver correctamente

# Modelo de creación
class ClienteCreate(ClienteBase):
    pass

# Modelo de actualización
class ClienteUpdate(BaseModel):
    nombre_cliente: Optional[str] = None
    RFC_cliente: Optional[str] = None
    domicilio: Optional[str] = None
    ciudad_id: Optional[str] = None

# Modelo de lectura (para respuestas)
class ClienteRead(ClienteBase):
    id: str = Field(..., alias="_id")  # convierte ObjectId a string automáticamente

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            ObjectId: str,        # ✅ convierte ObjectId a string
            Link: lambda link: str(link.id) if link else None  # convierte Link a string del id
        }
