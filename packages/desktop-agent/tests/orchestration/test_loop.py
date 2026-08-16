import pytest

from desktop_agent.observation.providers.mock import MockObservationProvider
from desktop_agent.observation.storage import ObservationStore
from desktop_agent.control.adapters.mock import MockControlAdapter
from desktop_agent.orchestration.loop import OrchestrationLoop, OrchestrationStep


def test_orchestration_loop_runs():
    loop = OrchestrationLoop()
    result = loop.run(session_id="test-session", user_request="test request", max_steps=5)
    assert result["session_id"] == "test-session"
    assert result["user_request"] == "test request"
    assert "loop_id" in result
    assert "steps" in result
    assert len(result["steps"]) > 0
    step_types = [step["step_type"] for step in result["steps"]]
    assert "observe" in step_types
    assert "plan" in step_types
    assert "act" in step_types
    assert "verify" in step_types


def test_orchestration_step_lifecycle():
    step = OrchestrationStep(step_id="step-1", step_type="observe", status="pending")
    assert step.status == "pending"
    step.started_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    step.status = "completed"
    step.completed_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    step.result = {"observation_id": "obs-1"}
    data = step.to_dict()
    assert data["status"] == "completed"
    assert data["result"]["observation_id"] == "obs-1"
    assert data["started_at"] is not None
    assert data["completed_at"] is not None


def test_orchestration_loop_handles_observation_failure():
    from desktop_agent.observation.engine import ObservationEngine
    from desktop_agent.control.engine import ControlEngine
    from desktop_agent.session_manager import SessionManager

    class FailingObservationProvider:
        def capture_screen(self, request):
            raise RuntimeError("capture failed")
        def capture_window(self, request, window_id):
            raise RuntimeError("capture failed")
        def capture_region(self, request, region):
            raise RuntimeError("capture failed")
        def capture_display(self, request, display_id):
            raise RuntimeError("capture failed")
        def capture_application(self, request, application_id):
            raise RuntimeError("capture failed")
        def list_displays(self):
            return []
        def list_windows(self):
            return []

    loop = OrchestrationLoop(
        session_manager=SessionManager(),
        observation_engine=ObservationEngine(provider=FailingObservationProvider()),
        control_engine=ControlEngine(adapter=MockControlAdapter()),
    )
    result = loop.run(session_id="test-session", user_request="test request")
    assert result["status"] == "failed"
    assert "failed" in result["message"].lower()
