from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class RevitConnectionState(str, Enum):
    NOT_RUNNING = "not_running"
    NOT_CONNECTED = "not_connected"
    API_UNAVAILABLE = "api_unavailable"
    CAPABILITY_UNAVAILABLE = "capability_unavailable"
    AVAILABLE = "available"
    CONNECTED = "connected"
    ERROR = "error"


class RevitCategoryGroup(str, Enum):
    ARCHITECTURAL = "architectural"
    STRUCTURAL = "structural"
    MEP = "mep"
    SITE = "site"
    DOCUMENT = "document"
    VIEW = "view"
    FAMILY = "family"
    PARAMETER = "parameter"
    GENERAL = "general"


class RevitElementType(str, Enum):
    WALL = "wall"
    DOOR = "door"
    WINDOW = "window"
    FLOOR = "floor"
    ROOF = "roof"
    CEILING = "ceiling"
    CURTAIN_WALL = "curtain_wall"
    CURTAIN_PANEL = "curtain_panel"
    CURTAIN_MULLION = "curtain_mullion"
    ROOM = "room"
    AREA = "area"
    SPACE = "space"
    FURNITURE = "furniture"
    CASEWORK = "casework"
    GENERIC_MODEL = "generic_model"
    SPECIALTY_EQUIPMENT = "specialty_equipment"
    PLUMBING_FIXTURE = "plumbing_fixture"
    PLANTING = "planting"
    ENTOURAGE = "entourage"
    MASS = "mass"
    STAIRS = "stairs"
    RAMP = "ramp"
    RAILING = "railing"
    TOPOGRAPHY = "topography"
    SITE = "site"
    BUILDING_PAD = "building_pad"
    STRUCTURAL_WALL = "structural_wall"
    STRUCTURAL_FLOOR = "structural_floor"
    STRUCTURAL_COLUMN = "structural_column"
    STRUCTURAL_FRAMING = "structural_framing"
    BEAM = "beam"
    BRACE = "brace"
    FOUNDATION = "foundation"
    FOOTING = "footing"
    STRUCTURAL_CONNECTION = "structural_connection"
    REBAR = "rebar"
    REBAR_SET = "rebar_set"
    FABRIC_REINFORCEMENT = "fabric_reinforcement"
    TENDON = "tendon"
    ANALYTICAL_MEMBER = "analytical_member"
    ANALYTICAL_NODE = "analytical_node"
    TRUSS = "truss"
    DUCT = "duct"
    DUCT_FITTING = "duct_fitting"
    DUCT_ACCESSORY = "duct_accessory"
    AIR_TERMINAL = "air_terminal"
    MECHANICAL_EQUIPMENT = "mechanical_equipment"
    FLEX_DUCT = "flex_duct"
    DUCT_INSULATION = "duct_insulation"
    DUCT_LINING = "duct_lining"
    PIPE = "pipe"
    PIPE_FITTING = "pipe_fitting"
    PIPE_ACCESSORY = "pipe_accessory"
    FLEX_PIPE = "flex_pipe"
    SPRINKLER = "sprinkler"
    PIPE_INSULATION = "pipe_insulation"
    ELECTRICAL_EQUIPMENT = "electrical_equipment"
    ELECTRICAL_FIXTURE = "electrical_fixture"
    LIGHTING_FIXTURE = "lighting_fixture"
    LIGHTING_DEVICE = "lighting_device"
    CABLE_TRAY = "cable_tray"
    CABLE_TRAY_FITTING = "cable_tray_fitting"
    CONDUIT = "conduit"
    CONDUIT_FITTING = "conduit_fitting"
    ELECTRICAL_CIRCUIT = "electrical_circuit"
    PANEL = "panel"
    TRANSFORMER = "transformer"
    SWITCHGEAR = "switchgear"
    FIRE_ALARM_DEVICE = "fire_alarm_device"
    FIRE_PROTECTION_EQUIPMENT = "fire_protection_equipment"
    FIRE_PROTECTION_PIPE = "fire_protection_pipe"
    UNKNOWN = "unknown"


class RevitViewType(str, Enum):
    VIEW_3D = "3d_view"
    FLOOR_PLAN = "floor_plan"
    CEILING_PLAN = "ceiling_plan"
    ENGINEERING_PLAN = "engineering_plan"
    ELEVATION = "elevation"
    SECTION = "section"
    DETAIL = "detail"
    DRAFTING = "drafting"
    SCHEDULE = "schedule"
    SHEET = "sheet"
    LEGEND = "legend"
    WALKTHROUGH = "walkthrough"
    RENDERING = "rendering"
    CALLOUT = "callout"
    DEPENDENT_VIEW = "dependent_view"
    VIEW_TEMPLATE = "view_template"


class RevitFamilyType(str, Enum):
    LOADABLE = "loadable"
    SYSTEM = "system"
    IN_PLACE = "in_place"
    NESTED = "nested"
    SHARED = "shared"


class RevitParameterStorageType(str, Enum):
    DOUBLE = "double"
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    ELEMENT_ID = "element_id"
    XYZ = "xyz"
    MILLIMETERS = "millimeters"
    METERS = "meters"
    DEGREES = "degrees"


class RevitParameterType(str, Enum):
    BUILTIN = "builtin"
    SHARED = "shared"
    PROJECT = "project"
    FAMILY = "family"
    TYPE_PARAMETER = "type_parameter"
    INSTANCE_PARAMETER = "instance_parameter"
    GLOBAL = "global"
    MATERIAL = "material"


class RevitRelationshipType(str, Enum):
    HOST = "host"
    LEVEL = "level"
    VIEW = "view"
    SHEET = "sheet"
    FAMILY = "family"
    TYPE = "type"
    MATERIAL = "material"
    SYSTEM = "system"
    LINK = "link"
    WORKSHARING = "worksharing"
    DEPENDENT = "dependent"


class RevitOperationGroup(str, Enum):
    PROJECT = "project"
    DOCUMENT = "document"
    ELEMENT = "element"
    PARAMETER = "parameter"
    VIEW = "view"
    FAMILY = "family"
    MEP = "mep"
    STRUCTURAL = "structural"
    SELECTION = "selection"
    TRANSACTION = "transaction"


class RevitParameter(BaseModel):
    parameter_id: str
    name: str
    display_name: str
    storage_type: RevitParameterStorageType
    parameter_type: RevitParameterType
    value: Any = None
    formatted_value: str | None = None
    unit: str | None = None
    read_only: bool = False
    instance: bool = True
    group: str | None = None
    definition: str | None = None
    shared: bool = False


class RevitProperty(BaseModel):
    property_id: str
    name: str
    value: Any
    unit: str | None = None
    read_only: bool = True


class RevitCategory(BaseModel):
    category_id: str
    name: str
    group: RevitCategoryGroup
    built_in: bool = True
    element_types: list[RevitElementType] = []


class RevitClass(BaseModel):
    class_id: str
    name: str
    category_id: str | None = None
    base_class: str | None = None
    abstract: bool = False
    properties: list[RevitProperty] = []


class RevitElement(BaseModel):
    element_id: str
    unique_id: str | None = None
    category_id: str | None = None
    category_name: str | None = None
    class_name: str | None = None
    family_id: str | None = None
    family_name: str | None = None
    type_id: str | None = None
    type_name: str | None = None
    level_id: str | None = None
    level_name: str | None = None
    room_id: str | None = None
    host_id: str | None = None
    parameters: list[RevitParameter] = []
    properties: list[RevitProperty] = []
    relationships: list["RevitRelationship"] = []
    selected: bool = False
    visible: bool = True


class RevitFamily(BaseModel):
    family_id: str
    name: str
    family_type: RevitFamilyType
    category_id: str | None = None
    category_name: str | None = None
    types: list["RevitFamilyTypeModel"] = []
    parameters: list[RevitParameter] = []
    loaded: bool = False
    editable: bool = False


class RevitFamilyTypeModel(BaseModel):
    type_id: str
    name: str
    family_id: str
    parameters: list[RevitParameter] = []


class RevitLevel(BaseModel):
    level_id: str
    name: str
    elevation: float | None = None
    height: float | None = None
    is_structural: bool = False
    is_ground: bool = False


class RevitView(BaseModel):
    view_id: str
    name: str
    view_type: RevitViewType
    discipline: str | None = None
    detail_level: str | None = None
    scale: int | None = None
    crop_box_visible: bool = False
    template_id: str | None = None
    phase: str | None = None
    design_option: str | None = None
    dependent_on: str | None = None


class RevitDocument(BaseModel):
    document_id: str
    name: str
    path: str | None = None
    is_workshared: bool = False
    active: bool = False
    modified: bool = False
    project_info: dict[str, Any] = {}
    phases: list[str] = []
    worksets: list[str] = []


class RevitRelationship(BaseModel):
    relationship_id: str
    relationship_type: RevitRelationshipType
    source_id: str
    target_id: str
    metadata: dict[str, Any] = {}


class RevitCapability(BaseModel):
    capability_id: str
    name: str
    group: RevitOperationGroup
    description: str | None = None
    available: bool = False
    requires_transaction: bool = False
    read_only: bool = True
    risk_level: str = "low"
    parameters: list[str] = []


class RevitOperation(BaseModel):
    operation_id: str
    capability_id: str
    name: str
    description: str | None = None
    parameters: dict[str, Any] = {}
    returns: str | None = None
    risk_level: str = "low"
    approval_required: bool = False
    reversible: bool = True


class RevitModelInfo(BaseModel):
    project_name: str | None = None
    document_name: str | None = None
    revit_version: str | None = None
    connection_state: RevitConnectionState = RevitConnectionState.NOT_RUNNING
    categories: list[RevitCategory] = []
    levels: list[RevitLevel] = []
    views: list[RevitView] = []
    documents: list[RevitDocument] = []
    families: list[RevitFamily] = []
    elements: list[RevitElement] = []
    capabilities: list[RevitCapability] = []
    warnings: list[str] = []
