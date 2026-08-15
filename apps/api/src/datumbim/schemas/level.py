from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class LevelBase(BaseModel):
    name: str
    elevation: float
    height: Optional[float] = None
    is_structural: bool = False
    is_ground: bool = False


class LevelCreate(LevelBase):
    project_id: str


class LevelUpdate(LevelBase):
    name: Optional[str] = None
    elevation: Optional[float] = None
    height: Optional[float] = None
    is_structural: Optional[bool] = None
    is_ground: Optional[bool] = None


class LevelResponse(LevelBase):
    id: str
    project_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
