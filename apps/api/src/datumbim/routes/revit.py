from datetime import UTC, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/revit", tags=["revit"])

_revit_state = {
    "connection_state": "not_running",
    "revit_version": None,
    "active_document": None,
    "active_view": None,
    "categories": [],
    "elements": [],
    "families": [],
    "levels": [],
    "views": [],
    "capabilities": [],
    "pyrevit_available": False,
    "dynamo_available": False,
    "api_available": False,
    "ui_available": False,
}


@router.get("/status")
async def revit_status() -> dict:
    return {"status": _revit_state}


@router.get("/categories")
async def revit_categories() -> dict:
    return {"categories": _revit_state["categories"]}


@router.get("/elements")
async def revit_elements(category_id: Optional[str] = None) -> dict:
    elements = _revit_state["elements"]
    if category_id:
        elements = [e for e in elements if e.get("category_id") == category_id]
    return {"elements": elements}


@router.get("/families")
async def revit_families() -> dict:
    return {"families": _revit_state["families"]}


@router.get("/levels")
async def revit_levels() -> dict:
    return {"levels": _revit_state["levels"]}


@router.get("/views")
async def revit_views() -> dict:
    return {"views": _revit_state["views"]}


@router.get("/documents")
async def revit_documents() -> dict:
    return {"documents": [_revit_state["active_document"]] if _revit_state["active_document"] else []}


@router.get("/capabilities")
async def revit_capabilities() -> dict:
    return {"capabilities": _revit_state["capabilities"]}


@router.post("/connect")
async def revit_connect() -> dict:
    try:
        from revit_connector.connector import RevitConnector
        connector = RevitConnector()
        result = connector.connect()
        _revit_state.update(result)
        return {"status": _revit_state["connection_state"], "message": _revit_state.get("window_title", "Revit")}
    except ImportError:
        _revit_state["connection_state"] = "not_implemented"
        return {"status": "not_implemented", "message": "Revit connector not available"}


@router.post("/discover")
async def revit_discover() -> dict:
    try:
        from revit_connector.connector import RevitConnector
        connector = RevitConnector()
        state = connector.detect()
        _revit_state["connection_state"] = state.value
        return {"status": state.value, "discovered": state in ("running", "connected", "document_open")}
    except ImportError:
        return {"status": "not_implemented", "discovered": False}
