from beanie import Document

class ReporteInventario(Document):
    fecha: str
    detalles: dict

    class Settings:
        name = "reportes_inventario"
