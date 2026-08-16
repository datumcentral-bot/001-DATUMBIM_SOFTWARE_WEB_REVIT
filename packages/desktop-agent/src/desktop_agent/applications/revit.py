from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.applications.base import ApplicationAdapter, ApplicationCapability, ConnectionState
from desktop_agent.control.models import ActionRequest, ActionResult
from desktop_agent.models import ApplicationInfo

try:
    from revit_model.discovery import RevitDiscovery
    from revit_model.models import RevitConnectionState, RevitModelInfo
    from revit_model.registry import RevitCapabilityRegistry

    REVIT_MODEL_AVAILABLE = True
except ImportError:
    REVIT_MODEL_AVAILABLE = False


class RevitAdapter(ApplicationAdapter):
    application_id = "revit"
    application_name = "Autodesk Revit"

    def __init__(self, application: ApplicationInfo | None = None) -> None:
        self.application = application
        self._connected = False
        self._api_available = False
        self._pyrevit_available = False
        self._dynamo_available = False
        self._discovery = RevitDiscovery() if REVIT_MODEL_AVAILABLE else None
        self._registry = RevitCapabilityRegistry() if REVIT_MODEL_AVAILABLE else None

    def identify(self) -> ActionResult:
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result="Revit adapter identified")

    def connect(self) -> ActionResult:
        if not self._is_running():
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_RUNNING.value)
        self._connected = True
        if REVIT_MODEL_AVAILABLE and self._registry:
            self._register_default_capabilities()
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result="connected to Revit")

    def disconnect(self) -> ActionResult:
        self._connected = False
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result="disconnected")

    def is_available(self) -> ActionResult:
        if self._is_running():
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=ConnectionState.AVAILABLE.value)
        return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=ConnectionState.NOT_RUNNING.value)

    def get_capabilities(self) -> ApplicationCapability:
        if not self._is_running():
            state = ConnectionState.NOT_RUNNING
        elif not self._api_available:
            state = ConnectionState.API_UNAVAILABLE
        else:
            state = ConnectionState.CONNECTED if self._connected else ConnectionState.AVAILABLE
        capabilities = [
            "ui_control", "document", "model", "view", "selection",
            "elements", "parameters", "families", "sheets", "export", "import",
        ]
        if REVIT_MODEL_AVAILABLE and self._registry:
            capabilities = [c.name for c in self._registry.list_capabilities() if c.available] or capabilities
        return ApplicationCapability(
            application_id=self.application_id,
            application_name=self.application_name,
            adapter_type="revit",
            connection_state=state,
            capabilities=capabilities,
            supported_actions=[
                "ui_control", "document_open", "document_save", "element_select",
                "view_activate", "parameter_read", "parameter_write",
            ],
            observation_support=True,
            automation_support=True,
            api_support=self._api_available,
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
            return ActionResult(action_id=request.action_id, status="failed", started_at=datetime.now(tz=UTC), error="Not connected to Revit")
        return ActionResult(action_id=request.action_id, status="failed", started_at=datetime.now(tz=UTC), error=ConnectionState.NOT_IMPLEMENTED.value)

    def verify(self, request: ActionRequest, result: ActionResult) -> ActionResult:
        return ActionResult(action_id=request.action_id, status="completed", started_at=datetime.now(tz=UTC), result="verification not implemented")

    def _is_running(self) -> bool:
        if self.application:
            return self.application.running
        return False

    def _register_default_capabilities(self) -> None:
        if not self._registry:
            return
        defaults = [
            ("ui_control", "UI Control", "element", True, True, "low", ["window_id", "action"]),
            ("document", "Document", "document", True, True, "low", ["document_path"]),
            ("model", "Model", "element", True, True, "medium", ["element_id"]),
            ("view", "View", "view", True, True, "low", ["view_id"]),
            ("selection", "Selection", "selection", True, True, "low", ["element_ids"]),
            ("elements", "Elements", "element", True, True, "medium", ["category_id"]),
            ("parameters", "Parameters", "parameter", True, False, "low", ["element_id", "parameter_name"]),
            ("families", "Families", "family", True, True, "medium", ["family_id"]),
            ("sheets", "Sheets", "document", True, True, "low", ["sheet_id"]),
            ("export", "Export", "document", True, True, "medium", ["document_path", "format"]),
            ("import", "Import", "document", True, True, "medium", ["file_path"]),
        ]
        for capability_id, name, group, available, requires_txn, risk, params in defaults:
            self._registry.register_capability(
                RevitCapability(
                    capability_id=capability_id,
                    name=name,
                    group=group,
                    available=available,
                    requires_transaction=requires_txn,
                    risk_level=risk,
                    parameters=params,
                )
            )
