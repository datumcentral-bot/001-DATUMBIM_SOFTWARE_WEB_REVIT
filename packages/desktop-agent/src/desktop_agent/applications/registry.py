from __future__ import annotations

from typing import TYPE_CHECKING, Any

from desktop_agent.applications.base import ApplicationAdapter, ApplicationCapability, ConnectionState
from desktop_agent.models import ApplicationInfo

if TYPE_CHECKING:
    from desktop_agent.control.models import ActionRequest, ActionResult


class ApplicationAdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, type[ApplicationAdapter]] = {}
        self._fallback: type[ApplicationAdapter] | None = None

    def register(self, application_id: str, adapter_cls: type[ApplicationAdapter]) -> None:
        self._adapters[application_id] = adapter_cls

    def unregister(self, application_id: str) -> None:
        self._adapters.pop(application_id, None)

    def get(self, application_id: str) -> type[ApplicationAdapter] | None:
        return self._adapters.get(application_id)

    def list(self) -> list[str]:
        return list(self._adapters.keys())

    def register_fallback(self, adapter_cls: type[ApplicationAdapter]) -> None:
        self._fallback = adapter_cls

    def detect(self, application: ApplicationInfo) -> ApplicationAdapter:
        adapter_cls = self._adapters.get(application.id.lower())
        if adapter_cls:
            return adapter_cls()
        if self._fallback:
            return self._fallback()
        raise ValueError(f"No adapter found for application: {application.id}")

    def resolve(self, application_id: str) -> ApplicationAdapter:
        adapter_cls = self._adapters.get(application_id.lower())
        if adapter_cls:
            return adapter_cls()
        if self._fallback:
            return self._fallback()
        raise ValueError(f"No adapter found for application: {application_id}")
