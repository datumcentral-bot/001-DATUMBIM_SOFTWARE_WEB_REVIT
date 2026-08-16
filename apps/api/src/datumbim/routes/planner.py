from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/planner", tags=["planner"])

_plans: dict[str, dict] = {}


@router.get("/providers")
async def list_planner_providers() -> dict:
    return {"providers": [{"provider_id": "mock", "display_name": "Mock Planner", "status": "available"}]}


@router.get("/health")
async def planner_health() -> dict:
    return {"providers": {"mock": {"status": "available"}}}


@router.post("/plan")
async def create_plan(request: dict) -> dict:
    user_request = request.get("user_request")
    application_id = request.get("application_id")
    session_id = request.get("session_id")
    dry_run = request.get("dry_run", False)
    if not user_request:
        raise HTTPException(status_code=400, detail="user_request is required")
    plan_id = str(__import__("uuid").uuid4())
    plan = {
        "plan_id": plan_id,
        "goal_id": str(__import__("uuid").uuid4()),
        "title": f"Plan: {user_request}",
        "objective": user_request,
        "summary": user_request,
        "application_id": application_id,
        "session_id": session_id,
        "actions": [
            {
                "action_id": str(__import__("uuid").uuid4()),
                "sequence": 1,
                "action_type": "detect_application",
                "description": f"Detect {application_id or 'target application'}",
                "application_id": application_id,
                "session_id": session_id,
                "parameters": {},
                "preconditions": [],
                "expected_result": "Application detected",
                "verification_strategy": "application_state_changed",
                "risk_level": "low",
                "approval_required": False,
                "reversible": True,
                "estimated_duration": 5.0,
                "dependencies": [],
                "confidence": 0.9,
                "source": "mock",
                "status": "proposed",
            },
            {
                "action_id": str(__import__("uuid").uuid4()),
                "sequence": 2,
                "action_type": "activate_application",
                "description": f"Activate {application_id or 'target application'}",
                "application_id": application_id,
                "session_id": session_id,
                "parameters": {},
                "preconditions": [],
                "expected_result": "Application activated",
                "verification_strategy": "window_changed",
                "risk_level": "low",
                "approval_required": False,
                "reversible": True,
                "estimated_duration": 3.0,
                "dependencies": [],
                "confidence": 0.85,
                "source": "mock",
                "status": "proposed",
            },
        ],
        "dependencies": {},
        "risk_level": "low",
        "approval_required": False,
        "estimated_duration": 8.0,
        "confidence": 0.9,
        "expected_observations": ["Application detected", "Application activated"],
        "success_criteria": ["Application is active"],
        "rollback_strategy": None,
        "planner_provider": "mock",
        "planner_model": "mock-planner",
        "created_at": datetime.now(tz=UTC).isoformat(),
        "status": "ready",
    }
    _plans[plan_id] = plan
    return {"plan": plan}


@router.get("/plans")
async def list_plans() -> dict:
    return {"plans": list(_plans.values())}


@router.get("/plans/{plan_id}")
async def get_plan(plan_id: str) -> dict:
    plan = _plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"plan": plan}


@router.post("/plans/{plan_id}/validate")
async def validate_plan(plan_id: str) -> dict:
    plan = _plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"validation": {"valid": True, "errors": [], "warnings": []}}


@router.post("/plans/{plan_id}/approve")
async def approve_plan(plan_id: str) -> dict:
    plan = _plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan["status"] = "approved"
    return {"plan": plan}


@router.post("/plans/{plan_id}/reject")
async def reject_plan(plan_id: str) -> dict:
    plan = _plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan["status"] = "rejected"
    return {"plan": plan}


@router.post("/plans/{plan_id}/cancel")
async def cancel_plan(plan_id: str) -> dict:
    plan = _plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan["status"] = "cancelled"
    return {"plan": plan}


@router.get("/plans/{plan_id}/explain")
async def explain_plan(plan_id: str) -> dict:
    plan = _plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    lines = [f"PLAN: {plan['title']}", f"OBJECTIVE: {plan['objective']}", "STEPS:"]
    for action in plan.get("actions", []):
        lines.append(f"  {action['sequence']}. {action['description']} ({action['action_type']})")
    lines.append(f"RISK: {plan['risk_level'].upper()}")
    lines.append(f"APPROVAL: {'Required' if plan['approval_required'] else 'Not required'}")
    return {"explanation": "\n".join(lines)}
