from __future__ import annotations

import platform
from typing import Any

from revit_connector.models import RevitConnectionState


class DynamoBridge:
    DYNAMO_INSTALL_PATH = r"C:\Program Files\Autodesk\Revit 2024\AddIns\DynamoForRevit"

    def __init__(self) -> None:
        self._available = False
        self._installed = False
        self._version: str | None = None
        self._workspaces: list[dict[str, Any]] = []
        self._error: str | None = None
        self._detect()

    def _detect(self) -> None:
        if platform.system() != "Windows":
            self._error = "Dynamo bridge requires Windows"
            return
        import os
        if os.path.isdir(self.DYNAMO_INSTALL_PATH):
            self._installed = True
            self._available = True
        else:
            self._installed = False
            self._available = False

    @property
    def available(self) -> bool:
        return self._available

    @property
    def installed(self) -> bool:
        return self._installed

    @property
    def version(self) -> str | None:
        return self._version

    def discover_workspaces(self) -> list[dict[str, Any]]:
        if not self._available:
            return []
        return self._workspaces

    def run(self, workspace_path: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "status": "not_implemented",
            "error": "Dynamo execution not yet implemented",
        }
