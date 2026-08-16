from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class RevitConnectionState(str, Enum):
    NOT_INSTALLED = "not_installed"
    NOT_RUNNING = "not_running"
    STARTING = "starting"
    RUNNING = "running"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DOCUMENT_OPEN = "document_open"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    DISCONNECTED = "disconnected"


class RevitElementType(str, Enum):
    WALL = "wall"
    DOOR = "door"
    WINDOW = "window"
    FLOOR = "floor"
    ROOF = "roof"
    CEILING = "ceiling"
    ROOM = "room"
    AREA = "area"
    STAIRS = "stairs"
    RAILING = "railing"
    COLUMN = "column"
    BEAM = "beam"
    BRACE = "brace"
    FOUNDATION = "foundation"
    DUCT = "duct"
    PIPE = "pipe"
    CONDUIT = "conduit"
    CABLE_TRAY = "cable_tray"
    ELECTRICAL_EQUIPMENT = "electrical_equipment"
    MECHANICAL_EQUIPMENT = "mechanical_equipment"
    SPRINKLER = "sprinkler"
    FURNITURE = "furniture"
    CASEWORK = "casework"
    GENERIC_MODEL = "generic_model"
    MASS = "mass"
    TOPOGRAPHY = "topography"
    SITE = "site"
    VIEW = "view"
    SHEET = "sheet"
    SCHEDULE = "schedule"
    FAMILY = "family"
    LEVEL = "level"
    GRID = "grid"
    REFERENCE_PLANE = "reference_plane"
    UNKNOWN = "unknown"


class RevitParameterStorageType(str, Enum):
    DOUBLE = "double"
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    ELEMENT_ID = "element_id"
    XYZ = "xyz"


class RevitParameter(BaseModel):
    parameter_id: str
    name: str
    display_name: str
    storage_type: RevitParameterStorageType
    value: Any = None
    formatted_value: str | None = None
    unit: str | None = None
    read_only: bool = False
    instance: bool = True
    is_shared: bool = False
    is_type: bool = False
    group: str | None = None


class RevitElement(BaseModel):
    element_id: int
    unique_id: str | None = None
    category: str | None = None
    category_id: int | None = None
    class_name: str | None = None
    family: str | None = None
    family_id: int | None = None
    type: str | None = None
    type_id: int | None = None
    level: str | None = None
    level_id: int | None = None
    room: str | None = None
    room_id: int | None = None
    host: str | None = None
    host_id: int | None = None
    parameters: list[RevitParameter] = []
    bounding_box: dict[str, Any] | None = None
    location: dict[str, Any] | None = None
    selected: bool = False
    visible: bool = True
    pinned: bool = False


class RevitView(BaseModel):
    view_id: int
    name: str
    view_type: str
    discipline: str | None = None
    detail_level: str | None = None
    scale: int | None = None
    crop_box_visible: bool = False
    template_id: int | None = None
    phase: str | None = None
    design_option: str | None = None


class RevitDocument(BaseModel):
    document_id: int
    name: str
    path: str | None = None
    is_workshared: bool = False
    active: bool = False
    modified: bool = False
    project_info: dict[str, Any] = {}
    phases: list[str] = []
    worksets: list[str] = []


class RevitCategory(BaseModel):
    category_id: int
    name: str
    built_in: bool = True
    element_types: list[str] = []


class RevitFamily(BaseModel):
    family_id: int
    name: str
    category: str | None = None
    types: list[str] = []
    loaded: bool = False


class RevitLevel(BaseModel):
    level_id: int
    name: str
    elevation: float | None = None
    height: float | None = None
    is_structural: bool = False
    is_ground: bool = False


class RevitConnectionInfo(BaseModel):
    state: RevitConnectionState
    revit_version: str | None = None
    build_number: str | None = None
    process_id: int | None = None
    window_title: str | None = None
    window_handle: int | None = None
    executable_path: str | None = None
    active_document: RevitDocument | None = None
    active_view: RevitView | None = None
    selected_element_ids: list[int] = []
    categories: list[RevitCategory] = []
    elements: list[RevitElement] = []
    families: list[RevitFamily] = []
    levels: list[RevitLevel] = []
    views: list[RevitView] = []
    capabilities: list[str] = []
    warnings: list[str] = []
    errors: list[str] = []


class RevitOperationResult(BaseModel):
    operation_id: str
    status: str
    result: Any = None
    error: str | None = None
    transaction_id: str | None = None
    rollback_available: bool = False
    metadata: dict[str, Any] = {}
