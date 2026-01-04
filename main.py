import subprocess
import argparse

def parse_readelf_symbol_line(line: str) -> dict[str, str] | None:
    parts = line.split()
    if len(parts) < 8:
        return None

    keys = ["num", "value", "size", "type", "bind", "vis", "ndx", "name"]
    return dict(zip(keys, parts[:8]))

def so_exported_functions(so_path: str, demangle = False) -> set[str]:

    cmd = ["readelf", "-Ws"]
    if demangle:
        cmd.append("--demangle")

    cmd.append(so_path)
    p = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )

    exported_funcs: set[str] = set()

    for line in p.stdout.splitlines():
        parsed_data = parse_readelf_symbol_line(line)
        if not parsed_data:
            continue


        if (
            parsed_data["type"] in ("FUNC", "IFUNC")
            and parsed_data["ndx"] != "UND"
            and parsed_data["bind"] in ("GLOBAL", "WEAK")
        ):
            exported_funcs.add(parsed_data["name"])

    return exported_funcs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="sotest",
                                     description="so?")
    parser.add_argument("--file", required=True, help="file")
    parser.add_argument(
        "--demangle",
        action="store_true",
        help="demangle symbol names"
    )
    args = parser.parse_args()
    exported_funcs = so_exported_functions(args.file)

    print(exported_funcs)
