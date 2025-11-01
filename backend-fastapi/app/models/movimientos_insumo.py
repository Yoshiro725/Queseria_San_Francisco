from beanie import Document

class MovimientoInsumo(Document):
    insumo_id: str
    tipo: str  # "entrada" o "salida"
    cantidad: float
    fecha: str

    class Settings:
        name = "movimientos_insumo"
