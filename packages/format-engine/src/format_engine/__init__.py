from format_engine.models import (
    FileFormat,
    FormatCategory,
    FormatDetectionResult,
    FormatReader,
    FormatParser,
    FormatWriter,
    ImportResult,
)
from format_engine.registry import FormatRegistry, FormatHandlerDescriptor, registry
from format_engine.detector import detect_format
from format_engine.exceptions import FormatEngineError, UnsupportedFormatError, InvalidFileError, ParseError, WriteError
from format_engine.handlers import (
    GenericReader,
    IFCMinimalReader,
    StubRevitReader,
    StubAutoCADReader,
    GenericParser,
    IFCMinimalParser,
    GenericWriter,
    JSONWriter,
)


registry.register(
    FormatHandlerDescriptor(
        format=GenericReader.format.value,
        category=GenericReader.category.value,
        extensions=[GenericReader.format.value],
        mime_types=["application/octet-stream"],
        reader=GenericReader(),
        parser=GenericParser(),
        writer=GenericWriter(),
    )
)

registry.register(
    FormatHandlerDescriptor(
        format=IFCMinimalReader.format.value,
        category=IFCMinimalReader.category.value,
        extensions=[IFCMinimalReader.format.value, "ifcxml"],
        mime_types=[],
        reader=IFCMinimalReader(),
        parser=IFCMinimalParser(),
    )
)

registry.register(
    FormatHandlerDescriptor(
        format=StubRevitReader.format.value,
        category=StubRevitReader.category.value,
        extensions=[StubRevitReader.format.value, "rfa"],
        mime_types=[],
        reader=StubRevitReader(),
    )
)

registry.register(
    FormatHandlerDescriptor(
        format=StubAutoCADReader.format.value,
        category=StubAutoCADReader.category.value,
        extensions=[StubAutoCADReader.format.value, "dxf"],
        mime_types=[],
        reader=StubAutoCADReader(),
    )
)

registry.register(
    FormatHandlerDescriptor(
        format=JSONWriter.format.value,
        category=JSONWriter.category.value,
        extensions=[JSONWriter.format.value],
        mime_types=["application/json"],
        writer=JSONWriter(),
    )
)

__all__ = [
    "FileFormat",
    "FormatCategory",
    "FormatDetectionResult",
    "FormatReader",
    "FormatParser",
    "FormatWriter",
    "ImportResult",
    "FormatHandlerDescriptor",
    "FormatRegistry",
    "registry",
    "detect_format",
    "FormatEngineError",
    "UnsupportedFormatError",
    "InvalidFileError",
    "ParseError",
    "WriteError",
    "GenericReader",
    "IFCMinimalReader",
    "StubRevitReader",
    "StubAutoCADReader",
    "GenericParser",
    "IFCMinimalParser",
    "GenericWriter",
    "JSONWriter",
]



