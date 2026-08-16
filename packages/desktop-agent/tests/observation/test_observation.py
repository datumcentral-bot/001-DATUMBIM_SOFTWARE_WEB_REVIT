import pytest

from desktop_agent.observation.engine import ObservationEngine
from desktop_agent.observation.models import (
    CaptureMode,
    ObservationRequest,
    ObservationResult,
    ObservationStatus,
    Region,
)
from desktop_agent.observation.providers.mock import MockObservationProvider
from desktop_agent.observation.storage import ObservationStore


class TestRegion:
    def test_valid_region(self) -> None:
        region = Region(x=0, y=0, width=100, height=100)
        assert region.valid() is True

    def test_invalid_region_zero_width(self) -> None:
        region = Region(x=0, y=0, width=0, height=100)
        assert region.valid() is False

    def test_invalid_region_negative_height(self) -> None:
        region = Region(x=0, y=0, width=100, height=-10)
        assert region.valid() is False


class TestMockProvider:
    def test_list_displays_returns_list(self) -> None:
        provider = MockObservationProvider()
        displays = provider.list_displays()
        assert isinstance(displays, list)
        assert len(displays) > 0

    def test_list_windows_returns_list(self) -> None:
        provider = MockObservationProvider()
        windows = provider.list_windows()
        assert isinstance(windows, list)
        assert len(windows) > 0

    def test_capture_screen_returns_completed(self) -> None:
        provider = MockObservationProvider()
        request = ObservationRequest(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.FULL_SCREEN,
            timestamp="2024-01-01T00:00:00Z",
        )
        result = provider.capture_screen(request)
        assert result.status == "completed"
        assert result.image_reference is not None

    def test_capture_window_returns_completed(self) -> None:
        provider = MockObservationProvider()
        request = ObservationRequest(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.WINDOW,
            target_id="window-1",
            timestamp="2024-01-01T00:00:00Z",
        )
        result = provider.capture_window(request, "window-1")
        assert result.status == "completed"

    def test_capture_region_returns_completed(self) -> None:
        provider = MockObservationProvider()
        request = ObservationRequest(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.REGION,
            region=Region(x=0, y=0, width=100, height=100),
            timestamp="2024-01-01T00:00:00Z",
        )
        result = provider.capture_region(request, Region(x=0, y=0, width=100, height=100))
        assert result.status == "completed"


class TestObservationEngine:
    def test_capture_full_screen(self) -> None:
        engine = ObservationEngine(provider=MockObservationProvider())
        request = ObservationRequest(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.FULL_SCREEN,
            timestamp="2024-01-01T00:00:00Z",
        )
        result = engine.capture(request)
        assert result.status == "completed"
        assert result.duration is not None
        assert result.duration >= 0

    def test_capture_invalid_region(self) -> None:
        engine = ObservationEngine(provider=MockObservationProvider())
        request = ObservationRequest(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.REGION,
            region=Region(x=0, y=0, width=0, height=0),
            timestamp="2024-01-01T00:00:00Z",
        )
        result = engine.capture(request)
        assert result.status == ObservationStatus.FAILED

    def test_list_displays(self) -> None:
        engine = ObservationEngine(provider=MockObservationProvider())
        displays = engine.list_displays()
        assert isinstance(displays, list)

    def test_list_windows(self) -> None:
        engine = ObservationEngine(provider=MockObservationProvider())
        windows = engine.list_windows()
        assert isinstance(windows, list)


class TestObservationStore:
    def test_save_and_get(self) -> None:
        store = ObservationStore()
        result = ObservationResult(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.FULL_SCREEN,
            status="completed",
            timestamp="2024-01-01T00:00:00Z",
        )
        entry = store.save(result)
        assert entry.observation_id == "obs-1"
        fetched = store.get("obs-1")
        assert fetched is not None
        assert fetched.session_id == "session-1"

    def test_list_by_session(self) -> None:
        store = ObservationStore()
        result = ObservationResult(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.FULL_SCREEN,
            status="completed",
            timestamp="2024-01-01T00:00:00Z",
        )
        store.save(result)
        entries = store.list_by_session("session-1")
        assert len(entries) == 1

    def test_delete(self) -> None:
        store = ObservationStore()
        result = ObservationResult(
            observation_id="obs-1",
            session_id="session-1",
            application_id="app-1",
            target_type=CaptureMode.FULL_SCREEN,
            status="completed",
            timestamp="2024-01-01T00:00:00Z",
        )
        store.save(result)
        assert store.delete("obs-1") is True
        assert store.get("obs-1") is None
