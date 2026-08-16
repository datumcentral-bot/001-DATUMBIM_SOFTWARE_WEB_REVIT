from __future__ import annotations

import platform
from datetime import UTC, datetime
from typing import Any

from desktop_agent.observation.ui_models import UIElement, UIElementType, UITree


class UIDetectionProvider:
    def __init__(self) -> None:
        self._available = platform.system() == "Windows"

    @property
    def available(self) -> bool:
        return self._available

    def detect_elements(self, image_reference: str, application_id: str, session_id: str) -> UITree:
        root_id = f"ui-root-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}"
        root = UIElement(
            element_id=root_id,
            type=UIElementType.WINDOW,
            label="Application Window",
            visible=True,
            enabled=True,
            clickable=False,
        )
        elements = {root_id: root}
        if not self._available:
            return UITree(root_id=root_id, elements=elements, application_id=application_id, session_id=session_id, timestamp=datetime.now(tz=UTC), provider="stub")
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if hwnd:
                title_length = user32.GetWindowTextLengthW(hwnd)
                if title_length > 0:
                    buffer = ctypes.create_unicode_buffer(title_length + 1)
                    user32.GetWindowTextW(hwnd, buffer, title_length + 1)
                    root.label = buffer.value
                    root.metadata["window_handle"] = str(hwnd)
        except Exception:
            pass
        return UITree(root_id=root_id, elements=elements, application_id=application_id, session_id=session_id, timestamp=datetime.now(tz=UTC), provider="windows_uiautomation")
