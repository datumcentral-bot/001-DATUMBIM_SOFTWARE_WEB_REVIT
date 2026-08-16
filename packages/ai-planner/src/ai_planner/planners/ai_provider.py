from __future__ import annotations

from typing import Any

from ai_planner.models import ActionPlan, GoalRequest
from ai_planner.registry import PlannerProvider


class AIPlannerProvider(PlannerProvider):
    provider_id = "openai_compatible"
    display_name = "OpenAI Compatible Planner"
    status = "not_configured"

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = base_url or ""
        self.api_key = api_key or ""
        if self.base_url and self.api_key:
            self.status = "auth_required"
        else:
            self.status = "not_configured"

    def plan(self, goal: GoalRequest) -> ActionPlan:
        raise NotImplementedError("AI planner requires configured provider")

    def explain(self, plan: ActionPlan) -> str:
        return "AI planner not configured"

    def estimate_risk(self, plan: ActionPlan) -> dict:
        return {"level": "low", "approval_required": False}
