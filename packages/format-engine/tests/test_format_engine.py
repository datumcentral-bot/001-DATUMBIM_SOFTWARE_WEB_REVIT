from pathlib import Path
from format_engine.detector import detect_format
from format_engine.registry import registry
from format_engine.handlers.readers import GenericReader, IFCMinimalReader, StubRevitReader, StubAutoCADReader
from format_engine.handlers.parsers import GenericParser, IFCMinimalParser
from format_engine.handlers.writers import GenericWriter, JSONWriter
from format_engine.models import FileFormat, FormatCategory
from format_engine.exceptions import InvalidFileError, ParseError


def test_detect_ifc_by_extension():
    result = detect_format(Path("model.ifc"))
    assert result.format == FileFormat.IFC
    assert result.category == FormatCategory.BIM
    assert result.confidence == 0.95


def test_detect_rvt_by_extension():
    result = detect_format(Path("project.rvt"))
    assert result.format == FileFormat.RVT
    assert result.category == FormatCategory.BIM
    assert result.confidence == 0.99


def test_detect_dwg_by_extension():
    result = detect_format(Path("drawing.dwg"))
    assert result.format == FileFormat.DWG
    assert result.category == FormatCategory.CAD
    assert result.confidence == 0.99


def test_detect_json_by_extension():
    result = detect_format(Path("data.json"))
    assert result.format == FileFormat.JSON
    assert result.category == FormatCategory.DATA


def test_detect_generic_fallback():
    result = detect_format(Path("unknown.xyz"))
    assert result.format == FileFormat.GENERIC
    assert result.category == FormatCategory.DATA
    assert result.confidence == 0.1


def test_registry_detect_by_extension():
    descriptor = registry.detect_by_extension("ifc")
    assert descriptor is not None
    assert descriptor.format == "ifc"


def test_registry_list_supported():
    handlers = registry.list_supported()
    assert len(handlers) > 0
    formats = {h.format for h in handlers}
    assert "ifc" in formats
    assert "rvt" in formats
    assert "dwg" in formats


def test_generic_reader_read(tmp_path: Path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    reader = GenericReader()
    result = reader.read(file_path)
    assert result["format"] == "generic"
    assert result["filename"] == "test.txt"
    assert result["size"] == 11


def test_generic_reader_validate_missing():
    reader = GenericReader()
    assert reader.validate(Path("nonexistent.txt")) is False


def test_ifc_minimal_reader_validate_valid():
    reader = IFCMinimalReader()
    assert reader.validate(Path("valid.ifc")) is False  # file doesn't exist


def test_ifc_minimal_reader_read(tmp_path: Path):
    file_path = tmp_path / "test.ifc"
    file_path.write_text("ISO-10303-21;\nHEADER;\nENDSEC;")
    reader = IFCMinimalReader()
    result = reader.read(file_path)
    assert result["format"] == "ifc"
    assert "header" in result


def test_stub_revit_reader():
    reader = StubRevitReader()
    assert reader.format == FileFormat.RVT
    assert reader.category == FormatCategory.BIM


def test_stub_autocad_reader():
    reader = StubAutoCADReader()
    assert reader.format == FileFormat.DWG
    assert reader.category == FormatCategory.CAD


def test_generic_parser():
    parser = GenericParser()
    result = parser.parse(b"hello world")
    assert result["format"] == "generic"
    assert result["text_length"] == 11


def test_generic_parser_metadata():
    parser = GenericParser()
    meta = parser.extract_metadata(b"hello world")
    assert meta["size"] == 11


def test_ifc_minimal_parser():
    parser = IFCMinimalParser()
    result = parser.parse(b"ISO-10303-21;\nHEADER;\nENDSEC;")
    assert result["format"] == "ifc"
    assert result["line_count"] == 3


def test_json_writer(tmp_path: Path):
    writer = JSONWriter()
    output = tmp_path / "output.json"
    writer.write({"key": "value"}, output)
    assert output.exists()
    assert writer.validate_output(output) is True


def test_json_writer_validate_invalid(tmp_path: Path):
    writer = JSONWriter()
    assert writer.validate_output(tmp_path / "nonexistent.json") is False
