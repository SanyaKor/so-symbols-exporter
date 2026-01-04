from so_symbols_exporter import so_exported_functions, parse_readelf_symbol_line
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_parser():
    line = "  12: 0000000000001139   34 FUNC GLOBAL DEFAULT   13 func1(int, int)"
    parsed = parse_readelf_symbol_line(line)
    assert parsed is not None
    assert parsed["type"] == "FUNC"
    assert parsed["bind"] == "GLOBAL"
    assert parsed["vis"] == "DEFAULT"
    assert parsed["ndx"] == "13"
    assert parsed["name"] == "func1(int, int)"

def test_exporter_functions():
    export_symbols = so_exported_functions(str(ROOT / "sample" / "libtestc.so"))

    assert export_symbols is not None
    assert len(export_symbols) == 6


