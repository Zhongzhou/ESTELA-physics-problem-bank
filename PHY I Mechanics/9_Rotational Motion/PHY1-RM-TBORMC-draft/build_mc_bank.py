"""Build the multiple-choice torque-balance bank from the adaptation plan."""

from __future__ import annotations

import math
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "PHY1-RM-TBOR-11112025.yaml"
OUT = ROOT / "PHY1-RM-TBORMC-11102026-draft.yaml"

SIN = math.sqrt(3) / 2
COS = 0.5

# Pivot, block, force as fractions of L from the right end; weights; unknown.
ROWS = [
    (0, "1/8", "3/4", 4, 32, "F"),  # q1 rod weight raised from 8 N to 32 N
    (0, "1/8", 1, 8, 16, "W_rod"),
    (0, "1/4", "3/4", 16, 32, "W_block"),
    (0, "1/4", 1, 32, 4, "F"),
    (0, "3/4", "1/4", 4, 8, "W_rod"),
    (0, "3/4", 1, 8, 16, "W_block"),
    (0, "7/8", "1/4", 16, 32, "F"),
    (0, "7/8", 1, 32, 4, "W_rod"),
    (0, 1, "1/4", 4, 8, "W_block"),
    (0, 1, "3/4", 8, 16, "F"),
    ("1/4", 0, "3/4", 16, 32, "W_rod"),
    ("1/4", 0, 1, 4, 32, "W_block"),
    ("1/4", "3/4", 1, 16, 8, "F"),  # q13 block weight raised from 4 N to 16 N
    ("1/4", "7/8", 1, 8, 16, "W_rod"),
    ("1/4", 1, "3/4", 16, 32, "W_block"),
    ("3/4", 0, "1/4", 32, 4, "F"),
    ("3/4", "1/8", 0, 4, 8, "W_rod"),
    ("3/4", "1/4", 0, 8, 16, "W_block"),
    ("3/4", 1, 0, 16, 32, "F"),
    ("3/4", 1, "1/4", 4, 32, "W_rod"),
    (1, 0, "1/4", 4, 32, "W_block"),  # q21 rod weight raised from 8 N to 32 N
    (1, 0, "3/4", 8, 16, "F"),
    (1, "1/8", 0, 16, 32, "W_rod"),
    (1, "1/8", "3/4", 32, 4, "W_block"),
    (1, "1/4", 0, 4, 8, "F"),
    (1, "1/4", "3/4", 8, 16, "W_rod"),
    (1, "3/4", 0, 16, 32, "W_block"),
    (1, "3/4", "1/4", 32, 4, "F"),
    (1, "7/8", 0, 8, 16, "W_rod"),  # q29 block 4 N to 8 N, rod answer 8 N to 16 N
    (1, "7/8", "1/4", 8, 16, "W_block"),
]

# Force printed in the problem when the force is known.
STATED_F = {
    2: 18,
    3: 53.33,
    5: 56,
    6: 28,
    8: 60,
    9: 64,
    11: 16,
    12: 18.67,
    14: 24,
    15: 80,
    17: 12.00,
    18: 21.33,
    20: 28.00,
    21: 53.33,
    23: 60.00,
    24: 240.00,
    26: 112.00,
    27: 40.00,
    29: 18,
    30: 24.00,
}


def frac(x) -> float:
    return float(Fraction(x))


def nearest(x: float) -> int:
    return int(math.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def magnitude(x: float) -> int:
    return abs(nearest(x))


def geometry(q: int):
    p, b, f, wb, wr, unk = ROWS[q - 1]
    ab = frac(b) - frac(p)
    ar = 0.5 - frac(p)
    af = frac(f) - frac(p)
    if unk == "F":
        force = (wb * ab + wr * ar) / (COS * af)
    else:
        force = STATED_F[q]
    return unk, ab, ar, af, float(wb), float(wr), float(force)


def solve(unk, perp, ab, ar, af, wb, wr, force) -> float:
    if unk == "F":
        return (wb * ab + wr * ar) / (perp * af)
    if unk == "W_rod":
        return (force * perp * af - wb * ab) / ar
    return (force * perp * af - wr * ar) / ab


def standard(q: int) -> dict[str, int]:
    """The six-role set before the documented per-item substitutes."""
    unk, ab, ar, af, wb, wr, force = geometry(q)
    full = math.copysign(1.0, ar)
    out = {
        "correct": magnitude(solve(unk, COS, ab, ar, af, wb, wr, force)),
        "no_angle": magnitude(solve(unk, 1.0, ab, ar, af, wb, wr, force)),
        "sincos": magnitude(solve(unk, SIN, ab, ar, af, wb, wr, force)),
        "full_length": magnitude(solve(unk, COS, ab, full, af, wb, wr, force)),
    }
    if unk == "F":
        out["opposite"] = magnitude((abs(wb * ab) - abs(wr * ar)) / (COS * abs(af)))
        out["ignore_rod"] = magnitude(solve("F", COS, ab, ar, af, wb, 0.0, force))
        out["weights_added"] = nearest(wb + wr)
    elif unk == "W_rod":
        out["opposite"] = magnitude((abs(force * COS * af) + abs(wb * ab)) / abs(ar))
        out["ignore_block"] = magnitude((force * COS * af) / ar)
        out["force_balance"] = magnitude(force - wb)
    else:
        out["opposite"] = magnitude((abs(force * COS * af) + abs(wr * ar)) / abs(ab))
        out["ignore_rod"] = magnitude((force * COS * af) / ab)
        out["force_balance"] = magnitude(force - wr)
    return out


def choices_for(q: int) -> list[tuple[int, bool]]:
    """Return (value, is_correct) in plan order."""
    base = standard(q)
    _, ab, ar, af, wb, wr, force = geometry(q)

    if q in {1, 7, 13, 16, 25, 28}:
        keys = ["correct", "no_angle", "sincos", "opposite", "ignore_rod", "full_length", "weights_added"]
        vals = [base[k] for k in keys]
    elif q == 4:
        ignore_block = magnitude((wr * ar) / (COS * af))
        vals = [base["correct"], base["no_angle"], base["sincos"], ignore_block, base["ignore_rod"], base["full_length"], base["weights_added"]]
    elif q in {10, 22}:
        force_balance = nearest(2 * (wb + wr))
        # Block moved to the center: both weights use lever arm L/2.
        center = 0.5 - (0.0 if q == 10 else 1.0)
        arm_f = af
        placed = magnitude((wb * center + wr * center) / (COS * arm_f))
        vals = [base["correct"], base["no_angle"], base["sincos"], force_balance, placed, base["full_length"], base["weights_added"]]
    elif q == 19:
        same_dir = magnitude((abs(wb * ab) + abs(wr * ar)) / (COS * abs(af)))
        ignore_block = magnitude((wr * ar) / (COS * af))
        vals = [base["correct"], base["no_angle"], base["sincos"], same_dir, ignore_block, base["full_length"], nearest(wb + wr)]
    elif q in {2, 5, 8, 23, 26, 29}:
        vals = [base["correct"], base["no_angle"], base["sincos"], base["opposite"], base["ignore_block"], base["full_length"], base["force_balance"]]
    elif q in {14, 17}:
        added = nearest(force * COS + wb)
        vals = [base["correct"], base["no_angle"], base["sincos"], base["opposite"], base["ignore_block"], base["full_length"], added]
    elif q == 11:
        # Lever arms read as distances from the right end.
        from_end = magnitude((force * COS * (0.75)) / 0.5)  # block arm 0, rod arm 1/2, force arm 3/4
        added = nearest(force * COS + wb)
        vals = [base["correct"], base["no_angle"], base["sincos"], from_end, base["ignore_block"], base["full_length"], added]
    elif q == 20:
        same_dir = magnitude((abs(force * COS * af) - abs(wb * ab)) / abs(ar))
        angled = magnitude(force * COS - wb)
        vals = [base["correct"], base["no_angle"], base["sincos"], same_dir, base["ignore_block"], base["full_length"], angled]
    elif q in {3, 6, 21, 24, 27}:
        vals = [base["correct"], base["no_angle"], base["sincos"], base["opposite"], base["ignore_rod"], base["full_length"], base["force_balance"]]
    elif q == 30:
        angled = magnitude(force * COS - wr)
        vals = [base["correct"], base["no_angle"], base["sincos"], base["opposite"], base["ignore_rod"], base["full_length"], angled]
    elif q == 9:
        angled = nearest(force * COS - wr)
        # Rod weight placed at the force.
        force_arm = abs(af)
        placed = magnitude((force * COS * af - wr * math.copysign(force_arm, ar)) / ab)
        vals = [base["correct"], base["no_angle"], base["sincos"], abs(angled), base["ignore_rod"], placed, base["force_balance"]]
    elif q == 15:
        half = magnitude(solve("W_block", COS, ab, math.copysign(0.5, ar), af, wb, wr, force))
        vals = [base["correct"], base["no_angle"], base["sincos"], base["opposite"], base["ignore_rod"], half, base["force_balance"]]
    elif q == 12:
        half = magnitude(solve("W_block", COS, ab, math.copysign(0.5, ar), af, wb, wr, force))
        vals = [base["correct"], base["no_angle"], base["sincos"], half, base["ignore_rod"], base["full_length"], base["force_balance"]]
    elif q == 18:
        # Distances from the right end; force at the right end contributes nothing.
        from_end = magnitude((wr * 0.5) / (0.25) * -1)  # Wb*(1/4) + Wr*(1/2) = 0
        added = nearest(force * COS + wr)
        vals = [base["correct"], base["no_angle"], base["sincos"], abs(from_end), base["ignore_rod"], added, base["force_balance"]]
    else:
        raise ValueError(q)

    flagged = [(v, i == 0) for i, v in enumerate(vals)]
    if len({v for v, _ in flagged}) != 7:
        raise SystemExit(f"q{q} choices are not distinct: {vals}")
    return flagged


def load_questions() -> list[dict[str, str]]:
    raw = SOURCE.read_text(encoding="utf-8")
    meta, body = raw.split("questions:", 1)
    meta = meta.replace(
        "bank_id: PHY1-RM-TBOR-11112025",
        "bank_id: PHY1-RM-TBORMC-11102026-draft",
        1,
    )
    chunks = re.split(r"\n- numerical:\n", body)[1:]
    questions = []
    for chunk in chunks:
        qid = re.search(r"^\s*id:\s*(\S+)", chunk, re.M).group(1)
        title = re.search(r"^\s*title:\s*(.+)$", chunk, re.M).group(1).rstrip()
        figure = re.search(r"^\s*figure:\s*(\S+)", chunk, re.M).group(1)
        text = re.search(r"text:\s*\|\n(?P<body>(?:    .*\n|\n)+?)\s*figure:", chunk).group("body")
        lines = [line[4:] if line.startswith("    ") else line for line in text.splitlines()]
        problem = "\n".join(lines).strip("\n")
        questions.append({"id": qid, "title": title, "figure": figure, "text": problem})
    return meta, questions


def solution(q: int) -> str:
    unk, ab, ar, af, wb, wr, force = geometry(q)
    correct = choices_for(q)[0][0]
    if unk == "F":
        asked = "force"
    elif unk == "W_rod":
        asked = "rod weight"
    else:
        asked = "block weight"
    return (
        "About the pivot, with the perpendicular component "
        "<latex>F\\cos 60^\\circ = F/2</latex> and the rod's weight at its center, "
        f"torque balance gives the {asked} "
        f"<b><latex>{correct}\\text{{ N}}</latex></b>."
    )


def emit(meta: str, questions: list[dict[str, str]]) -> str:
    parts = [meta.rstrip() + "\n\nquestions:\n"]
    for q, item in enumerate(questions, 1):
        text = item["text"]
        if q == 1:
            text = text.replace("The rod’s weight is **8 N**.", "The rod’s weight is **32 N**.", 1)
        if q == 13:
            text = text.replace("A block of weight **4 N**", "A block of weight **16 N**", 1)
        if q == 21:
            text = text.replace("The rod’s weight is **8 N**.", "The rod’s weight is **32 N**.", 1)
            text = text.replace("**21.33 N**", "**53.33 N**", 1)
        if q == 29:
            text = text.replace("A block of weight **4 N**", "A block of weight **8 N**", 1)
            text = text.replace("**9.00 N**", "**18 N**", 1)
        choices = choices_for(q)
        parts.append("- multiple_choice:\n")
        parts.append(f"    id: {item['id']}\n")
        parts.append(f"    title: {item['title']}\n")
        parts.append("    points: 1\n")
        parts.append("    text: |\n")
        for line in text.splitlines():
            parts.append(f"      {line}\n" if line else "\n")
        parts.append(f"    figure: {item['figure']}\n")
        parts.append("    answers:\n")
        for value, correct in choices:
            parts.append("        - answer:\n")
            parts.append(f"            text: {value} N\n")
            parts.append(f"            correct: {'true' if correct else 'false'}\n")
        parts.append("    feedback:\n")
        parts.append("        general: |\n")
        parts.append(f"          {solution(q)}\n")
        parts.append("        on_correct: Good job!\n")
        parts.append("        on_incorrect: Try again!\n\n")
    return "".join(parts)


def main() -> None:
    meta, questions = load_questions()
    if len(questions) != 30:
        raise SystemExit(f"expected 30 questions, found {len(questions)}")
    OUT.write_text(emit(meta, questions), encoding="utf-8")
    print(f"wrote {OUT.name}")
    for q in range(1, 31):
        vals = [v for v, _ in choices_for(q)]
        print(f"q{q}: {vals}")


if __name__ == "__main__":
    main()
