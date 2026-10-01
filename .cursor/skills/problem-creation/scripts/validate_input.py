"""Check a problem-creation input YAML for required fields and the scenario-count warning."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required. Run this skill with the repo venv:\n"
        ".venv/Scripts/python.exe -m pip install -r "
        ".cursor/skills/problem-creation/requirements.txt\n"
    )
    sys.exit(1)

# Warning threshold from the workflow spec. This is not the generation target.
WARN_ABOVE = 10

REQUIRED = (
    ("name", ("name",)),
    ("context.scenario", ("context", "scenario")),
    ("context.scenario_specifications", ("context", "scenario_specifications")),
    ("context.n_scenarios", ("context", "n_scenarios")),
    ("structure.formulas", ("structure", "formulas")),
    ("structure.variable_specifications", ("structure", "variable_specifications")),
    ("structure.possible_unknowns", ("structure", "possible_unknowns")),
)


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"Input file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Input YAML must be a mapping: {path}")
    return data


def lookup(data: dict, keys: tuple[str, ...]):
    current = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def formula_strings(value) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        text = value.strip()
        if text:
            found.append(text)
    elif isinstance(value, list):
        for item in value:
            found.extend(formula_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(formula_strings(item))
    return found


def positive_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def validate(path: Path) -> dict:
    data = load_yaml(path)
    missing: list[str] = []
    for label, keys in REQUIRED:
        value = lookup(data, keys)
        if label == "context.n_scenarios":
            if not positive_int(value):
                missing.append(label)
            continue
        if label == "structure.formulas":
            if not formula_strings(value):
                missing.append(label)
            continue
        if is_blank(value):
            missing.append(label)

    warnings: list[str] = []
    n_scenarios = lookup(data, ("context", "n_scenarios"))
    if positive_int(n_scenarios) and n_scenarios > WARN_ABOVE:
        warnings.append(
            f"n_scenarios is {n_scenarios}, which is greater than {WARN_ABOVE}."
        )

    return {
        "ok": not missing,
        "path": str(path),
        "missing": missing,
        "warnings": warnings,
        "n_scenarios": n_scenarios if positive_int(n_scenarios) else None,
        "formulas": formula_strings(lookup(data, ("structure", "formulas"))),
    }


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to the input YAML")
    args = parser.parse_args()
    report = validate(args.input)
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
