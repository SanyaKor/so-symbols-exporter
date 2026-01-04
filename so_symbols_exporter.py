import subprocess

def parse_readelf_symbol_line(line: str) -> dict[str, str] | None:
    parts = line.split()
    if len(parts) < 8:
        return None

    num, value, size, sym_type, bind, vis, ndx = parts[:7]
    name = " ".join(parts[7:])

    return {
        "num": num,
        "value": value,
        "size": size,
        "type": sym_type,
        "bind": bind,
        "vis": vis,
        "ndx": ndx,
        "name": name,
    }

### NOTES
# U Can also try "nm" command https://linux.die.net/man/1/nm .
# But personally i would prefer readelf, since there is much information about files, and structure of output is stable(Fixed table)
def so_exported_functions(so_path: str, demangle : bool = True) -> list[dict[str, str]] | None:

    cmd = ["readelf", "-Ws", "--syms"]
    if demangle:
        cmd.append("--demangle")

    cmd.append(so_path)
    p = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )

    exported_symbols: list[dict[str, str]] = []

    in_symtab = False

    for line in p.stdout.splitlines():
        s = line.strip()

        if s.startswith("Symbol table '"):
            in_symtab = "'.symtab'" in s
            continue
        if not in_symtab:
            continue

        parsed_data = parse_readelf_symbol_line(line)
        if not parsed_data:
            continue

        if (
                parsed_data["type"] in ("FUNC", "IFUNC")
                and parsed_data["ndx"] != "UND"
                and parsed_data["bind"] in ("GLOBAL", "WEAK")
        ):
            exported_symbols.append({
                "name": parsed_data["name"],
                "type": parsed_data["type"],
                "bind": parsed_data["bind"],
                "vis": parsed_data["vis"],
            })

    exported_symbols.sort(key=lambda x: x["name"])
    return exported_symbols