from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datumbim.db.session import get_db
from datumbim.models.project import Project
from datumbim.models.bim import Document
from datumbim.schemas.document import DocumentCreate
from format_engine.detector import detect_format
from format_engine.registry import registry
from format_engine.handlers.readers import (
    GenericReader,
    IFCMinimalReader,
    StubRevitReader,
    StubAutoCADReader,
)
from format_engine.handlers.parsers import GenericParser, IFCMinimalParser
from format_engine.models import ImportResult
from pathlib import Path
import uuid
import os

router = APIRouter(prefix="/format", tags=["format"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/formats")
async def list_formats():
    handlers = registry.list_supported()
    return {
        "formats": [
            {
                "format": h.format,
                "category": h.category,
                "extensions": h.extensions,
                "mime_types": h.mime_types,
            }
            for h in handlers
        ]
    }


@router.get("/detect")
async def detect_file_format(filename: str = Query(...), content_type: str | None = Query(None)):
    path = Path(filename)
    result = detect_format(path, mime_type=content_type)
    return {
        "format": result.format.value,
        "category": result.category.value,
        "confidence": result.confidence,
        "mime_type": result.mime_type,
        "metadata": result.metadata,
    }


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), project_id: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_id = str(uuid.uuid4())
    safe_name = f"{file_id}_{file.filename}"
    destination = UPLOAD_DIR / safe_name

    content = await file.read()
    with open(destination, "wb") as f:
        f.write(content)

    detection = detect_format(Path(file.filename), mime_type=file.content_type)

    document = None
    if project_id:
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if project:
            document = Document(
                id=str(uuid.uuid4()),
                project_id=project_id,
                name=file.filename,
                file_path=str(destination),
                file_format=detection.format.value,
                file_size=len(content),
                status="uploaded",
            )
            db.add(document)
            await db.commit()
            await db.refresh(document)

    reader = None
    if detection.format.value == "ifc":
        reader = IFCMinimalReader()
    elif detection.format.value == "rvt":
        reader = StubRevitReader()
    elif detection.format.value == "dwg":
        reader = StubAutoCADReader()
    else:
        reader = GenericReader()

    try:
        raw = reader.read(destination)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Failed to read file: {exc}") from exc

    return {
        "file_id": file_id,
        "filename": file.filename,
        "format": detection.format.value,
        "category": detection.category.value,
        "confidence": detection.confidence,
        "size": len(content),
        "document_id": document.id if document else None,
        "preview": raw.get("header") or raw.get("preview") or raw.get("note"),
    }


@router.post("/import/{format_name}")
async def import_file(format_name: str, file_id: str = Query(...), project_id: str | None = Query(None)):
    path = UPLOAD_DIR / file_id
    if not path.exists():
        raise HTTPException(status_code=404, detail="Uploaded file not found")

    reader = None
    if format_name == "ifc":
        reader = IFCMinimalReader()
    elif format_name == "rvt":
        reader = StubRevitReader()
    elif format_name == "dwg":
        reader = StubAutoCADReader()
    else:
        reader = GenericReader()

    try:
        raw = reader.read(path)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Read failed: {exc}") from exc

    parser = None
    if format_name == "ifc":
        parser = IFCMinimalParser()
    else:
        parser = GenericParser()

    try:
        parsed = parser.parse(raw.get("raw_data", b""))
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Parse failed: {exc}") from exc

    result = ImportResult(
        success=True,
        format=raw.get("format", format_name),
        elements_imported=0,
        metadata={
            "filename": raw.get("filename"),
            "size": raw.get("size"),
            "preview": parsed.get("preview") or parsed.get("header_lines"),
        },
    )
    return result
