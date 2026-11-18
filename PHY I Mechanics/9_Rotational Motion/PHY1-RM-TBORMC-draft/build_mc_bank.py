"""Build the multiple-choice torque-balance bank.

Balance, with positions measured from the right end:

    (x_F - x_p) * F / 2 = (0.5 - x_p) * W_r + (x_b - x_p) * W_b

The position differences stay signed. That one equation is the balance for
every pivot in the bank. Ties at n + 1/2 round to the even integer, which is
how the update plan lists 26.50 N as 26 N and 82.50 N as 82 N.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT.parent / "PHY1-RM-TBOR-11112025" / "PHY1-RM-TBOR-11112025.yaml"
OUT = ROOT / "PHY1-RM-TBORMC-11102026.yaml"

SIN = math.sqrt(3) / 2
COS = 0.5
TEXTBOOK = {4, 8, 16, 32}

# Pivot, block, force as fractions of L from the right end.
# Block weight, rod weight, unknown. A weight that is the unknown is stored
# as 0 and is not read back.
ROWS = [
    (0, "1/8", "3/4", 5, 42, "F"),
    (0, "1/8", 1, 14, 0, "W_rod"),
    (0, "1/4", "3/4", 0, 70, "W_block"),
    (0, "1/4", 1, 48, 6, "F"),
    (0, "3/4", "1/4", 10, 0, "W_rod"),
    (0, "3/4", 1, 0, 18, "W_block"),
    (0, "7/8", "1/4", 21, 42, "F"),
    (0, "7/8", 1, 54, 0, "W_rod"),
    (0, 1, "1/4", 0, 18, "W_block"),
    (0, 1, "3/4", 12, 24, "F"),
    ("1/4", 0, "3/4", 42, 0, "W_rod"),
    ("1/4", 0, 1, 0, 37, "W_block"),
    ("1/4", "3/4", 1, 21, 10, "F"),
    ("1/4", "7/8", 1, 14, 0, "W_rod"),
    ("1/4", 1, "3/4", 0, 70, "W_block"),
    ("3/4", 0, "1/4", 48, 6, "F"),
    ("3/4", "1/8", 0, 10, 0, "W_rod"),
    ("3/4", "1/4", 0, 0, 18, "W_block"),
    ("3/4", 1, 0, 21, 42, "F"),
    ("3/4", 1, "1/4", 7, 0, "W_rod"),
    (1, 0, "1/4", 0, 70, "W_block"),
    (1, 0, "3/4", 12, 24, "F"),
    (1, "1/8", 0, 42, 0, "W_rod"),
    (1, "1/8", "3/4", 0, 5, "W_block"),
    (1, "1/4", 0, 5, 10, "F"),
    (1, "1/4", "3/4", 14, 0, "W_rod"),
    (1, "3/4", 0, 0, 70, "W_block"),
    (1, "3/4", "1/4", 48, 6, "F"),
    (1, "7/8", 0, 21, 0, "W_rod"),
    (1, "7/8", "1/4", 0, 18, "W_block"),
]

# Force printed in the problem when the force is known.
STATED_F = {
    2: 31,
    3: 117,
    5: 146,
    6: 35,
    8: 120,
    9: 141,
    11: 42,
    12: 21,
    14: 41,
    15: 176,
    17: 31,
    18: 25,
    20: 48,
    21: 117,
    23: 156,
    24: 276,
    26: 190,
    27: 88,
    29: 47,
    30: 28,
}

# Nearest integer from the update plan.
EXPECTED = {
    1: 58,
    2: 28,
    3: 36,
    4: 30,
    5: 22,
    6: 11,
    7: 315,
    8: 26,
    9: 9,
    10: 64,
    11: 84,
    12: 6,
    13: 35,
    14: 26,
    15: 35,
    16: 150,
    17: 22,
    18: 10,
    19: 14,
    20: 55,
    21: 9,
    22: 192,
    23: 82,
    24: 37,
    25: 18,
    26: 26,
    27: 36,
    28: 40,
    29: 42,
    30: 12,
}


def frac(x) -> float:
    return float(Fraction(x))


def nearest(x: float) -> int:
    """Round half to even. Exact halves in this bank are dyadic, so floats are exact."""
    if abs(x) < 1e-9:
        return 0
    sign = 1 if x > 0 else -1
    ax = abs(x)
    n = math.floor(ax + 1e-9)
    frac_part = ax - n
    if abs(frac_part - 0.5) <= 1e-8:
        rounded = n if n % 2 == 0 else n + 1
    elif frac_part < 0.5:
        rounded = n
    else:
        rounded = n + 1
    return sign * rounded


def mag(x: float) -> int:
    return abs(nearest(x))


def geometry(q: int):
    p, b, f, wb, wr, unk = ROWS[q - 1]
    ab = frac(b) - frac(p)
    ar = 0.5 - frac(p)
    af = frac(f) - frac(p)
    wb = float(wb)
    wr = float(wr)
    if unk == "F":
        force = (wb * ab + wr * ar) / (COS * af)
    else:
        force = float(STATED_F[q])
    return unk, ab, ar, af, wb, wr, float(force)


def solve(unk, perp, ab, ar, af, wb, wr, force) -> float:
    if unk == "F":
        return (wb * ab + wr * ar) / (perp * af)
    if unk == "W_rod":
        return (force * perp * af - wb * ab) / ar
    return (force * perp * af - wr * ar) / ab


def standard(q: int) -> dict[str, int]:
    """Six distractor roles before the per-item stand-ins.

    On the same side of the pivot the direction mistake reverses one weight.
    On opposite sides that reversal is the correct balance, so the mistake
    gives the two weights the same direction.
    """
    unk, ab, ar, af, wb, wr, force = geometry(q)
    same = (ab > 0) == (ar > 0)
    full = math.copysign(1.0, ar)
    out = {
        "correct": mag(solve(unk, COS, ab, ar, af, wb, wr, force)),
        "no_angle": mag(solve(unk, 1.0, ab, ar, af, wb, wr, force)),
        "sincos": mag(solve(unk, SIN, ab, ar, af, wb, wr, force)),
        "full_length": mag(solve(unk, COS, ab, full, af, wb, wr, force)),
    }
    tauf = abs(force * COS * af)
    taub = abs(wb * ab)
    taur = abs(wr * ar)
    if unk == "F":
        if same:
            out["direction"] = mag((abs(wb * ab) - abs(wr * ar)) / (COS * abs(af)))
        else:
            out["direction"] = mag((abs(wb * ab) + abs(wr * ar)) / (COS * abs(af)))
        out["dropped"] = mag(solve("F", COS, ab, ar, af, wb, 0.0, force))
        out["nolever"] = nearest(wb + wr)
    elif unk == "W_rod":
        if same:
            out["direction"] = mag((tauf + taub) / abs(ar))
        else:
            out["direction"] = mag(abs(tauf - taub) / abs(ar))
        out["dropped"] = mag((force * COS * af) / ar)
        out["nolever"] = mag(force - wb)
    else:
        if same:
            out["direction"] = mag((tauf + taur) / abs(ab))
        else:
            out["direction"] = mag(abs(tauf - taur) / abs(ab))
        out["dropped"] = mag((force * COS * af) / ab)
        out["nolever"] = mag(force - wr)
    return out


def choices_for(q: int) -> list[tuple[int, bool]]:
    """Return (value, is_correct) in the bank's existing role order."""
    base = standard(q)
    unk, ab, ar, af, wb, wr, force = geometry(q)
    order = ["correct", "no_angle", "sincos", "direction", "dropped", "full_length", "nolever"]
    vals = [base[k] for k in order]

    # Stand-ins from choice-set-adaptation.md, used only where the standard
    # role is 0 N or the same integer as another choice.
    if q == 6:
        # Opposite-direction and no-angle both round to 35 N.
        # F/2 - W_r rounds to 0 N, so the angle-kept sum is the stand-in.
        vals[3] = nearest(force * COS + wr)
    elif q == 9:
        # A rod arm of L cancels the force torque, so the block weight is 0 N.
        force_arm = abs(af)
        vals[5] = mag((force * COS * af - wr * math.copysign(force_arm, ar)) / ab)
    elif q in {10, 22}:
        # Equal weight torques: the direction mistake is 0 N, and dropping
        # either weight matches the no-angle choice.
        vals[3] = nearest(2 * (wb + wr))
        center = 0.5 - (0.0 if q == 10 else 1.0)
        vals[4] = mag((wb * center + wr * center) / (COS * af))
    elif q == 11:
        # Block torque equals the force torque, and F equals the block weight.
        vals[3] = mag((force * COS * 0.75) / 0.5)
        vals[6] = nearest(force * COS + wb)
    elif q == 12:
        # Same-direction magnitude equals the correct block weight.
        vals[3] = mag(solve("W_block", COS, ab, math.copysign(0.5, ar), af, wb, wr, force))
    elif q == 14:
        # |F - W_b| = 27 N. The balance is exactly 26.5 N, so 27 N is the
        # other nearest integer. The angle-kept sum keeps that slot.
        vals[6] = nearest(force * COS + wb)
    elif q == 15:
        # Full-length magnitude equals the correct block weight.
        vals[5] = mag(solve("W_block", COS, ab, math.copysign(0.5, ar), af, wb, wr, force))
    elif q == 17:
        # |F - W_b| = 21 N, the other nearest integer of the exact 21.5 N rod.
        vals[6] = nearest(force * COS + wb)
    elif q == 18:
        # Opposite-direction rounds to the no-angle choice. The force is at
        # the right end, so distances printed in the stem give it no torque.
        vals[3] = mag((wr * 0.5) / 0.25)
    elif q == 19:
        # Dropping the rod repeats the correct force.
        vals[4] = mag((wr * ar) / (COS * af))
    elif q == 20:
        # F - W_b lands on the same-direction choice.
        vals[6] = mag(force * COS - wb)

    if len(vals) != 7 or len(set(vals)) != 7 or any(v <= 0 for v in vals):
        raise SystemExit(f"q{q} choices are not distinct positive integers: {vals}")
    if vals[0] != EXPECTED[q]:
        raise SystemExit(f"q{q} key {vals[0]} != planned {EXPECTED[q]}")
    if vals[0] in TEXTBOOK:
        raise SystemExit(f"q{q} key {vals[0]} is still in {{4, 8, 16, 32}}")
    return [(v, i == 0) for i, v in enumerate(vals)]


def load_questions() -> list[dict[str, str]]:
    raw = SOURCE.read_text(encoding="utf-8")
    _, body = raw.split("questions:", 1)
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
    return questions


def stamp_givens(text: str, q: int) -> str:
    """Write the new weights and force into the source stem. Leave the angle alone."""
    _, _, _, wb, wr, unk = ROWS[q - 1]
    if unk != "W_rod":
        text, n = re.subn(
            r"(The rod[’']s weight is \*\*)[0-9.]+( N\*\*)",
            rf"\g<1>{int(wr)}\2",
            text,
            count=1,
        )
        if n != 1:
            raise SystemExit(f"q{q} rod weight was not found in the stem")
    if unk != "W_block":
        text, n = re.subn(
            r"(A block of weight \*\*)[0-9.]+( N\*\*)",
            rf"\g<1>{int(wb)}\2",
            text,
            count=1,
        )
        if n != 1:
            raise SystemExit(f"q{q} block weight was not found in the stem")
    if unk != "F":
        text, n = re.subn(
            r"(magnitude \*\*)[0-9.]+( N\*\*)",
            rf"\g<1>{int(STATED_F[q])}\2",
            text,
            count=1,
        )
        if n != 1:
            raise SystemExit(f"q{q} force was not found in the stem")
    return text


def solution(q: int) -> str:
    unk = ROWS[q - 1][5]
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
        text = stamp_givens(item["text"], q)
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


def numbers_blanked(text: str) -> str:
    return re.sub(r"\d+(?:\.\d+)?", "#", text)


def main() -> None:
    questions = load_questions()
    if len(questions) != 30:
        raise SystemExit(f"expected 30 questions, found {len(questions)}")
    if not OUT.exists():
        raise SystemExit(f"missing {OUT.name}; its bank_info is kept")
    previous = OUT.read_text(encoding="utf-8")
    meta = previous.split("questions:", 1)[0]
    rendered = emit(meta, questions)
    if previous:
        old_lines = numbers_blanked(previous).splitlines()
        new_lines = numbers_blanked(rendered).splitlines()
        if old_lines != new_lines:
            import difflib

            diff = "\n".join(
                difflib.unified_diff(old_lines, new_lines, lineterm="", n=1)
            )
            raise SystemExit("stem wording changed beyond the newton values:\n" + diff[:4000])
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.name}")
    for q in range(1, 31):
        vals = [v for v, _ in choices_for(q)]
        close = sorted(
            {
                tuple(sorted((vals[i], vals[j])))
                for i in range(len(vals))
                for j in range(i + 1, len(vals))
                if abs(vals[i] - vals[j]) == 1
            }
        )
        note = f"  1 N apart: {close}" if close else ""
        print(f"q{q}: {vals}{note}")


if __name__ == "__main__":
    main()
