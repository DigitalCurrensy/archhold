"""ARCHHOLD kernel tests. Catalog freeze. Scorer named, not a vault verdict."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from archhold.arch import hold  # noqa: E402
from archhold.vaults import BEAM, BLAIR, GRAIL, MHP, MTP  # noqa: E402


class HoldTests(unittest.TestCase):
    def test_missing_first(self) -> None:
        self.assertEqual(hold(None, 135, None, False), "missing")
        self.assertEqual(hold(45, None, None, False), "missing")
        self.assertEqual(hold(None, None, None, False), "missing")
        self.assertEqual(hold(45, 1, None, False), "thin")
        self.assertEqual(hold(45, 2, None, False), "ok")
        self.assertEqual(hold(5000, 135, None, False), "ok")
        self.assertEqual(hold(5001, 135, None, False), "wide")
        self.assertEqual(hold(45, 135, 0.5, False), "weak")
        self.assertEqual(hold(45, 135, 1, False), "ok")
        self.assertEqual(hold(45, 135, None, True), "crack")
        self.assertEqual(hold(45, 135, None, False), "ok")

    def test_catalog_named_not_scored_as_wave0_verdict(self) -> None:
        self.assertEqual(MTP["id"], "ARCH-MTP-WEST")
        self.assertEqual(MTP["lat"], 8.3355)
        self.assertEqual(MTP["lon"], 33.222)
        self.assertEqual(MTP["span_m"], 45.0)
        self.assertEqual(MTP["span_unc_m"], 7.5)
        self.assertEqual(MTP["roof_lo_m"], 135.0)
        self.assertEqual(MTP["roof_hi_m"], 175.0)
        self.assertIsNone(MTP["tensile_mpa"])
        self.assertFalse(MTP["crack"])
        self.assertFalse(MTP["fetched"])
        self.assertEqual(MTP["parent"], "TUBE-MTP-WEST")
        self.assertEqual(MHP["id"], "ARCH-MHP-RILLE")
        self.assertEqual(MHP["lat"], 14.1)
        self.assertEqual(MHP["lon"], 303.262)
        self.assertIsNone(MHP["span_m"])
        self.assertEqual(MHP["roof_lo_m"], 100.0)
        self.assertEqual(MHP["roof_hi_m"], 225.0)
        self.assertFalse(MHP["fetched"])
        self.assertEqual(
            hold(MTP["span_m"], MTP["roof_lo_m"], MTP["tensile_mpa"], MTP["crack"]),
            "ok",
        )
        self.assertEqual(
            hold(MHP["span_m"], MHP["roof_lo_m"], MHP["tensile_mpa"], MHP["crack"]),
            "missing",
        )

    def test_blair_named_not_run(self) -> None:
        self.assertEqual(BLAIR["roof_lo_m"], 2)
        self.assertEqual(BLAIR["span_max_m"], 5000)
        self.assertEqual(BLAIR["span_1km_roof_m"], 2)
        self.assertEqual(BLAIR["burial_50m_span_m"], 3500)
        self.assertEqual(BLAIR["engine"], "ABAQUS")
        self.assertFalse(BLAIR["run"])
        self.assertFalse(BLAIR["vendored"])
        self.assertFalse(BLAIR["is_arch_py"])
        self.assertFalse(BLAIR["this_catalog"])

    def test_beam_is_not_an_arch(self) -> None:
        self.assertEqual(BEAM["max_span_m"], 385)
        self.assertEqual(BEAM["roof_m"], 65)
        self.assertEqual(BEAM["density_kg_m3"], 2500)
        self.assertFalse(BEAM["is_arch"])
        self.assertFalse(BEAM["this_score"])

    def test_grail_not_this_catalog(self) -> None:
        self.assertFalse(GRAIL["this_catalog"])
        self.assertFalse(GRAIL["is_arch"])
        self.assertFalse(GRAIL["is_radar"])
        self.assertEqual(GRAIL["degree"], 1200)
        self.assertEqual(GRAIL["cannot_resolve_m"], 45)
        self.assertFalse(GRAIL["fetched"])


if __name__ == "__main__":
    unittest.main()
