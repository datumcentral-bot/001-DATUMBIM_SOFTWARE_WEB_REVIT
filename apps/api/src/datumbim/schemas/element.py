from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ElementBase(BaseModel):
    type_id: str
    category: str
    name: str
    properties: Optional[str] = None
    transform_state: Optional[str] = None
    visibility: bool = True
    selection_state: str = "none"


class ElementCreate(ElementBase):
    project_id: str


class ElementUpdate(BaseModel):
    type_id: Optional[str] = None
    category: Optional[str] = None
    name: Optional[str] = None
    properties: Optional[str] = None
    transform_state: Optional[str] = None
    visibility: Optional[bool] = None
    selection_state: Optional[str] = None


class ElementResponse(ElementBase):
    id: str
    project_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
