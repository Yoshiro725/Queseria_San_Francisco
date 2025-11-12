from fastapi import FastAPI
from app.db.database import init_db
from app.routes import ai
from app.routes import ia_inventario 


# ✅ Importa las rutas antes de incluirlas
from app.routes import (
    cliente,
    proveedores,
    productos,
    producciones,
    categoria_insumo,
    ai,
    recetas,
    derivados,
    inventario_productos,
    ventas,
    precio_litro,
    movimiento_insumo,
    categoria_insumo,
    entrega_diaria,
    pagos_semanales,
    denominaciones,
    distribucion_pagos,
    reporte_inventario,
    reporte_produccion,
    cuidades
)



app = FastAPI(title="Quesería San Francisco API")

# ✅ Inicializa la base de datos al iniciar el servidor
@app.on_event("startup")
async def start_db():
    await init_db()

# ✅ Ruta de bienvenida
@app.get("/")
async def root():
    return {"mensaje": "Quesería San Francisco funcionando 🚀"}

# ✅ Registrar las rutas (endpoints) principales
app.include_router(cuidades.router)
app.include_router(proveedores.router)
app.include_router(cliente.router)
app.include_router(categoria_insumo.router)
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
app.include_router(ia_inventario.router)