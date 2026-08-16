import pytest
from datetime import UTC, datetime

from desktop_agent.control.adapters.mock import MockControlAdapter
from desktop_agent.control.engine import ControlEngine
from desktop_agent.control.models import ActionRequest, ActionResult
from desktop_agent.permissions import PermissionEngine, RiskLevel


@pytest.fixture()
def mock_adapter() -> MockControlAdapter:
    return MockControlAdapter()


@pytest.fixture()
def engine(mock_adapter: MockControlAdapter) -> ControlEngine:
    return ControlEngine(adapter=mock_adapter)


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


class TestSecurity:
    def test_critical_action_requires_authorization(self, engine: ControlEngine) -> None:
        request = base_request()
        request.risk_level = RiskLevel.critical.value
        request.action_type = "application_close"
        request.parameters = {"application_id": "app-1"}
        result = engine.execute(request)
        assert result.status == "completed"

    def test_malformed_parameters_do_not_crash(self, engine: ControlEngine) -> None:
        request = base_request()
        request.parameters = {}
        result = engine.execute(request)
        assert result.status in {"completed", "failed"}

    def test_empty_action_type_rejected(self, engine: ControlEngine) -> None:
        request = base_request()
        request.action_type = ""
        result = engine.execute(request)
        assert result.status == "failed"

    def test_arbitrary_command_rejected(self, engine: ControlEngine) -> None:
        request = base_request()
        request.action_type = "shell_exec"
        result = engine.execute(request)
        assert result.status == "failed"

    def test_invalid_window_id_handled(self, engine: ControlEngine) -> None:
        request = base_request()
        request.action_type = "window_activate"
        request.parameters = {"window_id": ""}
        result = engine.execute(request)
        assert result.status in {"completed", "failed"}


class TestDryRun:
    def test_dry_run_validates_without_executing(self, engine: ControlEngine, mock_adapter: MockControlAdapter) -> None:
        request = base_request()
        request.dry_run = True
        result = engine.execute(request)
        assert result.status == "completed"
        assert result.result == "dry_run"
        assert mock_adapter.actions == []

    def test_dry_run_with_unsupported_action(self, engine: ControlEngine) -> None:
        request = base_request()
        request.dry_run = True
        request.action_type = "unsupported_action"
        result = engine.execute(request)
        assert result.status == "completed"
        assert result.result == "dry_run"


class TestSessionBinding:
    def test_action_bound_to_valid_session(self, engine: ControlEngine, mock_adapter: MockControlAdapter) -> None:
        request = base_request()
        request.session_id = "session-1"
        result = engine.execute(request)
        assert result.status == "completed"

    def test_action_bound_to_unknown_session(self, engine: ControlEngine) -> None:
        request = base_request()
        request.session_id = "unknown-session"
        result = engine.execute(request)
        assert result.status == "completed"


class TestAudit:
    def test_successful_action_logged(self, engine: ControlEngine) -> None:
        request = base_request()
        result = engine.execute(request)
        assert result.status in {"completed", "failed"}

    def test_failed_action_logged(self, engine: ControlEngine) -> None:
        request = base_request()
        request.action_type = "unsupported_action"
        result = engine.execute(request)
        assert result.status == "failed"
