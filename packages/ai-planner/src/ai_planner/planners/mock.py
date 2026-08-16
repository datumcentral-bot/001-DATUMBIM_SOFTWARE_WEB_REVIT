from __future__ import annotations

from ai_planner.models import ActionPlan, GoalRequest
from ai_planner.registry import PlannerProvider


class MockPlannerProvider(PlannerProvider):
    provider_id = "mock"
    display_name = "Mock Planner"
    status = "available"

    def plan(self, goal: GoalRequest) -> ActionPlan:
        from ai_planner.decomposer import PlanDecomposer
        decomposer = PlanDecomposer()
        return decomposer.decompose(goal)

    def explain(self, plan: ActionPlan) -> str:
        lines = [f"PLAN: {plan.title}", f"OBJECTIVE: {plan.objective}", "STEPS:"]
        for action in plan.actions:
            lines.append(f"  {action.sequence}. {action.description} ({action.action_type})")
        lines.append(f"RISK: {plan.risk_level.value.upper()}")
        lines.append(f"APPROVAL: {'Required' if plan.approval_required else 'Not required'}")
        return "\n".join(lines)

    def estimate_risk(self, plan: ActionPlan) -> dict:
        return {"level": plan.risk_level.value, "approval_required": plan.approval_required}
