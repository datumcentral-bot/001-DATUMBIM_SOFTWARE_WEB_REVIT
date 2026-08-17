from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

from desktop_agent.execution.service import ExecutionService
from desktop_agent.execution.models import WorkflowDefinition

router = APIRouter(prefix="/workflows", tags=["workflows"])

_service = ExecutionService()


@router.get("/")
async def list_workflows() -> dict:
    workflows = _service.list_workflows()
    return {"workflows": [w.model_dump(mode="json") for w in workflows]}


@router.post("/")
async def create_workflow(workflow: WorkflowDefinition) -> dict:
    _service.register_workflow(workflow)
    return {"workflow": workflow.model_dump(mode="json")}


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str) -> dict:
    workflow = _service.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow": workflow.model_dump(mode="json")}


@router.post("/{workflow_id}/run")
async def run_workflow(workflow_id: str, request: Optional[dict] = None) -> dict:
    workflow = _service.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    execution = _service.run_workflow(workflow_id, inputs=request.get("inputs") if request else None, dry_run=request.get("dry_run", False) if request else False)
    return execution.model_dump(mode="json")


@router.post("/{workflow_id}/cancel")
async def cancel_workflow(workflow_id: str) -> dict:
    return {"workflow_id": workflow_id, "status": "cancelled"}
