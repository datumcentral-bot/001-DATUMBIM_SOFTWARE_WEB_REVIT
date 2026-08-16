from __future__ import annotations

import ctypes
import ctypes.wintypes
import os
import platform
from datetime import UTC, datetime
from typing import Any, Optional

from desktop_agent.control.adapters.base import ControlAdapter
from desktop_agent.control.models import ActionRequest, ActionResult


WINDOWS_AVAILABLE = platform.system() == "Windows"


def _require_windows() -> ActionResult | None:
    if not WINDOWS_AVAILABLE:
        return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error="Windows adapter unavailable on this platform")
    return None


class WindowsControlAdapter(ControlAdapter):
    def move_mouse(self, x: int, y: int) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            screen_w = ctypes.windll.user32.GetSystemMetrics(0)
            screen_h = ctypes.windll.user32.GetSystemMetrics(1)
            ctypes.windll.user32.SetCursorPos(x, y)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mouse moved to ({x}, {y})")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def click(self, x: int, y: int, button: str = "left") -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            ctypes.windll.user32.SetCursorPos(x, y)
            if button == "right":
                ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)
            else:
                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"{button} click at ({x}, {y})")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def double_click(self, x: int, y: int) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            ctypes.windll.user32.SetCursorPos(x, y)
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"double click at ({x}, {y})")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def right_click(self, x: int, y: int) -> ActionResult:
        return self.click(x, y, button="right")

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            ctypes.windll.user32.SetCursorPos(start_x, start_y)
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            ctypes.windll.user32.SetCursorPos(end_x, end_y)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"drag from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def scroll(self, delta: int) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            ctypes.windll.user32.mouse_event(0x0800, 0, 0, int(delta * 120), 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"scroll {delta}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def press_key(self, key: str, modifiers: list[str]) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            vk = _map_key_to_vk(key)
            for modifier in modifiers:
                vk_mod = _map_key_to_vk(modifier)
                ctypes.windll.user32.keybd_event(vk_mod, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk, 0, 0x0002, 0)
            for modifier in modifiers:
                vk_mod = _map_key_to_vk(modifier)
                ctypes.windll.user32.keybd_event(vk_mod, 0, 0x0002, 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"key press {key} with modifiers {modifiers}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def type_text(self, text: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            for char in text:
                vk = ctypes.windll.user32.VkKeyScanW(ord(char)) & 0xFF
                ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
                ctypes.windll.user32.keybd_event(vk, 0, 0x0002, 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"typed text length {len(text)}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def hotkey(self, keys: list[str]) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            vks = [_map_key_to_vk(key) for key in keys]
            for vk in vks[:-1]:
                ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vks[-1], 0, 0, 0)
            ctypes.windll.user32.keybd_event(vks[-1], 0, 0x0002, 0)
            for vk in reversed(vks[:-1]):
                ctypes.windll.user32.keybd_event(vk, 0, 0x0002, 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"hotkey {keys}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def activate_window(self, window_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            ctypes.windll.user32.ShowWindow(hwnd, 9)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"activated window {window_id}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def minimize_window(self, window_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            ctypes.windll.user32.ShowWindow(hwnd, 6)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"minimized window {window_id}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def maximize_window(self, window_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            ctypes.windll.user32.ShowWindow(hwnd, 3)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"maximized window {window_id}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def restore_window(self, window_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            ctypes.windll.user32.ShowWindow(hwnd, 9)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"restored window {window_id}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def resize_window(self, window_id: str, width: int, height: int) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            ctypes.windll.user32.MoveWindow(hwnd, 0, 0, width, height, True)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"resized window {window_id} to {width}x{height}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def move_window(self, window_id: str, x: int, y: int) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            ctypes.windll.user32.MoveWindow(hwnd, x, y, 0, 0, True)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"moved window {window_id} to ({x}, {y})")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def close_window(self, window_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"closed window {window_id}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def launch_application(self, application_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            os.startfile(application_id)
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"launched application {application_id}")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def close_application(self, application_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            import psutil
            for proc in psutil.process_iter(["pid", "name"]):
                if proc.info["name"] and proc.info["name"].lower() == application_id.lower():
                    proc.terminate()
                    return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"closed application {application_id}")
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=f"Process {application_id} not found")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def focus_application(self, application_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            import psutil
            for proc in psutil.process_iter(["pid", "name"]):
                if proc.info["name"] and proc.info["name"].lower() == application_id.lower():
                    pid = proc.info["pid"]
                    hwnd = ctypes.windll.user32.GetTopWindow(0)
                    while hwnd:
                        window_pid = ctypes.c_ulong()
                        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
                        if window_pid.value == pid:
                            ctypes.windll.user32.ShowWindow(hwnd, 9)
                            ctypes.windll.user32.SetForegroundWindow(hwnd)
                            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"focused application {application_id}")
                        hwnd = ctypes.windll.user32.GetWindow(hwnd, 2)
                    return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=f"No window found for {application_id}")
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=f"Process {application_id} not found")
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))

    def get_window_state(self, window_id: str) -> ActionResult:
        failure = _require_windows()
        if failure:
            return failure
        try:
            hwnd = int(window_id)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            state = {
                "left": rect.left,
                "top": rect.top,
                "right": rect.right,
                "bottom": rect.bottom,
            }
            return ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=str(state))
        except Exception as exc:
            return ActionResult(action_id="", status="failed", started_at=datetime.now(tz=UTC), error=str(exc))


_VK_MAP = {
    "ctrl": 0x11,
    "alt": 0x12,
    "shift": 0x10,
    "win": 0x5B,
    "enter": 0x0D,
    "esc": 0x1B,
    "tab": 0x09,
    "space": 0x20,
    "backspace": 0x08,
    "delete": 0x2E,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
}


def _map_key_to_vk(key: str) -> int:
    key_lower = key.lower()
    if key_lower in _VK_MAP:
        return _VK_MAP[key_lower]
    if len(key) == 1:
        return ctypes.windll.user32.VkKeyScanW(ord(key)) & 0xFF
    raise ValueError(f"Unsupported key: {key}")
