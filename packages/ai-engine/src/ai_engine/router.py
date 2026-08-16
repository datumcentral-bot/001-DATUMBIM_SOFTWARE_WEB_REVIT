from __future__ import annotations

from typing import Any

from ai_engine.models import AIRequest, AIResponse, AIModel, ProviderStatus
from ai_engine.registry import AIProviderRegistry
from ai_engine.vision_models import VisionRequest, VisionResponse


class AIRouter:
    def __init__(self, registry: AIProviderRegistry | None = None) -> None:
        self.registry = registry or AIProviderRegistry()

    def route_vision(self, request: VisionRequest) -> tuple[VisionRequest, str]:
        provider_id = request.provider_id
        if provider_id:
            provider = self.registry.get(provider_id)
            if not provider:
                raise ValueError(f"Unknown provider: {provider_id}")
            return request, provider_id
        for provider_id in self.registry.list():
            provider = self.registry.get(provider_id)
            if provider and provider.supports_vision():
                request.provider_id = provider_id
                return request, provider_id
        raise ValueError("No vision-capable provider available")

    def available_models(self) -> list[AIModel]:
        return self.registry.list_models()

    def provider_health(self) -> dict[str, Any]:
        return {provider_id: health.model_dump() for provider_id, health in self.registry.health().items()}
