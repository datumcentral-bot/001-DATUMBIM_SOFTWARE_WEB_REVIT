from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

from datumbim.models.connector import ApplicationSessionModel

router = APIRouter(prefix="/sessions", tags=["sessions"])

_sessions: dict[str, ApplicationSessionModel] = {}


@router.get("/")
async def list_sessions(application_id: Optional[str] = None) -> dict:
    sessions = list(_sessions.values())
    if application_id:
        sessions = [s for s in sessions if s.application_id == application_id]
    return {"sessions": [s.model_dump() for s in sessions]}


@router.get("/{session_id}")
async def get_session(session_id: str) -> dict:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.model_dump()


@router.post("/{application_id}/start")
async def start_session(application_id: str) -> dict:
    session = ApplicationSessionModel(
        id=f"{application_id}-{datetime.now(tz=UTC).timestamp()}",
        application_id=application_id,
        status="active",
        metadata={"source": "desktop-agent"},
    )
    _sessions[session.id] = session
    return {"session": session.model_dump()}


@router.post("/{application_id}/attach")
async def attach_session(application_id: str) -> dict:
    for session in _sessions.values():
        if session.application_id == application_id and session.status == "active":
            return {"session": session.model_dump()}
    session = ApplicationSessionModel(
        id=f"{application_id}-{datetime.now(tz=UTC).timestamp()}",
        application_id=application_id,
        status="active",
        metadata={"attached": "true", "source": "desktop-agent"},
    )
    _sessions[session.id] = session
    return {"session": session.model_dump()}


@router.post("/{session_id}/detach")
async def detach_session(session_id: str) -> dict:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.status = "detached"
    return {"session": session.model_dump()}


@router.delete("/{session_id}")
async def close_session(session_id: str) -> dict:
    session = _sessions.pop(session_id, None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "closed", "session_id": session_id}


@router.post("/{session_id}/restart")
async def restart_session(session_id: str) -> dict:
    session = _sessions.pop(session_id, None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    new_session = ApplicationSessionModel(
        id=f"{session.application_id}-{datetime.now(tz=UTC).timestamp()}",
        application_id=session.application_id,
        status="active",
        metadata={"restarted": "true", "source": "desktop-agent"},
    )
    _sessions[new_session.id] = new_session
    return {"session": new_session.model_dump()}
