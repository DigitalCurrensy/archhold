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

"""ARCHHOLD — the arch is the keep. Score the roof against the span."""

from .arch import hold
from .counsel import HOEK, THERMAL, compile_counsel, thermal_delta_k, trap_hoek_run, trap_thermal_as_roof
from .hoek import gsi_params, hoek_is_keep, lithostatic_mpa, probe as hoek_probe, sigma1_mpa, ucs_mass_mpa
from .letter import CARRER, LITHOSTATIC, compile_letter, lithostatic_holds_this_vault, trap_carrer_is_roof
from .score import SURVEYS, fem_run, score_eq, score_mhp, score_mtp
from .thermal import burial_delta_k, probe as thermal_probe, surface_delta_k
from .vaults import BEAM, BLAIR, GRAIL, MHP, MTP
from .walk import FEM, MTP_WALK, PITS, STATION, score_other, score_published, trap_fem_run, trap_pit_is_roof

__all__ = [
    "BEAM",
    "BLAIR",
    "CARRER",
    "FEM",
    "GRAIL",
    "HOEK",
    "LITHOSTATIC",
    "MHP",
    "MTP",
    "MTP_WALK",
    "PITS",
    "STATION",
    "SURVEYS",
    "THERMAL",
    "burial_delta_k",
    "compile_counsel",
    "compile_letter",
    "fem_run",
    "gsi_params",
    "hoek_is_keep",
    "hoek_probe",
    "hold",
    "lithostatic_holds_this_vault",
    "lithostatic_mpa",
    "score_eq",
    "score_mhp",
    "score_mtp",
    "score_other",
    "score_published",
    "sigma1_mpa",
    "surface_delta_k",
    "thermal_delta_k",
    "thermal_probe",
    "trap_carrer_is_roof",
    "trap_fem_run",
    "trap_hoek_run",
    "trap_pit_is_roof",
    "trap_thermal_as_roof",
    "ucs_mass_mpa",
]
