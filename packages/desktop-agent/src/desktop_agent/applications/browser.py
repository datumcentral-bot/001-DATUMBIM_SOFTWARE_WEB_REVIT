from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.applications.base import ApplicationAdapter, ApplicationCapability, ConnectionState
from desktop_agent.control.models import ActionRequest, ActionResult
from desktop_agent.models import ApplicationInfo


class BrowserAdapter(ApplicationAdapter):
    application_id = "browser"
    application_name = "Web Browser"

    def __init__(self, application: ApplicationInfo | None = None) -> None:
        self.application = application
        self._connected = False

    def identify(self) -> ActionResult:
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result="Browser adapter identified")

    def connect(self) -> ActionResult:
        if not self._is_running():
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_RUNNING.value)
        self._connected = True
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result="connected to browser")

    def disconnect(self) -> ActionResult:
        self._connected = False
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result="disconnected")

    def is_available(self) -> ActionResult:
        if self._is_running():
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=ConnectionState.AVAILABLE.value)
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=ConnectionState.NOT_RUNNING.value)

    def get_capabilities(self) -> ApplicationCapability:
        state = ConnectionState.CONNECTED if self._connected else ConnectionState.NOT_RUNNING
        if self.application and not self.application.running:
            state = ConnectionState.NOT_RUNNING
        return ApplicationCapability(
            application_id=self.application_id,
            application_name=self.application_name,
            adapter_type="browser",
            connection_state=state,
            capabilities=["ui_control", "navigation", "tabs", "dom"],
            supported_actions=["navigate", "click", "type", "screenshot"],
            observation_support=False,
            automation_support=True,
            api_support=False,
            ui_control_support=True,
        )

    def get_active_document(self) -> ActionResult:
        if not self._connected:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error="Not connected")
        return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_IMPLEMENTED.value)

    def get_active_window(self) -> ActionResult | None:
        if not self.application:
            return None
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=str(self.application.window_title))

    def observe(self) -> ActionResult:
        if not self._connected:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error="Not connected")
        return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_IMPLEMENTED.value)

    def execute(self, request: ActionRequest) -> ActionResult:
        if not self._connected:
            return ActionResult(action_id=request.action_id, status="failed", started_at=datetime.now(tz=UTC), error="Not connected to browser")
        return ActionResult(action_id=request.action_id, status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_IMPLEMENTED.value)

    def verify(self, request: ActionRequest, result: ActionResult) -> ActionResult:
        return ActionResult(action_id=request.action_id, status="completed", started_at=datetime.now(tz=UTC), result="verification not implemented")

    def _is_running(self) -> bool:
        if self.application:
            return self.application.running
        return False
