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

def hold(
    span_m: float | None,
    roof_m: float | None,
    tensile_mpa: float | None,
    crack: bool,
) -> str:
    if span_m is None or roof_m is None:
        return "missing"
    if roof_m < 2:
        return "thin"
    if span_m > 5000:
        return "wide"
    if tensile_mpa is not None and tensile_mpa < 1:
        return "weak"
    if crack:
        return "crack"
    return "ok"
