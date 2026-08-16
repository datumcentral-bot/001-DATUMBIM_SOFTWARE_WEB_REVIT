from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from ai_planner.models import ActionPlan, ActionProposal, GoalRequest, PlanStatus, PlanningContext
from ai_planner.registry import PlannerProvider


class PlanDecomposer:
    def decompose(self, goal: GoalRequest, available_capabilities: list[str] | None = None) -> ActionPlan:
        context = goal.context or PlanningContext()
        if available_capabilities is not None:
            context.available_capabilities = available_capabilities
        plan_id = str(uuid.uuid4())
        actions = self._build_actions(goal, context)
        return ActionPlan(
            plan_id=plan_id,
            goal_id=goal.goal_id,
            title=f"Plan: {goal.user_request}",
            objective=goal.user_request,
            summary=goal.user_request,
            application_id=goal.application_id,
            session_id=goal.session_id,
            context=context,
            actions=actions,
            dependencies={},
            risk_level=actions[0].risk_level if actions else "low",
            approval_required=any(action.approval_required for action in actions),
            confidence=actions[0].confidence if actions else None,
            planner_provider="mock",
            created_at=datetime.now(tz=UTC),
            status=PlanStatus.draft,
        )

    def _build_actions(self, goal: GoalRequest, context: PlanningContext) -> list[ActionProposal]:
        return [
            ActionProposal(
                action_id=str(uuid.uuid4()),
                sequence=1,
                action_type="detect_application",
                description=f"Detect {goal.application_id or 'target application'}",
                application_id=goal.application_id,
                session_id=goal.session_id,
                preconditions=[],
                expected_result="Application detected",
                verification_strategy="application_state_changed",
                risk_level="low",
                approval_required=False,
                reversible=True,
                estimated_duration=5.0,
                dependencies=[],
                confidence=0.9,
                source="mock",
            ),
            ActionProposal(
                action_id=str(uuid.uuid4()),
                sequence=2,
                action_type="activate_application",
                description=f"Activate {goal.application_id or 'target application'}",
                application_id=goal.application_id,
                session_id=goal.session_id,
                preconditions=[],
                expected_result="Application activated",
                verification_strategy="window_changed",
                risk_level="low",
                approval_required=False,
                reversible=True,
                estimated_duration=3.0,
                dependencies=[],
                confidence=0.85,
                source="mock",
            ),
            ActionProposal(
                action_id=str(uuid.uuid4()),
                sequence=3,
                action_type="verify_session",
                description="Verify active session",
                application_id=goal.application_id,
                session_id=goal.session_id,
                preconditions=[],
                expected_result="Session verified",
                verification_strategy="observation_match",
                risk_level="low",
                approval_required=False,
                reversible=True,
                estimated_duration=2.0,
                dependencies=[],
                confidence=0.8,
                source="mock",
            ),
        ]
