"""Compute multiple-choice options for forward sticking collisions (q13, q15, q17, q19, q21, q23).

Both incoming velocities are known; the combined speed after collision is asked.
Reads rows assigned to `calc_collision_forward.py` from `problem_inputs_temp.csv`.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT_CSV = Path(__file__).with_name("problem_inputs_temp.csv")


def compute_forward_collision_choices(row: dict[str, str]) -> dict[str, float]:
    Mf = float(row["M_total"])
    m1 = float(row["m_known"])
    v1x = float(row["v_known_x"])
    v1y = float(row["v_known_y"])
    m2 = float(row["m_other"])
    v2x = float(row["v_other_x"])
    v2y = float(row["v_other_y"])
    axis = row["parallel_axis"].strip().lower()

    Vfx = (m1 * v1x + m2 * v2x) / Mf
    Vfy = (m1 * v1y + m2 * v2y) / Mf
    correct = math.hypot(Vfx, Vfy)

    drop_perp = Vfy if axis == "y" else Vfx

    v1_speed = math.hypot(v1x, v1y)
    v2_speed = math.hypot(v2x, v2y)

    conserve_ke = math.sqrt((m1 * v1_speed**2 + m2 * v2_speed**2) / Mf)
    vec_sub_no_mass = math.hypot(v1x - v2x, v1y - v2y)
    one_d_momentum = (m1 * v1_speed + m2 * v2_speed) / Mf
    speed_diff = v1_speed - v2_speed

    return {
        "correct": correct,
        "drop_perp": drop_perp,
        "conserve_ke": conserve_ke,
        "vec_sub_no_mass": vec_sub_no_mass,
        "one_d_momentum": one_d_momentum,
        "speed_diff": speed_diff,
    }


def main() -> None:
    with INPUT_CSV.open(newline="", encoding="utf-8") as f:
        rows = [
            r for r in csv.DictReader(f) if r["script"] == "calc_collision_forward.py"
        ]

    for row in rows:
        vals = compute_forward_collision_choices(row)
        formatted = ", ".join(f"{k}={v:.2f}" for k, v in vals.items())
        print(f"{row['id']}: {formatted}")


if __name__ == "__main__":
    main()
