from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

from datumbim.models.connector import ApplicationSessionModel

router = APIRouter(prefix="/control", tags=["control"])

_actions: list[dict] = []


@router.get("/actions")
async def list_actions(session_id: Optional[str] = None) -> dict:
    actions = _actions
    if session_id:
        actions = [a for a in actions if a.get("session_id") == session_id]
    return {"actions": actions}


@router.post("/actions")
async def execute_action(action: dict) -> dict:
    action_id = action.get("action_id", "")
    session_id = action.get("session_id", "")
    application_id = action.get("application_id", "")
    action_type = action.get("action_type", "")
    parameters = action.get("parameters", {})
    requested_by = action.get("requested_by", "system")
    risk_level = action.get("risk_level", "low")
    approval_required = bool(action.get("approval_required", False))
    dry_run = bool(action.get("dry_run", False))
    if approval_required:
        return {"action": {**action, "status": "approval_required"}}
    status = "completed" if not dry_run else "dry_run"
    result_text = f"mock {action_type}" if not dry_run else "dry_run"
    record = {
        "action_id": action_id,
        "session_id": session_id,
        "application_id": application_id,
        "action_type": action_type,
        "parameters": parameters,
        "requested_by": requested_by,
        "risk_level": risk_level,
        "approval_required": approval_required,
        "status": status,
        "result": result_text,
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }
    _actions.append(record)
    return {"action": record}


@router.get("/actions/{action_id}")
async def get_action(action_id: str) -> dict:
    for action in _actions:
        if action.get("action_id") == action_id:
            return {"action": action}
    raise HTTPException(status_code=404, detail="Action not found")


@router.post("/actions/{action_id}/approve")
async def approve_action(action_id: str) -> dict:
    for action in _actions:
        if action.get("action_id") == action_id:
            action["status"] = "approved"
            return {"action": action}
    raise HTTPException(status_code=404, detail="Action not found")


@router.post("/actions/{action_id}/cancel")
async def cancel_action(action_id: str) -> dict:
    for action in _actions:
        if action.get("action_id") == action_id:
            action["status"] = "cancelled"
            return {"action": action}
    raise HTTPException(status_code=404, detail="Action not found")


@router.get("/sessions/{session_id}/state")
async def get_session_state(session_id: str) -> dict:
    return {"session_id": session_id, "status": "active", "actions": [a for a in _actions if a.get("session_id") == session_id]}
