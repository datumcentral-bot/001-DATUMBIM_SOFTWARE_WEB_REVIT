from __future__ import annotations

from typing import Any

from ai_planner.models import GoalRequest, PlanningContext


def build_context(goal: GoalRequest, available_capabilities: list[str] | None = None) -> PlanningContext:
    base = goal.context or PlanningContext()
    if available_capabilities is not None:
        base.available_capabilities = available_capabilities
    return base
