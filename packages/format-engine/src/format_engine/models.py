from typing import Protocol, runtime_checkable, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import uuid


class FormatCategory(str, Enum):
    BIM = "bim"
    CAD = "cad"
    MODEL = "model"
    DOCUMENT = "document"
    DATA = "data"


class FileFormat(str, Enum):
    IFC = "ifc"
    RVT = "rvt"
    DWG = "dwg"
    DXF = "dxf"
    NWD = "nwd"
    NWC = "nwc"
    PDF = "pdf"
    CSV = "csv"
    XLSX = "xlsx"
    JSON = "json"
    XML = "xml"
    GLTF = "gltf"
    GLB = "glb"
    OBJ = "obj"
    FBX = "fbx"
    GENERIC = "generic"


@dataclass
class FormatDetectionResult:
    format: FileFormat
    category: FormatCategory
    confidence: float
    mime_type: str | None = None
    encoding: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ImportResult:
    success: bool
    format: FileFormat
    elements_imported: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class FormatReader(Protocol):
    format: FileFormat

    def read(self, path: Path, **options: Any) -> dict[str, Any]:
        ...

    def validate(self, path: Path) -> bool:
        ...


@runtime_checkable
class FormatParser(Protocol):
    format: FileFormat

    def parse(self, raw_data: bytes, **options: Any) -> dict[str, Any]:
        ...

    def extract_metadata(self, raw_data: bytes) -> dict[str, Any]:
        ...


@runtime_checkable
class FormatWriter(Protocol):
    format: FileFormat

    def write(self, data: dict[str, Any], path: Path, **options: Any) -> None:
        ...

    def validate_output(self, path: Path) -> bool:
        ...
