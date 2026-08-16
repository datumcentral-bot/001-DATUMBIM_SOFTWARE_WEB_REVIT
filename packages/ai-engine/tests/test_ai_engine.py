import pytest

from ai_engine.models import AIModel, AIProviderCapabilities, AIProviderHealth, AIRequest, AIResponse
from ai_engine.providers.base import AIProvider
from ai_engine.providers.mock import MockAIProvider
from ai_engine.providers.openai_compatible import OpenAICompatibleProvider
from ai_engine.registry import AIProviderRegistry
from ai_engine.router import AIRouter
from ai_engine.vision import VisionEngine
from ai_engine.vision_models import VisionContext, VisionRequest


class TestMockProvider:
    def test_health_reports_available(self) -> None:
        provider = MockAIProvider()
        health = provider.health()
        assert health.status == "available"
        assert health.capabilities.vision is True

    def test_list_models_returns_models(self) -> None:
        provider = MockAIProvider()
        models = provider.list_models()
        assert len(models) >= 1
        assert any(model.model_id == "mock-vision" for model in models)

    def test_complete_returns_mock_response(self) -> None:
        provider = MockAIProvider()
        request = AIRequest(request_id="req-1", instructions="hello")
        response = provider.complete(request)
        assert response.status == "completed"
        assert "MOCK" in response.content
        assert response.provider_id == "mock"

    def test_supports_vision(self) -> None:
        provider = MockAIProvider()
        assert provider.supports_vision() is True


class TestRegistry:
    def test_register_and_get(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        assert registry.get("mock") is not None

    def test_unregister(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        registry.unregister("mock")
        assert registry.get("mock") is None

    def test_list_providers(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        assert "mock" in registry.list()

    def test_health(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        health = registry.health()
        assert "mock" in health

    def test_complete_unknown_provider_returns_error(self) -> None:
        registry = AIProviderRegistry()
        request = AIRequest(request_id="req-1", provider_id="unknown")
        response = registry.complete(request)
        assert response.status == "error"
        assert "Unknown provider" in response.error

    def test_openai_compatible_not_configured(self) -> None:
        provider = OpenAICompatibleProvider()
        assert provider.status == "not_configured"
        health = provider.health()
        assert health.status == "not_configured"


class TestRouter:
    def test_route_vision_with_provider(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        router = AIRouter(registry)
        request = VisionRequest(request_id="req-1", observation_id="obs-1", provider_id="mock")
        routed_request, provider_id = router.route_vision(request)
        assert provider_id == "mock"
        assert routed_request.provider_id == "mock"

    def test_route_vision_unknown_provider_raises(self) -> None:
        registry = AIProviderRegistry()
        router = AIRouter(registry)
        request = VisionRequest(request_id="req-1", observation_id="obs-1", provider_id="unknown")
        with pytest.raises(ValueError):
            router.route_vision(request)

    def test_route_vision_auto_select(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        router = AIRouter(registry)
        request = VisionRequest(request_id="req-1", observation_id="obs-1")
        routed_request, provider_id = router.route_vision(request)
        assert provider_id == "mock"


class TestVisionEngine:
    def test_analyze_with_provider(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        engine = VisionEngine(registry)
        request = VisionRequest(request_id="req-1", observation_id="obs-1", provider_id="mock")
        response = engine.analyze(request)
        assert response.status == "completed"
        assert response.provider_id == "mock"
        assert response.processing_time is not None
        assert response.processing_time >= 0

    def test_analyze_without_provider_returns_error(self) -> None:
        engine = VisionEngine()
        request = VisionRequest(request_id="req-1", observation_id="obs-1")
        response = engine.analyze(request)
        assert response.status == "error"
        assert "No vision-capable provider" in response.error

    def test_analyze_generates_elements_when_detect_ui(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        engine = VisionEngine(registry)
        request = VisionRequest(request_id="req-1", observation_id="obs-1", provider_id="mock", detect_ui=True)
        response = engine.analyze(request)
        assert len(response.elements) >= 1

    def test_analyze_generates_action_hints_when_requested(self) -> None:
        registry = AIProviderRegistry()
        registry.register(MockAIProvider())
        engine = VisionEngine(registry)
        request = VisionRequest(request_id="req-1", observation_id="obs-1", provider_id="mock", generate_action_hints=True)
        response = engine.analyze(request)
        assert len(response.action_hints) >= 1
