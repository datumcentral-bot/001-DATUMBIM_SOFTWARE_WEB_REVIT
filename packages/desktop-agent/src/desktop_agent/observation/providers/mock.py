from __future__ import annotations

import hashlib
import os
import uuid
from datetime import UTC, datetime
from typing import Any

from desktop_agent.observation.models import (
    CaptureMode,
    DisplayInfo,
    ObservationRequest,
    ObservationResult,
    ObservationStoreEntry,
    Region,
    WindowInfo,
)
from desktop_agent.observation.providers.base import (
    CaptureSupport,
    ObservationProvider,
)


class MockObservationProvider(ObservationProvider):
    def __init__(self) -> None:
        self._display_counter = 0
        self._window_counter = 0
        self._capture_counter = 0

    def list_displays(self) -> list[DisplayInfo]:
        self._display_counter += 1
        return [
            DisplayInfo(
                display_id="display-1",
                name="Primary Display",
                x=0,
                y=0,
                width=1920,
                height=1080,
                scale_factor=1.0,
                primary=True,
            )
        ]

    def list_windows(self) -> list[WindowInfo]:
        self._window_counter += 1
        return [
            WindowInfo(
                window_id="window-1",
                handle=12345,
                title="Mock Application",
                process_id=1000,
                application_id="mock-app",
                x=100,
                y=100,
                width=800,
                height=600,
                visible=True,
                minimized=False,
                active=True,
            )
        ]

    def capture_screen(self, request: ObservationRequest) -> ObservationResult:
        self._capture_counter += 1
        return self._build_result(request, status="completed", width=1920, height=1080, provider="mock")

    def capture_display(self, request: ObservationRequest, display_id: str) -> ObservationResult:
        self._capture_counter += 1
        return self._build_result(request, status="completed", width=1920, height=1080, provider="mock")

    def capture_window(self, request: ObservationRequest, window_id: str) -> ObservationResult:
        self._capture_counter += 1
        return self._build_result(request, status="completed", width=800, height=600, provider="mock")

    def capture_region(self, request: ObservationRequest, region: Any) -> ObservationResult:
        self._capture_counter += 1
        region = region or request.region or Region()
        width = max(region.width, 1)
        height = max(region.height, 1)
        return self._build_result(request, status="completed", width=width, height=height, provider="mock")

    def capture_application(self, request: ObservationRequest, application_id: str) -> ObservationResult:
        self._capture_counter += 1
        return self._build_result(request, status="completed", width=800, height=600, provider="mock")

    def _build_result(
        self,
        request: ObservationRequest,
        status: str = "completed",
        width: int = 0,
        height: int = 0,
        provider: str = "mock",
    ) -> ObservationResult:
        image_reference = None
        if status == "completed":
            image_reference = f"mock://observations/{request.observation_id}.{request.image_format}"
        return ObservationResult(
            observation_id=request.observation_id,
            session_id=request.session_id,
            application_id=request.application_id,
            target_type=request.target_type,
            target_id=request.target_id,
            status=status,
            image_reference=image_reference,
            image_format=request.image_format,
            width=width,
            height=height,
            timestamp=datetime.now(tz=UTC),
            duration=0.0,
            provider=provider,
            metadata={"mock": "true"},
        )
