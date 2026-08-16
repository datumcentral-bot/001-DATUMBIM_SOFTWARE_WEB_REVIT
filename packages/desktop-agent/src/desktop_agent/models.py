from datetime import datetime

from pydantic import BaseModel


class AgentRegistration(BaseModel):
    agent_id: str
    machine_name: str
    os: str
    os_version: str
    python_version: str
    hostname: str
    ip_addresses: list[str] = []
    paired_at: datetime | None = None
    token: str | None = None
    status: str = "unpaired"


class ApplicationInfo(BaseModel):
    id: str
    name: str
    display_name: str
    version: str | None = None
    executable: str | None = None
    install_path: str | None = None
    running: bool = False
    process_id: int | None = None
    window_title: str | None = None
    capabilities: list[str] = []


class WindowInfo(BaseModel):
    handle: int | None = None
    title: str
    process_name: str | None = None
    process_id: int | None = None
    class_name: str | None = None
    bounds: dict[str, int] | None = None
    visible: bool = False


class SessionInfo(BaseModel):
    session_id: str
    application_id: str
    status: str = "active"
    started_at: datetime
    process_id: int | None = None
    window: WindowInfo | None = None
    active_document: str | None = None
    active_view: str | None = None
    metadata: dict[str, str] = {}


class Heartbeat(BaseModel):
    agent_id: str
    timestamp: datetime
    status: str = "online"
    cpu_percent: float | None = None
    memory_percent: float | None = None
    active_sessions: int = 0
    pending_jobs: int = 0


class AgentCapabilities(BaseModel):
    screen_capture: bool = False
    input_control: bool = False
    process_discovery: bool = True
    window_discovery: bool = True
    file_system: bool = True
    command_execution: bool = False
    screenshot: bool = False
    clipboard: bool = False


class AgentHealth(BaseModel):
    agent_id: str
    status: str
    last_heartbeat: datetime | None = None
    uptime_seconds: int | None = None
    error: str | None = None
    capabilities: AgentCapabilities = AgentCapabilities()


class AuditLogEntry(BaseModel):
    id: str
    agent_id: str
    action: str
    target: str
    parameters: dict[str, str] = {}
    result: str
    timestamp: datetime
    duration_ms: int | None = None
    error: str | None = None
    evidence: str | None = None


class CommandRequest(BaseModel):
    command_id: str
    action: str
    parameters: dict[str, str] = {}
    risk_level: str = "low"
    approval_required: bool = False
    timeout_seconds: int = 30


class CommandResult(BaseModel):
    command_id: str
    status: str
    result: str | None = None
    error: str | None = None
    evidence: str | None = None
    duration_ms: int | None = None
    timestamp: datetime
