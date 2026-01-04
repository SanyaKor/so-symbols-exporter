import subprocess
import argparse
import sys
from so_symbols_exporter import so_exported_functions

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="sotest", description="so?")
    parser.add_argument("--file", required=True, help="file")

    parser.add_argument(
        "--pretty-output",
        action="store_true",
        help="pretty output"
    )
    args = parser.parse_args()

    try:
        ex_symbols = so_exported_functions(args.file)
        if args.pretty_output:
            print_table(ex_symbols)
        else:
            for f in ex_symbols:
                print(f["name"])

    except subprocess.CalledProcessError as e:
        err = (e.stderr or e.stdout or "").strip()
        print(f"ERROR: readelf failed\n{err}", file=sys.stderr)
        exit()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        exit()





