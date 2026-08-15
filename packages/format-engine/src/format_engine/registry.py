from typing import Any
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class FormatHandlerDescriptor:
    format: str
    category: str
    extensions: list[str]
    mime_types: list[str]
    reader: Any | None = None
    parser: Any | None = None
    writer: Any | None = None
    detector: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class FormatRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, FormatHandlerDescriptor] = {}
        self._extensions: dict[str, str] = {}
        self._mime_types: dict[str, str] = {}

    def register(self, descriptor: FormatHandlerDescriptor) -> None:
        self._handlers[descriptor.format] = descriptor
        for ext in descriptor.extensions:
            self._extensions[ext.lower()] = descriptor.format
        for mime in descriptor.mime_types:
            self._mime_types[mime.lower()] = descriptor.format

    def get_handler(self, format_name: str) -> FormatHandlerDescriptor | None:
        return self._handlers.get(format_name.lower())

    def detect_by_extension(self, extension: str) -> FormatHandlerDescriptor | None:
        format_name = self._extensions.get(extension.lower().lstrip("."))
        if format_name:
            return self._handlers.get(format_name)
        return None

    def detect_by_mime(self, mime_type: str) -> FormatHandlerDescriptor | None:
        format_name = self._mime_types.get(mime_type.lower())
        if format_name:
            return self._handlers.get(format_name)
        return None

    def list_supported(self) -> list[FormatHandlerDescriptor]:
        return list(self._handlers.values())


registry = FormatRegistry()
