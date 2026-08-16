from __future__ import annotations

from typing import Any

from revit_model.models import RevitCapability, RevitOperation


class RevitCapabilityRegistry:
    def __init__(self) -> None:
        self._capabilities: dict[str, RevitCapability] = {}
        self._operations: dict[str, RevitOperation] = {}

    def register_capability(self, capability: RevitCapability) -> None:
        self._capabilities[capability.capability_id] = capability

    def register_operation(self, operation: RevitOperation) -> None:
        self._operations[operation.operation_id] = operation

    def get_capability(self, capability_id: str) -> RevitCapability | None:
        return self._capabilities.get(capability_id)

    def list_capabilities(self) -> list[RevitCapability]:
        return list(self._capabilities.values())

    def list_operations(self) -> list[RevitOperation]:
        return list(self._operations.values())

    def is_available(self, capability_id: str) -> bool:
        capability = self._capabilities.get(capability_id)
        return bool(capability and capability.available)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capabilities": [c.model_dump() for c in self._capabilities.values()],
            "operations": [o.model_dump() for o in self._operations.values()],
        }
