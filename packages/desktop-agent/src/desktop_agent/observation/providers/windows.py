from __future__ import annotations

import platform
from datetime import UTC, datetime
from typing import Any

from desktop_agent.observation.models import (
    CaptureMode,
    DisplayInfo,
    ObservationRequest,
    ObservationResult,
    ObservationStatus,
    Region,
    WindowInfo,
)
from desktop_agent.observation.providers.base import ObservationProvider

WINDOWS_AVAILABLE = platform.system() == "Windows"


class WindowsObservationProvider(ObservationProvider):
    def list_displays(self) -> list[DisplayInfo]:
        if not WINDOWS_AVAILABLE:
            return []
        displays: list[DisplayInfo] = []
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            display_count = user32.GetSystemMetrics(80)
            for index in range(display_count):
                left = user32.GetSystemMetrics(76 + index * 2)
                top = user32.GetSystemMetrics(77 + index * 2)
                width = user32.GetSystemMetrics(78 + index * 2)
                height = user32.GetSystemMetrics(79 + index * 2)
                displays.append(
                    DisplayInfo(
                        display_id=f"display-{index}",
                        name=f"Display {index + 1}",
                        x=left,
                        y=top,
                        width=width,
                        height=height,
                        scale_factor=1.0,
                        primary=(index == 0),
                    )
                )
        except Exception:
            return []
        return displays

    def list_windows(self) -> list[WindowInfo]:
        if not WINDOWS_AVAILABLE:
            return []
        windows: list[WindowInfo] = []
        try:
            import win32gui
            import win32process

            def callback(hwnd: int, extra: Any) -> bool:
                if not win32gui.IsWindowVisible(hwnd):
                    return True
                title = win32gui.GetWindowText(hwnd)
                if not title:
                    return True
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                windows.append(
                    WindowInfo(
                        window_id=str(hwnd),
                        handle=hwnd,
                        title=title,
                        process_id=pid,
                        x=rect[0],
                        y=rect[1],
                        width=rect[2] - rect[0],
                        height=rect[3] - rect[1],
                        visible=True,
                        minimized=win32gui.IsIconic(hwnd) != 0,
                        active=hwnd == win32gui.GetForegroundWindow(),
                    )
                )
                return True

            win32gui.EnumWindows(callback, None)
        except Exception:
            return []
        return windows

    def capture_screen(self, request: ObservationRequest) -> ObservationResult:
        if not WINDOWS_AVAILABLE:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=request.target_id,
                status=ObservationStatus.CAPTURE_UNAVAILABLE,
                error="Screen capture unavailable on this platform",
                timestamp=datetime.now(tz=UTC),
            )
        return self._capture_unsupported(request)

    def capture_display(self, request: ObservationRequest, display_id: str) -> ObservationResult:
        if not WINDOWS_AVAILABLE:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=display_id,
                status=ObservationStatus.CAPTURE_UNAVAILABLE,
                error="Display capture unavailable on this platform",
                timestamp=datetime.now(tz=UTC),
            )
        return self._capture_unsupported(request)

    def capture_window(self, request: ObservationRequest, window_id: str) -> ObservationResult:
        if not WINDOWS_AVAILABLE:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=window_id,
                status=ObservationStatus.CAPTURE_UNAVAILABLE,
                error="Window capture unavailable on this platform",
                timestamp=datetime.now(tz=UTC),
            )
        try:
            hwnd = int(window_id)
            return self._capture_unsupported(request)
        except Exception as exc:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=window_id,
                status=ObservationStatus.WINDOW_NOT_FOUND,
                error=str(exc),
                timestamp=datetime.now(tz=UTC),
            )

    def capture_region(self, request: ObservationRequest, region: Any) -> ObservationResult:
        if not WINDOWS_AVAILABLE:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=None,
                status=ObservationStatus.CAPTURE_UNAVAILABLE,
                error="Region capture unavailable on this platform",
                timestamp=datetime.now(tz=UTC),
            )
        return self._capture_unsupported(request)

    def capture_application(self, request: ObservationRequest, application_id: str) -> ObservationResult:
        if not WINDOWS_AVAILABLE:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=application_id,
                status=ObservationStatus.CAPTURE_UNAVAILABLE,
                error="Application capture unavailable on this platform",
                timestamp=datetime.now(tz=UTC),
            )
        return self._capture_unsupported(request)

    def _capture_unsupported(self, request: ObservationRequest) -> ObservationResult:
        return ObservationResult(
            observation_id=request.observation_id,
            session_id=request.session_id,
            application_id=request.application_id,
            target_type=request.target_type,
            target_id=request.target_id,
            status=ObservationStatus.CAPTURE_UNAVAILABLE,
            error="Capture requires additional Windows imaging libraries not configured in this build",
            timestamp=datetime.now(tz=UTC),
        )
