from fastapi import FastAPI
from app.db.database import init_db

app = FastAPI(title="Quesería San Francisco API")

@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/")
async def root():
    return {"mensaje": " Quesería San Francisco funcionando 🚀"}
