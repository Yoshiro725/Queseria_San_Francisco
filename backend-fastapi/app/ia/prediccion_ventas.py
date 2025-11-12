import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Importaciones del proyecto
from app.models.ventas import Venta
from app.models.productos_lacteos import ProductoLacteo
from app.core.config import settings


async def cargar_datos_ventas(mostrar_grafica: bool = False):
    """
    Carga las ventas desde MongoDB, entrena un modelo de regresión lineal
    y devuelve la predicción y los datos agrupados.
    Si mostrar_grafica=True, muestra el gráfico de tendencia.
    """

    # 🔹 Conectar a MongoDB
    print(settings.MONGO_URI)

    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    await init_beanie(database=db, document_models=[Venta, ProductoLacteo])
    print("✅ Conectado a MongoDB Atlas")

    # 🔹 Obtener todas las ventas
    ventas = await Venta.find_all().to_list()
    print(f"📊 Ventas cargadas: {len(ventas)}")

    if not ventas:
        print("⚠️ No hay ventas registradas.")
        return {"mensaje": "No hay ventas registradas", "resultado": None}

    # 🔹 Crear un DataFrame
    df = pd.DataFrame([
        {
            "fecha_venta": v.fecha_venta,
            "total": v.total,
        }
        for v in ventas
    ])

    # 🔹 Agrupar por fecha
    df["fecha_venta"] = pd.to_datetime(df["fecha_venta"])
    df_agrupado = (
        df.groupby(df["fecha_venta"].dt.date)["total"]
        .sum()
        .reset_index()
        .sort_values("fecha_venta")
    )

    # 🔹 Entrenar modelo
    X = np.array(range(len(df_agrupado))).reshape(-1, 1)
    y = df_agrupado["total"].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    # 🔹 Predicción próxima venta
    prediccion = modelo.predict([[len(X)]])[0]
    print(f"🔮 Predicción próxima venta: ${prediccion:.2f}")

    # 🔹 Mostrar gráfico si se pide
    if mostrar_grafica:
        plt.figure(figsize=(8, 4))
        plt.plot(df_agrupado["fecha_venta"], df_agrupado["total"], marker="o", label="Histórico")
        plt.scatter(df_agrupado["fecha_venta"].iloc[-1] + pd.Timedelta(days=1), prediccion, color="red", label="Predicción")
        plt.title("📈 Tendencia de Ventas (Predicción)")
        plt.xlabel("Fecha")
        plt.ylabel("Total de Ventas ($)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # 🔹 Devolver resultado al endpoint
    return {
        "mensaje": "Predicción generada exitosamente",
        "resultado": round(float(prediccion), 2),
        "ventas_historicas": df_agrupado.to_dict(orient="records"),
    }



# Si ejecutas directamente el script, mostrará la gráfica
if __name__ == "__main__":
    asyncio.run(cargar_datos_ventas(mostrar_grafica=True))
