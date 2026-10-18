#!/usr/bin/env python3
"""Create feedback-only FBDs for the selected inclined-plane bank.

Keep the accompanying draw_inclined_plane_bank.py in the same directory.
Requires matplotlib, numpy, Pillow, and PyYAML. The bank file is read only.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon
import numpy as np
import yaml

from draw_inclined_plane_bank import STATE_TEXT, contact_sheet, state_signs

INK = "#253441"
VELOCITY = "#09696b"
ACCELERATION = "#713b79"
AXIS = "#73828c"


def arrow(ax, start, end, *, color=INK, dashed=False, width=2.2, scale=21, zorder=6, linestyle=None):
    patch = FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=scale,
        linewidth=width, color=color, shrinkA=0, shrinkB=0,
        linestyle=linestyle if linestyle is not None else ((0, (5, 3.3)) if dashed else "-"), zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def label(ax, point, value, *, size=23, color=INK, **kwargs):
    return ax.text(*point, value, ha="center", va="center",
                   fontsize=size, color=color, zorder=9, **kwargs)


def draw_fbd(scenario, state, out):
    velocity_sign, acceleration_sign = state_signs(scenario, state)
    alpha = math.radians(24 if scenario == "scenario 1" else -24)
    tangent = np.array([math.cos(alpha), math.sin(alpha)])
    normal = np.array([-math.sin(alpha), math.cos(alpha)])
    center = np.zeros(2)
    width, height = 1.02, 0.70
    contact = center-height/2*normal
    tension_start = center+width/2*tangent
    tension_end = tension_start+1.85*tangent
    friction_end = contact-velocity_sign*1.65*tangent
    normal_end = contact+1.95*normal
    weight_end = np.array([0.0, -2.10])

    fig, ax = plt.subplots(figsize=(7.5, 8.2), dpi=170)
    fig.patch.set_facecolor("white")
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-2.55, 3.50)
    ax.set_ylim(-3.05, 4.80)
    plt.subplots_adjust(left=.025, right=.975, bottom=.025, top=.975)

    vertices = np.array([
        center-width/2*tangent-height/2*normal,
        center+width/2*tangent-height/2*normal,
        center+width/2*tangent+height/2*normal,
        center-width/2*tangent+height/2*normal,
    ])
    ax.add_patch(Polygon(vertices, closed=True, facecolor="#e8edf1",
                         edgecolor=INK, linewidth=1.7, zorder=3))
    # The axes share an origin on A; the inward -y guide locates theta.
    axis_style = (0, (1.5, 3.0))
    arrow(ax, center, center+2.90*tangent, color=AXIS, width=1.45,
          scale=16, zorder=4, linestyle=axis_style)
    arrow(ax, center, center+2.72*normal, color=AXIS, width=1.45,
          scale=16, zorder=4, linestyle=axis_style)
    negative_y_end = center-2.47*normal
    ax.plot([center[0], negative_y_end[0]], [center[1], negative_y_end[1]],
            color=AXIS, linewidth=1.35, linestyle=axis_style, zorder=4)
    ax.add_patch(Circle(center, radius=.025, facecolor=AXIS, edgecolor=AXIS, zorder=8))
    label(ax, center+3.13*tangent+.08*normal, r"$+x$", color=AXIS, size=19)
    label(ax, center+2.98*normal, r"$+y$", color=AXIS, size=19)
    label(ax, center-2.67*normal+.16*tangent, r"$-y$", color=AXIS, size=19)

    gravity_angle = -90.0
    negative_y_angle = math.degrees(alpha)-90.0
    ax.add_patch(Arc(center, width=2.10, height=2.10,
                     theta1=min(gravity_angle, negative_y_angle),
                     theta2=max(gravity_angle, negative_y_angle),
                     color=INK, linewidth=1.5, zorder=7))
    half_angle = math.radians((gravity_angle+negative_y_angle)/2)
    theta_position = center+1.42*np.array([math.cos(half_angle), math.sin(half_angle)])
    label(ax, theta_position, r"$\theta$", size=23)
    force_arrows = [
        arrow(ax, tension_start, tension_end),
        arrow(ax, contact, normal_end),
        arrow(ax, center, weight_end),
        arrow(ax, contact, friction_end),
    ]
    label(ax, tension_end+.24*normal+.03*tangent, r"$\vec{T}$")
    label(ax, normal_end+.20*normal-.28*tangent, r"$\vec{N}$")
    weight_label_x = -.60 if scenario == "scenario 1" else .60
    label(ax, weight_end+np.array([weight_label_x, -.01]), r"$m_A\vec{g}$", size=24)
    label(ax, friction_end-.30*normal, r"$\vec{f}_k$", size=24)
    label(ax, center-.28*tangent+.15*normal, r"$A$", size=22,
          bbox=dict(facecolor="#e8edf1", edgecolor="none", pad=.15))

    # Kinematic arrows are detached above A and never counted as forces.
    velocity_center = np.array([.02, 2.90])
    acceleration_center = np.array([.02, 4.00])
    velocity_tail = velocity_center-velocity_sign*.95*tangent
    velocity_head = velocity_center+velocity_sign*.95*tangent
    acceleration_tail = acceleration_center-acceleration_sign*.95*tangent
    acceleration_head = acceleration_center+acceleration_sign*.95*tangent
    arrow(ax, velocity_tail, velocity_head, color=VELOCITY, width=2.5, scale=23)
    arrow(ax, acceleration_tail, acceleration_head, color=ACCELERATION,
          dashed=True, width=2.5, scale=23)
    label(ax, velocity_center+.29*normal, r"$\vec{v}_A$", color=VELOCITY, size=25)
    label(ax, acceleration_center+.29*normal, r"$\vec{a}_A$", color=ACCELERATION, size=25)

    label(ax, np.array([.90, -2.78]), "Arrow lengths are schematic.", color=AXIS, size=11)

    prefix = "U" if scenario == "scenario 1" else "D"
    name = f"fbd-{prefix}-{state.replace('_', '-')}"
    hill_velocity = "uphill" if state.startswith("uphill") else "downhill"
    hill_acceleration = hill_velocity if state.endswith("speeding_up") else ("downhill" if hill_velocity == "uphill" else "uphill")
    right_left_velocity = "right" if velocity_sign > 0 else "left"
    right_left_acceleration = "right" if acceleration_sign > 0 else "left"
    friction_hill = "downhill" if hill_velocity == "uphill" else "uphill"
    tension_hill = "uphill" if scenario == "scenario 1" else "downhill"
    alt = (
        f"Free-body diagram of isolated object A. Tension points {tension_hill} toward the right, "
        "the normal force is perpendicular to and outward from the incline, "
        f"weight points vertically down, and kinetic friction points {friction_hill}, opposite the motion. "
        f"Above A, a solid velocity arrow points {hill_velocity} toward the {right_left_velocity}; "
        f"a dashed acceleration arrow points {hill_acceleration} toward the {right_left_acceleration}. "
        "The coordinate axes originate on A: positive x points right along the incline and positive y "
        "points perpendicular and outward. A dotted guide extends in the negative y direction. "
        "The acute angle theta is marked between this negative y direction and the vertically downward weight."
    )
    png = out/"FeedbackFigures"/f"{name}.png"
    svg = out/"FeedbackVectors"/f"{name}.svg"
    fig.savefig(png, dpi=170, facecolor="white", metadata={"Title": "Feedback free-body diagram of A", "Description": alt})
    fig.savefig(svg, facecolor="white", metadata={"Title": "Feedback free-body diagram of A", "Description": alt})
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for text in ax.texts:
        bb = text.get_window_extent(renderer)
        assert fig.bbox.contains(bb.x0, bb.y0) and fig.bbox.contains(bb.x1, bb.y1), (name, text.get_text())
    plt.close(fig)

    assert len(force_arrows) == 4
    assert np.dot(tension_end-tension_start, tangent) > 0
    assert np.dot(friction_end-contact, velocity_sign*tangent) < 0
    assert np.dot(normal_end-contact, normal) > 0
    assert weight_end[0] == 0 and weight_end[1] < 0
    assert np.sign(np.dot(velocity_head-velocity_tail, tangent)) == velocity_sign
    assert np.sign(np.dot(acceleration_head-acceleration_tail, tangent)) == acceleration_sign
    measured_theta = math.degrees(math.acos(np.clip(np.dot(-normal, np.array([0.0,-1.0])), -1.0, 1.0)))
    assert abs(measured_theta-abs(math.degrees(alpha))) < 1e-10
    return {
        "scenario": scenario, "values": {"kinematic_state": state},
        "scene_id": prefix, "scene_caption": STATE_TEXT[state],
        "figure": f"FeedbackFigures/{name}.png",
        "vector_figure": f"FeedbackVectors/{name}.svg",
        "alt_text": alt, "velocity_sign_x": velocity_sign,
        "acceleration_sign_x": acceleration_sign,
        "axes_origin": center.tolist(),
        "negative_y_direction": (-normal).tolist(),
        "theta_degrees": measured_theta,
        "forces": {
            "tension_direction": tangent.tolist(),
            "normal_direction": normal.tolist(),
            "weight_direction": [0.0, -1.0],
            "kinetic_friction_direction": (-velocity_sign*tangent).tolist(),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", type=Path, default=Path(__file__).with_name("input-inclined-plane-confirmed.mcq.yaml"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("inclined-plane-feedback"))
    args = parser.parse_args()
    bank = yaml.safe_load(args.bank.read_text())
    out = args.output.resolve()
    for name in ["FeedbackFigures", "FeedbackVectors"]:
        (out/name).mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans", "svg.fonttype": "none"})
    diagrams = []
    for scenario in bank["scenarios"]:
        axes = bank["variation_axes"]["common"] + bank["variation_axes"]["by_scenario"][scenario["id"]]
        states = next(axis["values"] for axis in axes if axis["id"] == "kinematic_state")
        for state in states:
            diagrams.append(draw_fbd(scenario["id"], state, out))
    (out/"feedback-figure-manifest.json").write_text(json.dumps({"figures": diagrams}, ensure_ascii=False, indent=2)+"\n")
    review = contact_sheet(diagrams, out, "inclined-plane-feedback-review.png",
                           "Feedback: free-body diagrams and motion arrows", columns=2)
    print(json.dumps({"feedback_diagrams": len(diagrams), "review": str(review), "force_and_motion_direction_checks": "passed"}, indent=2))


if __name__ == "__main__":
    main()
