from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.control.adapters.base import ControlAdapter
from desktop_agent.control.adapters.mock import MockControlAdapter
from desktop_agent.control.models import ActionPlan, ActionRequest, ActionResult
from desktop_agent.session_manager import SessionManager


class ControlEngine:
    def __init__(self, session_manager: SessionManager | None = None, adapter: ControlAdapter | None = None) -> None:
        self.session_manager = session_manager or SessionManager()
        self.adapter = adapter or MockControlAdapter()

    def execute(self, request: ActionRequest) -> ActionResult:
        started_at = datetime.now(tz=UTC)
        if request.dry_run:
            return ActionResult(action_id=request.action_id, status="completed", started_at=started_at, result="dry_run")
        try:
            result = self._dispatch(request)
            result.started_at = started_at
            result.completed_at = datetime.now(tz=UTC)
            result.duration = (result.completed_at - started_at).total_seconds()
            return result
        except Exception as exc:  # pragma: no cover - safety net
            return ActionResult(action_id=request.action_id, status="failed", started_at=started_at, completed_at=datetime.now(tz=UTC), error=str(exc))

    def _dispatch(self, request: ActionRequest) -> ActionResult:
        action_type = request.action_type
        parameters = request.parameters or {}
        if action_type == "mouse_move":
            return self.adapter.move_mouse(int(parameters.get("x", 0)), int(parameters.get("y", 0)))
        if action_type == "mouse_click":
            return self.adapter.click(int(parameters.get("x", 0)), int(parameters.get("y", 0)), parameters.get("button", "left"))
        if action_type == "mouse_double_click":
            return self.adapter.double_click(int(parameters.get("x", 0)), int(parameters.get("y", 0)))
        if action_type == "mouse_right_click":
            return self.adapter.right_click(int(parameters.get("x", 0)), int(parameters.get("y", 0)))
        if action_type == "mouse_drag":
            return self.adapter.drag(int(parameters.get("start_x", 0)), int(parameters.get("start_y", 0)), int(parameters.get("end_x", 0)), int(parameters.get("end_y", 0)), float(parameters.get("duration", 0.1)))
        if action_type == "mouse_scroll":
            return self.adapter.scroll(int(parameters.get("delta", 0)))
        if action_type == "keyboard_key":
            return self.adapter.press_key(str(parameters.get("key", "")), list(parameters.get("modifiers", [])))
        if action_type == "keyboard_type":
            return self.adapter.type_text(str(parameters.get("text", "")))
        if action_type == "keyboard_hotkey":
            return self.adapter.hotkey(list(parameters.get("keys", [])))
        if action_type == "window_activate":
            return self.adapter.activate_window(str(parameters.get("window_id", "")))
        if action_type == "window_minimize":
            return self.adapter.minimize_window(str(parameters.get("window_id", "")))
        if action_type == "window_maximize":
            return self.adapter.maximize_window(str(parameters.get("window_id", "")))
        if action_type == "window_restore":
            return self.adapter.restore_window(str(parameters.get("window_id", "")))
        if action_type == "window_resize":
            return self.adapter.resize_window(str(parameters.get("window_id", "")), int(parameters.get("width", 0)), int(parameters.get("height", 0)))
        if action_type == "window_move":
            return self.adapter.move_window(str(parameters.get("window_id", "")), int(parameters.get("x", 0)), int(parameters.get("y", 0)))
        if action_type == "window_close":
            return self.adapter.close_window(str(parameters.get("window_id", "")))
        if action_type == "application_launch":
            return self.adapter.launch_application(str(parameters.get("application_id", "")))
        if action_type == "application_close":
            return self.adapter.close_application(str(parameters.get("application_id", "")))
        if action_type == "application_focus":
            return self.adapter.focus_application(str(parameters.get("application_id", "")))
        if action_type == "window_state":
            return self.adapter.get_window_state(str(parameters.get("window_id", "")))
        return ActionResult(action_id=request.action_id, status="failed", started_at=datetime.now(tz=UTC), error=f"Unsupported action type: {action_type}")

    def execute_plan(self, plan: ActionPlan) -> list[ActionResult]:
        results: list[ActionResult] = []
        for action in plan.actions:
            results.append(self.execute(action))
        return results
