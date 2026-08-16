from desktop_agent.agent import DesktopAgent
from desktop_agent.models import CommandRequest
from desktop_agent.permissions import RiskLevel


def test_desktop_agent_registration():
    agent = DesktopAgent()
    registration = agent.register()
    assert registration.agent_id is not None
    assert registration.status == "paired"
    assert agent.agent_id == registration.agent_id


def test_desktop_agent_pairing():
    agent = DesktopAgent()
    registration = agent.register()
    assert agent.pair(registration.token or "") is True
    assert agent.pair("wrong-token") is False


def test_desktop_agent_heartbeat():
    agent = DesktopAgent()
    agent.register()
    heartbeat = agent.heartbeat()
    assert heartbeat.agent_id == agent.agent_id
    assert heartbeat.status == "online"


def test_desktop_agent_command_permission():
    agent = DesktopAgent()
    agent.register()
    agent.permissions.register("read", risk_level=RiskLevel.low, approval_required=False)
    request = CommandRequest(command_id="cmd-1", action="read", parameters={})
    result = agent.execute_command(request)
    assert result.status in ("pending", "denied")


def test_desktop_agent_command_unknown_action():
    agent = DesktopAgent()
    agent.register()
    request = CommandRequest(command_id="cmd-2", action="unknown", parameters={})
    result = agent.execute_command(request)
    assert result.status == "denied"


def test_desktop_agent_audit_logging():
    agent = DesktopAgent()
    agent.register()
    request = CommandRequest(command_id="cmd-3", action="read", parameters={})
    agent.execute_command(request)
    logs = agent.get_audit_logs()
    assert len(logs) == 1
    assert logs[0].action == "read"
