import pytest
from datetime import UTC, datetime

from desktop_agent.control.adapters.mock import MockControlAdapter
from desktop_agent.control.engine import ControlEngine
from desktop_agent.control.models import ActionPlan, ActionRequest, ActionResult
from desktop_agent.permissions import PermissionEngine, RiskLevel


@pytest.fixture()
def mock_adapter() -> MockControlAdapter:
    return MockControlAdapter()


@pytest.fixture()
def engine(mock_adapter: MockControlAdapter) -> ControlEngine:
    return ControlEngine(adapter=mock_adapter)


@pytest.fixture()
def base_request() -> ActionRequest:
    return ActionRequest(
        action_id="action-1",
        session_id="session-1",
        application_id="app-1",
        action_type="mouse_click",
        parameters={"x": 10, "y": 20},
        requested_by="tester",
        risk_level="low",
        approval_required=False,
        timestamp=datetime.now(tz=UTC),
        timeout=10,
        dry_run=False,
    )


def test_valid_mouse_click(engine: ControlEngine, base_request: ActionRequest) -> None:
    result = engine.execute(base_request)
    assert result.status == "completed"
    assert result.error is None
    assert result.completed_at is not None


def test_dry_run_returns_simulated_result(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.dry_run = True
    result = engine.execute(base_request)
    assert result.status == "completed"
    assert result.result == "dry_run"


def test_invalid_action_returns_failed(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.action_type = "unsupported_action"
    result = engine.execute(base_request)
    assert result.status == "failed"
    assert "Unsupported action type" in (result.error or "")


def test_keyboard_type_action(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.action_type = "keyboard_type"
    base_request.parameters = {"text": "hello"}
    result = engine.execute(base_request)
    assert result.status == "completed"


def test_hotkey_action(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.action_type = "keyboard_hotkey"
    base_request.parameters = {"keys": ["ctrl", "s"]}
    result = engine.execute(base_request)
    assert result.status == "completed"


def test_window_activate_action(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.action_type = "window_activate"
    base_request.parameters = {"window_id": "win-1"}
    result = engine.execute(base_request)
    assert result.status == "completed"


def test_window_resize_action(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.action_type = "window_resize"
    base_request.parameters = {"window_id": "win-1", "width": 1024, "height": 768}
    result = engine.execute(base_request)
    assert result.status == "completed"


def test_application_launch_action(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.action_type = "application_launch"
    base_request.parameters = {"application_id": "app-1"}
    result = engine.execute(base_request)
    assert result.status == "completed"


def test_action_plan_executes_all(engine: ControlEngine, base_request: ActionRequest) -> None:
    plan = ActionPlan(plan_id="plan-1", goal="demo", session_id="session-1", actions=[base_request, base_request], approval_required=False, risk_level="low")
    results = engine.execute_plan(plan)
    assert len(results) == 2
    assert all(result.status == "completed" for result in results)


def test_mock_adapter_records_actions(base_request: ActionRequest) -> None:
    adapter = MockControlAdapter()
    result = adapter.click(10, 20, button="left")
    assert result.status == "completed"
    assert len(adapter.actions) == 1


def test_mock_adapter_records_application_action(base_request: ActionRequest) -> None:
    adapter = MockControlAdapter()
    result = adapter.launch_application("app-1")
    assert result.status == "completed"
    assert len(adapter.actions) == 1


def test_risk_classification_low_allows_execution(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.risk_level = RiskLevel.low.value
    result = engine.execute(base_request)
    assert result.status == "completed"


def test_risk_classification_medium_may_require_approval(engine: ControlEngine, base_request: ActionRequest) -> None:
    base_request.risk_level = RiskLevel.medium.value
    base_request.approval_required = True
    result = engine.execute(base_request)
    assert result.status == "completed"


def test_duration_is_set(engine: ControlEngine, base_request: ActionRequest) -> None:
    result = engine.execute(base_request)
    assert result.duration is not None
    assert result.duration >= 0


def test_started_and_completed_at_are_set(engine: ControlEngine, base_request: ActionRequest) -> None:
    started = datetime.now(tz=UTC)
    result = engine.execute(base_request)
    assert result.started_at >= started
    assert result.completed_at >= result.started_at
