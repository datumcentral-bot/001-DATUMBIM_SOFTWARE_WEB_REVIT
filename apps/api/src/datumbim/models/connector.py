from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ApplicationCapabilityModel(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    channel: str
    risk_level: str
    available: bool
    metadata: Optional[dict] = None


class ApplicationSessionModel(BaseModel):
    id: str
    application_id: str
    status: str
    capabilities: list[ApplicationCapabilityModel] = []
    active_job_id: Optional[str] = None
    metadata: Optional[dict] = None


class ApplicationConnectorModel(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    version: Optional[str] = None
    capabilities: list[ApplicationCapabilityModel] = []
    sessions: list[ApplicationSessionModel] = []
