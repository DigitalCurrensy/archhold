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

"""Declared Diviner thermal cache + 1D skin-depth damping. Not a live GET. Not a roof."""

from __future__ import annotations

import math

NOON_MID_K = 392
DAWN_K = 95
NOON_LO_K = 387
NOON_HI_K = 397
EQUATOR_MEAN_K = 215.5
EQUATOR_MAX_K = 392.3
EQUATOR_MIN_K = 94.3
POLAR_MAX_K = 202
POLAR_MIN_K = 50
COUNSEL_DELTA_K = 300
SKIN_REGOLITH_M = 0.07
SKIN_ROCK_M = 0.75
YOUNG_GPA = 30.0
ALPHA_PER_K = 6e-6
POISSON = 0.25
FETCHED = False


def surface_delta_k() -> float:
    return float(NOON_MID_K - DAWN_K)


def burial_delta_k(depth_m: float, skin_m: float, surface: float | None = None) -> float:
    if skin_m <= 0:
        return 0.0
    delta = surface_delta_k() if surface is None else surface
    ratio = math.exp(-depth_m / skin_m)
    if ratio < 1e-12:
        return 0.0
    return delta * ratio


def constrained_stress_mpa(delta_k: float) -> float:
    e_mpa = YOUNG_GPA * 1e3
    return (e_mpa * ALPHA_PER_K * delta_k) / (1.0 - POISSON)


def probe() -> dict:
    surface = surface_delta_k()
    at2 = burial_delta_k(2.0, SKIN_ROCK_M, surface)
    at135 = burial_delta_k(135.0, SKIN_ROCK_M, surface)
    return {
        "noon_lo_k": NOON_LO_K,
        "noon_hi_k": NOON_HI_K,
        "dawn_k": DAWN_K,
        "equator_mean_k": EQUATOR_MEAN_K,
        "polar_max_k": POLAR_MAX_K,
        "polar_min_k": POLAR_MIN_K,
        "polar_delta_k": POLAR_MAX_K - POLAR_MIN_K,
        "surface_delta_k": surface,
        "counsel_delta_k": COUNSEL_DELTA_K,
        "at_2_rock_delta_k": at2,
        "at_135_rock_delta_k": at135,
        "surface_stress_mpa": constrained_stress_mpa(surface),
        "at_2_rock_stress_mpa": constrained_stress_mpa(at2),
        "fetched": FETCHED,
        "is_roof": False,
        "kapton_is_roof": False,
    }
