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

"""Two published arches. Declared roof stats. Not a scored vault."""

MTP = {
    "id": "ARCH-MTP-WEST",
    "name": "Mare Tranquillitatis west arch",
    "lat": 8.3355,
    "lon": 33.222,
    "alt": (8.336, 33.222),
    "span_m": 45.0,
    "span_unc_m": 7.5,
    "roof_lo_m": 135.0,
    "roof_hi_m": 175.0,
    "tensile_mpa": None,
    "crack": False,
    "parent": "TUBE-MTP-WEST",
    "mouth": "BAG-MTP-TRANQ",
    "fetched": False,
}

MHP = {
    "id": "ARCH-MHP-RILLE",
    "name": "Marius Hills rille arch",
    "lat": 14.1,
    "lon": 303.262,
    "alt": (14.091, 303.23),
    "span_m": None,
    "span_unc_m": None,
    "roof_lo_m": 100.0,
    "roof_hi_m": 225.0,
    "tensile_mpa": None,
    "crack": False,
    "parent": "TUBE-MHP-RILLE",
    "mouth": "BAG-MHP-MARIUS",
    "fetched": False,
}

BLAIR = {
    "id": "blair-2017",
    "name": "Blair FEM roof",
    "cite": "Blair et al. Icarus 282 47-55 (2017)",
    "engine": "ABAQUS",
    "roof_lo_m": 2,
    "span_1km_roof_m": 2,
    "span_max_m": 5000,
    "burial_50m_span_m": 3500,
    "width_height": "3:1",
    "stress": ("lithostatic", "Poisson"),
    "gsi": True,
    "this_catalog": False,
    "run": False,
    "vendored": False,
    "is_arch_py": False,
}

BEAM = {
    "id": "elastic-beam",
    "name": "Elastic beam max span",
    "cite": "Hörz 1985; Blair 2017 citing prior beam models",
    "max_span_m": 385,
    "roof_m": 65,
    "density_kg_m3": 2500,
    "is_arch": False,
    "this_score": False,
}

GRAIL = {
    "id": "grail-rille",
    "name": "GRAIL rille A deficit",
    "this_catalog": False,
    "is_arch": False,
    "is_radar": False,
    "model": "GRGM1200A",
    "degree": 1200,
    "cannot_resolve_m": 45,
    "fetched": False,
}
