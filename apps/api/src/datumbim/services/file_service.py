import hashlib
import uuid
from pathlib import Path
from typing import Any
from format_engine.detector import detect_format
from format_engine.registry import registry
from format_engine.handlers.readers import GenericReader, IFCMinimalReader, StubRevitReader, StubAutoCADReader
from format_engine.models import FileFormat, ImportResult


class FileService:
    def __init__(self, storage: Any):
        self.storage = storage

    def detect_format(self, filename: str, content_type: str | None = None) -> dict[str, Any]:
        path = Path(filename)
        result = detect_format(path, mime_type=content_type)
        return {
            "format": result.format.value,
            "category": result.category.value,
            "confidence": result.confidence,
            "mime_type": result.mime_type,
            "metadata": result.metadata,
        }

    def compute_checksum(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def validate_path(self, filename: str) -> dict[str, Any]:
        path = Path(filename)
        issues = []
        if ".." in path.parts or any(part == ".." for part in path.parts):
            issues.append("Path traversal detected")
        if path.is_absolute():
            issues.append("Absolute paths not allowed")
        if path.suffix.lower() not in {".ifc", ".rvt", ".rfa", ".dwg", ".dxf", ".nwd", ".nwc", ".pdf", ".csv", ".xlsx", ".json", ".xml", ".gltf", ".glb", ".obj", ".fbx", ".step", ".stp", ".stl", ".png", ".jpg", ".jpeg", ".svg"}:
            issues.append(f"Unsupported extension: {path.suffix}")
        return {"valid": len(issues) == 0, "issues": issues}

    def import_file(self, file_bytes: bytes, filename: str, project_id: int | None = None) -> ImportResult:
        validation = self.validate_path(filename)
        if not validation["valid"]:
            return ImportResult(
                success=False,
                format=FileFormat.GENERIC,
                errors=validation["issues"],
            )

        detection = self.detect_format(filename)
        fmt = detection["format"]

        reader = None
        if fmt == "ifc":
            reader = IFCMinimalReader()
        elif fmt == "rvt":
            reader = StubRevitReader()
        elif fmt == "dwg":
            reader = StubAutoCADReader()
        else:
            reader = GenericReader()

        try:
            temp_path = Path(f"/tmp/{uuid.uuid4()}_{filename}")
            temp_path.write_bytes(file_bytes)
            raw = reader.read(temp_path)
            temp_path.unlink(missing_ok=True)
        except Exception as exc:
            return ImportResult(
                success=False,
                format=FileFormat(fmt),
                errors=[str(exc)],
            )

        return ImportResult(
            success=True,
            format=FileFormat(fmt),
            metadata={
                "filename": filename,
                "size": len(file_bytes),
                "checksum": self.compute_checksum(file_bytes),
                "preview": raw.get("header") or raw.get("preview") or raw.get("note"),
                "project_id": project_id,
            },
        )
