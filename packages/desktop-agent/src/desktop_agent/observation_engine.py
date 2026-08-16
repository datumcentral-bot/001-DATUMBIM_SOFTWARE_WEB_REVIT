from __future__ import annotations

import uuid
from datetime import UTC, datetime

from desktop_agent.observation_models import (
    ObservationEngineState,
    ObservationEntry,
    ScreenObservationRequest,
    ScreenshotCapture,
)
from desktop_agent.session_manager import SessionManager


class ObservationEngine:
    def __init__(self, session_manager: SessionManager | None = None) -> None:
        self.session_manager = session_manager or SessionManager()
        self._states: dict[str, ObservationEngineState] = {}
        self._captures: dict[str, list[ScreenshotCapture]] = {}

    def observe_screen(self, request: ScreenObservationRequest) -> ScreenshotCapture:
        session = self.session_manager.get_session(request.session_id)
        if not session:
            raise ValueError(f"Session not found: {request.session_id}")

        capture = ScreenshotCapture(
            capture_id=str(uuid.uuid4()),
            session_id=request.session_id,
            application_id=session.application_id,
            timestamp=datetime.now(tz=UTC),
            width=0,
            height=0,
            format=request.format,
            metadata={
                "include_cursor": str(request.include_cursor),
                "monitor_index": str(request.monitor_index),
            },
        )
        self._captures.setdefault(request.session_id, []).append(capture)
        self._states[request.session_id] = ObservationEngineState(
            session_id=request.session_id,
            status="captured",
            last_capture=capture.timestamp,
            captures_count=len(self._captures[request.session_id]),
        )
        return capture

    def observe_window(self, session_id: str) -> ObservationEntry | None:
        session = self.session_manager.get_session(session_id)
        if not session:
            return None
        entry = ObservationEntry(
            observation_id=str(uuid.uuid4()),
            session_id=session_id,
            application_id=session.application_id,
            kind="window",
            timestamp=datetime.now(tz=UTC),
            metadata={
                "window_title": session.window.title if session.window else "",
                "process_id": str(session.process_id) if session.process_id else "",
            },
        )
        return entry

    def get_state(self, session_id: str) -> ObservationEngineState | None:
        return self._states.get(session_id)

    def get_captures(self, session_id: str) -> list[ScreenshotCapture]:
        return list(self._captures.get(session_id, []))

    def clear(self, session_id: str) -> None:
        self._captures.pop(session_id, None)
        self._states.pop(session_id, None)
