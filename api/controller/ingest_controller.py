from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.config.database import get_db
from api.repository.document_repository import DocumentRepository
from api.services.ingest_service import IngestService
from api.models.document import Document

router = APIRouter()

async def get_repository(session: AsyncSession = Depends(get_db)) -> DocumentRepository:
    return DocumentRepository(session)

async def get_service(repo: DocumentRepository = Depends(get_repository)) -> IngestService:
    return IngestService(repo)

@router.post("/ingest", response_model=Document)
async def ingest_document(
    file: UploadFile = File(...),
    service: IngestService = Depends(get_service)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        doc = await service.ingest_document(file)
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
