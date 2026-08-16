from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from ai_engine.models import AIRequest, AIResponse
from ai_engine.registry import AIProviderRegistry
from ai_engine.vision_models import (
    ActionHint,
    BoundingBox,
    TextBlock,
    VisionContext,
    VisionElement,
    VisionRegion,
    VisionRequest,
    VisionResponse,
)


class VisionEngine:
    def __init__(self, registry: AIProviderRegistry | None = None) -> None:
        self.registry = registry or AIProviderRegistry()

    def analyze(self, request: VisionRequest) -> VisionResponse:
        started_at = datetime.now(tz=UTC)
        ai_request = AIRequest(
            request_id=request.request_id,
            provider_id=request.provider_id,
            model_id=request.model_id,
            instructions=request.instructions,
            image_reference=request.image_reference,
            metadata={
                "detect_ui": request.detect_ui,
                "detect_text": request.detect_text,
                "detect_regions": request.detect_regions,
                "describe_application": request.describe_application,
                "generate_action_hints": request.generate_action_hints,
            },
        )
        ai_response: AIResponse | None = None
        if request.provider_id:
            provider = self.registry.get(request.provider_id)
            if provider:
                ai_response = provider.complete(ai_request)
            else:
                ai_response = AIResponse(
                    request_id=request.request_id,
                    provider_id=request.provider_id,
                    model_id=request.model_id,
                    status="error",
                    error=f"Unknown provider: {request.provider_id}",
                )
        else:
            for provider_id in self.registry.list():
                provider = self.registry.get(provider_id)
                if provider and provider.supports_vision():
                    ai_response = provider.complete(ai_request)
                    break
            if ai_response is None:
                ai_response = AIResponse(
                    request_id=request.request_id,
                    provider_id=None,
                    model_id=None,
                    status="error",
                    error="No vision-capable provider available",
                )
        completed_at = datetime.now(tz=UTC)
        processing_time = (completed_at - started_at).total_seconds()
        vision_response = VisionResponse(
            request_id=request.request_id,
            observation_id=request.observation_id,
            provider_id=ai_response.provider_id,
            model_id=ai_response.model_id,
            status=ai_response.status,
            processing_time=processing_time,
            usage=ai_response.usage,
            raw_reference=request.image_reference,
            error=ai_response.error,
        )
        if ai_response.content:
            vision_response.screen_description = ai_response.content
        if request.detect_ui:
            vision_response.elements.append(
                VisionElement(
                    id="element-1",
                    type="unknown",
                    label="Mock UI Element",
                    confidence=0.5,
                    clickable=False,
                    enabled=False,
                    visible=False,
                )
            )
        if request.generate_action_hints:
            vision_response.action_hints.append(
                ActionHint(
                    element_id="element-1",
                    action_type="CLICK",
                    description="Mock action hint",
                    confidence=0.5,
                    requires_confirmation=True,
                )
            )
        return vision_response
