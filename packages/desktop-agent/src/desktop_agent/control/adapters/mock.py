from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.control.adapters.base import ControlAdapter
from desktop_agent.control.models import ActionRequest, ActionResult


class MockControlAdapter(ControlAdapter):
    def __init__(self) -> None:
        self.actions: list[tuple[ActionRequest, ActionResult]] = []

    def _record(self, request: ActionRequest, result: ActionResult) -> None:
        self.actions.append((request, result))

    def move_mouse(self, x: int, y: int) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock mouse move to ({x}, {y})")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="mouse_move", timestamp=datetime.now(tz=UTC)), result)
        return result

    def click(self, x: int, y: int, button: str = "left") -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock {button} click at ({x}, {y})")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="mouse_click", timestamp=datetime.now(tz=UTC)), result)
        return result

    def double_click(self, x: int, y: int) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock double click at ({x}, {y})")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="mouse_double_click", timestamp=datetime.now(tz=UTC)), result)
        return result

    def right_click(self, x: int, y: int) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock right click at ({x}, {y})")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="mouse_right_click", timestamp=datetime.now(tz=UTC)), result)
        return result

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock drag from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="mouse_drag", timestamp=datetime.now(tz=UTC)), result)
        return result

    def scroll(self, delta: int) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock scroll {delta}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="mouse_scroll", timestamp=datetime.now(tz=UTC)), result)
        return result

    def press_key(self, key: str, modifiers: list[str]) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock key press {key} with modifiers {modifiers}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="keyboard_key", timestamp=datetime.now(tz=UTC)), result)
        return result

    def type_text(self, text: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock type text length {len(text)}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="keyboard_type", timestamp=datetime.now(tz=UTC)), result)
        return result

    def hotkey(self, keys: list[str]) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock hotkey {keys}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="keyboard_hotkey", timestamp=datetime.now(tz=UTC)), result)
        return result

    def activate_window(self, window_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock activate window {window_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_activate", timestamp=datetime.now(tz=UTC)), result)
        return result

    def minimize_window(self, window_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock minimize window {window_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_minimize", timestamp=datetime.now(tz=UTC)), result)
        return result

    def maximize_window(self, window_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock maximize window {window_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_maximize", timestamp=datetime.now(tz=UTC)), result)
        return result

    def restore_window(self, window_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock restore window {window_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_restore", timestamp=datetime.now(tz=UTC)), result)
        return result

    def resize_window(self, window_id: str, width: int, height: int) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock resize window {window_id} to {width}x{height}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_resize", timestamp=datetime.now(tz=UTC)), result)
        return result

    def move_window(self, window_id: str, x: int, y: int) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock move window {window_id} to ({x}, {y})")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_move", timestamp=datetime.now(tz=UTC)), result)
        return result

    def close_window(self, window_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock close window {window_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_close", timestamp=datetime.now(tz=UTC)), result)
        return result

    def launch_application(self, application_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock launch application {application_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id=application_id, action_type="application_launch", timestamp=datetime.now(tz=UTC)), result)
        return result

    def close_application(self, application_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock close application {application_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id=application_id, action_type="application_close", timestamp=datetime.now(tz=UTC)), result)
        return result

    def focus_application(self, application_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock focus application {application_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id=application_id, action_type="application_focus", timestamp=datetime.now(tz=UTC)), result)
        return result

    def get_window_state(self, window_id: str) -> ActionResult:
        result = ActionResult(action_id="", status="completed", started_at=datetime.now(tz=UTC), result=f"mock window state for {window_id}")
        self._record(ActionRequest(action_id="", session_id="", application_id="", action_type="window_state", timestamp=datetime.now(tz=UTC)), result)
        return result
