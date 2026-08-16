from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel

from ai_engine.models import AIModel, AIProviderHealth, AIRequest, AIResponse


class VisionElementType(str, Enum):
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
    UNKNOWN = "unknown"


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class VisionElement(BaseModel):
    id: str
    type: VisionElementType = VisionElementType.UNKNOWN
    label: str | None = None
    text: str | None = None
    bounding_box: BoundingBox | None = None
    confidence: float | None = None
    clickable: bool = False
    enabled: bool = False
    visible: bool = False
    role: str | None = None


class VisionRegion(BaseModel):
    x: int
    y: int
    width: int
    height: int
    label: str | None = None
    confidence: float | None = None


class TextBlock(BaseModel):
    text: str
    bounding_box: BoundingBox | None = None
    confidence: float | None = None


class ActionHint(BaseModel):
    element_id: str
    action_type: str
    description: str | None = None
    confidence: float | None = None
    requires_confirmation: bool = True


class VisionContext(BaseModel):
    application_id: str | None = None
    application_name: str | None = None
    session_id: str | None = None
    window_id: str | None = None
    observation_id: str | None = None
    active_document: str | None = None
    active_view: str | None = None
    previous_observation_id: str | None = None


class VisionRequest(BaseModel):
    request_id: str
    observation_id: str
    provider_id: str | None = None
    model_id: str | None = None
    context: VisionContext | None = None
    instructions: str | None = None
    detect_ui: bool = True
    detect_text: bool = True
    detect_regions: bool = True
    describe_application: bool = False
    generate_action_hints: bool = False
    image_reference: str | None = None
    metadata: dict[str, Any] = {}


class VisionResponse(BaseModel):
    request_id: str
    observation_id: str
    provider_id: str | None = None
    model_id: str | None = None
    status: str
    confidence: float | None = None
    application: str | None = None
    window: str | None = None
    screen_description: str | None = None
    elements: list[VisionElement] = []
    regions: list[VisionRegion] = []
    text_blocks: list[TextBlock] = []
    action_hints: list[ActionHint] = []
    warnings: list[str] = []
    processing_time: float | None = None
    usage: dict[str, Any] | None = None
    raw_reference: str | None = None
    error: str | None = None
