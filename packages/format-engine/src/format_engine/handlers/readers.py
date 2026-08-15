from pathlib import Path
from typing import Any
from format_engine.models import FormatReader, FileFormat, FormatCategory
from format_engine.exceptions import UnsupportedFormatError, InvalidFileError


class GenericReader:
    format = FileFormat.GENERIC
    category = FormatCategory.DATA

    def read(self, path: Path, **options: Any) -> dict[str, Any]:
        if not path.exists() or not path.is_file():
            raise InvalidFileError(f"File not found: {path}")
        data = path.read_bytes()
        return {
            "format": self.format.value,
            "filename": path.name,
            "size": path.stat().st_size,
            "raw_data": data,
        }

    def validate(self, path: Path) -> bool:
        return path.exists() and path.is_file()


class IFCMinimalReader:
    format = FileFormat.IFC
    category = FormatCategory.BIM

    def read(self, path: Path, **options: Any) -> dict[str, Any]:
        if not path.exists() or not path.is_file():
            raise InvalidFileError(f"File not found: {path}")
        content = path.read_text(errors="ignore")
        lines = content.splitlines()
        header = lines[:10] if lines else []
        return {
            "format": self.format.value,
            "filename": path.name,
            "size": path.stat().st_size,
            "header": header,
            "line_count": len(lines),
            "note": "Minimal ICF reader — full parsing requires ifcopenshell",
        }

    def validate(self, path: Path) -> bool:
        if not path.exists() or not path.is_file():
            return False
        try:
            with open(path, "r", errors="ignore") as f:
                first_line = f.readline()
            return "ISO-10303-21" in first_line or "HEADER" in first_line
        except Exception:
            return False


class StubRevitReader:
    format = FileFormat.RVT
    category = FormatCategory.BIM

    def read(self, path: Path, **options: Any) -> dict[str, Any]:
        if not path.exists() or not path.is_file():
            raise InvalidFileError(f"File not found: {path}")
        return {
            "format": self.format.value,
            "filename": path.name,
            "size": path.stat().st_size,
            "note": "Revit reader requires APS / Revit API — stub only",
        }

    def validate(self, path: Path) -> bool:
        return path.exists() and path.suffix.lower() == ".rvt"


class StubAutoCADReader:
    format = FileFormat.DWG
    category = FormatCategory.CAD

    def read(self, path: Path, **options: Any) -> dict[str, Any]:
        if not path.exists() or not path.is_file():
            raise InvalidFileError(f"File not found: {path}")
        return {
            "format": self.format.value,
            "filename": path.name,
            "size": path.stat().st_size,
            "note": "AutoCAD reader requires AutoCAD API / ODA — stub only",
        }

    def validate(self, path: Path) -> bool:
        return path.exists() and path.suffix.lower() == ".dwg"
