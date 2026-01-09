import os
import tempfile
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from api.config import env
from api.models.document import Document, DocumentChunk
from api.repository.document_repository import DocumentRepository

class IngestService:
    def __init__(self, repo: DocumentRepository):
        self.repo = repo
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=env.GOOGLE_GEMINI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def ingest_document(self, file: UploadFile) -> Document:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            loader = PyPDFLoader(tmp_path)
            raw_docs = loader.load()
            chunks = self.text_splitter.split_documents(raw_docs)

            doc = Document(
                title=file.filename or "Untitled",
                filename=file.filename or "untitled.pdf",
                file_path="stored_in_db_for_now", 
                file_size_bytes=len(content)
            )
            doc = await self.repo.create_document(doc)
            doc_chunks = []
            texts = [c.page_content for c in chunks]
            
            vectors = self.embeddings.embed_documents(texts)

            for i, chunk in enumerate(chunks):
                doc_chunks.append(
                    DocumentChunk(
                        document_id=doc.id,
                        chunk_index=i,
                        content=chunk.page_content,
                        embedding=vectors[i]
                    )
                )

            await self.repo.create_chunks(doc_chunks)
            
            return doc

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
