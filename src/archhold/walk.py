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

"""One bad vault. Mare Tranquillitatis west arch walked. Blair FEM named, not run. Wagner pits named, not roofs."""

from __future__ import annotations

import math

from .arch import hold
from .score import SURVEYS, fem_run
from .vaults import BEAM, BLAIR, MHP, MTP

MOON_RADIUS_M = 1_737_400

MTP_WALK = {
    "id": "ARCH-MTP-WEST",
    "lat": 8.3355,
    "lon": 33.222,
    "frame": "Carrer et al. Nat. Astron. 2024 Mini-RF",
    "wagner": (8.336, 33.222),
    "carrer_m": 15,
    "west_void_m": 40,
    "span_m": 45.0,
    "span_unc_m": 7.5,
    "roof_lo_m": 135.0,
    "roof_hi_m": 175.0,
    "fem": True,
    "fem_run": False,
    "pit_is_roof": False,
}

FEM = {
    "name": "Blair 2017 FEM",
    "engine": "ABAQUS",
    "cite": "Blair et al. Icarus 282 47-55 (2017)",
    "gsi": 70,
    "poisson": 0.25,
    "lithostatic_keystone": True,
    "span_max_m": 5000,
    "span_max_poisson_m": 3500,
    "roof_lo_m": 2,
    "run": False,
    "vendored": False,
    "is_arch_py": False,
}

PITS = {
    "mare_pits": 16,
    "melt_pits": 300,
    "highland_pits": 5,
    "pit_is_roof": False,
    "this_catalog": False,
}

STATION = {
    "id": "archhold",
    "stations_this_build": 9,
    "tenth": False,
    "remain_after": 2,
    "never_certificate": True,
}


def lunar_offset_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    to_r = math.pi / 180.0
    p1, p2 = a[0] * to_r, b[0] * to_r
    dp = (b[0] - a[0]) * to_r
    dl = (b[1] - a[1]) * to_r
    s = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * MOON_RADIUS_M * math.asin(min(1.0, math.sqrt(s)))


def score_published() -> str:
    return hold(MTP["span_m"], MTP["roof_lo_m"], MTP["tensile_mpa"], MTP["crack"])


def score_other() -> str:
    return hold(MHP["span_m"], MHP["roof_lo_m"], MHP["tensile_mpa"], MHP["crack"])


def trap_fem_run() -> bool:
    return bool(FEM["run"] or FEM["vendored"] or BLAIR["run"] or fem_run())


def trap_pit_is_roof() -> bool:
    return bool(PITS["pit_is_roof"] or SURVEYS["pit_is_roof"])
