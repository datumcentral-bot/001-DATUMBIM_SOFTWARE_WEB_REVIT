from datetime import UTC, datetime
from typing import Any

from desktop_agent.discovery import ApplicationDiscovery, WindowDiscovery
from desktop_agent.models import ApplicationInfo, SessionInfo, WindowInfo


class SessionManager:
    def __init__(
        self,
        discovery: ApplicationDiscovery | None = None,
        window_discovery: WindowDiscovery | None = None,
    ) -> None:
        self.discovery = discovery or ApplicationDiscovery()
        self.window_discovery = window_discovery or WindowDiscovery()
        self._sessions: dict[str, SessionInfo] = {}

    def discover_applications(self) -> list[ApplicationInfo]:
        return self.discovery.discover()

    def discover_windows(self) -> list[WindowInfo]:
        return self.window_discovery.discover_windows()

    def start_session(self, application_id: str) -> SessionInfo:
        application = self._find_application(application_id)
        window = self._find_window_for_application(application_id)
        session = SessionInfo(
            session_id=f"{application_id}-{datetime.now(tz=UTC).timestamp()}",
            application_id=application_id,
            status="active",
            started_at=datetime.now(tz=UTC),
            process_id=application.process_id if application else None,
            window=window,
            active_document=None,
            active_view=None,
            metadata={},
        )
        self._sessions[session.session_id] = session
        return session

    def attach_session(self, application_id: str) -> SessionInfo | None:
        application = self._find_running_application(application_id)
        if not application:
            return None
        window = self._find_window_for_application(application_id)
        session = SessionInfo(
            session_id=f"{application_id}-{datetime.now(tz=UTC).timestamp()}",
            application_id=application_id,
            status="active",
            started_at=datetime.now(tz=UTC),
            process_id=application.process_id,
            window=window,
            active_document=None,
            active_view=None,
            metadata={"attached": "true"},
        )
        self._sessions[session.session_id] = session
        return session

    def detach_session(self, session_id: str) -> bool:
        session = self._sessions.get(session_id)
        if not session:
            return False
        session.status = "detached"
        return True

    def close_session(self, session_id: str) -> bool:
        if session_id not in self._sessions:
            return False
        del self._sessions[session_id]
        return True

    def restart_session(self, session_id: str) -> SessionInfo | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        application_id = session.application_id
        self.close_session(session_id)
        return self.start_session(application_id)

    def get_session(self, session_id: str) -> SessionInfo | None:
        return self._sessions.get(session_id)

    def get_sessions(self) -> list[SessionInfo]:
        return list(self._sessions.values())

    def get_sessions_by_application(self, application_id: str) -> list[SessionInfo]:
        return [s for s in self._sessions.values() if s.application_id == application_id]

    def update_session(self, session_id: str, **kwargs: Any) -> SessionInfo | None:
        session = self._sessions.get(session_id)
        if not session:
            return None
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        return session

    def _find_application(self, application_id: str) -> ApplicationInfo | None:
        for app in self.discovery.discover():
            if app.id == application_id:
                return app
        return None

    def _find_running_application(self, application_id: str) -> ApplicationInfo | None:
        for app in self.discovery.discover():
            if app.id == application_id and app.running:
                return app
        return None

    def _find_window_for_application(self, application_id: str) -> WindowInfo | None:
        for window in self.window_discovery.discover_windows():
            if window.process_name and window.process_name.lower() == application_id.lower():
                return window
        return None
