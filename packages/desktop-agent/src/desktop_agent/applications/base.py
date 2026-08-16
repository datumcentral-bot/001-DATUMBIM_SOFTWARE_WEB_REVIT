from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from desktop_agent.control.models import ActionRequest, ActionResult
from desktop_agent.models import ApplicationInfo, WindowInfo


class ConnectionState(str, Enum):
    AVAILABLE = "available"
    CONNECTED = "connected"
    NOT_INSTALLED = "not_installed"
    NOT_RUNNING = "not_running"
    API_UNAVAILABLE = "api_unavailable"
    PYREVIT_UNAVAILABLE = "pyrevit_unavailable"
    DYNAMO_UNAVAILABLE = "dynamo_unavailable"
    NOT_IMPLEMENTED = "not_implemented"
    ERROR = "error"


class ApplicationCapability:
    def __init__(
        self,
        application_id: str,
        application_name: str,
        adapter_type: str,
        connection_state: ConnectionState = ConnectionState.NOT_RUNNING,
        capabilities: list[str] | None = None,
        supported_actions: list[str] | None = None,
        observation_support: bool = False,
        automation_support: bool = False,
        api_support: bool = False,
        ui_control_support: bool = False,
    ) -> None:
        self.application_id = application_id
        self.application_name = application_name
        self.adapter_type = adapter_type
        self.connection_state = connection_state
        self.capabilities = capabilities or []
        self.supported_actions = supported_actions or []
        self.observation_support = observation_support
        self.automation_support = automation_support
        self.api_support = api_support
        self.ui_control_support = ui_control_support

    def to_dict(self) -> dict[str, Any]:
        return {
            "application_id": self.application_id,
            "application_name": self.application_name,
            "adapter_type": self.adapter_type,
            "connection_state": self.connection_state.value,
            "capabilities": self.capabilities,
            "supported_actions": self.supported_actions,
            "observation_support": self.observation_support,
            "automation_support": self.automation_support,
            "api_support": self.api_support,
            "ui_control_support": self.ui_control_support,
        }


class ApplicationAdapter(ABC):
    application_id: str
    application_name: str

    @abstractmethod
    def identify(self) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def get_capabilities(self) -> ApplicationCapability:
        raise NotImplementedError

    @abstractmethod
    def get_active_document(self) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def get_active_window(self) -> ActionResult | None:
        raise NotImplementedError

    @abstractmethod
    def observe(self) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def execute(self, request: ActionRequest) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def verify(self, request: ActionRequest, result: ActionResult) -> ActionResult:
        raise NotImplementedError
