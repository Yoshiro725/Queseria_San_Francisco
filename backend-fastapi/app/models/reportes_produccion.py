from beanie import Document

class ReporteProduccion(Document):
    fecha: str
    detalles: dict

    class Settings:
        name = "reportes_produccion"
