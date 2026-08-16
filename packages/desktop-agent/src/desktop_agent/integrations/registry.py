from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from desktop_agent.integrations.models import (
    Integration,
    IntegrationCapability,
    IntegrationEvent,
    IntegrationHealth,
    IntegrationRequest,
    IntegrationResult,
    IntegrationSession,
    IntegrationStatus,
    IntegrationType,
    IntegrationWebhook,
    IntegrationWorkflow,
)


class IntegrationRegistry:
    def __init__(self) -> None:
        self._integrations: dict[str, Integration] = {}
        self._events: list[IntegrationEvent] = []

    def register(self, integration: Integration) -> None:
        self._integrations[integration.integration_id] = integration
        self._emit("integration.registered", integration=integration)

    def unregister(self, integration_id: str) -> None:
        integration = self._integrations.pop(integration_id, None)
        if integration:
            self._emit("integration.unregistered", integration=integration)

    def get(self, integration_id: str) -> Integration | None:
        return self._integrations.get(integration_id)

    def list(self, integration_type: IntegrationType | None = None, status: IntegrationStatus | None = None) -> list[Integration]:
        integrations = list(self._integrations.values())
        if integration_type:
            integrations = [i for i in integrations if i.integration_type == integration_type]
        if status:
            integrations = [i for i in integrations if i.status == status]
        return integrations

    def update_status(self, integration_id: str, status: IntegrationStatus, error: str | None = None) -> None:
        integration = self._integrations.get(integration_id)
        if not integration:
            return
        integration.status = status
        integration.error = error
        integration.updated_at = datetime.now(tz=UTC)
        if status == IntegrationStatus.CONNECTED:
            integration.health = IntegrationHealth(
                integration_id=integration_id,
                status=status,
                last_check=datetime.now(tz=UTC),
            )
        self._emit(f"integration.{status.value}", integration=integration)

    def add_capability(self, integration_id: str, capability: IntegrationCapability) -> None:
        integration = self._integrations.get(integration_id)
        if not integration:
            return
        integration.capabilities.append(capability)
        self._emit("integration.capability_added", integration=integration, capability=capability)

    def start_session(self, integration_id: str) -> IntegrationSession | None:
        integration = self._integrations.get(integration_id)
        if not integration:
            return None
        session = IntegrationSession(
            session_id=f"{integration_id}-session-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}",
            integration_id=integration_id,
            status=IntegrationStatus.CONNECTED,
            started_at=datetime.now(tz=UTC),
        )
        integration.sessions.append(session)
        self._emit("integration.session.started", integration=integration, session=session)
        return session

    def end_session(self, integration_id: str, session_id: str) -> None:
        integration = self._integrations.get(integration_id)
        if not integration:
            return
        for session in integration.sessions:
            if session.session_id == session_id:
                session.status = IntegrationStatus.DISCONNECTED
                session.ended_at = datetime.now(tz=UTC)
                self._emit("integration.session.ended", integration=integration, session=session)
                break

    def add_workflow(self, integration_id: str, workflow: IntegrationWorkflow) -> None:
        integration = self._integrations.get(integration_id)
        if not integration:
            return
        integration.workflows.append(workflow)
        self._emit("integration.workflow.added", integration=integration, workflow=workflow)

    def add_webhook(self, integration_id: str, webhook: IntegrationWebhook) -> None:
        integration = self._integrations.get(integration_id)
        if not integration:
            return
        integration.webhooks.append(webhook)
        self._emit("integration.webhook.added", integration=integration, webhook=webhook)

    def _emit(self, event_type: str, **payload: Any) -> None:
        event = IntegrationEvent(
            event_id=f"evt-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}",
            event_type=event_type,
            timestamp=datetime.now(tz=UTC),
            source="integration_registry",
            payload=payload,
        )
        self._events.append(event)

    def get_events(self, integration_id: str | None = None, event_type: str | None = None, limit: int = 100) -> list[IntegrationEvent]:
        events = self._events
        if integration_id:
            events = [e for e in events if e.payload.get("integration", {}).get("integration_id") == integration_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events[-limit:]
