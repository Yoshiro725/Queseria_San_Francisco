from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.routes import insumos
from app.routes import (
    cliente, proveedores, productos, producciones, categoria_insumo,
    ai, recetas, derivados, inventario_productos, ventas, precio_litro,
    movimiento_insumo, entrega_diaria, pagos_semanales, denominaciones,
    distribucion_pagos, reporte_inventario, reporte_produccion, cuidades
)

app = FastAPI(title="Quesería San Francisco API")

# ✅ CONFIGURACIÓN CORS CORRECTA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # URL de Angular
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # ← INCLUIR OPTIONS
    allow_headers=["*"],  # Permitir todos los headers
)

# ✅ Inicializa la base de datos
@app.on_event("startup")
async def start_db():
    await init_db()

# ✅ Ruta de bienvenida
@app.get("/")
async def root():
    return {"mensaje": "Quesería San Francisco funcionando 🚀"}

# ✅ Registrar las rutas
app.include_router(insumos.router)
app.include_router(cuidades.router)
app.include_router(proveedores.router)
app.include_router(cliente.router)
app.include_router(categoria_insumo.router)
app.include_router(movimiento_insumo.router)
app.include_router(productos.router)
app.include_router(recetas.router)
app.include_router(derivados.router)
app.include_router(producciones.router)
app.include_router(inventario_productos.router)
app.include_router(ventas.router)
app.include_router(precio_litro.router)
app.include_router(entrega_diaria.router)
app.include_router(pagos_semanales.router)
app.include_router(denominaciones.router)
app.include_router(distribucion_pagos.router)
app.include_router(reporte_inventario.router)
app.include_router(reporte_produccion.router)
app.include_router(ai.router)