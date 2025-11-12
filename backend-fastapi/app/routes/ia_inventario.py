from fastapi import APIRouter
import asyncio
from app.ia.inventario_prediccion import predecir_inventario  # tu módulo IA

router = APIRouter(
    prefix="/inventario",
    tags=["IA Inventario"]
)

@router.get("/prediccion")
async def obtener_prediccion_inventario(mostrar_grafica: bool = False, dias_prediccion: int = 7):
    """
    Retorna la predicción de inventario para todos los productos.
    - mostrar_grafica: si True, generará gráficas (para desarrollo/local)
    - dias_prediccion: número de días a predecir
    """
    resultado = await predecir_inventario(mostrar_grafica=mostrar_grafica, dias_prediccion=dias_prediccion)
    return {
        "mensaje": "Predicción generada exitosamente",
        "resultado": resultado["resultado"]
    }
