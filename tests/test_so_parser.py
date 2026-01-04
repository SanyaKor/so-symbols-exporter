from so_symbols_exporter import so_exported_functions, parse_readelf_symbol_line
from pathlib import Path


def test_parser():
    line = "  12: 0000000000001139   34 FUNC GLOBAL DEFAULT   13 func1(int, int)"
    parsed = parse_readelf_symbol_line(line)
    assert parsed is not None
    assert parsed["type"] == "FUNC"
    assert parsed["bind"] == "GLOBAL"
    assert parsed["vis"] == "DEFAULT"
    assert parsed["ndx"] == "13"
    assert parsed["name"] == "func1(int, int)"


def test_parser_missing_fields_returns_none():

    assert parse_readelf_symbol_line("") is None

    assert parse_readelf_symbol_line("Num: Value Size Type Bind Vis Ndx Name") is None

    assert parse_readelf_symbol_line("  12: 0000000000001139") is None
    assert parse_readelf_symbol_line("  12: 0000000000001139 34 FUNC") is None
    assert parse_readelf_symbol_line("  12: 0000000000001139 34 FUNC GLOBAL") is None
    assert parse_readelf_symbol_line("  12: 0000000000001139 34 FUNC GLOBAL DEFAULT") is None
    assert parse_readelf_symbol_line("  12: 0000000000001139 34 FUNC GLOBAL DEFAULT 13") is None  # нет Name

    assert parse_readelf_symbol_line("just garbage line") is None

def test_exporter_functions():
    export_symbols = so_exported_functions(
        str(Path(__file__).resolve().parents[1] / "sample" / "libtestc.so")
    )

    assert export_symbols is not None
    assert len(export_symbols) == 6


def test_duplication():
    export_symbols = so_exported_functions(
        str(Path(__file__).resolve().parents[1] / "sample" / "libtestc.so")
    )

    names = [s["name"] for s in export_symbols]

    assert len(names) == len(set(names)), f"duplicates found: {names}"





