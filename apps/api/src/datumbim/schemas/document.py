from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    file_format: Optional[str] = None
    version: Optional[str] = None
    revision: Optional[str] = None
    status: str = "active"


class DocumentCreate(DocumentBase):
    project_id: str


class DocumentUpdate(DocumentBase):
    name: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    file_format: Optional[str] = None
    version: Optional[str] = None
    revision: Optional[str] = None
    status: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: str
    project_id: str
    file_size: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
