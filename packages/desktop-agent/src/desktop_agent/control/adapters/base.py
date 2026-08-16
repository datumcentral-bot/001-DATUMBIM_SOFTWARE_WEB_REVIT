from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from desktop_agent.control.models import ActionRequest, ActionResult


class ControlAdapter(ABC):
    @abstractmethod
    def move_mouse(self, x: int, y: int) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def click(self, x: int, y: int, button: str = "left") -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def double_click(self, x: int, y: int) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def right_click(self, x: int, y: int) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def scroll(self, delta: int) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def press_key(self, key: str, modifiers: list[str]) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def type_text(self, text: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def hotkey(self, keys: list[str]) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def activate_window(self, window_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def minimize_window(self, window_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def maximize_window(self, window_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def restore_window(self, window_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def resize_window(self, window_id: str, width: int, height: int) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def move_window(self, window_id: str, x: int, y: int) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def close_window(self, window_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def launch_application(self, application_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def close_application(self, application_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def focus_application(self, application_id: str) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def get_window_state(self, window_id: str) -> ActionResult:
        raise NotImplementedError
