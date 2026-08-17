from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

from desktop_agent.execution.service import ExecutionService
from desktop_agent.execution.models import ExecutionMode, ExecutionRequest, ExecutionResult, ExecutionStatus, ToolDefinition

router = APIRouter(prefix="/execution", tags=["execution"])

_service = ExecutionService()


@router.get("/tools")
async def list_tools(capability: Optional[str] = None, provider: Optional[str] = None, integration_id: Optional[str] = None, available_only: bool = True) -> dict:
    tools = _service.list_tools(capability=capability, provider=provider, integration_id=integration_id, available_only=available_only)
    return {"tools": [t.model_dump(mode="json") for t in tools]}


@router.post("/execute")
async def execute_tool(request: ExecutionRequest) -> dict:
    result = _service.execute(request)
    return result.model_dump(mode="json")


@router.get("/{execution_id}")
async def get_execution(execution_id: str) -> dict:
    result = _service.get_execution(execution_id)
    if not result:
        raise HTTPException(status_code=404, detail="Execution not found")
    return result.model_dump(mode="json")


@router.post("/{execution_id}/approve")
async def approve_execution(execution_id: str) -> dict:
    result = _service.get_execution(execution_id)
    if not result:
        raise HTTPException(status_code=404, detail="Execution not found")
    if result.status != ExecutionStatus.WAITING_APPROVAL:
        raise HTTPException(status_code=400, detail="Execution is not waiting for approval")
    return {"execution_id": execution_id, "status": "approved"}


@router.post("/{execution_id}/cancel")
async def cancel_execution(execution_id: str) -> dict:
    result = _service.get_execution(execution_id)
    if not result:
        raise HTTPException(status_code=404, detail="Execution not found")
    if result.status != ExecutionStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Execution is not running")
    result.status = ExecutionStatus.CANCELLED
    return {"execution_id": execution_id, "status": "cancelled"}


@router.post("/{execution_id}/retry")
async def retry_execution(execution_id: str) -> dict:
    result = _service.get_execution(execution_id)
    if not result:
        raise HTTPException(status_code=404, detail="Execution not found")
    if result.status not in (ExecutionStatus.FAILED, ExecutionStatus.TIMEOUT, ExecutionStatus.VERIFICATION_FAILED):
        raise HTTPException(status_code=400, detail="Execution is not retryable")
    return {"execution_id": execution_id, "status": "queued"}
