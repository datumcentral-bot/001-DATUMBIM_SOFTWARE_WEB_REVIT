from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from ai_engine.models import AIModel, AIProviderCapabilities, AIProviderHealth, AIRequest, AIResponse
from ai_engine.providers.base import AIProvider


class OpenAICompatibleProvider(AIProvider):
    provider_id = "openai_compatible"
    display_name = "OpenAI Compatible"
    status = "not_configured"

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = base_url or os.getenv("OPENAI_COMPATIBLE_BASE_URL", "")
        self.api_key = api_key or os.getenv("OPENAI_COMPATIBLE_API_KEY", "")
        if self.base_url and self.api_key:
            self.status = "auth_required"
        else:
            self.status = "not_configured"

    def health(self) -> AIProviderHealth:
        capabilities = AIProviderCapabilities()
        available_models: list[AIModel] = []
        if self.status == "auth_required":
            capabilities.text = True
            capabilities.structured_output = True
            capabilities.reasoning = True
            available_models = [
                AIModel(
                    provider_id=self.provider_id,
                    model_id="auto",
                    display_name="OpenAI Compatible Model",
                    capabilities=["text", "structured_output", "reasoning"],
                    context_window=8192,
                    vision_supported=False,
                    tool_calling_supported=False,
                    structured_output_supported=True,
                    local=False,
                    availability="auth_required",
                )
            ]
        return AIProviderHealth(
            provider_id=self.provider_id,
            status=self.status,
            capabilities=capabilities,
            available_models=available_models,
        )

    def list_models(self) -> list[AIModel]:
        return self.health().available_models

    def complete(self, request: AIRequest) -> AIResponse:
        started_at = datetime.now(tz=UTC)
        if self.status != "auth_required":
            return AIResponse(
                request_id=request.request_id,
                provider_id=self.provider_id,
                model_id=request.model_id,
                status="error",
                error=f"Provider not configured: {self.status}",
                latency_ms=0,
            )
        try:
            import httpx

            payload: dict[str, Any] = {
                "model": request.model_id or "auto",
                "messages": request.messages or [{"role": "user", "content": request.instructions or ""}],
                "temperature": request.temperature,
            }
            if request.max_tokens:
                payload["max_tokens"] = request.max_tokens
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            response = httpx.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = data.get("usage", {})
            completed_at = datetime.now(tz=UTC)
            latency_ms = (completed_at - started_at).total_seconds() * 1000
            return AIResponse(
                request_id=request.request_id,
                provider_id=self.provider_id,
                model_id=request.model_id or "auto",
                status="completed",
                content=content,
                usage=usage,
                latency_ms=latency_ms,
            )
        except Exception as exc:
            completed_at = datetime.now(tz=UTC)
            latency_ms = (completed_at - started_at).total_seconds() * 1000
            return AIResponse(
                request_id=request.request_id,
                provider_id=self.provider_id,
                model_id=request.model_id,
                status="error",
                error=str(exc),
                latency_ms=latency_ms,
            )
