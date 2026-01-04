import subprocess
import argparse
import sys

def print_table(symbols: list[dict[str, str]]) -> None:

    if not symbols:
        print("(no exported functions)")
        return

    name_w = max(len(s["name"]) for s in symbols)
    name_w = max(name_w, 20)

    header = f"{'NAME'.ljust(name_w)}  TYPE   BIND   VIS"

    print(header)
    print("-" * len(header))

    for s in symbols:
        print(
            f"{s['name'].ljust(name_w)}  "
            f"{s['type'].ljust(6)} "
            f"{s['bind'].ljust(6)} "
            f"{s['vis']}"
        )

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

def so_exported_functions(so_path: str, demangle : bool = False) -> list[dict[str, str]] | None:

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

    exported_funcs: list[dict[str, str]] = []

    for line in p.stdout.splitlines():
        parsed_data = parse_readelf_symbol_line(line)
        if not parsed_data:
            continue


        if (
            parsed_data["type"] in ("FUNC", "IFUNC")
            and parsed_data["ndx"] != "UND"
            and parsed_data["bind"] in ("GLOBAL", "WEAK")
        ):
            exported_funcs.append({
                "name": parsed_data["name"],
                "type": parsed_data["type"],
                "bind": parsed_data["bind"],
                "vis": parsed_data["vis"],
            })

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
    parser.add_argument(
        "--pretty-output",
        action="store_true",
        help="pretty output"
    )
    args = parser.parse_args()

    try:
        names = so_exported_functions(args.file, demangle=args.demangle)
        if args.pretty_output:
            print_table(names)
        else:
            print(names)

    except subprocess.CalledProcessError as e:
        err = (e.stderr or e.stdout or "").strip()
        print(f"ERROR: readelf failed\n{err}", file=sys.stderr)
        exit()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        exit()





