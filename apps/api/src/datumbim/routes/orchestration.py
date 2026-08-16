from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/orchestration", tags=["orchestration"])

_loops: dict[str, dict] = {}


@router.post("/loop")
async def run_orchestration_loop(request: dict) -> dict:
    session_id = request.get("session_id")
    user_request = request.get("user_request")
    max_steps = request.get("max_steps", 10)
    if not session_id or not user_request:
        raise HTTPException(status_code=400, detail="session_id and user_request are required")
    try:
        from desktop_agent.orchestration.loop import OrchestrationLoop
        loop = OrchestrationLoop()
        result = loop.run(session_id=session_id, user_request=user_request, max_steps=max_steps)
        _loops[result["loop_id"]] = result
        return result
    except ImportError:
        return {
            "loop_id": str(__import__("uuid").uuid4()),
            "session_id": session_id,
            "user_request": user_request,
            "status": "not_implemented",
            "message": "Orchestration loop requires desktop-agent package",
            "steps": [],
            "started_at": datetime.now(tz=UTC).isoformat(),
            "completed_at": datetime.now(tz=UTC).isoformat(),
        }


@router.get("/loops")
async def list_orchestration_loops() -> dict:
    return {"loops": list(_loops.values())}


@router.get("/loops/{loop_id}")
async def get_orchestration_loop(loop_id: str) -> dict:
    loop = _loops.get(loop_id)
    if not loop:
        raise HTTPException(status_code=404, detail="Loop not found")
    return loop
