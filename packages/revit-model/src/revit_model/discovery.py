from __future__ import annotations

from typing import Any

from revit_model.models import (
    RevitCapability,
    RevitCategory,
    RevitDocument,
    RevitElement,
    RevitFamily,
    RevitLevel,
    RevitModelInfo,
    RevitView,
)


class RevitDiscovery:
    def __init__(self) -> None:
        self._model_info: RevitModelInfo | None = None

    def discover(self) -> RevitModelInfo:
        if self._model_info is None:
            self._model_info = RevitModelInfo(
                connection_state="not_running",
                categories=[],
                levels=[],
                views=[],
                documents=[],
                families=[],
                elements=[],
                capabilities=[],
                warnings=["Revit discovery requires actual Revit API connection"],
            )
        return self._model_info

    def discover_categories(self) -> list[RevitCategory]:
        return []

    def discover_elements(self, category_id: str | None = None) -> list[RevitElement]:
        return []

    def discover_families(self) -> list[RevitFamily]:
        return []

    def discover_levels(self) -> list[RevitLevel]:
        return []

    def discover_views(self) -> list[RevitView]:
        return []

    def discover_documents(self) -> list[RevitDocument]:
        return []

    def discover_capabilities(self) -> list[RevitCapability]:
        return []
