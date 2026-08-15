from pathlib import Path
from typing import Any
from format_engine.models import FormatParser, FileFormat, FormatCategory
from format_engine.exceptions import ParseError


class GenericParser:
    format = FileFormat.GENERIC
    category = FormatCategory.DATA

    def parse(self, raw_data: bytes, **options: Any) -> dict[str, Any]:
        try:
            text = raw_data.decode("utf-8", errors="ignore")
        except Exception as exc:
            raise ParseError(f"Failed to decode generic data: {exc}") from exc
        return {
            "format": self.format.value,
            "text_length": len(text),
            "preview": text[:200],
        }

    def extract_metadata(self, raw_data: bytes) -> dict[str, Any]:
        return {
            "size": len(raw_data),
        }


class IFCMinimalParser:
    format = FileFormat.IFC
    category = FormatCategory.BIM

    def parse(self, raw_data: bytes, **options: Any) -> dict[str, Any]:
        try:
            text = raw_data.decode("utf-8", errors="ignore")
        except Exception as exc:
            raise ParseError(f"Failed to decode IFC data: {exc}") from exc
        lines = text.splitlines()
        return {
            "format": self.format.value,
            "line_count": len(lines),
            "header_lines": lines[:20],
            "note": "Minimal IFC parser — full parsing requires ifcopenshell",
        }

    def extract_metadata(self, raw_data: bytes) -> dict[str, Any]:
        try:
            text = raw_data.decode("utf-8", errors="ignore")
            lines = text.splitlines()
            return {
                "header": lines[:10],
                "size": len(raw_data),
            }
        except Exception:
            return {"size": len(raw_data)}
