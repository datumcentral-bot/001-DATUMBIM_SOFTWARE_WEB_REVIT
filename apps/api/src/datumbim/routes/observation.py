from datetime import UTC, datetime
from enum import Enum
from typing import Optional
from fastapi import APIRouter, HTTPException

from datumbim.models.connector import ApplicationSessionModel

router = APIRouter(prefix="/observation", tags=["observation"])

_sessions: dict[str, ApplicationSessionModel] = {}
_captures: dict[str, list[dict]] = {}


class CaptureMode(str, Enum):
    full_screen = "full_screen"
    display = "display"
    window = "window"
    region = "region"
    application = "application"


def _get_observation_engine():
    try:
        from desktop_agent.observation.engine import ObservationEngine
        from desktop_agent.observation.providers.mock import MockObservationProvider
        return ObservationEngine(provider=MockObservationProvider())
    except ImportError:
        return None


@router.get("/displays")
async def list_displays() -> dict:
    engine = _get_observation_engine()
    if engine:
        return {"displays": [d.__dict__ if hasattr(d, '__dict__') else str(d) for d in engine.list_displays()]}
    return {"displays": []}


@router.get("/windows")
async def list_windows() -> dict:
    engine = _get_observation_engine()
    if engine:
        return {"windows": [w.__dict__ if hasattr(w, '__dict__') else str(w) for w in engine.list_windows()]}
    return {"windows": []}


@router.get("/sessions/{session_id}/state")
async def get_observation_state(session_id: str) -> dict:
    captures = _captures.get(session_id, [])
    return {
        "session_id": session_id,
        "status": "active" if captures else "idle",
        "captures_count": len(captures),
        "last_capture": captures[-1]["timestamp"] if captures else None,
    }


@router.post("/capture")
async def capture_observation(request: dict) -> dict:
    session_id = request.get("session_id")
    application_id = request.get("application_id")
    target_type = request.get("target_type", "full_screen")
    target_id = request.get("target_id")
    if not session_id or not application_id:
        raise HTTPException(status_code=400, detail="session_id and application_id are required")
    session = _sessions.get(session_id)
    if not session:
        session = ApplicationSessionModel(
            id=session_id,
            application_id=application_id,
            status="active",
            metadata={"source": "observation"},
        )
        _sessions[session_id] = session
    engine = _get_observation_engine()
    if engine:
        from desktop_agent.observation.models import CaptureMode as CMode
        from desktop_agent.observation.models import ObservationRequest
        mode_map = {
            "full_screen": CMode.FULL_SCREEN,
            "display": CMode.DISPLAY,
            "window": CMode.WINDOW,
            "region": CMode.REGION,
            "application": CMode.APPLICATION,
        }
        obs_request = ObservationRequest(
            observation_id=str(__import__("uuid").uuid4()),
            session_id=session_id,
            application_id=application_id,
            target_type=mode_map.get(target_type, CMode.FULL_SCREEN),
            target_id=target_id,
            timestamp=datetime.now(tz=UTC),
        )
        result = engine.capture(obs_request)
        capture = {
            "capture_id": result.observation_id,
            "session_id": session_id,
            "application_id": application_id,
            "target_type": target_type,
            "target_id": target_id,
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "width": result.width,
            "height": result.height,
            "format": result.image_format,
            "status": result.status.value if hasattr(result.status, "value") else str(result.status),
            "provider": result.provider,
            "metadata": result.metadata,
            "image_reference": result.image_reference,
            "error": result.error,
        }
    else:
        capture = {
            "capture_id": str(__import__("uuid").uuid4()),
            "session_id": session_id,
            "application_id": application_id,
            "target_type": target_type,
            "target_id": target_id,
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "width": 0,
            "height": 0,
            "format": "png",
            "status": "completed",
            "provider": "mock",
            "metadata": {"source": "stub"},
        }
    _captures.setdefault(session_id, []).append(capture)
    return {"capture": capture}


@router.post("/capture/screen")
async def capture_screen(request: dict) -> dict:
    return await capture_observation(request)


@router.post("/capture/window")
async def capture_window(request: dict) -> dict:
    return await capture_observation(request)


@router.post("/capture/region")
async def capture_region(request: dict) -> dict:
    return await capture_observation(request)


@router.get("/sessions/{session_id}/captures")
async def list_captures(session_id: str) -> dict:
    return {"captures": _captures.get(session_id, [])}


@router.get("/{observation_id}")
async def get_observation(observation_id: str) -> dict:
    for captures in _captures.values():
        for capture in captures:
            if capture.get("capture_id") == observation_id:
                return {"capture": capture}
    raise HTTPException(status_code=404, detail="Observation not found")


@router.delete("/{observation_id}")
async def delete_observation(observation_id: str) -> dict:
    for session_id, captures in _captures.items():
        for capture in captures:
            if capture.get("capture_id") == observation_id:
                captures.remove(capture)
                return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Observation not found")


@router.delete("/sessions/{session_id}/captures")
async def clear_captures(session_id: str) -> dict:
    _captures.pop(session_id, None)
    return {"status": "cleared"}
