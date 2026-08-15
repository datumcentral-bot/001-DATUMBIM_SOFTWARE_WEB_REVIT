from datetime import datetime, timezone
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datumbim.models.project import Project
from datumbim.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_projects(self) -> list[Project]:
        result = await self.db.execute(select(Project).order_by(Project.updated_at.desc()))
        return list(result.scalars().all())

    async def get_project(self, project_id: int) -> Project | None:
        result = await self.db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()

    async def create_project(self, payload: ProjectCreate) -> Project:
        project = Project(
            name=payload.name,
            code=payload.code,
            description=payload.description,
            client=payload.client,
            location=payload.location,
            project_number=payload.project_number,
            status=payload.status,
            units=payload.units,
            version=payload.version,
            is_active=payload.is_active,
        )
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def update_project(self, project_id: int, payload: ProjectUpdate) -> Project | None:
        project = await self.get_project(project_id)
        if not project:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project_id: int) -> bool:
        project = await self.get_project(project_id)
        if not project:
            return False
        await self.db.delete(project)
        await self.db.commit()
        return True

    async def open_project(self, project_id: int) -> Project | None:
        project = await self.get_project(project_id)
        if not project:
            return None
        project.last_opened_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def close_project(self, project_id: int) -> Project | None:
        project = await self.get_project(project_id)
        if not project:
            return None
        project.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def save_project(self, project_id: int) -> Project | None:
        project = await self.get_project(project_id)
        if not project:
            return None
        project.last_saved_at = datetime.now(timezone.utc)
        project.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get_recent_projects(self, limit: int = 20) -> list[Project]:
        result = await self.db.execute(
            select(Project)
            .where(Project.is_active == True)
            .order_by(Project.last_opened_at.desc().nullslast(), Project.updated_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
