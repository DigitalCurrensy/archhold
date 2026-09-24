# Copyright 2026 Digital Currensy Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Print one hold() verdict per roof row. Empty numbers are missing."""

from __future__ import annotations

import csv
import math
import subprocess
import sys
from pathlib import Path

from .arch import hold
from .hoek import lithostatic_mpa, ucs_mass_mpa
from .mesh import mesh_line
from .fea import fea_line

COLUMNS = ("span_m", "roof_m", "tensile_mpa", "crack")


def _cell(row: dict[str, str | None], name: str) -> str:
    value = row.get(name)
    if value is None:
        return ""
    return value.strip()


def _optional_float(text: str) -> float | None:
    if text == "":
        return None
    return float(text)


def _bool(text: str) -> bool:
    if text == "":
        return False
    lowered = text.casefold()
    if lowered in {"true", "yes", "y", "1"}:
        return True
    if lowered in {"false", "no", "n", "0"}:
        return False
    raise ValueError(f"not a boolean: {text}")



def _show(value: float | None) -> str:
    if value is None:
        return "missing"
    if not math.isfinite(value):
        return "bad"
    return f"{value:.10g}"


def score_row(row: dict[str, str | None]) -> str:
    return hold(
        _optional_float(_cell(row, "span_m")),
        _optional_float(_cell(row, "roof_m")),
        _optional_float(_cell(row, "tensile_mpa")),
        _bool(_cell(row, "crack")),
    )


from .record import finish


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in args
    args = [item for item in args if item != "--json"]
    if args and args[0] == "mesh":
        if len(args) != 6:
            print("usage: python -m archhold mesh SPAN ROOF DEPTH NX NZ", file=sys.stderr)
            return 2
        try:
            span, roof, depth = (float(args[1]), float(args[2]), float(args[3]))
            nx, nz = int(args[4]), int(args[5])
            if str(nx) != args[4] or str(nz) != args[5]:
                raise ValueError("not a mesh")
            print(mesh_line(span, roof, depth, nx, nz))
        except ValueError:
            print("not a mesh", file=sys.stderr)
            return 2
        return 0
    if args and args[0] == "verify":
        root = Path(__file__).resolve().parents[2]
        line = root / "examples" / "roof.line"
        sig = root / "examples" / "roof.sig"
        pub = root / "examples" / "roof.pub.pem"
        if fea_line(45, 10, 135, 3, 3) + "\n" != line.read_text(encoding="utf-8"):
            print("line moved", file=sys.stderr)
            return 1
        proc = subprocess.run(
            [
                "openssl", "pkeyutl", "-verify", "-pubin", "-inkey", str(pub),
                "-rawin", "-in", str(line), "-sigfile", str(sig),
            ],
            capture_output=True,
        )
        if proc.returncode != 0:
            print("not signed", file=sys.stderr)
            return 1
        print("verified digest")
        return 0
    if args and args[0] == "fea":
        if len(args) != 6:
            print("usage: python -m archhold fea SPAN ROOF DEPTH NX NZ", file=sys.stderr)
            return 2
        try:
            span, roof, depth = (float(args[1]), float(args[2]), float(args[3]))
            nx, nz = int(args[4]), int(args[5])
            if str(nx) != args[4] or str(nz) != args[5]:
                raise ValueError("not a mesh")
            print(fea_line(span, roof, depth, nx, nz))
        except ValueError:
            print("not a mesh", file=sys.stderr)
            return 2
        return 0
    if len(args) != 1:
        print("usage: python -m archhold <csv>", file=sys.stderr)
        return 2
    path = Path(args[0])
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        names = [name.strip() for name in (reader.fieldnames or [])]
        allowed = {tuple(COLUMNS), tuple(COLUMNS) + ("depth_m",)}
        if tuple(names) not in allowed:
            print(
                "csv columns must be span_m,roof_m,tensile_mpa,crack",
                file=sys.stderr,
            )
            return 2
        strength = f"{ucs_mass_mpa():.10g}"
        lines: list[str] = []
        words: list[str] = []
        for row in reader:
            if all(not (value or "").strip() for value in row.values()):
                continue
            span = _optional_float(_cell(row, "span_m"))
            roof = _optional_float(_cell(row, "roof_m"))
            tensile = _optional_float(_cell(row, "tensile_mpa"))
            crack = _bool(_cell(row, "crack"))
            depth = _optional_float(_cell(row, "depth_m")) if "depth_m" in names else None
            word = hold(span, roof, tensile, crack, depth)
            if depth is None:
                lith = "unset"
            else:
                lith = _show(lithostatic_mpa(depth)) if depth >= 0 else "bad"
            lines.append(
                f"{word} span={_show(span)} roof={_show(roof)} tensile={_show(tensile)} "
                f"crack={'true' if crack else 'false'} ucs={strength} lithostatic={lith}"
            )
            words.append(word)
    return finish("archhold", "Ok is not a keep. Full burial does not balance.", lines, as_json, words)


if __name__ == "__main__":
    raise SystemExit(main())
