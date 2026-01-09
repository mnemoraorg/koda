from fastapi import APIRouter
from api.controller import ingest_controller

router = APIRouter()

router.include_router(ingest_controller.router, tags=["Ingestion"])
