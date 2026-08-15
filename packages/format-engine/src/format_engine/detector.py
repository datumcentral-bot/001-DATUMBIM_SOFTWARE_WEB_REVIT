from pathlib import Path
from typing import Any
from format_engine.models import FormatDetectionResult, FileFormat, FormatCategory
from format_engine.registry import registry


EXTENSION_MAP: dict[str, tuple[FileFormat, FormatCategory, float]] = {
    ".ifc": (FileFormat.IFC, FormatCategory.BIM, 0.95),
    ".rvt": (FileFormat.RVT, FormatCategory.BIM, 0.99),
    ".rfa": (FileFormat.RVT, FormatCategory.BIM, 0.99),
    ".dwg": (FileFormat.DWG, FormatCategory.CAD, 0.99),
    ".dxf": (FileFormat.DXF, FormatCategory.CAD, 0.99),
    ".nwd": (FileFormat.NWD, FormatCategory.MODEL, 0.95),
    ".nwc": (FileFormat.NWC, FormatCategory.MODEL, 0.95),
    ".pdf": (FileFormat.PDF, FormatCategory.DOCUMENT, 0.99),
    ".csv": (FileFormat.CSV, FormatCategory.DATA, 0.99),
    ".xlsx": (FileFormat.XLSX, FormatCategory.DATA, 0.99),
    ".json": (FileFormat.JSON, FormatCategory.DATA, 0.95),
    ".xml": (FileFormat.XML, FormatCategory.DATA, 0.95),
    ".gltf": (FileFormat.GLTF, FormatCategory.MODEL, 0.99),
    ".glb": (FileFormat.GLB, FormatCategory.MODEL, 0.99),
    ".obj": (FileFormat.OBJ, FormatCategory.MODEL, 0.95),
    ".fbx": (FileFormat.FBX, FormatCategory.MODEL, 0.95),
}

MIME_MAP: dict[str, tuple[FileFormat, FormatCategory]] = {
    "application/octet-stream": (FileFormat.GENERIC, FormatCategory.DATA),
    "application/json": (FileFormat.JSON, FormatCategory.DATA),
    "text/xml": (FileFormat.XML, FormatCategory.DATA),
    "text/csv": (FileFormat.CSV, FormatCategory.DATA),
    "application/pdf": (FileFormat.PDF, FormatCategory.DOCUMENT),
    "image/vnd.dwg": (FileFormat.DWG, FormatCategory.CAD),
    "image/vnd.dxf": (FileFormat.DXF, FormatCategory.CAD),
}


def detect_format(path: Path, mime_type: str | None = None, content_sample: bytes | None = None) -> FormatDetectionResult:
    suffix = path.suffix.lower()
    if suffix in EXTENSION_MAP:
        fmt, category, confidence = EXTENSION_MAP[suffix]
        return FormatDetectionResult(
            format=fmt,
            category=category,
            confidence=confidence,
            mime_type=mime_type,
            metadata={"detected_by": "extension", "extension": suffix},
        )

    if mime_type and mime_type.lower() in MIME_MAP:
        fmt, category = MIME_MAP[mime_type.lower()]
        return FormatDetectionResult(
            format=fmt,
            category=category,
            confidence=0.7,
            mime_type=mime_type,
            metadata={"detected_by": "mime_type", "mime_type": mime_type},
        )

    handler = registry.detect_by_extension(suffix)
    if handler:
        return FormatDetectionResult(
            format=FileFormat(handler.format),
            category=FormatCategory(handler.category),
            confidence=0.8,
            mime_type=mime_type,
            metadata={"detected_by": "registry", "extension": suffix},
        )

    return FormatDetectionResult(
        format=FileFormat.GENERIC,
        category=FormatCategory.DATA,
        confidence=0.1,
        mime_type=mime_type,
        metadata={"detected_by": "fallback"},
    )
