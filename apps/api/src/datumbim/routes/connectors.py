from fastapi import APIRouter, HTTPException
from typing import Optional
from datumbim.models.connector import ApplicationConnectorModel, ApplicationSessionModel

router = APIRouter(prefix="/connectors", tags=["connectors"])

_registered_connectors: dict[str, ApplicationConnectorModel] = {}
_sessions: dict[str, ApplicationSessionModel] = {}


@router.get("/")
async def list_connectors(status: Optional[str] = None) -> dict:
    connectors = list(_registered_connectors.values())
    if status:
        connectors = [c for c in connectors if c.status == status]
    return {"connectors": [c.model_dump() for c in connectors]}


@router.get("/{connector_id}")
async def get_connector(connector_id: str) -> dict:
    connector = _registered_connectors.get(connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    return connector.model_dump()


@router.post("/{connector_id}/connect")
async def connect_connector(connector_id: str) -> dict:
    connector = _registered_connectors.get(connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    session = ApplicationSessionModel(
        id=f"{connector_id}-session-{datetime.utcnow().timestamp()}",
        application_id=connector_id,
        status="connected",
        capabilities=connector.capabilities,
    )
    _sessions[session.id] = session
    connector.sessions.append(session)
    connector.status = "connected"
    return {"session": session.model_dump()}


@router.delete("/{connector_id}/sessions/{session_id}")
async def disconnect_session(connector_id: str, session_id: str) -> dict:
    connector = _registered_connectors.get(connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    session = _sessions.pop(session_id, None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    connector.sessions = [s for s in connector.sessions if s.id != session_id]
    if not connector.sessions:
        connector.status = "discovered"
    return {"status": "disconnected"}


@router.get("/sessions")
async def list_sessions() -> dict:
    return {"sessions": [s.model_dump() for s in _sessions.values()]}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str) -> dict:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.model_dump()
