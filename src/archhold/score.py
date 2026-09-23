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

"""Vault scorer. arch.py ported. Catalog scores. FEM unrun."""

from .arch import hold
from .vaults import BEAM, BLAIR, MHP, MTP

SURVEYS = {
    "mare_pits": 16,
    "melt_pits": 300,
    "highland_pits": 5,
    "pit_is_roof": False,
    "scored": False,
    "fetched": False,
}


def score_mtp() -> str:
    return hold(MTP["span_m"], MTP["roof_lo_m"], MTP["tensile_mpa"], MTP["crack"])


def score_mhp() -> str:
    return hold(MHP["span_m"], MHP["roof_lo_m"], MHP["tensile_mpa"], MHP["crack"])


def score_eq() -> str:
    return hold(5000.0, 2.0, 1.0, False)


def fem_run() -> bool:
    return bool(BLAIR["run"] or BLAIR["vendored"] or BEAM["is_arch"] or SURVEYS["scored"])
