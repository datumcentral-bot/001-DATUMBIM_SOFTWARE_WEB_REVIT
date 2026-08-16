from desktop_agent.agent import DesktopAgent
from desktop_agent.session_manager import SessionManager


def test_session_manager_start_session():
    manager = SessionManager()
    session = manager.start_session("revit")
    assert session.application_id == "revit"
    assert session.status == "active"
    assert session.session_id.startswith("revit-")


def test_session_manager_attach_session_without_running_app():
    manager = SessionManager()
    session = manager.attach_session("revit")
    assert session is None


def test_session_manager_close_session():
    manager = SessionManager()
    session = manager.start_session("revit")
    result = manager.close_session(session.session_id)
    assert result is True
    assert manager.get_session(session.session_id) is None


def test_session_manager_close_missing_session():
    manager = SessionManager()
    result = manager.close_session("missing")
    assert result is False


def test_session_manager_get_sessions():
    manager = SessionManager()
    session1 = manager.start_session("revit")
    session2 = manager.start_session("autocad")
    sessions = manager.get_sessions()
    assert len(sessions) == 2
    assert session1 in sessions
    assert session2 in sessions


def test_session_manager_get_sessions_by_application():
    manager = SessionManager()
    manager.start_session("revit")
    manager.start_session("autocad")
    manager.start_session("revit")
    sessions = manager.get_sessions_by_application("revit")
    assert len(sessions) == 2


def test_session_manager_detach_session():
    manager = SessionManager()
    session = manager.start_session("revit")
    result = manager.detach_session(session.session_id)
    assert result is True
    updated = manager.get_session(session.session_id)
    assert updated is not None
    assert updated.status == "detached"


def test_session_manager_restart_session():
    manager = SessionManager()
    session = manager.start_session("revit")
    restarted = manager.restart_session(session.session_id)
    assert restarted is not None
    assert restarted.application_id == "revit"
    assert restarted.status == "active"
    assert manager.get_session(session.session_id) is None


def test_desktop_agent_delegates_to_session_manager():
    agent = DesktopAgent()
    agent.register()
    session = agent.create_session("revit")
    assert session.application_id == "revit"
    assert agent.get_session(session.session_id) is not None
    assert len(agent.get_sessions()) == 1
