from __future__ import annotations

import platform
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


class N8NConnector:
    N8N_DEFAULT_URL = "http://localhost:5678"
    N8N_INSTALL_PATHS = [
        r"C:\Program Files\n8n",
        r"C:\Users\Asad\AppData\Local\n8n",
    ]

    def __init__(self) -> None:
        self._available = False
        self._installed = False
        self._url: str | None = None
        self._version: str | None = None
        self._error: str | None = None
        self._workflows: list[dict[str, Any]] = []
        self._detect()

    def _detect(self) -> None:
        if platform.system() != "Windows":
            self._error = "n8n connector requires Windows"
            self._status = IntegrationStatus.NOT_INSTALLED
            return
        import os
        for path in self.N8N_INSTALL_PATHS:
            if os.path.isdir(path):
                self._installed = True
                self._url = self.N8N_DEFAULT_URL
                self._status = IntegrationStatus.NOT_CONFIGURED
                return
        self._installed = False
        self._status = IntegrationStatus.NOT_INSTALLED
        self._error = "n8n installation not found"

    @property
    def available(self) -> bool:
        return self._available

    @property
    def installed(self) -> bool:
        return self._installed

    @property
    def status(self) -> IntegrationStatus:
        return self._status

    @property
    def error(self) -> str | None:
        return self._error

    def connect(self) -> IntegrationResult:
        if not self._installed:
            return IntegrationResult(
                request_id="",
                status="failed",
                error="n8n is not installed",
                timestamp=datetime.now(tz=UTC),
            )
        self._available = True
        self._status = IntegrationStatus.CONNECTED
        return IntegrationResult(
            request_id="",
            status="completed",
            result={"url": self._url, "version": self._version},
            timestamp=datetime.now(tz=UTC),
        )

    def disconnect(self) -> IntegrationResult:
        self._available = False
        self._status = IntegrationStatus.DISCONNECTED
        return IntegrationResult(
            request_id="",
            status="completed",
            result={"message": "disconnected"},
            timestamp=datetime.now(tz=UTC),
        )

    def health(self) -> IntegrationHealth:
        return IntegrationHealth(
            integration_id="n8n",
            status=self._status,
            error=self._error,
            last_check=datetime.now(tz=UTC),
        )

    def list_workflows(self) -> list[dict[str, Any]]:
        if not self._available:
            return []
        return self._workflows

    def execute_workflow(self, workflow_id: str, payload: dict[str, Any] | None = None) -> IntegrationResult:
        if not self._available:
            return IntegrationResult(
                request_id="",
                status="failed",
                error="n8n is not available",
                timestamp=datetime.now(tz=UTC),
            )
        return IntegrationResult(
            request_id="",
            status="not_implemented",
            error="n8n workflow execution not yet implemented",
            timestamp=datetime.now(tz=UTC),
        )

    def trigger_webhook(self, webhook_id: str, payload: dict[str, Any] | None = None) -> IntegrationResult:
        if not self._available:
            return IntegrationResult(
                request_id="",
                status="failed",
                error="n8n is not available",
                timestamp=datetime.now(tz=UTC),
            )
        return IntegrationResult(
            request_id="",
            status="not_implemented",
            error="n8n webhook triggering not yet implemented",
            timestamp=datetime.now(tz=UTC),
        )

    def to_integration(self) -> Integration:
        capabilities = [
            IntegrationCapability(
                capability_id="n8n_health",
                name="Health Check",
                description="Check n8n health",
                category="automation",
                target_type="workflow",
                available=self._available,
            ),
            IntegrationCapability(
                capability_id="n8n_list_workflows",
                name="List Workflows",
                description="List available n8n workflows",
                category="automation",
                target_type="workflow",
                available=self._available,
            ),
            IntegrationCapability(
                capability_id="n8n_execute_workflow",
                name="Execute Workflow",
                description="Execute an n8n workflow",
                category="automation",
                target_type="workflow",
                requires_transaction=True,
                approval_required=True,
                risk_level="medium",
                available=self._available,
            ),
            IntegrationCapability(
                capability_id="n8n_trigger_webhook",
                name="Trigger Webhook",
                description="Trigger an n8n webhook",
                category="automation",
                target_type="webhook",
                requires_transaction=True,
                approval_required=True,
                risk_level="medium",
                available=self._available,
            ),
        ]
        return Integration(
            integration_id="n8n",
            name="n8n",
            description="n8n workflow automation",
            integration_type=IntegrationType.AUTOMATION,
            status=self._status,
            capabilities=capabilities,
            health=IntegrationHealth(
                integration_id="n8n",
                status=self._status,
                error=self._error,
                last_check=datetime.now(tz=UTC),
            ),
            metadata={"url": self._url or "", "version": self._version or ""},
        )
