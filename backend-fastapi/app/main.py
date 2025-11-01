from fastapi import FastAPI
from app.db.database import init_db

# ✅ Importa las rutas antes de incluirlas
from app.routes import clientes, productos, proveedores, ventas, producciones


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
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(proveedores.router)
app.include_router(ventas.router)
app.include_router(producciones.router)
