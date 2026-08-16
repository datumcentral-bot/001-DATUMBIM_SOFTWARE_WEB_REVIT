from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class CaptureMode(str, Enum):
    FULL_SCREEN = "full_screen"
    DISPLAY = "display"
    WINDOW = "window"
    REGION = "region"
    APPLICATION = "application"


class ObservationStatus(str, Enum):
    PENDING = "pending"
    CAPTURING = "capturing"
    COMPLETED = "completed"
    FAILED = "failed"
    CAPTURE_UNAVAILABLE = "capture_unavailable"
    WINDOW_NOT_FOUND = "window_not_found"
    APPLICATION_NOT_RUNNING = "application_not_running"
    SESSION_NOT_FOUND = "session_not_found"
    PERMISSION_DENIED = "permission_denied"


class Region(BaseModel):
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def valid(self) -> bool:
        return self.width > 0 and self.height > 0


class DisplayInfo(BaseModel):
    display_id: str
    name: str
    x: int
    y: int
    width: int
    height: int
    scale_factor: float = 1.0
    primary: bool = False


class WindowInfo(BaseModel):
    window_id: str
    handle: int | None = None
    title: str
    process_id: int | None = None
    application_id: str | None = None
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    visible: bool = False
    minimized: bool = False
    active: bool = False


class ObservationRequest(BaseModel):
    observation_id: str
    session_id: str
    application_id: str
    target_type: CaptureMode
    target_id: str | None = None
    region: Region | None = None
    requested_by: str = "system"
    timestamp: Any
    include_cursor: bool = False
    image_format: str = "png"
    quality: int = 90


class ObservationResult(BaseModel):
    observation_id: str
    session_id: str
    application_id: str
    target_type: CaptureMode
    target_id: str | None = None
    status: ObservationStatus
    image_reference: str | None = None
    image_format: str = "png"
    width: int = 0
    height: int = 0
    timestamp: Any
    started_at: Any | None = None
    completed_at: Any | None = None
    duration: float | None = None
    provider: str | None = None
    metadata: dict[str, Any] = {}
    error: str | None = None


class ObservationStoreEntry(BaseModel):
    observation_id: str
    session_id: str
    application_id: str
    target_type: CaptureMode
    target_id: str | None = None
    image_reference: str | None = None
    image_format: str = "png"
    width: int = 0
    height: int = 0
    timestamp: Any
    duration: float | None = None
    provider: str | None = None
    metadata: dict[str, Any] = {}
    error: str | None = None
