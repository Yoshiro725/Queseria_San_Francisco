from beanie import Document
from pydantic import Field

class Ciudad(Document):
    nom_ciudad: str = Field(..., description="Nombre de la ciudad")
    estado: str = Field(..., description="Estado al que pertenece")

    class Settings:
        name = "ciudades"
