from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class UIElementType(str, Enum):
    WINDOW = "window"
    DIALOG = "dialog"
    BUTTON = "button"
    MENU = "menu"
    TAB = "tab"
    TEXT = "text"
    INPUT = "input"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DROPDOWN = "dropdown"
    TREE = "tree"
    LIST = "list"
    TABLE = "table"
    TOOLBAR = "toolbar"
    RIBBON = "ribbon"
    VIEWPORT = "viewport"
    ICON = "icon"
    SCROLLBAR = "scrollbar"
    STATUSBAR = "statusbar"
    UNKNOWN = "unknown"


class UIElement(BaseModel):
    element_id: str
    type: UIElementType
    label: str | None = None
    text: str | None = None
    bounding_box: dict[str, int] | None = None
    confidence: float = 1.0
    clickable: bool = False
    enabled: bool = True
    visible: bool = True
    parent_id: str | None = None
    children: list[str] = []
    metadata: dict[str, Any] = {}


class UITree(BaseModel):
    root_id: str
    elements: dict[str, UIElement]
    application_id: str
    session_id: str
    timestamp: Any
    provider: str | None = None
