from beanie import Document

class PagoSemanal(Document):
    proveedor_id: str
    monto: float
    fecha: str

    class Settings:
        name = "pagos_semanales"
