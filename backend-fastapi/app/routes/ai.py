from fastapi import APIRouter
import asyncio
from app.ia.prediccion_ventas import cargar_datos_ventas

router = APIRouter(prefix="/ia", tags=["Inteligencia Artificial"])

@router.get("/predicciones")
async def obtener_prediccion():
    # Ejecuta el modelo de IA y obtiene la predicción
    resultado = await cargar_datos_ventas()
    return {"mensaje": "Predicción generada exitosamente", "resultado": resultado}
