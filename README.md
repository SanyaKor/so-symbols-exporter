# so-symbols-exporter

A small Python CLI tool that lists **native functions implemented inside a Linux shared object (`.so`)**.

The tool analyzes ELF symbol tables using `readelf` and reports **function symbols defined in the file itself**, excluding imported (`UND`) symbols and avoiding duplicates originating from multiple symbol tables.

Built and run using **`uv`**.

---

## Features

- Lists native functions from a `.so` file
- Supports `FUNC` and `IFUNC` symbols
- Filters out imported (`UND`) symbols
- Avoids duplicates from `.symtab` / `.dynsym`
- Optional pretty output
- Designed for CI and local inspection

---

## Requirements

### System requirements

- Linux (ELF binaries only)
- `readelf` (from `binutils`)

Install on Debian/Ubuntu:

```bash
sudo apt-get install binutils
```

### Python requirements

- Python 3.13+
- `uv`

Install `uv`:

```bash
pip install uv
```

## Building test shared libraries

Test `.so` libraries used by this project were built using `g++` with position-independent code:

```bash
g++ -fPIC -shared -o libtestc.so testlib.c
```

This produces a standard ELF shared object suitable for analysis with `readelf`.

> Libraries built on macOS (Mach-O format) are **not supported**.


---

## Usage

Run the tool using `uv`:

```bash
uv run so-symbols-exporter libexample.so
```

Help:

```bash
uv run so-symbols-exporter --help
```

---

## Help output

```text
usage: so-symbols-exporter [-h] [--pretty-output] file

List native functions defined in a Linux shared object (.so).

positional arguments:
  file              Path to the .so file

options:
  -h, --help        Show this help message and exit
  --pretty-output   Pretty-print output
```

## Pretty output example

Command:

```bash
uv run so-symbols-exporter libexample.so --pretty-output
```


Output:

```text
Exported native functions: 4

+---------------------------+--------+--------+----------+
| Name                      | Type   | Bind   | Vis      |
+---------------------------+--------+--------+----------+
| call_smth                 | FUNC   | GLOBAL | DEFAULT  |
| default_func1(int,int)    | FUNC   | GLOBAL | DEFAULT  |
| default_func1(char*)      | FUNC   | GLOBAL | DEFAULT  |
| weak_func2(char*)         | FUNC   | WEAK   | DEFAULT  |
+---------------------------+--------+--------+----------+
```

### Column description

- **Name** — function name (demangled if enabled)
- **Type** — `FUNC` or `IFUNC`
- **Bind** — `GLOBAL` (strong) or `WEAK`
- **Vis** — symbol visibility (`DEFAULT`, `HIDDEN`)

---


## Development

Sync Python dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

> Tests that rely on real ELF binaries require `binutils` to be installed on the system.

---

## Notes and limitations

- `.so` files built on macOS are Mach-O binaries and **are not supported**
- The tool works only with ELF binaries on Linux
- Output format depends on `readelf` and may vary slightly between `binutils` versions
- `uv` manages **Python dependencies only**; system tools must be installed separately

---
