from datetime import UTC, datetime
from typing import Any, Optional
from pydantic import BaseModel


class ActionRequest(BaseModel):
    action_id: str
    session_id: str
    application_id: str
    action_type: str
    parameters: dict[str, Any] = {}
    requested_by: str = "system"
    risk_level: str = "low"
    approval_required: bool = False
    timestamp: datetime
    timeout: int = 30
    dry_run: bool = False


class ActionResult(BaseModel):
    action_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None
    result: Optional[str] = None
    error: Optional[str] = None
    verification_state: Optional[str] = None


class MouseAction(BaseModel):
    x: int
    y: int
    button: str = "left"
    duration: float = 0.1


class KeyboardAction(BaseModel):
    key: str
    text: Optional[str] = None
    modifiers: list[str] = []


class WindowAction(BaseModel):
    window_id: Optional[str] = None
    window_title: Optional[str] = None
    action: str
    parameters: dict[str, Any] = {}


class ApplicationAction(BaseModel):
    application_id: str
    action: str
    parameters: dict[str, Any] = {}


class ActionPlan(BaseModel):
    plan_id: str
    goal: str
    session_id: str
    actions: list[ActionRequest]
    risk_level: str = "low"
    approval_required: bool = False
