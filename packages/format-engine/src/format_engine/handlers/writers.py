from pathlib import Path
from typing import Any
from format_engine.models import FormatWriter, FileFormat, FormatCategory
from format_engine.exceptions import WriteError


class GenericWriter:
    format = FileFormat.GENERIC
    category = FormatCategory.DATA

    def write(self, data: dict[str, Any], path: Path, **options: Any) -> None:
        try:
            content = str(data.get("content", ""))
            path.write_text(content, encoding="utf-8")
        except Exception as exc:
            raise WriteError(f"Failed to write generic file: {exc}") from exc

    def validate_output(self, path: Path) -> bool:
        return path.exists() and path.is_file()


class JSONWriter:
    format = FileFormat.JSON
    category = FormatCategory.DATA

    def write(self, data: dict[str, Any], path: Path, **options: Any) -> None:
        import json
        try:
            path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        except Exception as exc:
            raise WriteError(f"Failed to write JSON file: {exc}") from exc

    def validate_output(self, path: Path) -> bool:
        if not path.exists() or not path.is_file():
            return False
        try:
            import json
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
            return True
        except Exception:
            return False
