"""Compute multiple-choice options for inverse sticking collisions (q14, q16, q18, q20, q22, q24).

The combined velocity and one incoming velocity are known; the other incoming speed is asked.
Reads rows assigned to `calc_collision_inverse.py` from `problem_inputs_temp.csv`.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT_CSV = Path(__file__).with_name("problem_inputs_temp.csv")


def compute_inverse_collision_choices(row: dict[str, str]) -> dict[str, float]:
    Mf = float(row["M_total"])
    Vfx = float(row["V_total_x"])
    Vfy = float(row["V_total_y"])
    m1 = float(row["m_known"])
    v1x = float(row["v_known_x"])
    v1y = float(row["v_known_y"])
    m2 = float(row["m_other"])
    axis = row["parallel_axis"].strip().lower()

    v2x = (Mf * Vfx - m1 * v1x) / m2
    v2y = (Mf * Vfy - m1 * v1y) / m2
    correct = math.hypot(v2x, v2y)

    drop_perp = v2y if axis == "y" else v2x

    Vf_speed = math.hypot(Vfx, Vfy)
    v1_speed = math.hypot(v1x, v1y)

    ke_radicand = Mf * Vf_speed**2 - m1 * v1_speed**2
    conserve_ke = math.sqrt(abs(ke_radicand) / m2)

    vec_sub_no_mass = math.hypot(Vfx - v1x, Vfy - v1y)
    one_d_momentum = (Mf * Vf_speed - m1 * v1_speed) / m2
    speed_diff = Vf_speed - v1_speed

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
            r for r in csv.DictReader(f) if r["script"] == "calc_collision_inverse.py"
        ]

    for row in rows:
        vals = compute_inverse_collision_choices(row)
        formatted = ", ".join(f"{k}={v:.2f}" for k, v in vals.items())
        print(f"{row['id']}: {formatted}")


if __name__ == "__main__":
    main()
