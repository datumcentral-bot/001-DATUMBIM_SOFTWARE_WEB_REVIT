from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from desktop_agent.control.adapters.mock import MockControlAdapter
from desktop_agent.control.engine import ControlEngine
from desktop_agent.control.models import ActionPlan, ActionRequest, ActionResult
from desktop_agent.observation.engine import ObservationEngine
from desktop_agent.observation.models import CaptureMode, ObservationRequest, ObservationResult
from desktop_agent.observation.providers.mock import MockObservationProvider
from desktop_agent.session_manager import SessionManager


class OrchestrationStep:
    def __init__(self, step_id: str, step_type: str, status: str = "pending") -> None:
        self.step_id = step_id
        self.step_type = step_type
        self.status = status
        self.started_at: datetime | None = None
        self.completed_at: datetime | None = None
        self.result: Any = None
        self.error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "step_type": self.step_type,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
        }


class OrchestrationLoop:
    def __init__(
        self,
        session_manager: SessionManager | None = None,
        observation_engine: ObservationEngine | None = None,
        control_engine: ControlEngine | None = None,
    ) -> None:
        self.session_manager = session_manager or SessionManager()
        self.observation_engine = observation_engine or ObservationEngine(provider=MockObservationProvider())
        self.control_engine = control_engine or ControlEngine(session_manager=self.session_manager, adapter=MockControlAdapter())

    def run(self, session_id: str, user_request: str, max_steps: int = 10) -> dict[str, Any]:
        loop_id = str(uuid.uuid4())
        steps: list[OrchestrationStep] = []
        started_at = datetime.now(tz=UTC)
        try:
            observe_step = self._observe(session_id, loop_id)
            steps.append(observe_step)
            if observe_step.status != "completed":
                return self._result(loop_id, session_id, user_request, steps, started_at, "failed", "Observation failed")
            understand_step = self._understand(session_id, loop_id, observe_step.result)
            steps.append(understand_step)
            plan = self._plan(session_id, user_request, understand_step.result)
            plan_step = OrchestrationStep(step_id=f"{loop_id}-plan", step_type="plan", status="completed")
            plan_step.result = plan
            plan_step.completed_at = datetime.now(tz=UTC)
            steps.append(plan_step)
            if plan.get("approval_required"):
                approval_step = OrchestrationStep(step_id=f"{loop_id}-approval", step_type="approval", status="pending_approval")
                approval_step.started_at = datetime.now(tz=UTC)
                steps.append(approval_step)
                return self._result(loop_id, session_id, user_request, steps, started_at, "pending_approval", "Approval required")
            action_results = self._act(session_id, plan.get("actions", []))
            for i, result in enumerate(action_results):
                action_step = OrchestrationStep(step_id=f"{loop_id}-action-{i}", step_type="act", status=result.status)
                action_step.result = result.result
                action_step.error = result.error
                action_step.completed_at = datetime.now(tz=UTC)
                steps.append(action_step)
                if result.status == "failed":
                    return self._result(loop_id, session_id, user_request, steps, started_at, "failed", f"Action failed: {result.error}")
            verify_step = self._verify(session_id, plan.get("actions", []), action_results)
            steps.append(verify_step)
            final_status = "completed" if verify_step.status == "completed" else "failed"
            return self._result(loop_id, session_id, user_request, steps, started_at, final_status, verify_step.error or "Loop completed")
        except Exception as exc:
            error_step = OrchestrationStep(step_id=f"{loop_id}-error", step_type="error", status="failed")
            error_step.error = str(exc)
            error_step.completed_at = datetime.now(tz=UTC)
            steps.append(error_step)
            return self._result(loop_id, session_id, user_request, steps, started_at, "failed", str(exc))

    def _observe(self, session_id: str, loop_id: str) -> OrchestrationStep:
        step = OrchestrationStep(step_id=f"{loop_id}-observe", step_type="observe")
        step.started_at = datetime.now(tz=UTC)
        try:
            request = ObservationRequest(
                observation_id=f"{loop_id}-observe",
                session_id=session_id,
                application_id="revit",
                target_type=CaptureMode.FULL_SCREEN,
                timestamp=datetime.now(tz=UTC),
            )
            result = self.observation_engine.capture(request)
            step.status = result.status.value if hasattr(result.status, "value") else str(result.status)
            step.result = result.model_dump()
            step.completed_at = datetime.now(tz=UTC)
        except Exception as exc:
            step.status = "failed"
            step.error = str(exc)
            step.completed_at = datetime.now(tz=UTC)
        return step

    def _understand(self, session_id: str, loop_id: str, observation: dict[str, Any]) -> OrchestrationStep:
        step = OrchestrationStep(step_id=f"{loop_id}-understand", step_type="understand")
        step.started_at = datetime.now(tz=UTC)
        step.status = "completed"
        step.result = {"screen_description": "Application observed", "elements": []}
        step.completed_at = datetime.now(tz=UTC)
        return step

    def _plan(self, session_id: str, user_request: str, understanding: dict[str, Any]) -> dict[str, Any]:
        return {
            "plan_id": str(uuid.uuid4()),
            "goal": user_request,
            "session_id": session_id,
            "actions": [
                {
                    "action_id": str(uuid.uuid4()),
                    "action_type": "mouse_click",
                    "parameters": {"x": 100, "y": 100, "button": "left"},
                    "risk_level": "low",
                    "approval_required": False,
                }
            ],
            "risk_level": "low",
            "approval_required": False,
            "status": "ready",
        }

    def _act(self, session_id: str, actions: list[dict[str, Any]]) -> list[ActionResult]:
        results: list[ActionResult] = []
        for action in actions:
            request = ActionRequest(
                action_id=action.get("action_id", str(uuid.uuid4())),
                session_id=session_id,
                application_id=action.get("application_id", "revit"),
                action_type=action.get("action_type", ""),
                parameters=action.get("parameters", {}),
                risk_level=action.get("risk_level", "low"),
                approval_required=action.get("approval_required", False),
                dry_run=False,
                timestamp=datetime.now(tz=UTC),
            )
            results.append(self.control_engine.execute(request))
        return results

    def _verify(self, session_id: str, actions: list[dict[str, Any]], results: list[ActionResult]) -> OrchestrationStep:
        step = OrchestrationStep(step_id=f"{uuid.uuid4()}-verify", step_type="verify")
        step.started_at = datetime.now(tz=UTC)
        all_success = all(r.status == "completed" for r in results)
        step.status = "completed" if all_success else "failed"
        step.result = {"all_actions_succeeded": all_success, "results_count": len(results)}
        step.completed_at = datetime.now(tz=UTC)
        return step

    def _result(self, loop_id: str, session_id: str, user_request: str, steps: list[OrchestrationStep], started_at: datetime, status: str, message: str) -> dict[str, Any]:
        return {
            "loop_id": loop_id,
            "session_id": session_id,
            "user_request": user_request,
            "status": status,
            "message": message,
            "steps": [step.to_dict() for step in steps],
            "started_at": started_at.isoformat(),
            "completed_at": datetime.now(tz=UTC).isoformat(),
        }
