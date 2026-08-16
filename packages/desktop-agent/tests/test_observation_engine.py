from desktop_agent.observation_engine import ObservationEngine
from desktop_agent.observation_models import ScreenObservationRequest
from desktop_agent.session_manager import SessionManager


def test_observation_engine_capture_screen():
    manager = SessionManager()
    engine = ObservationEngine(session_manager=manager)
    session = manager.start_session("revit")
    request = ScreenObservationRequest(session_id=session.session_id)
    capture = engine.observe_screen(request)
    assert capture.session_id == session.session_id
    assert capture.application_id == "revit"
    assert capture.format == "png"


def test_observation_engine_observe_window():
    manager = SessionManager()
    engine = ObservationEngine(session_manager=manager)
    session = manager.start_session("revit")
    entry = engine.observe_window(session.session_id)
    assert entry is not None
    assert entry.session_id == session.session_id
    assert entry.kind == "window"


def test_observation_engine_observe_window_missing_session():
    manager = SessionManager()
    engine = ObservationEngine(session_manager=manager)
    entry = engine.observe_window("missing")
    assert entry is None


def test_observation_engine_state():
    manager = SessionManager()
    engine = ObservationEngine(session_manager=manager)
    session = manager.start_session("revit")
    request = ScreenObservationRequest(session_id=session.session_id)
    engine.observe_screen(request)
    state = engine.get_state(session.session_id)
    assert state is not None
    assert state.captures_count == 1
    assert state.status == "captured"


def test_observation_engine_get_captures():
    manager = SessionManager()
    engine = ObservationEngine(session_manager=manager)
    session = manager.start_session("revit")
    request = ScreenObservationRequest(session_id=session.session_id)
    engine.observe_screen(request)
    engine.observe_screen(request)
    captures = engine.get_captures(session.session_id)
    assert len(captures) == 2


def test_observation_engine_clear():
    manager = SessionManager()
    engine = ObservationEngine(session_manager=manager)
    session = manager.start_session("revit")
    request = ScreenObservationRequest(session_id=session.session_id)
    engine.observe_screen(request)
    engine.clear(session.session_id)
    assert engine.get_captures(session.session_id) == []
    assert engine.get_state(session.session_id) is None
