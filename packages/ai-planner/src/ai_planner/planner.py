from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from ai_planner.decomposer import PlanDecomposer
from ai_planner.dependencies import DependencyResolver
from ai_planner.models import ActionPlan, GoalRequest, PlanStatus, ValidationResult
from ai_planner.registry import PlannerProvider
from ai_planner.risk import RiskAnalyzer
from ai_planner.validator import PlanValidator
from ai_planner.verifier import VerificationStrategy


class PlannerEngine:
    def __init__(self, provider: PlannerProvider | None = None) -> None:
        self.provider = provider
        self.decomposer = PlanDecomposer()
        self.validator = PlanValidator()
        self.risk_analyzer = RiskAnalyzer()
        self.dependency_resolver = DependencyResolver()

    def plan(self, goal: GoalRequest) -> ActionPlan:
        if self.provider:
            plan = self.provider.plan(goal)
        else:
            plan = self.decomposer.decompose(goal)
        validation = self.validator.validate(plan)
        if not validation.valid:
            raise ValueError(f"Invalid plan: {validation.errors}")
        plan = self.dependency_resolver.resolve(plan)
        risk = self.risk_analyzer.analyze(plan)
        plan.risk_level = risk.level
        plan.approval_required = risk.approval_required
        plan.status = PlanStatus.ready if not risk.approval_required else PlanStatus.awaiting_approval
        return plan
