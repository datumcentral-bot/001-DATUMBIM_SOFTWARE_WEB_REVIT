from __future__ import annotations

import abc
from typing import Any

from ai_engine.models import (
    AIModel,
    AIProviderCapabilities,
    AIProviderHealth,
    AIRequest,
    AIResponse,
)


class AIProvider(abc.ABC):
    provider_id: str
    display_name: str
    status: str = "not_configured"

    @abc.abstractmethod
    def health(self) -> AIProviderHealth:
        raise NotImplementedError

    @abc.abstractmethod
    def list_models(self) -> list[AIModel]:
        raise NotImplementedError

    @abc.abstractmethod
    def complete(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError

    def supports_vision(self) -> bool:
        return any(model.vision_supported for model in self.list_models())

    def supports_tools(self) -> bool:
        return any(model.tool_calling_supported for model in self.list_models())
