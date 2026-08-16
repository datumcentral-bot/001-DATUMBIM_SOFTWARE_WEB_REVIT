from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class IntegrationType(str, Enum):
    APPLICATION = "application"
    AI_PROVIDER = "ai_provider"
    API = "api"
    WEBHOOK = "webhook"
    WORKFLOW = "workflow"
    DATABASE = "database"
    STORAGE = "storage"
    BROWSER = "browser"
    OFFICE = "office"
    CAD = "cad"
    BIM = "bim"
    MEP = "mep"
    STRUCTURAL = "structural"
    AUTOMATION = "automation"
    GENERIC = "generic"


class IntegrationStatus(str, Enum):
    NOT_INSTALLED = "not_installed"
    NOT_CONFIGURED = "not_configured"
    AUTH_REQUIRED = "auth_required"
    OFFLINE = "offline"
    UNAVAILABLE = "unavailable"
    NOT_SUPPORTED = "not_supported"
    MOCK = "mock"
    CONNECTED = "connected"
    ERROR = "error"
    READY = "ready"
    BUSY = "busy"
    DISCONNECTED = "disconnected"


class IntegrationCapability(BaseModel):
    capability_id: str
    name: str
    description: str
    category: str
    target_type: str
    parameters: list[str] = []
    required_capabilities: list[str] = []
    requires_document: bool = False
    requires_transaction: bool = False
    requires_selection: bool = False
    risk_level: str = "low"
    approval_required: bool = False
    verification_strategy: str | None = None
    available: bool = True


class IntegrationCredential(BaseModel):
    credential_id: str
    integration_id: str
    type: str
    configured: bool = False
    valid: bool = False
    expires_at: datetime | None = None
    metadata: dict[str, str] = {}
    error: str | None = None


class IntegrationSession(BaseModel):
    session_id: str
    integration_id: str
    status: IntegrationStatus
    started_at: datetime
    ended_at: datetime | None = None
    metadata: dict[str, str] = {}
    error: str | None = None


class IntegrationRequest(BaseModel):
    request_id: str
    integration_id: str
    session_id: str | None = None
    capability_id: str
    parameters: dict[str, Any] = {}
    risk_level: str = "low"
    approval_required: bool = False
    dry_run: bool = False
    timeout_seconds: int = 30
    retry_policy: dict[str, Any] = {}
    timestamp: datetime | None = None


class IntegrationResult(BaseModel):
    request_id: str
    status: str
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = {}
    duration_ms: float | None = None
    timestamp: datetime | None = None
    verification: dict[str, Any] = {}
    rollback_available: bool = False
    transaction_id: str | None = None


class IntegrationHealth(BaseModel):
    integration_id: str
    status: IntegrationStatus
    latency_ms: float | None = None
    error: str | None = None
    last_check: datetime | None = None
    capabilities: list[str] = []
    metadata: dict[str, str] = {}


class IntegrationEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    source: str
    correlation_id: str | None = None
    session_id: str | None = None
    project_id: str | None = None
    application_id: str | None = None
    payload: dict[str, Any] = {}
    status: str = "info"
    error: str | None = None
    metadata: dict[str, Any] = {}


class IntegrationWorkflow(BaseModel):
    workflow_id: str
    name: str
    description: str
    integration_id: str
    trigger: str
    inputs: dict[str, Any] = {}
    steps: list[dict[str, Any]] = []
    permissions: list[str] = []
    risk_level: str = "low"
    execution_state: str = "idle"
    outputs: dict[str, Any] = {}
    artifacts: list[str] = []
    verification: dict[str, Any] = {}
    retry_policy: dict[str, Any] = {}
    rollback_strategy: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class IntegrationWebhook(BaseModel):
    webhook_id: str
    integration_id: str
    url: str
    events: list[str] = []
    active: bool = True
    headers: dict[str, str] = {}
    secret: str | None = None
    timeout_seconds: int = 30
    retry_count: int = 3
    last_delivery: datetime | None = None
    last_status: str | None = None
    error: str | None = None
    metadata: dict[str, str] = {}


class Integration(BaseModel):
    integration_id: str
    name: str
    description: str
    integration_type: IntegrationType
    status: IntegrationStatus
    version: str | None = None
    installed_path: str | None = None
    executable: str | None = None
    capabilities: list[IntegrationCapability] = []
    credentials: list[IntegrationCredential] = []
    sessions: list[IntegrationSession] = []
    health: IntegrationHealth | None = None
    workflows: list[IntegrationWorkflow] = []
    webhooks: list[IntegrationWebhook] = []
    metadata: dict[str, str] = {}
    created_at: datetime | None = None
    updated_at: datetime | None = None
    error: str | None = None
