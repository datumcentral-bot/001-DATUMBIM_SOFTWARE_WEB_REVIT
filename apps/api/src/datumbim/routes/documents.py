from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datumbim.db.session import get_db
from datumbim.models.bim import Document, Level, Wall, Door, Window, Roof, Floor, Column, Beam, Grid
from datumbim.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from datumbim.schemas.level import LevelCreate, LevelUpdate, LevelResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(project_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.project_id == project_id).order_by(Document.created_at.desc()))
    return result.scalars().all()


@router.post("/", response_model=DocumentResponse)
async def create_document(payload: DocumentCreate, db: AsyncSession = Depends(get_db)):
    document = Document(**payload.model_dump())
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(document_id: str, payload: DocumentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(document, key, value)
    await db.commit()
    await db.refresh(document)
    return document


@router.delete("/{document_id}")
async def delete_document(document_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(document)
    await db.commit()
    return {"detail": "Document deleted"}
