from __future__ import annotations

import abc
import enum
from typing import Any

from desktop_agent.observation.models import (
    CaptureMode,
    DisplayInfo,
    ObservationRequest,
    ObservationResult,
    WindowInfo,
)


class CaptureSupport(enum.Enum):
    FULL_SCREEN = "full_screen"
    DISPLAY = "display"
    WINDOW = "window"
    REGION = "region"
    APPLICATION = "application"


class ObservationProvider(abc.ABC):
    @abc.abstractmethod
    def list_displays(self) -> list[DisplayInfo]:
        raise NotImplementedError

    @abc.abstractmethod
    def list_windows(self) -> list[WindowInfo]:
        raise NotImplementedError

    @abc.abstractmethod
    def capture_screen(self, request: ObservationRequest) -> ObservationResult:
        raise NotImplementedError

    @abc.abstractmethod
    def capture_display(self, request: ObservationRequest, display_id: str) -> ObservationResult:
        raise NotImplementedError

    @abc.abstractmethod
    def capture_window(self, request: ObservationRequest, window_id: str) -> ObservationResult:
        raise NotImplementedError

    @abc.abstractmethod
    def capture_region(self, request: ObservationRequest, region: Any) -> ObservationResult:
        raise NotImplementedError

    @abc.abstractmethod
    def capture_application(self, request: ObservationRequest, application_id: str) -> ObservationResult:
        raise NotImplementedError
