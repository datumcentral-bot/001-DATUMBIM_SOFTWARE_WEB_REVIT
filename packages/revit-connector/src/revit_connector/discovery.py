from __future__ import annotations

import platform
from datetime import UTC, datetime
from typing import Any

import psutil

from revit_connector.models import RevitConnectionInfo, RevitConnectionState, RevitDocument, RevitElement, RevitFamily, RevitLevel, RevitView


class RevitDiscovery:
    REVIT_EXECUTABLE = "Revit.exe"
    REVIT_INSTALL_PATH = r"C:\Program Files\Autodesk\Revit 2024"

    def __init__(self) -> None:
        self._connection_info = RevitConnectionInfo(state=RevitConnectionState.NOT_RUNNING)

    def detect(self) -> RevitConnectionInfo:
        if platform.system() != "Windows":
            self._connection_info.state = RevitConnectionState.NOT_INSTALLED
            self._connection_info.errors.append("Revit connector requires Windows")
            return self._connection_info
        try:
            for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
                try:
                    if proc.info["name"] == self.REVIT_EXECUTABLE:
                        self._connection_info.state = RevitConnectionState.RUNNING
                        self._connection_info.process_id = proc.info["pid"]
                        self._connection_info.executable_path = proc.info["exe"]
                        self._connection_info.revit_version = self._get_version_from_path(proc.info["exe"])
                        return self._connection_info
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except ImportError:
            self._connection_info.errors.append("psutil not available")
        self._connection_info.state = RevitConnectionState.NOT_RUNNING
        return self._connection_info

    def discover_window(self) -> dict[str, Any] | None:
        if self._connection_info.state != RevitConnectionState.RUNNING or not self._connection_info.process_id:
            return None
        try:
            import win32gui
            import win32process

            def callback(hwnd, extra):
                if win32gui.IsWindowVisible(hwnd):
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    if pid == self._connection_info.process_id:
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            self._connection_info.window_handle = hwnd
                            self._connection_info.window_title = title
                            self._connection_info.state = RevitConnectionState.CONNECTED
                            return {"hwnd": hwnd, "title": title, "pid": self._connection_info.process_id}
                return None
            return win32gui.EnumWindows(callback, None)
        except ImportError:
            self._connection_info.window_title = "Revit"
            return None

    def discover_document(self) -> RevitDocument | None:
        if self._connection_info.state not in (RevitConnectionState.CONNECTED, RevitConnectionState.READY, RevitConnectionState.BUSY):
            return None
        window_title = self._connection_info.window_title
        if not window_title:
            return None
        doc = RevitDocument(
            document_id=0,
            name=window_title,
            active=True,
            modified=False,
        )
        self._connection_info.active_document = doc
        self._connection_info.state = RevitConnectionState.DOCUMENT_OPEN
        return doc

    def discover_views(self) -> list[RevitView]:
        return []

    def discover_categories(self) -> list[dict[str, Any]]:
        return []

    def discover_elements(self, category_id: int | None = None) -> list[RevitElement]:
        return []

    def discover_families(self) -> list[RevitFamily]:
        return []

    def discover_levels(self) -> list[RevitLevel]:
        return []

    def get_capabilities(self) -> list[str]:
        return [
            "ui_control",
            "document",
            "model",
            "view",
            "selection",
            "elements",
            "parameters",
            "families",
            "sheets",
            "export",
            "import",
        ]

    def _get_version_from_path(self, exe_path: str | None) -> str | None:
        if not exe_path:
            return None
        try:
            parts = exe_path.split("\\")
            for part in parts:
                if part.startswith("Revit "):
                    return part.replace("Revit ", "")
        except Exception:
            pass
        return None
