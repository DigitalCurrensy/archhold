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

import math


def _bad(value: float | None) -> bool:
    return value is not None and not math.isfinite(value)


def hold(
    span_m: float | None,
    roof_m: float | None,
    tensile_mpa: float | None,
    crack: bool,
    depth_m: float | None = None,
) -> str:
    if span_m is None or roof_m is None:
        return "missing"
    if _bad(span_m) or _bad(roof_m) or _bad(tensile_mpa) or _bad(depth_m):
        return "missing"
    if span_m < 0 or roof_m < 0:
        return "missing"
    if tensile_mpa is not None and tensile_mpa < 0:
        return "missing"
    if depth_m is not None and depth_m < 0:
        return "missing"
    if roof_m < 2:
        return "thin"
    if span_m > 5000:
        return "wide"
    if tensile_mpa is not None and tensile_mpa < 1:
        return "weak"
    if crack:
        return "crack"
    if depth_m is not None and depth_m >= 0:
        from archhold.hoek import lithostatic_mpa, ucs_mass_mpa

        if lithostatic_mpa(depth_m) > ucs_mass_mpa():
            return "load"
    return "ok"
