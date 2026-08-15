from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    client: Optional[str] = None
    location: Optional[str] = None
    project_number: Optional[str] = None
    status: str = "active"
    units: str = "metric"
    version: str = "1.0"
    is_active: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    client: Optional[str] = None
    location: Optional[str] = None
    project_number: Optional[str] = None
    status: Optional[str] = None
    units: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_opened_at: Optional[datetime] = None
    last_saved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectOpenResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    status: str
    opened_at: Optional[datetime] = None
    message: str
