from fastapi import APIRouter
from app.models.ciudad import Ciudad

router = APIRouter(prefix="/ciudades", tags=["Ciudades"])

@router.get("/")
async def listar_ciudades():
    return await Ciudad.find_all().to_list()

@router.post("/")
async def agregar_ciudad(ciudad: Ciudad):
    await ciudad.insert()
    return {"mensaje": "Ciudad agregada correctamente"}
