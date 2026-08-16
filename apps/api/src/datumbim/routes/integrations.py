from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/integrations", tags=["integrations"])

_integrations: dict[str, dict] = {}
_tools: dict[str, dict] = {}
_workflows: dict[str, dict] = {}


@router.get("/")
async def list_integrations(integration_type: Optional[str] = None, status: Optional[str] = None) -> dict:
    integrations = list(_integrations.values())
    if integration_type:
        integrations = [i for i in integrations if i.get("integration_type") == integration_type]
    if status:
        integrations = [i for i in integrations if i.get("status") == status]
    return {"integrations": integrations}


@router.get("/{integration_id}")
async def get_integration(integration_id: str) -> dict:
    integration = _integrations.get(integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    return {"integration": integration}


@router.post("/{integration_id}/connect")
async def connect_integration(integration_id: str) -> dict:
    integration = _integrations.get(integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    integration["status"] = "connected"
    integration["updated_at"] = datetime.now(tz=UTC).isoformat()
    return {"integration": integration}


@router.post("/{integration_id}/disconnect")
async def disconnect_integration(integration_id: str) -> dict:
    integration = _integrations.get(integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    integration["status"] = "disconnected"
    integration["updated_at"] = datetime.now(tz=UTC).isoformat()
    return {"integration": integration}


@router.get("/{integration_id}/health")
async def integration_health(integration_id: str) -> dict:
    integration = _integrations.get(integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    return {"health": {"integration_id": integration_id, "status": integration.get("status", "unknown"), "last_check": datetime.now(tz=UTC).isoformat()}}


@router.post("/{integration_id}/execute")
async def execute_integration_action(integration_id: str, request: dict) -> dict:
    integration = _integrations.get(integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    capability_id = request.get("capability_id")
    parameters = request.get("parameters", {})
    result = {
        "request_id": str(__import__("uuid").uuid4()),
        "status": "completed",
        "result": {"message": f"Executed {capability_id} on {integration_id}", "parameters": parameters},
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }
    return result


@router.get("/tools")
async def list_tools(capability: Optional[str] = None, provider: Optional[str] = None) -> dict:
    tools = list(_tools.values())
    if capability:
        tools = [t for t in tools if capability in t.get("capabilities", [])]
    if provider:
        tools = [t for t in tools if t.get("provider") == provider]
    return {"tools": tools}


@router.post("/tools/register")
async def register_tool(tool: dict) -> dict:
    tool_id = tool.get("tool_id")
    if not tool_id:
        raise HTTPException(status_code=400, detail="tool_id is required")
    _tools[tool_id] = tool
    return {"tool": tool}


@router.get("/workflows")
async def list_workflows() -> dict:
    return {"workflows": list(_workflows.values())}


@router.post("/workflows")
async def create_workflow(workflow: dict) -> dict:
    workflow_id = workflow.get("workflow_id")
    if not workflow_id:
        raise HTTPException(status_code=400, detail="workflow_id is required")
    _workflows[workflow_id] = workflow
    return {"workflow": workflow}


@router.post("/webhooks/register")
async def register_webhook(webhook: dict) -> dict:
    webhook_id = webhook.get("webhook_id")
    if not webhook_id:
        raise HTTPException(status_code=400, detail="webhook_id is required")
    integration_id = webhook.get("integration_id")
    integration = _integrations.get(integration_id)
    if integration:
        integration.setdefault("webhooks", []).append(webhook)
    return {"webhook": webhook}
