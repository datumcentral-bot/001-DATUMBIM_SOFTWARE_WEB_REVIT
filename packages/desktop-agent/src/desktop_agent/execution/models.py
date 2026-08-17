from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class ExecutionStatus(str, Enum):
    QUEUED = "queued"
    WAITING_APPROVAL = "waiting_approval"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    UNAVAILABLE = "unavailable"
    AUTH_REQUIRED = "auth_required"
    VERIFICATION_FAILED = "verification_failed"


class ExecutionMode(str, Enum):
    LOCAL = "local"
    DESKTOP = "desktop"
    APPLICATION = "application"
    API = "api"
    WEBHOOK = "webhook"
    N8N = "n8n"
    AI = "ai"
    SIMULATION = "simulation"


class ToolDefinition(BaseModel):
    tool_id: str
    name: str
    description: str
    version: str | None = None
    category: str
    provider: str
    integration_id: str
    application_id: str | None = None
    capabilities: list[str] = []
    input_schema: dict[str, Any] = {}
    output_schema: dict[str, Any] = {}
    risk_level: str = "low"
    requires_approval: bool = False
    requires_session: bool = False
    requires_observation: bool = False
    requires_verification: bool = False
    timeout: int = 30
    retry_policy: dict[str, Any] = {}
    enabled: bool = True
    availability: str = "available"
    execution_mode: ExecutionMode = ExecutionMode.LOCAL


class ExecutionRequest(BaseModel):
    execution_id: str
    tool_id: str
    integration_id: str
    application_id: str | None = None
    session_id: str | None = None
    requested_by: str = "system"
    parameters: dict[str, Any] = {}
    risk_level: str = "low"
    approval_required: bool = False
    approval_state: str = "pending"
    dry_run: bool = False
    timeout: int = 30
    retry_policy: dict[str, Any] = {}
    created_at: datetime | None = None


class ExecutionResult(BaseModel):
    execution_id: str
    status: ExecutionStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration: float | None = None
    provider: str | None = None
    tool: str | None = None
    result: Any = None
    error: str | None = None
    verification_state: str | None = None
    observation_id: str | None = None
    audit_id: str | None = None
    metadata: dict[str, Any] = {}


class WorkflowDefinition(BaseModel):
    workflow_id: str
    name: str
    description: str
    version: str | None = None
    inputs: dict[str, Any] = {}
    steps: list[dict[str, Any]] = []
    conditions: dict[str, Any] = {}
    outputs: dict[str, Any] = {}
    risk_level: str = "low"
    approval_policy: str = "none"
    enabled: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class WorkflowExecution(BaseModel):
    execution_id: str
    workflow_id: str
    status: ExecutionStatus
    current_step: int = 0
    inputs: dict[str, Any] = {}
    outputs: dict[str, Any] = {}
    steps: list[dict[str, Any]] = []
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration: float | None = None
    error: str | None = None
    metadata: dict[str, Any] = {}
