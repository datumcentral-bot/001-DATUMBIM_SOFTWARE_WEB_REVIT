from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from ai_engine.models import AIModel, AIProviderCapabilities, AIProviderHealth, AIRequest, AIResponse
from ai_engine.providers.base import AIProvider


class MockAIProvider(AIProvider):
    provider_id = "mock"
    display_name = "Mock AI Provider"
    status = "available"

    def health(self) -> AIProviderHealth:
        return AIProviderHealth(
            provider_id=self.provider_id,
            status="available",
            capabilities=AIProviderCapabilities(
                text=True,
                vision=True,
                image_analysis=True,
                ocr=True,
                ui_understanding=True,
                structured_output=True,
                tool_calling=True,
                code=True,
                reasoning=True,
            ),
            available_models=self.list_models(),
        )

    def list_models(self) -> list[AIModel]:
        return [
            AIModel(
                provider_id=self.provider_id,
                model_id="mock-vision",
                display_name="Mock Vision",
                capabilities=["vision", "image_analysis", "ocr", "ui_understanding", "structured_output"],
                context_window=8192,
                vision_supported=True,
                tool_calling_supported=True,
                structured_output_supported=True,
                local=True,
                availability="available",
            ),
            AIModel(
                provider_id=self.provider_id,
                model_id="mock-text",
                display_name="Mock Text",
                capabilities=["text", "reasoning", "code"],
                context_window=4096,
                vision_supported=False,
                tool_calling_supported=False,
                structured_output_supported=True,
                local=True,
                availability="available",
            ),
        ]

    def complete(self, request: AIRequest) -> AIResponse:
        model_id = request.model_id or "mock-vision"
        started_at = datetime.now(tz=UTC)
        content = "MOCK: This is a deterministic mock AI response for testing purposes."
        if request.image_reference:
            content = "MOCK: Analyzed image reference " + request.image_reference
        completed_at = datetime.now(tz=UTC)
        latency_ms = (completed_at - started_at).total_seconds() * 1000
        return AIResponse(
            request_id=request.request_id,
            provider_id=self.provider_id,
            model_id=model_id,
            status="completed",
            content=content,
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            latency_ms=latency_ms,
            metadata={"mock": "true"},
        )
