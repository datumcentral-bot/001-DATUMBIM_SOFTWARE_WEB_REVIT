from __future__ import annotations

from ai_engine.models import AIModel, AIProviderHealth, AIResponse
from ai_engine.providers.base import AIProvider


class AIProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider) -> None:
        self._providers[provider.provider_id] = provider

    def unregister(self, provider_id: str) -> None:
        self._providers.pop(provider_id, None)

    def get(self, provider_id: str) -> AIProvider | None:
        return self._providers.get(provider_id)

    def list(self) -> list[str]:
        return list(self._providers.keys())

    def health(self) -> dict[str, AIProviderHealth]:
        return {provider_id: provider.health() for provider_id, provider in self._providers.items()}

    def list_models(self) -> list[AIModel]:
        models: list[AIModel] = []
        for provider in self._providers.values():
            models.extend(provider.list_models())
        return models

    def complete(self, request: AIRequest) -> AIResponse:
        provider_id = request.provider_id
        if not provider_id:
            raise ValueError("provider_id is required")
        provider = self._providers.get(provider_id)
        if not provider:
            return AIResponse(
                request_id=request.request_id,
                provider_id=provider_id,
                model_id=request.model_id,
                status="error",
                error=f"Unknown provider: {provider_id}",
            )
        return provider.complete(request)
