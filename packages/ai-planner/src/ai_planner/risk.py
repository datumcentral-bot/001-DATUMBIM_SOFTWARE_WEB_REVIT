from __future__ import annotations

from ai_planner.models import ActionPlan, ActionProposal, RiskAssessment, RiskLevel


class RiskAnalyzer:
    def analyze(self, plan: ActionPlan) -> RiskAssessment:
        reasons: list[str] = []
        max_risk = RiskLevel.low
        for action in plan.actions:
            action_risk = action.risk_level
            if action_risk == RiskLevel.critical:
                max_risk = RiskLevel.critical
            elif action_risk == RiskLevel.high and max_risk != RiskLevel.critical:
                max_risk = RiskLevel.high
            elif action_risk == RiskLevel.medium and max_risk == RiskLevel.low:
                max_risk = RiskLevel.medium
            reasons.append(f"{action.action_type}: {action_risk.value}")
        approval_required = max_risk in (RiskLevel.high, RiskLevel.critical)
        reversible = all(action.reversible for action in plan.actions)
        return RiskAssessment(
            level=max_risk,
            reasons=reasons,
            approval_required=approval_required,
            reversible=reversible,
            affected_resources=[plan.application_id] if plan.application_id else [],
            warnings=[],
        )
