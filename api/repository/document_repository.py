from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from api.models.document import Document, DocumentChunk

class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(self, document: Document) -> Document:
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def create_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        self.session.add_all(chunks)
        await self.session.commit()
        return chunks

    async def get_document_by_id(self, doc_id: UUID) -> Document | None:
        statement = select(Document).where(Document.id == doc_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def search_similarity(self, embedding: List[float], limit: int = 5) -> List[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .order_by(DocumentChunk.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
