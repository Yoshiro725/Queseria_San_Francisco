from beanie import Document

class EntregaDiaria(Document):
    cliente_id: str
    producto_id: str
    cantidad: float
    fecha: str

    class Settings:
        name = "entregas_diarias"
