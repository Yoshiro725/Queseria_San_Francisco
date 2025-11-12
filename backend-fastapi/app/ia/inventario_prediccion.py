# app/ia/inventario_prediccion.py
import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Importaciones del proyecto
from app.models.productos_lacteos import ProductoLacteo
from app.core.config import settings


async def predecir_inventario(mostrar_grafica: bool = False, dias_prediccion: int = 7):
    """
    Predice el inventario de productos lácteos usando regresión lineal.
    """
    # 🔹 Conectar a MongoDB
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    await init_beanie(database=db, document_models=[ProductoLacteo])
    print("✅ Conectado a MongoDB Atlas")

    # 🔹 Obtener todos los productos
    productos = await ProductoLacteo.find_all().to_list()
    if not productos:
        return {"mensaje": "No hay productos en inventario", "resultado": None}

    # 🔹 Crear DataFrame asegurando que los campos obligatorios sean opcionales
    df = pd.DataFrame([
        {
            "desc_queso": getattr(p, "desc_queso", "Desconocido"),
            "precio": getattr(p, "precio", 0.0),
            "totalInventario": getattr(p, "totalInventario", 0)
        }
        for p in productos
    ])

    # 🔹 Preparar datos para modelo
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df["totalInventario"].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    # 🔹 Predecir inventario para los próximos días
    X_pred = np.array(range(len(df), len(df) + dias_prediccion)).reshape(-1, 1)
    predicciones = modelo.predict(X_pred)

    # 🔹 Mostrar gráfico si se pide
    if mostrar_grafica:
        plt.figure(figsize=(8, 4))
        plt.plot(range(len(df)), y, marker="o", label="Inventario Histórico")
        plt.plot(range(len(df), len(df) + dias_prediccion), predicciones, "ro", label="Predicción")
        plt.title("📈 Predicción de Inventario")
        plt.xlabel("Productos")
        plt.ylabel("Total Inventario")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # 🔹 Formatear resultado
    resultado = {
        "mensaje": "Predicción generada exitosamente",
        "resultado": predicciones.tolist(),
        "productos": df.to_dict(orient="records")
    }

    return resultado


# Para prueba rápida
if __name__ == "__main__":
    res = asyncio.run(predecir_inventario(mostrar_grafica=True))
    print(res)
