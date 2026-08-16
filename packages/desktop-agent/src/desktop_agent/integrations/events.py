from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.integrations.models import IntegrationEvent


class EventBus:
    def __init__(self) -> None:
        self._events: list[IntegrationEvent] = []
        self._subscribers: list[dict[str, Any]] = []

    def publish(self, event_type: str, source: str, payload: dict[str, Any] | None = None, **kwargs: Any) -> IntegrationEvent:
        event = IntegrationEvent(
            event_id=f"evt-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}",
            event_type=event_type,
            timestamp=datetime.now(tz=UTC),
            source=source,
            payload=payload or {},
            **kwargs,
        )
        self._events.append(event)
        for subscriber in self._subscribers:
            handler = subscriber.get("handler")
            if handler:
                try:
                    handler(event)
                except Exception:
                    pass
        return event

    def subscribe(self, handler: Any, event_types: list[str] | None = None) -> str:
        subscription_id = f"sub-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}"
        self._subscribers.append({"id": subscription_id, "handler": handler, "event_types": event_types})
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        self._subscribers = [s for s in self._subscribers if s.get("id") != subscription_id]

    def get_events(self, event_type: str | None = None, source: str | None = None, limit: int = 100) -> list[IntegrationEvent]:
        events = self._events
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if source:
            events = [e for e in events if e.source == source]
        return events[-limit:]
