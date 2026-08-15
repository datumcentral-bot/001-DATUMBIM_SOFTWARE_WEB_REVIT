from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datumbim.db.session import get_db
from datumbim.models.project import Project, Model
from datumbim.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectOpenResponse
from datumbim.services.project_service import ProjectService
from datumbim.models.bim import Document
from pathlib import Path

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(service: ProjectService = Depends(get_project_service)):
    projects = await service.list_projects()
    return projects


@router.post("/", response_model=ProjectResponse)
async def create_project(payload: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    project = await service.create_project(payload)
    return project


@router.get("/recent", response_model=list[ProjectResponse])
async def recent_projects(limit: int = Query(20, ge=1, le=100), service: ProjectService = Depends(get_project_service)):
    projects = await service.get_recent_projects(limit=limit)
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, payload: ProjectUpdate, service: ProjectService = Depends(get_project_service)):
    project = await service.update_project(project_id, payload)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
async def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted"}


@router.post("/{project_id}/open", response_model=ProjectOpenResponse)
async def open_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = await service.open_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectOpenResponse(
        id=project.id,
        name=project.name,
        code=project.code,
        status=project.status,
        opened_at=project.last_opened_at,
        message=f"Project '{project.name}' opened",
    )


@router.post("/{project_id}/close")
async def close_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = await service.close_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": f"Project '{project.name}' closed", "id": project.id}


@router.post("/{project_id}/save")
async def save_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = await service.save_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": f"Project '{project.name}' saved", "id": project.id, "last_saved_at": project.last_saved_at}


@router.get("/{project_id}/models")
async def list_models(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.project_id == project_id))
    return result.scalars().all()


@router.get("/{project_id}/documents")
async def list_project_documents(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.project_id == project_id).order_by(Document.created_at.desc()))
    documents = result.scalars().all()
    return [
        {
            "id": doc.id,
            "name": doc.name,
            "file_path": doc.file_path,
            "file_format": doc.file_format,
            "file_size": doc.file_size,
            "version": doc.version,
            "revision": doc.revision,
            "status": doc.status,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at,
        }
        for doc in documents
    ]
