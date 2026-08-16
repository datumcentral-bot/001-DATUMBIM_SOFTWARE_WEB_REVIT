from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

from datumbim.models.connector import ApplicationSessionModel

router = APIRouter(prefix="/observation", tags=["observation"])

_sessions: dict[str, ApplicationSessionModel] = {}
_captures: dict[str, list[dict]] = {}


@router.get("/sessions/{session_id}/state")
async def get_observation_state(session_id: str) -> dict:
    captures = _captures.get(session_id, [])
    return {
        "session_id": session_id,
        "status": "active" if captures else "idle",
        "captures_count": len(captures),
        "last_capture": captures[-1]["timestamp"] if captures else None,
    }


@router.post("/sessions/{session_id}/capture")
async def capture_screen(session_id: str) -> dict:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    capture = {
        "capture_id": str(__import__('uuid').uuid4()),
        "session_id": session_id,
        "application_id": session.application_id,
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "width": 0,
        "height": 0,
        "format": "png",
        "metadata": {"source": "stub"},
    }
    _captures.setdefault(session_id, []).append(capture)
    return {"capture": capture}


@router.get("/sessions/{session_id}/captures")
async def list_captures(session_id: str) -> dict:
    return {"captures": _captures.get(session_id, [])}


@router.delete("/sessions/{session_id}/captures")
async def clear_captures(session_id: str) -> dict:
    _captures.pop(session_id, None)
    return {"status": "cleared"}
