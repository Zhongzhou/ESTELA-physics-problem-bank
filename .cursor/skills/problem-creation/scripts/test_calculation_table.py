"""Checks for equation combinations, calculation functions, and scenario rows."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = Path(__file__).with_name("calculation_table.py")
SPEC = importlib.util.spec_from_file_location("calculation_table", SCRIPT)
calc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(calc)


CENTRIPETAL = r"""
name: centripetal
context:
  scenario: uniform circular motion
  scenario_specifications:
    - one object
  n_scenarios: 1
structure:
  formulas:
    - 'F_{\mathrm{net}} = \frac{m v^{2}}{r}'
    - One of:
      - 'T = \frac{2 \pi r}{v}'
      - 'f = \frac{v}{2 \pi r}'
  variable_specifications:
    - r is the radius
  question_unknowns: F_net, m, T or f, r
  unknown_rotation: 2
other (optional):
  parameters: F_net, m, r
  rounding_decimal: 2
"""


SCENARIOS = """
source_input: input.yaml
target: 2
update_count: 1
scenarios:
  - text: A puck slides in a circle on a frictionless table.
    status: accepted
  - text: A satellite travels in a circular orbit.
    status: accepted
rejected: []
"""


class FormulaTests(unittest.TestCase):
    def test_one_of_expands_to_two_sets(self):
        formulas = [
            r"F_{\mathrm{net}} = \frac{m v^{2}}{r}",
            {"One of": [r"T = \frac{2 \pi r}{v}", r"f = \frac{v}{2 \pi r}"]},
        ]
        combinations = calc.expand_formulas(formulas)
        self.assertEqual(len(combinations), 2)
        self.assertEqual(len(combinations[0]), 2)
        self.assertIn("T", combinations[0][1])
        self.assertIn("f", combinations[1][1])

    def test_latex_parses_centripetal_force(self):
        equation = calc.parse_formula(r"F_{\mathrm{net}} = \frac{m v^{2}}{r}")
        names = {symbol.name for symbol in equation.free_symbols}
        self.assertEqual(names, {"F_net", "m", "v", "r"})

    def test_period_formula_uses_pi_as_a_constant(self):
        equation = calc.parse_formula(r"T = \frac{2 \pi r}{v}")
        names = {symbol.name for symbol in equation.free_symbols}
        self.assertEqual(names, {"T", "r", "v"})
        self.assertTrue(equation.has(calc.sympy.pi))

    def test_round_half_up(self):
        self.assertEqual(calc.round_step(1.225, 2), 1.23)
        self.assertEqual(calc.round_step(1.224, 2), 1.22)


class WorkflowTests(unittest.TestCase):
    def write_inputs(self, directory: Path, source: str = CENTRIPETAL, scenarios: str = SCENARIOS):
        input_path = directory / "input.yaml"
        scenario_path = directory / "input.scenarios.yaml"
        input_path.write_text(source, encoding="utf-8")
        scenario_path.write_text(scenarios, encoding="utf-8")
        return input_path, scenario_path

    def test_specified_parameters_build_and_associate(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path, scenario_path = self.write_inputs(directory)
            calc_path = directory / "input.calculations.yaml"
            code, payload = run(
                "prepare",
                "--input",
                str(input_path),
                "--scenarios",
                str(scenario_path),
                "--out",
                str(calc_path),
            )
            self.assertEqual(code, 0, payload)
            self.assertFalse(payload["needs_classifier"])
            sets = {item["id"]: item for item in payload["equation_sets"]}
            self.assertEqual(sets["eqset_01"]["parameters"], ["F_net", "m", "r"])
            self.assertEqual(sets["eqset_01"]["computed"], ["v", "T"])
            self.assertEqual(sets["eqset_02"]["computed"], ["v", "f"])
            self.assertNotIn("question_unknowns", payload)

            code, payload = run("build", "--file", str(calc_path))
            self.assertEqual(code, 0, payload)
            self.assertTrue(payload["validated"])
            module = calc.load_module(calc.module_path_for(calc_path))
            values = module.solve_eqset_01(F_net=10, m=3, r=4)
            self.assertEqual(values["v"], 3.65)
            self.assertEqual(values["T"], calc.round_step(2 * calc.math.pi * 4 / 3.65, 2))

            code, payload = run("associate", "--file", str(calc_path))
            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["rows"], 4)
            self.assertTrue(payload["complete"])

    def test_parameter_count_mismatch_stops_without_writing(self):
        source = CENTRIPETAL.replace("parameters: F_net, m, r", "parameters: F_net, m")
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path, scenario_path = self.write_inputs(directory, source)
            calc_path = directory / "input.calculations.yaml"
            code, payload = run(
                "prepare",
                "--input",
                str(input_path),
                "--scenarios",
                str(scenario_path),
                "--out",
                str(calc_path),
            )
            self.assertEqual(code, 2, payload)
            self.assertTrue(payload["stop"])
            self.assertFalse(calc_path.exists())

    def test_classifier_must_keep_one_role_per_symbol(self):
        source = CENTRIPETAL.replace("parameters: F_net, m, r\n", "")
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path, scenario_path = self.write_inputs(directory, source)
            calc_path = directory / "input.calculations.yaml"
            code, _payload = run(
                "prepare",
                "--input",
                str(input_path),
                "--scenarios",
                str(scenario_path),
                "--out",
                str(calc_path),
            )
            self.assertEqual(code, 0)
            code, payload = run("classify-receive", "--file", str(calc_path))
            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["classify_attempts"], 1)
            self.assertNotIn("question_unknowns", payload)
            bad = {
                "sets": [
                    {"id": "eqset_01", "parameters": ["F_net", "m", "r"], "computed": ["v", "T"]},
                    {"id": "eqset_02", "parameters": ["F_net", "m", "v"], "computed": ["r", "f"]},
                ]
            }
            json_path = directory / "classify.json"
            json_path.write_text(json.dumps(bad), encoding="utf-8")
            code, payload = run(
                "apply",
                "--file",
                str(calc_path),
                "--json-file",
                str(json_path),
            )
            self.assertEqual(code, 1, payload)
            self.assertTrue(any("same role" in message for message in payload["errors"]))

            good = {
                "sets": [
                    {"id": "eqset_01", "parameters": ["F_net", "m", "r"], "computed": ["v", "T"]},
                    {"id": "eqset_02", "parameters": ["F_net", "m", "r"], "computed": ["v", "f"]},
                ]
            }
            json_path.write_text(json.dumps(good), encoding="utf-8")
            code, payload = run(
                "apply",
                "--file",
                str(calc_path),
                "--json-file",
                str(json_path),
            )
            self.assertEqual(code, 0, payload)
            code, payload = run("build", "--file", str(calc_path))
            self.assertEqual(code, 0, payload)


def run(command: str, *args: str) -> tuple[int, dict]:
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, str(SCRIPT), command, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    try:
        payload = json.loads(completed.stdout) if completed.stdout.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not payload:
        payload = {"stdout": completed.stdout, "stderr": completed.stderr}
    return completed.returncode, payload


if __name__ == "__main__":
    unittest.main()
