from beanie import Document

class DistribucionPago(Document):
    proveedor_id: str
    monto: float
    fecha: str

    class Settings:
        name = "distribucion_pagos"
