from __future__ import annotations

from desktop_agent.integrations.fabric import UniversalIntegrationFabric
from desktop_agent.integrations.models import (
    Integration,
    IntegrationCapability,
    IntegrationCredential,
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
from desktop_agent.integrations.n8n import N8NConnector
from desktop_agent.integrations.registry import IntegrationRegistry
from desktop_agent.integrations.tools import ToolExecutionPipeline, ToolRegistry

__all__ = [
    "UniversalIntegrationFabric",
    "IntegrationRegistry",
    "N8NConnector",
    "ToolRegistry",
    "ToolExecutionPipeline",
    "Integration",
    "IntegrationCapability",
    "IntegrationCredential",
    "IntegrationEvent",
    "IntegrationHealth",
    "IntegrationRequest",
    "IntegrationResult",
    "IntegrationSession",
    "IntegrationStatus",
    "IntegrationType",
    "IntegrationWebhook",
    "IntegrationWorkflow",
]
