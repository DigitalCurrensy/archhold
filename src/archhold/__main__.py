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
import sys
from pathlib import Path

from .arch import hold
from .hoek import lithostatic_mpa, ucs_mass_mpa

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


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
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
            print(
                f"{word} span={_show(span)} roof={_show(roof)} tensile={_show(tensile)} "
                f"crack={'true' if crack else 'false'} ucs={strength} lithostatic={lith}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
