from datetime import datetime

from pydantic import BaseModel


class ScreenshotCapture(BaseModel):
    capture_id: str
    session_id: str
    application_id: str
    timestamp: datetime
    width: int
    height: int
    format: str = "png"
    data_uri: str | None = None
    path: str | None = None
    metadata: dict[str, str] = {}


class ObservationEntry(BaseModel):
    observation_id: str
    session_id: str
    application_id: str
    kind: str
    timestamp: datetime
    data: str | None = None
    metadata: dict[str, str] = {}


class ScreenObservationRequest(BaseModel):
    session_id: str
    include_cursor: bool = False
    monitor_index: int = 0
    format: str = "png"


class ObservationEngineState(BaseModel):
    session_id: str
    status: str
    last_capture: datetime | None = None
    captures_count: int = 0
    error: str | None = None
