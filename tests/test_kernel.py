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

"""ARCHHOLD kernel tests. Ok is not a keep."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from archhold.arch import hold  # noqa: E402
from archhold.counsel import (  # noqa: E402
    HOEK,
    THERMAL,
    compile_counsel,
    thermal_delta_k,
    trap_hoek_run,
    trap_thermal_as_roof,
)
from archhold.letter import (  # noqa: E402
    CARRER,
    LITHOSTATIC,
    compile_letter,
    lithostatic_holds_this_vault,
    trap_carrer_is_roof,
)
from archhold.score import SURVEYS, fem_run, score_eq, score_mhp, score_mtp  # noqa: E402
from archhold.vaults import BEAM, BLAIR, GRAIL, MHP, MTP  # noqa: E402
from archhold.hoek import gsi_params, hoek_is_keep, lithostatic_mpa, probe as hoek_probe, ucs_mass_mpa  # noqa: E402
from archhold.thermal import burial_delta_k, probe as thermal_probe, surface_delta_k  # noqa: E402
from archhold.walk import (  # noqa: E402
    FEM,
    MTP_WALK,
    PITS,
    STATION,
    lunar_offset_m,
    score_other,
    score_published,
    trap_fem_run,
    trap_pit_is_roof,
)


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

    def test_negative_span_or_tensile_is_missing_and_depth_load_is_closed_form(self) -> None:
        self.assertEqual(hold(-1, 135, None, False), "missing")
        self.assertEqual(hold(45, 135, -1, False), "missing")
        self.assertNotEqual(hold(45, 135, -1, False), "weak")
        stress_per_m = lithostatic_mpa(1.0)
        self.assertGreater(stress_per_m, 0.0)
        depth_m = ucs_mass_mpa() / stress_per_m + 1.0
        self.assertGreater(lithostatic_mpa(depth_m), ucs_mass_mpa())
        self.assertEqual(hold(45, 135, None, False, depth_m), "load")
        self.assertEqual(hold(45, 135, None, False, 0), "ok")
        self.assertNotEqual(hold(45, 135, None, False, 0), "load")
        self.assertFalse(hoek_is_keep())
        self.assertFalse(fem_run())

    def test_named_catalog_is_not_a_fetched_survey(self) -> None:
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


class Wave1Tests(unittest.TestCase):
    def test_catalog_scores(self) -> None:
        self.assertEqual(score_mtp(), "ok")
        self.assertEqual(score_mhp(), "missing")
        self.assertEqual(score_eq(), "ok")
        self.assertFalse(fem_run())
        self.assertEqual(SURVEYS["mare_pits"], 16)
        self.assertFalse(SURVEYS["pit_is_roof"])
        self.assertFalse(SURVEYS["scored"])


class Wave2Tests(unittest.TestCase):
    def test_published_ok_is_not_a_keep(self) -> None:
        self.assertEqual(MTP_WALK["id"], "ARCH-MTP-WEST")
        self.assertEqual(score_published(), "ok")
        self.assertEqual(score_other(), "missing")
        self.assertFalse(MTP_WALK["fem_run"])
        self.assertFalse(MTP_WALK["pit_is_roof"])
        self.assertEqual(round(lunar_offset_m((8.3355, 33.222), (8.336, 33.222))), 15)

    def test_blair_fem_named_not_run(self) -> None:
        self.assertEqual(FEM["name"], "Blair 2017 FEM")
        self.assertFalse(FEM["run"])
        self.assertFalse(FEM["vendored"])
        self.assertFalse(FEM["is_arch_py"])
        self.assertTrue(FEM["lithostatic_keystone"])
        self.assertEqual(FEM["engine"], "ABAQUS")
        self.assertEqual(FEM["gsi"], 70)
        self.assertEqual(FEM["poisson"], 0.25)
        self.assertEqual(FEM["span_max_m"], 5000)
        self.assertEqual(FEM["span_max_poisson_m"], 3500)
        self.assertFalse(trap_fem_run())
        self.assertFalse(BEAM["is_arch"])
        self.assertFalse(BLAIR["run"])

    def test_wagner_pits_not_this_roof(self) -> None:
        self.assertEqual(PITS["mare_pits"], 16)
        self.assertEqual(PITS["melt_pits"], 300)
        self.assertEqual(PITS["highland_pits"], 5)
        self.assertFalse(PITS["pit_is_roof"])
        self.assertFalse(PITS["this_catalog"])
        self.assertFalse(trap_pit_is_roof())
        self.assertEqual(STATION["stations_this_build"], 9)
        self.assertFalse(STATION["tenth"])
        self.assertEqual(STATION["remain_after"], 2)
        self.assertTrue(STATION["never_certificate"])


class Wave3Tests(unittest.TestCase):
    def test_published_ok_letter_is_not_a_keep(self) -> None:
        letter = compile_letter("walk")
        self.assertEqual(letter["title"], "VAULT LETTER")
        self.assertTrue(letter["issued"])
        self.assertEqual(letter["stamp"], "ok")
        self.assertTrue(letter["do_not_enter"])
        self.assertTrue(letter["not_a_certificate"])
        self.assertLessEqual(letter["words"], 80)
        self.assertIn("ok is not a keep", letter["body"])

    def test_blair_lithostatic_named_not_run(self) -> None:
        letter = compile_letter("fem")
        self.assertTrue(letter["issued"])
        self.assertEqual(letter["why"], "fem_named_not_scored")
        self.assertFalse(letter["fem_run"])
        self.assertEqual(LITHOSTATIC["engine"], "ABAQUS")
        self.assertEqual(LITHOSTATIC["gsi"], 70)
        self.assertEqual(LITHOSTATIC["poisson"], 0.25)
        self.assertTrue(LITHOSTATIC["lithostatic_keystone"])
        self.assertTrue(LITHOSTATIC["fail_surface_down"])
        self.assertEqual(LITHOSTATIC["span_max_m"], 5000)
        self.assertEqual(LITHOSTATIC["span_max_poisson_m"], 3500)
        self.assertFalse(LITHOSTATIC["run"])
        self.assertFalse(LITHOSTATIC["vendored"])
        self.assertTrue(lithostatic_holds_this_vault())

    def test_carrer_inversion_is_not_a_roof(self) -> None:
        letter = compile_letter("carrer")
        self.assertTrue(letter["issued"])
        self.assertEqual(letter["why"], "carrer_named_not_roof")
        self.assertFalse(letter["carrer_is_roof"])
        self.assertFalse(letter["inversion_run"])
        self.assertEqual(CARRER["span_m"], 45.0)
        self.assertEqual(CARRER["span_unc_m"], 7.5)
        self.assertEqual(CARRER["burial_lo_m"], 135.0)
        self.assertEqual(CARRER["burial_hi_m"], 175.0)
        self.assertEqual(CARRER["lat"], 8.3355)
        self.assertEqual(CARRER["lon"], 33.222)
        self.assertEqual(CARRER["west_of_mouth_m"], 40)
        self.assertEqual(CARRER["bounce_need"], 3)
        self.assertFalse(CARRER["fetched"])
        self.assertFalse(trap_carrer_is_roof())
        mhp = compile_letter("mhp")
        self.assertFalse(mhp["issued"])
        self.assertEqual(mhp["why"], "not_this_letter")
        self.assertFalse(mhp["mhp_is_this_letter"])


class Wave4Tests(unittest.TestCase):
    def test_compiled_unsigned_is_not_a_certificate(self) -> None:
        paper = compile_counsel("compiled")
        self.assertEqual(paper["title"], "VAULT COUNSEL PASS")
        self.assertTrue(paper["issued"])
        self.assertEqual(paper["stamp"], "unsigned")
        self.assertFalse(paper["signed"])
        self.assertFalse(paper["wet_ink"])
        self.assertTrue(paper["not_a_certificate"])
        self.assertTrue(paper["do_not_enter"])
        self.assertLessEqual(paper["words"], 80)
        self.assertIn("ok is not a keep", paper["body"])

    def test_hoek_named_not_run(self) -> None:
        paper = compile_counsel("hoek")
        self.assertFalse(paper["issued"])
        self.assertEqual(paper["why"], "hoek_named_not_scored")
        self.assertFalse(paper["hoek_run"])
        self.assertEqual(HOEK["gsi"], 70)
        self.assertEqual(HOEK["ucs_mpa"], 100)
        self.assertEqual(HOEK["engine"], "ABAQUS")
        self.assertFalse(HOEK["run"])
        self.assertFalse(HOEK["vendored"])
        self.assertFalse(HOEK["is_arch_py"])
        self.assertFalse(trap_hoek_run())
        self.assertFalse(BEAM["is_arch"])
        self.assertFalse(BLAIR["run"])

    def test_thermal_is_not_a_roof(self) -> None:
        paper = compile_counsel("thermal")
        self.assertFalse(paper["issued"])
        self.assertEqual(paper["why"], "thermal_is_not_a_roof")
        self.assertFalse(paper["thermal_is_roof"])
        self.assertFalse(paper["kapton_is_roof"])
        self.assertEqual(THERMAL["t_day_k"], 390)
        self.assertEqual(THERMAL["t_night_k"], 90)
        self.assertEqual(thermal_delta_k(), 300)
        self.assertEqual(THERMAL["gevs"], "GSFC-STD-7000")
        self.assertFalse(THERMAL["gevs_is_roof"])
        self.assertFalse(THERMAL["kapton_is_roof"])
        self.assertTrue(THERMAL["kapton_is_mli"])
        self.assertFalse(trap_thermal_as_roof())
        unnamed = compile_counsel("unnamed-sign")
        self.assertFalse(unnamed["issued"])
        self.assertEqual(unnamed["why"], "unnamed_signature")


class ClosedFormTests(unittest.TestCase):
    def test_hoek_gsi_envelope_is_not_a_keep(self) -> None:
        p = gsi_params(70, 17)
        self.assertAlmostEqual(p["mb"], 5.822821, places=5)
        self.assertAlmostEqual(ucs_mass_mpa(), 18.8024, places=3)
        self.assertAlmostEqual(lithostatic_mpa(135), 0.67797, places=4)
        probe = hoek_probe()
        self.assertFalse(probe["abaqus"])
        self.assertFalse(probe["is_keep"])
        self.assertFalse(hoek_is_keep())

    def test_diviner_burial_damps_to_zero(self) -> None:
        self.assertEqual(surface_delta_k(), 297)
        self.assertGreater(burial_delta_k(2.0, 0.75), 19)
        self.assertLess(burial_delta_k(2.0, 0.75), 22)
        self.assertEqual(burial_delta_k(135.0, 0.75), 0.0)
        probe = thermal_probe()
        self.assertFalse(probe["fetched"])
        self.assertFalse(probe["is_roof"])
        self.assertEqual(probe["polar_delta_k"], 152)


class CsvMissingTests(unittest.TestCase):
    def test_blank_required_number_is_missing_not_ok(self) -> None:
        from archhold.__main__ import score_row

        blank_span = score_row(
            {"span_m": "", "roof_m": "135", "tensile_mpa": "", "crack": "false"}
        )
        blank_roof = score_row(
            {"span_m": "45", "roof_m": "", "tensile_mpa": "", "crack": "false"}
        )
        blank_tensile = score_row(
            {"span_m": "45", "roof_m": "135", "tensile_mpa": "", "crack": "false"}
        )
        self.assertEqual(blank_span, hold(None, 135.0, None, False))
        self.assertEqual(blank_roof, hold(45.0, None, None, False))
        self.assertEqual(blank_tensile, hold(45.0, 135.0, None, False))
        self.assertEqual(blank_span, "missing")
        self.assertEqual(blank_roof, "missing")
        self.assertNotEqual(blank_span, "ok")
        self.assertNotEqual(blank_roof, "ok")
        self.assertEqual(blank_tensile, "ok")



class FiniteRoofTests(unittest.TestCase):
    def test_non_finite_is_missing(self) -> None:
        self.assertEqual(hold(100.0, float("nan"), 5.0, False), "missing")



class PrintedLineTests(unittest.TestCase):
    def test_ucs_is_on_the_line(self) -> None:
        import subprocess
        repo = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [sys.executable, "-m", "archhold", str(repo / "examples" / "roof.csv")],
            cwd=repo, env={**__import__("os").environ, "PYTHONPATH": str(repo / "src")},
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(
            proc.stdout.splitlines()[0],
            "ok span=45 roof=135 tensile=missing crack=false ucs=18.80243413 lithostatic=unset",
        )

    def test_depth_above_strength_is_load(self) -> None:
        self.assertEqual(hold(45.0, 135.0, None, False, 4000.0), "load")


if __name__ == "__main__":
    unittest.main()
