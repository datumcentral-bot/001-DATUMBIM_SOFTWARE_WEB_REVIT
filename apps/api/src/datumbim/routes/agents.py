from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

from desktop_agent.agent_runtime.service import AgentService
from desktop_agent.agent_runtime.models import AgentDefinition, AgentRun

router = APIRouter(prefix="/agents", tags=["agents"])

_service = AgentService()


@router.get("/")
async def list_agents(enabled_only: bool = True) -> dict:
    agents = _service.list_agents(enabled_only=enabled_only)
    return {"agents": [a.model_dump(mode="json") for a in agents]}


@router.post("/")
async def create_agent(agent: AgentDefinition) -> dict:
    _service.register_agent(agent)
    return {"agent": agent.model_dump(mode="json")}


@router.get("/{agent_id}")
async def get_agent(agent_id: str) -> dict:
    agent = _service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": agent.model_dump(mode="json")}


@router.post("/{agent_id}/run")
async def run_agent(agent_id: str, request: Optional[dict] = None) -> dict:
    agent = _service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    goal = request.get("goal") if request else None
    if not goal:
        raise HTTPException(status_code=400, detail="goal is required")
    run = _service.create_run(
        agent_id=agent_id,
        goal=goal,
        session_id=request.get("session_id") if request else None,
        application_id=request.get("application_id") if request else None,
        dry_run=request.get("dry_run", False) if request else False,
    )
    if not run:
        raise HTTPException(status_code=400, detail="Agent not available")
    started = _service.start_run(run.run_id)
    return started.model_dump(mode="json") if started else run.model_dump(mode="json")


@router.get("/runs")
async def list_runs() -> dict:
    return {"runs": []}


@router.get("/runs/{run_id}")
async def get_run(run_id: str) -> dict:
    run = _service.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run.model_dump(mode="json")


@router.post("/runs/{run_id}/approve")
async def approve_run(run_id: str, request: Optional[dict] = None) -> dict:
    step_id = request.get("step_id") if request else None
    if not step_id:
        raise HTTPException(status_code=400, detail="step_id is required")
    run = _service.approve_step(run_id=run_id, step_id=step_id, approved=True)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "status": run.status.value}


@router.post("/runs/{run_id}/reject")
async def reject_run(run_id: str, request: Optional[dict] = None) -> dict:
    step_id = request.get("step_id") if request else None
    if not step_id:
        raise HTTPException(status_code=400, detail="step_id is required")
    run = _service.approve_step(run_id=run_id, step_id=step_id, approved=False)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "status": run.status.value}


@router.post("/runs/{run_id}/cancel")
async def cancel_run(run_id: str) -> dict:
    run = _service.cancel_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "status": run.status.value}


@router.post("/runs/{run_id}/retry")
async def retry_run(run_id: str) -> dict:
    run = _service.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "status": "queued"}
