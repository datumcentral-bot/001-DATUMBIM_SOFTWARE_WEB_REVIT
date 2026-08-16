from __future__ import annotations

from desktop_agent.observation.engine import ObservationEngine
from desktop_agent.observation.models import (
    CaptureMode,
    ObservationRequest,
    ObservationResult,
    ObservationStatus,
    Region,
    WindowInfo,
    DisplayInfo,
)
from desktop_agent.observation.providers.base import ObservationProvider
from desktop_agent.observation.providers.mock import MockObservationProvider
from desktop_agent.observation.providers.windows import WindowsObservationProvider
from desktop_agent.observation.storage import ObservationStore


def create_windows_observation_engine() -> ObservationEngine:
    provider = WindowsObservationProvider()
    store = ObservationStore()
    return ObservationEngine(provider=provider, store=store)


def create_mock_observation_engine() -> ObservationEngine:
    provider = MockObservationProvider()
    store = ObservationStore()
    return ObservationEngine(provider=provider, store=store)
