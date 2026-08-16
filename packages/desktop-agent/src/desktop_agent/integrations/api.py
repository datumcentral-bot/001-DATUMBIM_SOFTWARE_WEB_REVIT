from __future__ import annotations

import platform
from datetime import UTC, datetime
from typing import Any

from desktop_agent.integrations.models import (
    Integration,
    IntegrationCapability,
    IntegrationCredential,
    IntegrationHealth,
    IntegrationRequest,
    IntegrationResult,
    IntegrationStatus,
    IntegrationType,
)


class UniversalApiAdapter:
    def __init__(self) -> None:
        self._available = True
        self._status = IntegrationStatus.READY
        self._error: str | None = None

    @property
    def available(self) -> bool:
        return self._available

    @property
    def status(self) -> IntegrationStatus:
        return self._status

    def execute(self, request: IntegrationRequest) -> IntegrationResult:
        started = datetime.now(tz=UTC)
        try:
            import httpx

            method = request.parameters.get("method", "GET").upper()
            url = request.parameters.get("url")
            headers = request.parameters.get("headers", {})
            body = request.parameters.get("body")
            timeout = request.timeout_seconds
            if not url:
                return IntegrationResult(
                    request_id=request.request_id,
                    status="failed",
                    error="url is required",
                    timestamp=started,
                )
            with httpx.Client(timeout=timeout) as client:
                response = client.request(method, url, headers=headers, json=body)
            duration = (datetime.now(tz=UTC) - started).total_seconds() * 1000
            return IntegrationResult(
                request_id=request.request_id,
                status="completed",
                result={
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text,
                },
                duration_ms=duration,
                timestamp=datetime.now(tz=UTC),
            )
        except ImportError:
            self._error = "httpx not available"
            self._status = IntegrationStatus.UNAVAILABLE
            return IntegrationResult(
                request_id=request.request_id,
                status="failed",
                error="httpx not available",
                timestamp=started,
            )
        except Exception as exc:
            return IntegrationResult(
                request_id=request.request_id,
                status="failed",
                error=str(exc),
                timestamp=datetime.now(tz=UTC),
            )

    def health(self) -> IntegrationHealth:
        return IntegrationHealth(
            integration_id="universal_api",
            status=self._status,
            error=self._error,
            last_check=datetime.now(tz=UTC),
        )

    def to_integration(self) -> Integration:
        capabilities = [
            IntegrationCapability(
                capability_id="api_get",
                name="HTTP GET",
                description="Perform HTTP GET request",
                category="api",
                target_type="http",
                parameters=["url", "headers", "query_params"],
                risk_level="low",
                approval_required=False,
            ),
            IntegrationCapability(
                capability_id="api_post",
                name="HTTP POST",
                description="Perform HTTP POST request",
                category="api",
                target_type="http",
                parameters=["url", "headers", "body"],
                requires_transaction=True,
                risk_level="medium",
                approval_required=True,
            ),
            IntegrationCapability(
                capability_id="api_put",
                name="HTTP PUT",
                description="Perform HTTP PUT request",
                category="api",
                target_type="http",
                parameters=["url", "headers", "body"],
                requires_transaction=True,
                risk_level="medium",
                approval_required=True,
            ),
            IntegrationCapability(
                capability_id="api_delete",
                name="HTTP DELETE",
                description="Perform HTTP DELETE request",
                category="api",
                target_type="http",
                parameters=["url", "headers"],
                requires_transaction=True,
                risk_level="high",
                approval_required=True,
            ),
        ]
        return Integration(
            integration_id="universal_api",
            name="Universal API",
            description="Universal REST/API adapter",
            integration_type=IntegrationType.API,
            status=self._status,
            capabilities=capabilities,
            health=IntegrationHealth(
                integration_id="universal_api",
                status=self._status,
                error=self._error,
                last_check=datetime.now(tz=UTC),
            ),
            metadata={"platform": platform.system()},
        )
