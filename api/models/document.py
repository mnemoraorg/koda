from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, SQLModel, Relationship

class DocumentBase(SQLModel):
    title: str
    filename: str
    file_path: str
    file_size_bytes: int
    content_type: str = "application/pdf"
    
class Document(DocumentBase, table=True):
    __tablename__ = "documents"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    
    # Relationships
    chunks: List["DocumentChunk"] = Relationship(back_populates="document")

class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunks"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_id: UUID = Field(foreign_key="documents.id")
    
    # Text Content
    chunk_index: int
    content: str
    
    # Vector Embedding (Length 768 for Gemini Pro, usually)
    # Using sa_column to define the custom Vector type from pgvector
    embedding: List[float] = Field(sa_column=Column(Vector(768)))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    document: Document = Relationship(back_populates="chunks")
