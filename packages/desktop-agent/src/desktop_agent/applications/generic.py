from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.applications.base import ApplicationAdapter, ApplicationCapability, ConnectionState
from desktop_agent.control.adapters.windows import WindowsControlAdapter
from desktop_agent.control.models import ActionRequest, ActionResult
from desktop_agent.models import ApplicationInfo, WindowInfo


class GenericWindowsApplicationAdapter(ApplicationAdapter):
    application_id = "generic_windows"
    application_name = "Generic Windows Application"

    def __init__(self, application: ApplicationInfo | None = None) -> None:
        self.application = application
        self._control = WindowsControlAdapter()
        self._connected = False

    def identify(self) -> ActionResult:
        if not self.application:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error="No application bound")
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"identified {self.application.id}")

    def connect(self) -> ActionResult:
        if not self.application or not self.application.running:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error="Application not running")
        self._connected = True
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"connected to {self.application.id}")

    def disconnect(self) -> ActionResult:
        self._connected = False
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result="disconnected")

    def is_available(self) -> ActionResult:
        if not self.application:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error="No application bound")
        state = ConnectionState.NOT_RUNNING if not self.application.running else ConnectionState.AVAILABLE
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=state.value)

    def get_capabilities(self) -> ApplicationCapability:
        state = ConnectionState.CONNECTED if self._connected else ConnectionState.NOT_RUNNING
        if self.application and not self.application.running:
            state = ConnectionState.NOT_RUNNING
        return ApplicationCapability(
            application_id=self.application_id,
            application_name=self.application_name,
            adapter_type="generic",
            connection_state=state,
            capabilities=["ui_control", "window_control", "process_control"],
            supported_actions=["mouse_move", "mouse_click", "keyboard_type", "window_activate"],
            observation_support=False,
            automation_support=True,
            api_support=False,
            ui_control_support=True,
        )

    def get_active_document(self) -> ActionResult:
        return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_IMPLEMENTED.value)

    def get_active_window(self) -> ActionResult | None:
        if not self.application:
            return None
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=str(self.application.window_title))

    def observe(self) -> ActionResult:
        return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_IMPLEMENTED.value)

    def execute(self, request: ActionRequest) -> ActionResult:
        generic_ui_actions = {
            "mouse_move", "mouse_click", "mouse_double_click", "mouse_right_click",
            "mouse_drag", "mouse_scroll", "keyboard_key", "keyboard_type",
            "keyboard_hotkey", "window_activate", "window_minimize", "window_maximize",
            "window_restore", "window_resize", "window_move", "window_close",
            "application_launch", "application_close", "application_focus", "window_state",
        }
        if request.action_type not in generic_ui_actions:
            return ActionResult(action_id=request.action_id, status="failed", started_at=datetime.now(tz=UTC), error=f"Unsupported action for generic adapter: {request.action_type}")
        return self._control._dispatch(request)

    def verify(self, request: ActionRequest, result: ActionResult) -> ActionResult:
        return ActionResult(action_id=request.action_id, status="completed", started_at=datetime.now(tz=UTC), result="verification not implemented")
