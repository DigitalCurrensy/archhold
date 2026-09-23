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

"""VAULT COUNSEL PASS. Unsigned. Hoek-Brown GSI named, not run. Thermal is not a roof."""

from __future__ import annotations

from .letter import compile_letter
from .vaults import BEAM, BLAIR

TITLE = "VAULT COUNSEL PASS"
OFFER = "Unsigned. Not an invoice."
COUNSEL = "unsigned"
WORD_CAP = 80

HOEK = {
    "name": "Hoek-Brown GSI 70",
    "gsi": 70,
    "ucs_mpa": 100,
    "engine": "ABAQUS",
    "criterion": "sigma1 = sigma3 + sci (mb sigma3/sci + s)^a",
    "continuum": True,
    "run": False,
    "vendored": False,
    "is_arch_py": False,
    "scored": False,
    "this_letter": False,
}

THERMAL = {
    "t_day_k": 390,
    "t_night_k": 90,
    "delta_k": 300,
    "gevs": "GSFC-STD-7000",
    "gevs_is_roof": False,
    "kapton_is_roof": False,
    "kapton_is_mli": True,
    "kapton_lo_c": -269,
    "kapton_hi_c": 400,
    "scored": False,
    "this_letter": False,
}

STATION = {
    "id": "archhold",
    "stations_this_build": 9,
    "tenth": False,
    "remain_after": 0,
    "never_certificate": True,
}


def _words(body: str) -> int:
    return len([w for w in body.split() if w])


def thermal_delta_k() -> int:
    return int(THERMAL["t_day_k"] - THERMAL["t_night_k"])


def trap_hoek_run() -> bool:
    return bool(HOEK["run"] or HOEK["vendored"] or HOEK["is_arch_py"] or BLAIR["run"])


def trap_thermal_as_roof() -> bool:
    return bool(THERMAL["scored"] or THERMAL["kapton_is_roof"] or THERMAL["gevs_is_roof"])


def compile_counsel(kind: str) -> dict:
    walk = compile_letter("walk")
    base = {
        "title": TITLE,
        "counsel": COUNSEL,
        "engineer_of_record": COUNSEL,
        "signed": False,
        "wet_ink": False,
        "not_a_certificate": True,
        "not_survey_grade": True,
        "walk_stamp": walk["stamp"],
        "walk_issued": walk["issued"],
        "do_not_enter": walk["do_not_enter"],
        "hoek_run": False,
        "thermal_is_roof": False,
        "kapton_is_roof": False,
        "radar_fetched": False,
    }
    if kind == "hoek":
        body = (
            "No counsel pass. Hoek-Brown GSI 70 is Blair's constitutive. "
            "A yield envelope is not arch.py. ABAQUS stays upstream. "
            "Named, not run. Not a certificate."
        )
        return {
            **base,
            "issued": False,
            "stamp": "refused",
            "why": "hoek_named_not_scored",
            "body": body,
            "words": _words(body),
        }
    if kind == "thermal":
        body = (
            "No counsel pass. Lunar ΔT ~300 K is not a keep. "
            "GSFC GEVS is a test standard. Kapton is MLI, not overburden. "
            "A hot roof is not this span. Not a certificate."
        )
        return {
            **base,
            "issued": False,
            "stamp": "refused",
            "why": "thermal_is_not_a_roof",
            "body": body,
            "words": _words(body),
        }
    if kind == "pretty-keep":
        body = (
            "No counsel pass. A pretty cave is not a keep. Google Moon is not a score. "
            "ok still sits. Famous is not a door. Do-not-enter is abort. "
            "Not a certificate. Not survey-grade."
        )
        return {
            **base,
            "issued": False,
            "stamp": "refused",
            "why": "pretty_is_not_a_keep",
            "body": body,
            "words": _words(body),
        }
    if kind == "unnamed-sign":
        body = (
            "No counsel pass. Counsel unnamed. Engineer of record unnamed. "
            "A checked box is not a wet signature. This console does not mint ink. "
            "Not a certificate. Research tool."
        )
        return {
            **base,
            "issued": False,
            "stamp": "refused",
            "why": "unnamed_signature",
            "body": body,
            "words": _words(body),
        }
    if kind == "named-unsigned":
        body = (
            "VAULT COUNSEL PASS. Named seats are not a wet signature. Research tool. "
            "Not a certificate. ok is not a keep. Hoek-Brown unrun. Thermal is not a roof. "
            "Counsel unsigned. Engineer of record unsigned."
        )
        return {
            **base,
            "issued": True,
            "stamp": "unsigned",
            "why": "names_are_not_wet_ink",
            "body": body,
            "words": _words(body),
        }
    body = (
        "VAULT COUNSEL PASS. Research tool. Not a certificate. Not survey-grade. "
        "ARCH-MTP-WEST still OK. ok is not a keep. Counsel unsigned. "
        "Engineer of record unsigned."
    )
    return {
        **base,
        "issued": True,
        "stamp": "unsigned",
        "why": "compiled_unsigned",
        "body": body,
        "words": _words(body),
        "beam_is_arch": BEAM["is_arch"],
    }
