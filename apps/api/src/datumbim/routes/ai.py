from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/ai", tags=["ai"])

_providers: dict[str, dict] = {
    "mock": {
        "provider_id": "mock",
        "display_name": "Mock AI Provider",
        "status": "available",
        "supports_vision": True,
        "supports_tools": True,
    }
}


@router.get("/providers")
async def list_providers() -> dict:
    return {"providers": list(_providers.values())}


@router.get("/providers/{provider_id}")
async def get_provider(provider_id: str) -> dict:
    provider = _providers.get(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"provider": provider}


@router.get("/models")
async def list_models() -> dict:
    models = [
        {
            "provider_id": "mock",
            "model_id": "mock-vision",
            "display_name": "Mock Vision",
            "capabilities": ["vision", "image_analysis", "ocr", "ui_understanding"],
            "vision_supported": True,
            "tool_calling_supported": True,
            "structured_output_supported": True,
            "local": True,
            "availability": "available",
        },
        {
            "provider_id": "mock",
            "model_id": "mock-text",
            "display_name": "Mock Text",
            "capabilities": ["text", "reasoning", "code"],
            "vision_supported": False,
            "tool_calling_supported": False,
            "structured_output_supported": True,
            "local": True,
            "availability": "available",
        },
    ]
    return {"models": models}


@router.get("/health")
async def ai_health() -> dict:
    return {
        "providers": {
            provider_id: {
                "status": provider["status"],
                "capabilities": {
                    "text": True,
                    "vision": provider.get("supports_vision", False),
                    "image_analysis": provider.get("supports_vision", False),
                    "ocr": provider.get("supports_vision", False),
                    "ui_understanding": provider.get("supports_vision", False),
                    "structured_output": True,
                    "tool_calling": provider.get("supports_tools", False),
                    "code": True,
                    "reasoning": True,
                },
            }
            for provider_id, provider in _providers.items()
        }
    }


@router.post("/vision/analyze")
async def analyze_vision(request: dict) -> dict:
    observation_id = request.get("observation_id")
    provider_id = request.get("provider_id", "mock")
    model_id = request.get("model_id", "mock-vision")
    instructions = request.get("instructions")
    detect_ui = request.get("detect_ui", True)
    detect_text = request.get("detect_text", True)
    detect_regions = request.get("detect_regions", True)
    describe_application = request.get("describe_application", False)
    generate_action_hints = request.get("generate_action_hints", False)
    if not observation_id:
        raise HTTPException(status_code=400, detail="observation_id is required")
    response = {
        "request_id": str(__import__("uuid").uuid4()),
        "observation_id": observation_id,
        "provider_id": provider_id,
        "model_id": model_id,
        "status": "completed",
        "confidence": 0.8,
        "application": "mock-application",
        "window": "Mock Application",
        "screen_description": "MOCK: Analyzed screen for " + observation_id,
        "elements": [
            {
                "id": "element-1",
                "type": "button",
                "label": "Mock Button",
                "text": "OK",
                "bounding_box": {"x": 100, "y": 100, "width": 80, "height": 30},
                "confidence": 0.9,
                "clickable": True,
                "enabled": True,
                "visible": True,
                "role": "button",
            }
        ]
        if detect_ui
        else [],
        "regions": [
            {"x": 0, "y": 0, "width": 1920, "height": 1080, "label": "screen", "confidence": 0.9}
        ]
        if detect_regions
        else [],
        "text_blocks": [
            {"text": "Mock text", "bounding_box": {"x": 10, "y": 10, "width": 100, "height": 20}, "confidence": 0.8}
        ]
        if detect_text
        else [],
        "action_hints": [
            {
                "element_id": "element-1",
                "action_type": "CLICK",
                "description": "Click the mock button",
                "confidence": 0.7,
                "requires_confirmation": True,
            }
        ]
        if generate_action_hints
        else [],
        "warnings": [],
        "processing_time": 0.1,
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        "raw_reference": f"mock://observations/{observation_id}.png",
        "error": None,
    }
    return {"vision": response}


@router.post("/vision/observe")
async def observe_vision(request: dict) -> dict:
    return await analyze_vision(request)
