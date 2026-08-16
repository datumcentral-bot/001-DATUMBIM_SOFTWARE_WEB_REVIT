import platform

import pytest

from revit_connector.models import RevitConnectionState, RevitDocument, RevitElement, RevitLevel, RevitView
from revit_connector.connector import RevitConnector
from revit_connector.discovery import RevitDiscovery
from revit_connector.pyrevit_bridge import PyRevitBridge
from revit_connector.dynamo_bridge import DynamoBridge
from revit_connector.transaction_engine import TransactionManager


def test_connector_initial_state():
    connector = RevitConnector()
    assert connector.state == RevitConnectionState.NOT_RUNNING
    assert connector.connected is False


def test_discovery_windows():
    discovery = RevitDiscovery()
    info = discovery.detect()
    if platform.system() == "Windows":
        assert info.state in (RevitConnectionState.RUNNING, RevitConnectionState.NOT_RUNNING)
    else:
        assert info.state == RevitConnectionState.NOT_INSTALLED
        assert "Windows" in info.errors[0]


def test_pyrevit_bridge_defaults():
    bridge = PyRevitBridge()
    if platform.system() == "Windows":
        assert bridge.available is False
        assert bridge.installed is False
    else:
        assert bridge.available is False
        assert bridge.installed is False
    assert bridge.discover_extensions() == []


def test_dynamo_bridge_defaults():
    bridge = DynamoBridge()
    if platform.system() == "Windows":
        assert bridge.available is True
        assert bridge.installed is True
    else:
        assert bridge.available is False
        assert bridge.installed is False
    assert bridge.discover_workspaces() == []


def test_transaction_manager_basic():
    manager = TransactionManager()
    ctx = manager.begin("test_op")
    assert ctx.transaction_id is not None
    assert ctx.operation_id == "test_op"
    assert ctx.dry_run is False
    retrieved = manager.get_transaction(ctx.transaction_id)
    assert retrieved is ctx


def test_document_model():
    doc = RevitDocument(document_id=1, name="Test.rvt", active=True)
    assert doc.document_id == 1
    assert doc.name == "Test.rvt"
    assert doc.active is True
    data = doc.model_dump()
    assert data["name"] == "Test.rvt"


def test_element_model():
    element = RevitElement(element_id=123, category="Walls", family="Basic Wall")
    assert element.element_id == 123
    assert element.category == "Walls"
    assert element.family == "Basic Wall"


def test_view_model():
    view = RevitView(view_id=456, name="Level 1", view_type="FloorPlan")
    assert view.view_id == 456
    assert view.name == "Level 1"
    assert view.view_type == "FloorPlan"
