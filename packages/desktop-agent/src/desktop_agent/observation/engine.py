from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from desktop_agent.observation.models import (
    CaptureMode,
    ObservationRequest,
    ObservationResult,
    ObservationStatus,
    Region,
)
from desktop_agent.observation.providers.base import ObservationProvider
from desktop_agent.observation.storage import ObservationStore


class ObservationEngine:
    def __init__(
        self,
        provider: ObservationProvider | None = None,
        store: ObservationStore | None = None,
    ) -> None:
        self.provider = provider or ObservationProvider()
        self.store = store or ObservationStore()

    def capture(self, request: ObservationRequest) -> ObservationResult:
        started_at = datetime.now(tz=UTC)
        if request.target_type == CaptureMode.FULL_SCREEN:
            result = self.provider.capture_screen(request)
        elif request.target_type == CaptureMode.DISPLAY:
            target_id = request.target_id or ""
            result = self.provider.capture_display(request, target_id)
        elif request.target_type == CaptureMode.WINDOW:
            target_id = request.target_id or ""
            result = self.provider.capture_window(request, target_id)
        elif request.target_type == CaptureMode.REGION:
            region = request.region or Region()
            if not region.valid():
                result = ObservationResult(
                    observation_id=request.observation_id,
                    session_id=request.session_id,
                    application_id=request.application_id,
                    target_type=request.target_type,
                    target_id=request.target_id,
                    status=ObservationStatus.FAILED,
                    error="Invalid region",
                    timestamp=datetime.now(tz=UTC),
                )
            else:
                result = self.provider.capture_region(request, region)
        elif request.target_type == CaptureMode.APPLICATION:
            target_id = request.application_id
            result = self.provider.capture_application(request, target_id)
        else:
            result = ObservationResult(
                observation_id=request.observation_id,
                session_id=request.session_id,
                application_id=request.application_id,
                target_type=request.target_type,
                target_id=request.target_id,
                status=ObservationStatus.FAILED,
                error=f"Unsupported capture mode: {request.target_type}",
                timestamp=datetime.now(tz=UTC),
            )
        result.started_at = started_at
        result.completed_at = datetime.now(tz=UTC)
        result.duration = (result.completed_at - started_at).total_seconds()
        self.store.save(result)
        return result

    def list_displays(self) -> list[Any]:
        return self.provider.list_displays()

    def list_windows(self) -> list[Any]:
        return self.provider.list_windows()
