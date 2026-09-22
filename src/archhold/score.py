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
