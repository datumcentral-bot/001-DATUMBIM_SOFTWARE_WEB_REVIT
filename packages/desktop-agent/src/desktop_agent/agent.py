from datetime import UTC, datetime

from desktop_agent.audit import AuditLogger
from desktop_agent.control.engine import ControlEngine
from desktop_agent.control.adapters.mock import MockControlAdapter
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
from desktop_agent.observation.engine import ObservationEngine
from desktop_agent.observation.models import CaptureMode, ObservationRequest, Region
from desktop_agent.observation.providers.mock import MockObservationProvider
from desktop_agent.observation.providers.windows import WindowsObservationProvider
from desktop_agent.pairing import PairingManager
from desktop_agent.permissions import PermissionEngine
from desktop_agent.session_manager import SessionManager


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
        self.session_manager = SessionManager(
            discovery=self.discovery,
            window_discovery=self.window_discovery,
        )
        self.control_engine = ControlEngine(session_manager=self.session_manager, adapter=MockControlAdapter())
        self.observation_engine = ObservationEngine(provider=WindowsObservationProvider())

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
        return self.session_manager.discover_applications()

    def discover_windows(self) -> list[dict]:
        return [w.model_dump() for w in self.session_manager.discover_windows()]

    def create_session(self, application_id: str) -> SessionInfo:
        return self.session_manager.start_session(application_id)

    def attach_session(self, application_id: str) -> SessionInfo | None:
        return self.session_manager.attach_session(application_id)

    def detach_session(self, session_id: str) -> bool:
        return self.session_manager.detach_session(session_id)

    def close_session(self, session_id: str) -> bool:
        return self.session_manager.close_session(session_id)

    def restart_session(self, session_id: str) -> SessionInfo | None:
        return self.session_manager.restart_session(session_id)

    def get_session(self, session_id: str) -> SessionInfo | None:
        return self.session_manager.get_session(session_id)

    def get_sessions(self) -> list[SessionInfo]:
        return self.session_manager.get_sessions()

    def list_displays(self) -> list[dict]:
        return [display.model_dump() for display in self.observation_engine.list_displays()]

    def list_windows(self) -> list[dict]:
        return [window.model_dump() for window in self.observation_engine.list_windows()]

    def capture_screen(self, session_id: str, application_id: str, requested_by: str = "system") -> dict:
        return self._capture(session_id, application_id, requested_by, CaptureMode.FULL_SCREEN)

    def capture_display(self, session_id: str, application_id: str, target_id: str, requested_by: str = "system") -> dict:
        return self._capture(session_id, application_id, requested_by, CaptureMode.DISPLAY, target_id=target_id)

    def capture_window(self, session_id: str, application_id: str, target_id: str, requested_by: str = "system") -> dict:
        return self._capture(session_id, application_id, requested_by, CaptureMode.WINDOW, target_id=target_id)

    def capture_region(self, session_id: str, application_id: str, region: Any, requested_by: str = "system") -> dict:
        return self._capture(session_id, application_id, requested_by, CaptureMode.REGION, region=region)

    def capture_application(self, session_id: str, application_id: str, requested_by: str = "system") -> dict:
        return self._capture(session_id, application_id, requested_by, CaptureMode.APPLICATION)

    def _capture(self, session_id: str, application_id: str, requested_by: str, target_type: CaptureMode, target_id: str | None = None, region: Any = None) -> dict:
        if not self.health:
            raise RuntimeError("Agent not registered")
        request = ObservationRequest(
            observation_id=str(__import__("uuid").uuid4()),
            session_id=session_id,
            application_id=application_id,
            target_type=target_type,
            target_id=target_id,
            region=region,
            requested_by=requested_by,
            timestamp=datetime.now(tz=UTC),
        )
        result = self.observation_engine.capture(request)
        self.audit.log(
            AuditLogEntry(
                id=request.observation_id,
                agent_id=self.agent_id or "unknown",
                action="observation",
                target=target_id or target_type.value,
                parameters={},
                result=result.status.value if hasattr(result.status, "value") else str(result.status),
                timestamp=datetime.now(tz=UTC),
                error=result.error,
            )
        )
        return result.model_dump()


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

    def execute_action(self, request: CommandRequest) -> CommandResult:
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
        action_request = ActionRequest(
            action_id=request.command_id,
            session_id="",
            application_id="",
            action_type=request.action,
            parameters=request.parameters,
            requested_by=self.agent_id or "unknown",
            risk_level=request.risk_level,
            approval_required=request.approval_required,
            timestamp=datetime.now(tz=UTC),
            timeout=request.timeout_seconds,
            dry_run=False,
        )
        action_result = self.control_engine.execute(action_request)
        self.audit.log(
            AuditLogEntry(
                id=request.command_id,
                agent_id=self.agent_id or "unknown",
                action=request.action,
                target="",
                parameters=request.parameters,
                result=action_result.status,
                timestamp=datetime.now(tz=UTC),
                error=action_result.error,
            )
        )
        return CommandResult(
            command_id=request.command_id,
            status=action_result.status,
            result=action_result.result,
            error=action_result.error,
            timestamp=datetime.now(tz=UTC),
        )

    def execute_action_plan(self, plan: ActionPlan) -> list[CommandResult]:
        if not self.health:
            raise RuntimeError("Agent not registered")
        results: list[CommandResult] = []
        action_results = self.control_engine.execute_plan(plan)
        for action_result in action_results:
            results.append(
                CommandResult(
                    command_id=action_result.action_id,
                    status=action_result.status,
                    result=action_result.result,
                    error=action_result.error,
                    timestamp=datetime.now(tz=UTC),
                )
            )
            self.audit.log(
                AuditLogEntry(
                    id=action_result.action_id,
                    agent_id=self.agent_id or "unknown",
                    action="plan_action",
                    target="",
                    parameters={},
                    result=action_result.status,
                    timestamp=datetime.now(tz=UTC),
                    error=action_result.error,
                )
            )
        return results
