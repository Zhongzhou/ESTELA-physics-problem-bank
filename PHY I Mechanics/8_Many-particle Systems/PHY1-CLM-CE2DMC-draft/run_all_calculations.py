"""Dispatch every row of `problem_inputs_temp.csv` to its calculation script and write `calculated_choices_temp.csv`."""

from __future__ import annotations

import csv
from pathlib import Path

from calc_collision_forward import compute_forward_collision_choices
from calc_collision_inverse import compute_inverse_collision_choices
from calc_split import compute_split_choices

BASE = Path(__file__).parent
INPUT_CSV = BASE / "problem_inputs_temp.csv"
OUTPUT_CSV = BASE / "calculated_choices_temp.csv"

DISPATCH = {
    "calc_split.py": compute_split_choices,
    "calc_collision_forward.py": compute_forward_collision_choices,
    "calc_collision_inverse.py": compute_inverse_collision_choices,
}

CHOICE_KEYS = [
    "correct",
    "drop_perp",
    "conserve_ke",
    "vec_sub_no_mass",
    "one_d_momentum",
    "speed_diff",
]


def main() -> None:
    with INPUT_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    for row in rows:
        script_name = row["script"].strip()
        fn = DISPATCH[script_name]
        vals = fn(row)
        rounded = [f"{vals[k]:.2f}" for k in CHOICE_KEYS]
        distinct = len(set(rounded)) == len(rounded)
        out_row = {
            "id": row["id"],
            "title": row["title"],
            "script": script_name,
            **{k: f"{vals[k]:.2f}" for k in CHOICE_KEYS},
            "all_six_distinct": str(distinct),
        }
        out_rows.append(out_row)

    fieldnames = ["id", "title", "script", *CHOICE_KEYS, "all_six_distinct"]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    for r in out_rows:
        choices_str = ", ".join(f"{k}={r[k]}" for k in CHOICE_KEYS)
        print(f"{r['id']} ({r['script']}): {choices_str} | distinct={r['all_six_distinct']}")


if __name__ == "__main__":
    main()
