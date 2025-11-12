from beanie import Document, Link
from app.models.ciudad import Ciudad

class Cliente(Document):
    nombre_cliente: str
    RFC_cliente: str
    domicilio: str
    ciudad_id: Link[Ciudad]  # 👈 sigue siendo Link, eso está bien
