from __future__ import annotations

import os
import sys
from datetime import UTC, datetime
from typing import Any

from revit_connector.models import RevitConnectionState, RevitDocument, RevitElement, RevitLevel, RevitParameter, RevitView
from revit_connector.discovery import RevitDiscovery
from revit_connector.api_bridge import RevitApiBridge
from revit_connector.ui_bridge import RevitUIBridge
from revit_connector.pyrevit_bridge import PyRevitBridge
from revit_connector.dynamo_bridge import DynamoBridge
from revit_connector.transaction_engine import TransactionManager


class RevitConnector:
    def __init__(self) -> None:
        self._state = RevitConnectionState.NOT_RUNNING
        self._discovery = RevitDiscovery()
        self._api_bridge = RevitApiBridge()
        self._ui_bridge = RevitUIBridge()
        self._pyrevit_bridge = PyRevitBridge()
        self._dynamo_bridge = DynamoBridge()
        self._transaction_manager = TransactionManager()
        self._document: RevitDocument | None = None
        self._connected = False

    @property
    def state(self) -> RevitConnectionState:
        return self._state

    @property
    def discovery(self) -> RevitDiscovery:
        return self._discovery

    @property
    def api_bridge(self) -> RevitApiBridge:
        return self._api_bridge

    @property
    def ui_bridge(self) -> RevitUIBridge:
        return self._ui_bridge

    @property
    def pyrevit_bridge(self) -> PyRevitBridge:
        return self._pyrevit_bridge

    @property
    def dynamo_bridge(self) -> DynamoBridge:
        return self._dynamo_bridge

    @property
    def transaction_manager(self) -> TransactionManager:
        return self._transaction_manager

    @property
    def document(self) -> RevitDocument | None:
        return self._document

    @property
    def connected(self) -> bool:
        return self._connected

    def detect(self) -> RevitConnectionState:
        info = self._discovery.detect()
        self._state = info.state
        return self._state

    def connect(self) -> dict[str, Any]:
        self._state = RevitConnectionState.CONNECTING
        window_info = self._discovery.discover_window()
        if window_info and self._ui_bridge:
            self._ui_bridge.set_window_handle(window_info.get("hwnd"))
        self._document = self._discovery.discover_document()
        capabilities = self._discovery.get_capabilities()
        self._connected = True
        self._state = RevitConnectionState.CONNECTED
        return {
            "state": self._state.value,
            "process_id": self._discovery._connection_info.process_id,
            "window_title": self._discovery._connection_info.window_title,
            "window_handle": self._discovery._connection_info.window_handle,
            "executable_path": self._discovery._connection_info.executable_path,
            "revit_version": self._discovery._connection_info.revit_version,
            "document": self._document.model_dump() if self._document else None,
            "capabilities": capabilities,
            "pyrevit_available": self._pyrevit_bridge.available,
            "dynamo_available": self._dynamo_bridge.available,
            "api_available": self._api_bridge.available,
        }

    def disconnect(self) -> dict[str, Any]:
        self._connected = False
        self._document = None
        self._state = RevitConnectionState.DISCONNECTED
        return {"state": self._state.value}

    def get_status(self) -> dict[str, Any]:
        return {
            "state": self._state.value,
            "connected": self._connected,
            "document": self._document.model_dump() if self._document else None,
            "api_available": self._api_bridge.available,
            "pyrevit_available": self._pyrevit_bridge.available,
            "dynamo_available": self._dynamo_bridge.available,
            "ui_available": self._ui_bridge.available,
        }

    def get_document(self) -> dict[str, Any] | None:
        if not self._document:
            self._document = self._discovery.discover_document()
        return self._document.model_dump() if self._document else None

    def get_active_view(self) -> dict[str, Any] | None:
        return None

    def get_selection(self) -> list[dict[str, Any]]:
        return []

    def get_categories(self) -> list[dict[str, Any]]:
        return []

    def get_elements(self, category_id: int | None = None) -> list[dict[str, Any]]:
        return []

    def get_families(self) -> list[dict[str, Any]]:
        return []

    def get_levels(self) -> list[dict[str, Any]]:
        return []

    def get_views(self) -> list[dict[str, Any]]:
        return []

    def get_parameters(self, element_id: int) -> list[dict[str, Any]]:
        return []

    def get_capabilities(self) -> list[str]:
        return self._discovery.get_capabilities()
