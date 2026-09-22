"""VAULT LETTER. Paper on the arch. Fail still issues. ok is not a keep. Not a certificate."""

from __future__ import annotations

from .arch import hold
from .vaults import MTP
from .walk import MTP_WALK

TITLE = "VAULT LETTER"
OFFER = "roof letter $6k–$14k. Not an invoice."
COUNSEL = "unsigned"
WORD_CAP = 80

LITHOSTATIC = {
    "authors": "Blair, Chappaz, Sood, Milbury, Bobet, Melosh, Howell, Freed",
    "cite": "Blair et al. Icarus 282 47-55 (2017)",
    "engine": "ABAQUS",
    "width_height": "3:1",
    "gsi": 70,
    "poisson": 0.25,
    "lithostatic_keystone": True,
    "fail_surface_down": True,
    "compression_throughout": True,
    "roof_lo_m": 2,
    "span_max_m": 5000,
    "span_max_poisson_m": 3500,
    "lithostatic_burial_m": 500,
    "run": False,
    "vendored": False,
    "is_arch_py": False,
    "this_letter": False,
}

CARRER = {
    "lat": 8.3355,
    "lon": 33.222,
    "span_m": 45.0,
    "span_unc_m": 7.5,
    "length_lo_m": 30,
    "length_hi_m": 80,
    "burial_lo_m": 135.0,
    "burial_hi_m": 175.0,
    "west_of_mouth_m": 40,
    "look_deg": 47,
    "slope_max_deg": 45,
    "bounce_need": 3,
    "inversion": "RaySAR",
    "year_acquired": 2010,
    "fetched": False,
    "inversion_run": False,
    "is_roof": False,
    "this_letter": False,
}


def _words(body: str) -> int:
    return len([w for w in body.split() if w])


def lithostatic_holds_this_vault() -> bool:
    return (
        CARRER["span_m"] < LITHOSTATIC["span_max_m"]
        and CARRER["span_m"] < LITHOSTATIC["span_max_poisson_m"]
        and CARRER["burial_lo_m"] > LITHOSTATIC["roof_lo_m"]
    )


def trap_carrer_is_roof() -> bool:
    return bool(CARRER["is_roof"] or CARRER["fetched"] or CARRER["inversion_run"])


def compile_letter(kind: str) -> dict:
    if kind == "mhp":
        body = (
            "No letter issued. Marius Hills rille is a different vault. "
            "One walk remains ARCH-MTP-WEST. GRAIL 60 km is not this letter. "
            "Not survey-grade."
        )
        return {
            "title": TITLE,
            "issued": False,
            "stamp": "refused",
            "vault_id": "ARCH-MHP-RILLE",
            "why": "not_this_letter",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_enter": False,
            "mhp_is_this_letter": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    if kind == "okform":
        body = (
            "VAULT LETTER. Synthetic walk-in vs SYN-ARCH-FLAT. OK. Not ARCH-MTP-WEST. "
            "Different vault. ok is not survey-grade. Not a certificate. Counsel unsigned."
        )
        return {
            "title": TITLE,
            "issued": True,
            "stamp": "ok",
            "vault_id": "SYN-ARCH-FLAT",
            "why": "ok_form_other_vault",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_enter": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    if kind == "undeclared":
        body = (
            "No letter issued. ARCH-MTP-WEST identity is off. Undeclared is not a vault. "
            "Not a certificate. Not survey-grade."
        )
        return {
            "title": TITLE,
            "issued": False,
            "stamp": "refused",
            "vault_id": MTP_WALK["id"],
            "why": "undeclared_identity",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_enter": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    if kind == "fem":
        body = (
            "VAULT LETTER. ARCH-MTP-WEST vs SYN-ARCH-MTP. OK. Lithostatic keystone named. "
            "ABAQUS stays upstream. A mesh is not a score. "
            "Not survey-grade. Counsel unsigned."
        )
        return {
            "title": TITLE,
            "issued": True,
            "stamp": "ok",
            "vault_id": MTP["id"],
            "why": "fem_named_not_scored",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_enter": True,
            "fem_run": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    if kind == "carrer":
        body = (
            "VAULT LETTER. ARCH-MTP-WEST vs SYN-ARCH-MTP. OK. Mini-RF inversion named. "
            "Span 45 is not a roof. Burial 135 is overburden, not a keep. "
            "Not survey-grade. Counsel unsigned."
        )
        return {
            "title": TITLE,
            "issued": True,
            "stamp": "ok",
            "vault_id": MTP["id"],
            "why": "carrer_named_not_roof",
            "body": body,
            "words": _words(body),
            "counsel": COUNSEL,
            "do_not_enter": True,
            "carrer_is_roof": False,
            "inversion_run": False,
            "not_a_certificate": True,
            "not_survey_grade": True,
        }
    stamp = hold(MTP["span_m"], MTP["roof_lo_m"], MTP["tensile_mpa"], MTP["crack"])
    body = (
        "VAULT LETTER. ARCH-MTP-WEST vs SYN-ARCH-MTP. OK. Span 45 sits. Roof 135 sits. "
        "ok is not a keep. Famous is not a vault. Not survey-grade. Counsel unsigned."
    )
    return {
        "title": TITLE,
        "issued": True,
        "stamp": stamp,
        "vault_id": MTP["id"],
        "why": stamp,
        "body": body,
        "words": _words(body),
        "counsel": COUNSEL,
        "do_not_enter": True,
        "not_a_certificate": True,
        "not_survey_grade": True,
    }
