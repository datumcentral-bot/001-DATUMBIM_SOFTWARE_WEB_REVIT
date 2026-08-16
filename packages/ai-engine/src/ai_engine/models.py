from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class ProviderStatus(str, Enum):
    NOT_CONFIGURED = "not_configured"
    AUTH_REQUIRED = "auth_required"
    NOT_RUNNING = "not_running"
    AVAILABLE = "available"
    ERROR = "error"


class ModelCapability(str, Enum):
    TEXT = "text"
    VISION = "vision"
    IMAGE_ANALYSIS = "image_analysis"
    OCR = "ocr"
    UI_UNDERSTANDING = "ui_understanding"
    STRUCTURED_OUTPUT = "structured_output"
    TOOL_CALLING = "tool_calling"
    CODE = "code"
    REASONING = "reasoning"
    EMBEDDING = "embedding"


class AIModel(BaseModel):
    provider_id: str
    model_id: str
    display_name: str
    capabilities: list[ModelCapability] = []
    context_window: int | None = None
    vision_supported: bool = False
    tool_calling_supported: bool = False
    structured_output_supported: bool = False
    local: bool = False
    availability: ProviderStatus = ProviderStatus.NOT_CONFIGURED


class AIProviderCapabilities(BaseModel):
    text: bool = False
    vision: bool = False
    image_analysis: bool = False
    ocr: bool = False
    ui_understanding: bool = False
    structured_output: bool = False
    tool_calling: bool = False
    code: bool = False
    reasoning: bool = False
    embedding: bool = False


class AIRequest(BaseModel):
    request_id: str
    provider_id: str | None = None
    model_id: str | None = None
    instructions: str | None = None
    messages: list[dict[str, Any]] = []
    image_reference: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    metadata: dict[str, Any] = {}


class AIResponse(BaseModel):
    request_id: str
    provider_id: str | None = None
    model_id: str | None = None
    status: str
    content: str | None = None
    usage: dict[str, Any] | None = None
    latency_ms: float | None = None
    error: str | None = None
    metadata: dict[str, Any] = {}


class AITokenUsage(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class AIProviderHealth(BaseModel):
    provider_id: str
    status: ProviderStatus
    latency_ms: float | None = None
    error: str | None = None
    capabilities: AIProviderCapabilities = AIProviderCapabilities()
    available_models: list[AIModel] = []
