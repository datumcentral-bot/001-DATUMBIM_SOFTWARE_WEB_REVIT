from __future__ import annotations

import base64
import io
import platform
from datetime import UTC, datetime
from typing import Any

from desktop_agent.observation.models import (
    CaptureMode,
    ObservationRequest,
    ObservationResult,
    ObservationStatus,
    Region,
    WindowInfo,
)
from desktop_agent.observation.providers.base import ObservationProvider

WINDOWS_AVAILABLE = platform.system() == "Windows"


class _BITMAPINFOHEADER:
    pass


class _BITMAPINFO:
    pass


if WINDOWS_AVAILABLE:
    import ctypes
    from ctypes import wintypes

    class _BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize", ctypes.c_uint32),
            ("biWidth", ctypes.c_long),
            ("biHeight", ctypes.c_long),
            ("biPlanes", ctypes.c_uint16),
            ("biBitCount", ctypes.c_uint16),
            ("biCompression", ctypes.c_uint32),
            ("biSizeImage", ctypes.c_uint32),
            ("biXPelsPerMeter", ctypes.c_long),
            ("biYPelsPerMeter", ctypes.c_long),
            ("biClrUsed", ctypes.c_uint32),
            ("biClrImportant", ctypes.c_uint32),
        ]

    class _BITMAPINFO(ctypes.Structure):
        _fields_ = [("bmiHeader", _BITMAPINFOHEADER), ("bmiColors", ctypes.c_uint8 * 3)]


def _get_cursor_position() -> dict[str, int] | None:
    if not WINDOWS_AVAILABLE:
        return None
    try:
        import ctypes

        class _POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

        point = _POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        return {"x": point.x, "y": point.y}
    except Exception:
        return None


def _get_window_text(hwnd: int) -> str | None:
    if not WINDOWS_AVAILABLE:
        return None
    try:
        import ctypes

        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return None
        buffer = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
        return buffer.value
    except Exception:
        return None


def _encode_image(buffer: bytes, width: int, height: int) -> str:
    try:
        from PIL import Image

        img = Image.frombuffer("RGB", (width, height), buffer, "raw", "BGR", 0, 1)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception:
        return base64.b64encode(buffer).decode("ascii")


def _capture_window_impl(hwnd: int) -> tuple[bytes, int, int] | None:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    if width <= 0 or height <= 0:
        return None
    hdc = user32.GetDC(hwnd)
    memdc = gdi32.CreateCompatibleDC(hdc)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc, width, height)
    gdi32.SelectObject(memdc, hbitmap)
    gdi32.BitBlt(memdc, 0, 0, width, height, hdc, 0, 0, 0x00CC0020)
    bmi = _BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(_BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 24
    bmi.bmiHeader.biCompression = 0
    buffer = ctypes.create_string_buffer(width * height * 3)
    gdi32.GetDIBits(memdc, hbitmap, 0, height, buffer, ctypes.byref(bmi), 0)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(hwnd, hdc)
    return buffer.raw, width, height


def _capture_screen_impl() -> tuple[bytes, int, int]:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc, width, height)
    gdi32.SelectObject(memdc, hbitmap)
    gdi32.BitBlt(memdc, 0, 0, width, height, hdc, 0, 0, 0x00CC0020)
    bmi = _BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(_BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 24
    bmi.bmiHeader.biCompression = 0
    buffer = ctypes.create_string_buffer(width * height * 3)
    gdi32.GetDIBits(memdc, hbitmap, 0, height, buffer, ctypes.byref(bmi), 0)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)
    return buffer.raw, width, height


def _capture_region_impl(x: int, y: int, width: int, height: int) -> tuple[bytes, int, int]:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc, width, height)
    gdi32.SelectObject(memdc, hbitmap)
    gdi32.BitBlt(memdc, 0, 0, width, height, hdc, x, y, 0x00CC0020)
    bmi = _BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(_BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 24
    bmi.bmiHeader.biCompression = 0
    buffer = ctypes.create_string_buffer(width * height * 3)
    gdi32.GetDIBits(memdc, hbitmap, 0, height, buffer, ctypes.byref(bmi), 0)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)
    return buffer.raw, width, height


class WindowsObservationProvider(ObservationProvider):
    def list_displays(self) -> list[Any]:
        if not WINDOWS_AVAILABLE:
            return []
        displays: list[Any] = []
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
                    type(
                        "DisplayInfo",
                        (),
                        {
                            "display_id": f"display-{index}",
                            "name": f"Display {index + 1}",
                            "x": left,
                            "y": top,
                            "width": width,
                            "height": height,
                            "scale_factor": 1.0,
                            "primary": (index == 0),
                        },
                    )()
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
        try:
            buffer, width, height = _capture_screen_impl()
            encoded = _encode_image(buffer, width, height)
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=request.target_id,
                status=ObservationStatus.COMPLETED,
                image_reference=f"data:image/png;base64,{encoded}",
                image_format="png",
                width=width,
                height=height,
                timestamp=datetime.now(tz=UTC),
                provider="windows_gdi",
                metadata={"capture_source": "screen", "cursor_position": _get_cursor_position()},
            )
        except Exception as exc:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=request.target_id,
                status=ObservationStatus.FAILED,
                error=str(exc),
                timestamp=datetime.now(tz=UTC),
            )

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
        return self.capture_screen(request)

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
            result = _capture_window_impl(hwnd)
            if result is None:
                return ObservationResult(
                    observation_id=request.observation_id,
                    session_id=request.session_id,
                    application_id=request.application_id,
                    target_type=request.target_type,
                    target_id=window_id,
                    status=ObservationStatus.WINDOW_NOT_FOUND,
                    error="Invalid window size",
                    timestamp=datetime.now(tz=UTC),
                )
            buffer, width, height = result
            encoded = _encode_image(buffer, width, height)
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=window_id,
                status=ObservationStatus.COMPLETED,
                image_reference=f"data:image/png;base64,{encoded}",
                image_format="png",
                width=width,
                height=height,
                timestamp=datetime.now(tz=UTC),
                provider="windows_gdi",
                metadata={"capture_source": "window", "window_title": _get_window_text(hwnd)},
            )
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
        try:
            buffer, width, height = _capture_region_impl(region.x, region.y, region.width, region.height)
            encoded = _encode_image(buffer, width, height)
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=None,
                status=ObservationStatus.COMPLETED,
                image_reference=f"data:image/png;base64,{encoded}",
                image_format="png",
                width=width,
                height=height,
                timestamp=datetime.now(tz=UTC),
                provider="windows_gdi",
                metadata={"capture_source": "region", "region": region.model_dump()},
            )
        except Exception as exc:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=None,
                status=ObservationStatus.FAILED,
                error=str(exc),
                timestamp=datetime.now(tz=UTC),
            )

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
        try:
            import psutil
            import win32gui
            import win32process

            for proc in psutil.process_iter(["pid", "name"]):
                if proc.info["name"] and proc.info["name"].lower() == application_id.lower():
                    pid = proc.info["pid"]

                    def callback(hwnd: int, extra: Any) -> bool:
                        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if window_pid == pid and win32gui.IsWindowVisible(hwnd):
                            title = win32gui.GetWindowText(hwnd)
                            if title:
                                return self.capture_window(request, str(hwnd))
                        return True

                    win32gui.EnumWindows(callback, None)
                    break
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=application_id,
                status=ObservationStatus.APPLICATION_NOT_RUNNING,
                error="Application window not found",
                timestamp=datetime.now(tz=UTC),
            )
        except Exception as exc:
            return ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=application_id,
                status=ObservationStatus.FAILED,
                error=str(exc),
                timestamp=datetime.now(tz=UTC),
            )
