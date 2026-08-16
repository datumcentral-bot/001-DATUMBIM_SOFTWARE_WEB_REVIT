from __future__ import annotations

import platform
from typing import Any

from revit_connector.models import RevitConnectionState, RevitElement, RevitParameter, RevitView


class RevitUIBridge:
    def __init__(self, window_handle: int | None = None) -> None:
        self._window_handle = window_handle
        self._available = platform.system() == "Windows"

    @property
    def available(self) -> bool:
        return self._available

    def set_window_handle(self, handle: int | None) -> None:
        self._window_handle = handle

    def focus_window(self) -> bool:
        if not self._available or not self._window_handle:
            return False
        try:
            import win32gui
            import win32con
            win32gui.ShowWindow(self._window_handle, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self._window_handle)
            return True
        except ImportError:
            return False

    def get_window_title(self) -> str | None:
        if not self._available or not self._window_handle:
            return None
        try:
            import win32gui
            return win32gui.GetWindowText(self._window_handle)
        except ImportError:
            return None

    def get_window_rect(self) -> dict[str, int] | None:
        if not self._available or not self._window_handle:
            return None
        try:
            import win32gui
            left, top, right, bottom = win32gui.GetWindowRect(self._window_handle)
            return {"left": left, "top": top, "right": right, "bottom": bottom, "width": right - left, "height": bottom - top}
        except ImportError:
            return None

    def capture_screenshot(self) -> bytes | None:
        return None

    def get_ui_elements(self) -> list[dict[str, Any]]:
        return []

    def click(self, x: int, y: int) -> bool:
        return False

    def send_keys(self, keys: str) -> bool:
        return False
