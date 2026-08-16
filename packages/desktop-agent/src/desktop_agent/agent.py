from datetime import UTC, datetime

from desktop_agent.audit import AuditLogger
from desktop_agent.discovery import (
    ApplicationDiscovery,
    WindowDiscovery,
    get_machine_name,
)
from desktop_agent.health import HealthManager
from desktop_agent.heartbeat import HeartbeatManager
from desktop_agent.job_queue import JobQueue
from desktop_agent.models import (
    AgentHealth,
    AgentRegistration,
    ApplicationInfo,
    AuditLogEntry,
    CommandRequest,
    CommandResult,
    Heartbeat,
    SessionInfo,
)
from desktop_agent.pairing import PairingManager
from desktop_agent.permissions import PermissionEngine


class DesktopAgent:
    def __init__(self) -> None:
        self.agent_id: str | None = None
        self.registration: AgentRegistration | None = None
        self.discovery = ApplicationDiscovery()
        self.window_discovery = WindowDiscovery()
        self.pairing = PairingManager()
        self.heartbeat_manager: HeartbeatManager | None = None
        self.permissions = PermissionEngine()
        self.audit = AuditLogger()
        self.job_queue = JobQueue()
        self.health: HealthManager | None = None
        self._sessions: dict[str, SessionInfo] = {}

    def register(self) -> AgentRegistration:
        machine_name = get_machine_name()
        self.registration = self.pairing.register(machine_name=machine_name)
        self.agent_id = self.registration.agent_id
        self.heartbeat_manager = HeartbeatManager(agent_id=self.agent_id)
        self.health = HealthManager(agent_id=self.agent_id)
        return self.registration

    def pair(self, token: str) -> bool:
        registration = self.pairing.get_registration()
        return bool(registration and registration.token == token)

    def heartbeat(self) -> Heartbeat:
        if not self.heartbeat_manager:
            raise RuntimeError("Agent not registered")
        heartbeat = self.heartbeat_manager.create_heartbeat()
        if self.health:
            self.health.record_heartbeat()
        return heartbeat

    def discover_applications(self) -> list[ApplicationInfo]:
        return self.discovery.discover()

    def discover_windows(self) -> list[dict]:
        return [w.model_dump() for w in self.window_discovery.discover_windows()]

    def create_session(self, application_id: str) -> SessionInfo:
        session = SessionInfo(
            session_id=f"{application_id}-{datetime.now(tz=UTC).timestamp()}",
            application_id=application_id,
            started_at=datetime.now(tz=UTC),
        )
        self._sessions[session.session_id] = session
        return session

    def close_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def get_session(self, session_id: str) -> SessionInfo | None:
        return self._sessions.get(session_id)

    def get_sessions(self) -> list[SessionInfo]:
        return list(self._sessions.values())

    def execute_command(self, request: CommandRequest) -> CommandResult:
        if not self.health:
            raise RuntimeError("Agent not registered")
        allowed, reason = self.permissions.check(request)
        if not allowed:
            result = CommandResult(
                command_id=request.command_id,
                status="denied",
                error=reason,
                timestamp=datetime.now(tz=UTC),
            )
            self.audit.log(
                AuditLogEntry(
                    id=request.command_id,
                    agent_id=self.agent_id or "unknown",
                    action=request.action,
                    target="",
                    parameters=request.parameters,
                    result="denied",
                    timestamp=datetime.now(tz=UTC),
                    error=reason,
                )
            )
            return result
        job = self.job_queue.enqueue(request)
        job.start()
        result = CommandResult(
            command_id=request.command_id,
            status="pending",
            timestamp=datetime.now(tz=UTC),
        )
        job.finish(result)
        self.audit.log(
            AuditLogEntry(
                id=request.command_id,
                agent_id=self.agent_id or "unknown",
                action=request.action,
                target="",
                parameters=request.parameters,
                result="pending",
                timestamp=datetime.now(tz=UTC),
            )
        )
        return result

    def get_health(self) -> AgentHealth:
        if not self.health:
            raise RuntimeError("Agent not registered")
        return self.health.get_health()

    def get_audit_logs(self) -> list[AuditLogEntry]:
        if not self.agent_id:
            return []
        return self.audit.get_entries(agent_id=self.agent_id)
