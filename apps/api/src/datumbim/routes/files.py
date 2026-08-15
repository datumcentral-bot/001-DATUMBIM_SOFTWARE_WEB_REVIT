from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datumbim.db.session import get_db
from datumbim.models.project import Project
from datumbim.models.bim import Document
from datumbim.schemas.document import DocumentCreate
from datumbim.services.file_service import FileService
from datumbim.services.storage import StorageService, LocalStorageProvider
from pathlib import Path
import uuid

router = APIRouter(prefix="/files", tags=["files"])


def get_file_service() -> FileService:
    storage = StorageService(LocalStorageProvider(Path("storage")))
    return FileService(storage)


@router.get("/validate")
async def validate_file(filename: str = Query(...), service: FileService = Depends(get_file_service)):
    validation = service.validate_path(filename)
    detection = service.detect_format(filename)
    return {
        "filename": filename,
        "validation": validation,
        "detection": detection,
    }


@router.post("/import")
async def import_file(
    file: UploadFile = File(...),
    project_id: int | None = Query(None),
    service: FileService = Depends(get_file_service),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    content = await file.read()
    result = service.import_file(content, file.filename, project_id)

    document = None
    if project_id and result.success:
        project_result = await db.execute(select(Project).where(Project.id == project_id))
        project = project_result.scalar_one_or_none()
        if project:
            document = Document(
                id=str(uuid.uuid4()),
                project_id=str(project_id),
                name=file.filename,
                file_path=result.metadata.get("filename", ""),
                file_format=result.format.value,
                file_size=len(content),
                status="imported",
            )
            db.add(document)
            await db.commit()
            await db.refresh(document)

    return {
        "success": result.success,
        "format": result.format.value,
        "elements_imported": result.elements_imported,
        "errors": result.errors,
        "warnings": result.warnings,
        "metadata": result.metadata,
        "document_id": document.id if document else None,
    }
