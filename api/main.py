from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.config.database import init_db
from api.config import env
from api.routes import v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting up Koda API in {env.ENVIRONMENT} mode...")
    await init_db()
    print("Database connection established and tables initialized.")
    
    yield
    
    print("Shutting down Koda API...")

app = FastAPI(
    title="Koda Knowledge Engine API",
    version="0.1.0",
    description="Backend for RAG-based knowledge synthesis.",
    lifespan=lifespan
)

app.include_router(v1.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {
        "status": "operational",
        "environment": env.ENVIRONMENT,
        "database": "connected"
    }

@app.get("/")
async def root():
    return {"message": "Welcome to Koda API"}
