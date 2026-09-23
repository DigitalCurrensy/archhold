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

"""Closed-form Hoek-Brown GSI envelope. Not ABAQUS. Not arch.py. Not a keep."""

from __future__ import annotations

import math

GSI = 70
D = 0.0
MI_CONSERVATIVE = 17
MI_BLAIR = 20
MI_BASALT = 25
SCI_MPA = 100.0
RHO = 3100.0
G_MOON = 1.62
BURIAL_M = 135.0
ROOF_THIN_M = 2.0


def gsi_params(gsi: float = GSI, mi: float = MI_CONSERVATIVE, disturbance: float = D) -> dict:
    mb = mi * math.exp((gsi - 100.0) / (28.0 - 14.0 * disturbance))
    s = math.exp((gsi - 100.0) / (9.0 - 3.0 * disturbance))
    a = 0.5 + (1.0 / 6.0) * (math.exp(-gsi / 15.0) - math.exp(-20.0 / 3.0))
    return {"gsi": gsi, "mi": mi, "D": disturbance, "mb": mb, "s": s, "a": a, "sci_mpa": SCI_MPA}


def sigma1_mpa(sigma3_mpa: float, gsi: float = GSI, mi: float = MI_CONSERVATIVE) -> float:
    p = gsi_params(gsi, mi)
    inside = p["mb"] * (sigma3_mpa / p["sci_mpa"]) + p["s"]
    if inside <= 0:
        return sigma3_mpa
    return sigma3_mpa + p["sci_mpa"] * (inside ** p["a"])


def lithostatic_mpa(depth_m: float) -> float:
    return RHO * G_MOON * depth_m / 1e6


def ucs_mass_mpa(gsi: float = GSI, mi: float = MI_CONSERVATIVE) -> float:
    return sigma1_mpa(0.0, gsi, mi)


def tensile_cutoff_mpa(gsi: float = GSI, mi: float = MI_CONSERVATIVE) -> float:
    """Uniaxial tensile strength, as a positive number.

    s * intact strength / mb. Compression is not this number.
    """
    p = gsi_params(gsi, mi)
    return p["s"] * p["sci_mpa"] / p["mb"]


def envelope_hit(sigma1: float, sigma3: float, gsi: float = GSI, mi: float = MI_CONSERVATIVE) -> str:
    """Hoek-Brown check. Compression is positive. sigma1 is the larger compression.

    A negative sigma3 is tension of size -sigma3. That fails when the size
    exceeds the tensile cutoff. Otherwise it fails when sigma1 is above the
    envelope at that sigma3. A bad number raises ValueError.
    """
    if not math.isfinite(sigma1) or not math.isfinite(sigma3) or sigma1 < sigma3:
        raise ValueError("bad stress")
    if sigma3 < 0.0:
        if -sigma3 > tensile_cutoff_mpa(gsi, mi):
            return "tension"
        sigma3 = 0.0
    if sigma1 > sigma1_mpa(sigma3, gsi, mi):
        return "envelope"
    return "inside"


def hoek_is_keep() -> bool:
    return False


def probe(gsi: float = GSI, mi: float = MI_CONSERVATIVE) -> dict:
    p = gsi_params(gsi, mi)
    litho = lithostatic_mpa(BURIAL_M)
    return {
        **p,
        "ucs_mass_mpa": ucs_mass_mpa(gsi, mi),
        "litho_135_mpa": litho,
        "sigma1_135_mpa": sigma1_mpa(litho, gsi, mi),
        "abaqus": False,
        "is_arch_py": False,
        "is_keep": False,
    }
