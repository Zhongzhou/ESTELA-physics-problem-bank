#!/usr/bin/env python3
"""Assemble the 12-question Coulomb-law YAML bank and its figure package."""

from __future__ import annotations

import math
import shutil
import zipfile
from pathlib import Path

import yaml

from coulomb_problem_bank_diagrams import SCENARIOS
from generate_coulomb_solution_snippets import LiteralString, force_data


ROOT = Path(__file__).resolve().parent
HEADS_PATH = ROOT / "coulomb_problem_heads.yaml"
SOLUTIONS_PATH = ROOT / "coulomb_solution_snippets.yaml"
FIGURE_SOURCE = ROOT / "coulomb_problem_diagrams_400px"
BANK_FILENAME = "PHY2-EM-NFPC-test7.yaml"
BANK_PATH = ROOT / BANK_FILENAME
PACKAGE_DIRECTORY = ROOT / "PHY2-EM-NFPC-test7"
PACKAGE_ZIP = ROOT / "PHY2-EM-NFPC-test7.zip"


def by_id(path: Path, root_key: str) -> dict[str, str]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {entry["id"]: entry["html"] for entry in payload[root_key]}


def magnitude_for_scenario(scenario) -> float:
    sources = sorted(
        label for label, _charge, _position in scenario.charges if label != scenario.target
    )
    first = force_data(scenario, sources[0])
    second = force_data(scenario, sources[1])
    net_x = float(first["force_x"]) + float(second["force_x"])
    net_y = float(first["force_y"]) + float(second["force_y"])
    return math.hypot(net_x, net_y)


def two_significant_digit_interval(value: float) -> tuple[float, float]:
    """Return the full rounding interval for a two-significant-digit response."""

    exponent = math.floor(math.log10(abs(value)))
    increment = 10 ** (exponent - 1)
    rounded_value = round(value / increment) * increment
    lower = rounded_value - increment / 2
    upper = rounded_value + increment / 2
    # Remove floating-point representation noise before YAML serialization.
    return float(f"{lower:.12g}"), float(f"{upper:.12g}")


def build_bank() -> dict[str, object]:
    heads = by_id(HEADS_PATH, "problem_heads")
    solutions = by_id(SOLUTIONS_PATH, "solution_snippets")
    expected_ids = {f"q{number}" for number in range(1, 13)}
    if set(heads) != expected_ids or set(solutions) != expected_ids:
        raise ValueError("The head and solution files must each contain q1 through q12.")

    questions: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        question_id = f"q{scenario.number}"
        sources = sorted(
            label
            for label, _charge, _position in scenario.charges
            if label != scenario.target
        )
        geometry_figure = f"Figures/coulomb_problem_{scenario.number:02d}.png"
        feedback_figures = [
            (
                f"Figures/coulomb_problem_{scenario.number:02d}_"
                f"force_{source}_on_{scenario.target}.png"
            )
            for source in sources
        ]
        lower, upper = two_significant_digit_interval(
            magnitude_for_scenario(scenario)
        )
        questions.append(
            {
                "numerical": {
                    "id": question_id,
                    "title": (
                        f"PHY2-EM-Electrostatics-NFPC problem {scenario.number}"
                    ),
                    "points": 1,
                    "text": LiteralString(heads[question_id]),
                    "figure": geometry_figure,
                    "settings": {"scientific": True},
                    "answer": {
                        "range_start": lower,
                        "range_end": upper,
                    },
                    "feedback": {
                        "general": LiteralString(solutions[question_id]),
                        "figure": feedback_figures,
                    },
                }
            }
        )

    return {
        "bank_info": {
            "title": "Electrostatic Forces due to Point Charges",
            "bank_id": "PHY2-EM-NFPC-test7",
            "description": LiteralString(
                "These problems involve net force, Coulomb's law, and vector addition."
            ),
            "date_created": "08-31-2026",
            "status": "draft",
            "LLM": "ChatGPT 5.6",
            "generation prompts": [
                {
                    "prompt 1": (
                        "Testing formatting with delimiters for math and figures in "
                        "the question head and feedback."
                    )
                }
            ],
            "authors": ["author 1"],
        },
        "questions": questions,
    }


def validate_bank(bank: dict[str, object]) -> None:
    questions = bank["questions"]
    if not isinstance(questions, list) or len(questions) != 12:
        raise ValueError("The bank must contain exactly 12 questions.")

    for expected_number, wrapper in enumerate(questions, start=1):
        question = wrapper["numerical"]
        if question["id"] != f"q{expected_number}":
            raise ValueError("Question IDs are out of sequence.")
        if question["answer"]["range_start"] >= question["answer"]["range_end"]:
            raise ValueError(f"Question q{expected_number} has an invalid answer range.")
        figure_paths = [question["figure"], *question["feedback"]["figure"]]
        if len(figure_paths) != 3 or len(set(figure_paths)) != 3:
            raise ValueError(f"Question q{expected_number} must have three figures.")
        for relative_path in figure_paths:
            source_path = FIGURE_SOURCE / Path(relative_path).name
            if not source_path.is_file():
                raise FileNotFoundError(source_path)


def write_bank_and_package(bank: dict[str, object]) -> None:
    rendered = yaml.safe_dump(
        bank,
        sort_keys=False,
        allow_unicode=True,
        width=10_000,
    )
    BANK_PATH.write_text(rendered, encoding="utf-8")

    figures_directory = PACKAGE_DIRECTORY / "Figures"
    figures_directory.mkdir(parents=True, exist_ok=True)
    (PACKAGE_DIRECTORY / BANK_FILENAME).write_text(rendered, encoding="utf-8")

    expected_images: set[str] = set()
    for wrapper in bank["questions"]:
        question = wrapper["numerical"]
        expected_images.add(Path(question["figure"]).name)
        expected_images.update(Path(path).name for path in question["feedback"]["figure"])
    for filename in sorted(expected_images):
        shutil.copy2(FIGURE_SOURCE / filename, figures_directory / filename)

    with zipfile.ZipFile(PACKAGE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIRECTORY.rglob("*")):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(PACKAGE_DIRECTORY))


def main() -> None:
    bank = build_bank()
    validate_bank(bank)
    write_bank_and_package(bank)

    reparsed = yaml.safe_load(BANK_PATH.read_text(encoding="utf-8"))
    validate_bank(reparsed)
    print(f"Created problem bank: {BANK_PATH}")
    print(f"Created package: {PACKAGE_ZIP}")
    print("Questions: 12; referenced figures: 36")


if __name__ == "__main__":
    main()
