from __future__ import annotations

import platform
from datetime import UTC, datetime

from desktop_agent.observation_models import ScreenshotCapture


class ScreenCapture:
    def __init__(self) -> None:
        self.system = platform.system()

    def capture_window(self, session_id: str, application_id: str, width: int = 0, height: int = 0) -> ScreenshotCapture:
        return ScreenshotCapture(
            capture_id="",
            session_id=session_id,
            application_id=application_id,
            timestamp=datetime.now(tz=UTC),
            width=width,
            height=height,
            format="png",
            metadata={"source": "stub", "system": self.system},
        )

    def capture_screen(self, session_id: str, application_id: str, monitor_index: int = 0) -> ScreenshotCapture:
        return ScreenshotCapture(
            capture_id="",
            session_id=session_id,
            application_id=application_id,
            timestamp=datetime.now(tz=UTC),
            width=0,
            height=0,
            format="png",
            metadata={"source": "stub", "monitor_index": str(monitor_index)},
        )
