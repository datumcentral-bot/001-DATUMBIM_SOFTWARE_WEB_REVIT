from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from ai_planner.models import ActionPlan, GoalRequest

if TYPE_CHECKING:
    from ai_planner.models import ActionProposal


class PlannerProvider(abc.ABC):
    provider_id: str
    display_name: str
    status: str = "not_configured"

    @abc.abstractmethod
    def plan(self, goal: GoalRequest) -> ActionPlan:
        raise NotImplementedError

    @abc.abstractmethod
    def explain(self, plan: ActionPlan) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def estimate_risk(self, plan: ActionPlan) -> dict:
        raise NotImplementedError
