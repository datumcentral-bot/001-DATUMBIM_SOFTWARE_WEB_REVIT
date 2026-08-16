from __future__ import annotations

import platform
from datetime import UTC, datetime
from typing import Any

from revit_connector.models import RevitConnectionState


class PyRevitBridge:
    PYREVIT_INSTALL_PATH = r"C:\Program Files\pyRevit"

    def __init__(self) -> None:
        self._available = False
        self._installed = False
        self._version: str | None = None
        self._extensions: list[dict[str, Any]] = []
        self._error: str | None = None
        self._detect()

    def _detect(self) -> None:
        if platform.system() != "Windows":
            self._error = "pyRevit bridge requires Windows"
            return
        import os
        if os.path.isdir(self.PYREVIT_INSTALL_PATH):
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

    def discover_extensions(self) -> list[dict[str, Any]]:
        if not self._available:
            return []
        return self._extensions

    def run_script(self, script_path: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "status": "not_implemented",
            "error": "pyRevit script execution not yet implemented",
        }
