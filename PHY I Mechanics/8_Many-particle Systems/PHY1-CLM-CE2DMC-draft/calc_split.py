"""Compute multiple-choice options for split / explosion / launch problems (q1-q12).

Reads rows assigned to `calc_split.py` from `problem_inputs_temp.csv`.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT_CSV = Path(__file__).with_name("problem_inputs_temp.csv")


def compute_split_choices(row: dict[str, str]) -> dict[str, float]:
    M = float(row["M_total"])
    Vx = float(row["V_total_x"])
    Vy = float(row["V_total_y"])
    mk = float(row["m_known"])
    vkx = float(row["v_known_x"])
    vky = float(row["v_known_y"])
    mu = float(row["m_other"])
    axis = row["parallel_axis"].strip().lower()

    vux = (M * Vx - mk * vkx) / mu
    vuy = (M * Vy - mk * vky) / mu
    correct = math.hypot(vux, vuy)

    drop_perp = vuy if axis == "y" else vux

    V_speed = math.hypot(Vx, Vy)
    vk_speed = math.hypot(vkx, vky)

    ke_radicand = M * V_speed**2 - mk * vk_speed**2
    conserve_ke = math.sqrt(abs(ke_radicand) / mu)

    vec_sub_no_mass = math.hypot(Vx - vkx, Vy - vky)
    one_d_momentum = (M * V_speed - mk * vk_speed) / mu
    speed_diff = V_speed - vk_speed

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
        rows = [r for r in csv.DictReader(f) if r["script"] == "calc_split.py"]

    for row in rows:
        vals = compute_split_choices(row)
        formatted = ", ".join(f"{k}={v:.2f}" for k, v in vals.items())
        print(f"{row['id']}: {formatted}")


if __name__ == "__main__":
    main()
