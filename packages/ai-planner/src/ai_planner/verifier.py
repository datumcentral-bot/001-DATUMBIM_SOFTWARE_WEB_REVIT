from __future__ import annotations

from ai_planner.models import ActionPlan, ActionProposal, VerificationStrategyType
from ai_planner.exceptions import VerificationError


class VerificationStrategy:
    @staticmethod
    def validate(action: ActionProposal) -> bool:
        if action.verification_strategy is None:
            return False
        valid = True
        if action.verification_strategy == VerificationStrategyType.text_detected:
            if not action.verification_parameters.get("text"):
                valid = False
        elif action.verification_strategy == VerificationStrategyType.element_detected:
            if not action.verification_parameters.get("element_id"):
                valid = False
        elif action.verification_strategy == VerificationStrategyType.file_created:
            if not action.verification_parameters.get("path"):
                valid = False
        return valid
