"""Build the multiple-choice linear-momentum bank from the adaptation plan."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT.parent / "PHY1-CLM-CE2D-10232025" / "PHY1-CLM-CE2D-10232025.yaml"
CHOICES = ROOT / "calculated_choices_temp.csv"
OUT = ROOT / "PHY1-CLM-CE2DMC-11102026.yaml"

CHOICE_KEYS = [
    "correct",
    "drop_perp",
    "conserve_ke",
    "vec_sub_no_mass",
    "one_d_momentum",
    "speed_diff",
]

Q2_OLD = r"\vec{v}_2 = (4996.67 \hat{i}) \text{ m/s}"
Q2_NEW = r"\vec{v}_2 = (4996.67 \hat{i} - 50.00 \hat{j}) \text{ m/s}"
Q5_OLD = (
    r"\vec{V} = (50.00 \hat{i}) \text{ m/s}</latex> explodes into two "
    r"non-identical pieces. (Assuming that the <latex>\hat{i}</latex> "
    r"direction is defined vertically upwards.)"
)
Q5_NEW = (
    r"\vec{V} = (50.00 \hat{j}) \text{ m/s}</latex> explodes into two "
    r"non-identical pieces. (Assuming that the <latex>\hat{j}</latex> "
    r"direction is defined vertically upwards.)"
)


def load_questions(meta_and_body: str) -> list[dict[str, str]]:
    _, body = meta_and_body.split("questions:", 1)
    chunks = re.split(r"\n- numerical:\n", body)[1:]
    questions = []
    for chunk in chunks:
        qid = re.search(r"^\s*id:\s*(\S+)", chunk, re.M).group(1)
        title = re.search(r"^\s*title:\s*(.+)$", chunk, re.M).group(1).rstrip()
        text = re.search(
            r"text:\s*\|\n(?P<body>(?:    .*\n|\n)+?)\s*answer:",
            chunk,
        ).group("body")
        lines = [line[4:] if line.startswith("    ") else line for line in text.splitlines()]
        problem = "\n".join(lines).strip("\n")
        if qid == "q2":
            if Q2_OLD not in problem:
                raise SystemExit("q2 velocity text was not found")
            problem = problem.replace(Q2_OLD, Q2_NEW, 1)
        if qid == "q5":
            if Q5_OLD not in problem:
                raise SystemExit("q5 initial-velocity text was not found")
            problem = problem.replace(Q5_OLD, Q5_NEW, 1)
        questions.append({"id": qid, "title": title, "text": problem})
    return questions


def load_choices() -> dict[str, list[str]]:
    with CHOICES.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["id"]: [row[key] for key in CHOICE_KEYS] for row in rows}


def emit(meta: str, questions: list[dict[str, str]], choices: dict[str, list[str]]) -> str:
    parts = [meta.rstrip() + "\n\nquestions:\n"]
    for item in questions:
        values = choices[item["id"]]
        if len(set(values)) != 6:
            raise SystemExit(f"{item['id']} choices are not distinct: {values}")
        correct = values[0]
        parts.append("- multiple_choice:\n")
        parts.append(f"    id: {item['id']}\n")
        parts.append(f"    title: {item['title']}\n")
        parts.append("    points: 3\n")
        parts.append("    text: |\n")
        for line in item["text"].splitlines():
            parts.append(f"      {line}\n" if line else "\n")
        parts.append("    answers:\n")
        for index, value in enumerate(values):
            parts.append("        - answer:\n")
            parts.append(f"            text: {value} m/s\n")
            parts.append(f"            correct: {'true' if index == 0 else 'false'}\n")
        parts.append("    feedback:\n")
        parts.append("        general: |\n")
        parts.append(
            "          Conserve linear momentum separately on each axis, then combine the "
            f"components. The magnitude is <b><latex>{correct}\\text{{ m/s}}</latex></b>.\n"
        )
        parts.append("        on_correct: Good job!\n")
        parts.append("        on_incorrect: Try again!\n\n")
    return "".join(parts)


def main() -> None:
    questions = load_questions(SOURCE.read_text(encoding="utf-8"))
    choices = load_choices()
    if [item["id"] for item in questions] != [f"q{n}" for n in range(1, 25)]:
        raise SystemExit("expected q1 through q24")
    meta = OUT.read_text(encoding="utf-8").split("questions:", 1)[0]
    OUT.write_text(emit(meta, questions, choices), encoding="utf-8")
    print(f"wrote {OUT.name} ({len(questions)} questions)")


if __name__ == "__main__":
    main()
