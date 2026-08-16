from __future__ import annotations

from ai_planner.models import ActionPlan, ValidationResult
from ai_planner.exceptions import ValidationError


class PlanValidator:
    def validate(self, plan: ActionPlan) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
        if not plan.actions:
            errors.append("Plan has no actions")
        for action in plan.actions:
            if not action.action_type:
                errors.append(f"Action {action.action_id} missing action_type")
            if not action.verification_strategy:
                warnings.append(f"Action {action.action_id} has no verification strategy")
        valid = len(errors) == 0
        return ValidationResult(valid=valid, errors=errors, warnings=warnings, normalized_plan=plan if valid else None)
