#!/usr/bin/env python3
"""Draw the selected inclined-plane bank without changing its workflow state.

Requires Python 3.10+, matplotlib, numpy, Pillow, and PyYAML.
Example:
    python draw_inclined_plane_bank.py --bank input-inclined-plane-confirmed.mcq.yaml

Individual student figures show only geometry and coordinate axes.
Each scene's figure is reused across its permitted motion states.
Review sheets add captions outside the individual figures.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import yaml


INK = "#263442"
AXIS = "#18577d"
SURFACE = "#e9edf0"
ROPE = "#333333"

OBJECTS = {
    ("scenario 1", 0): ("wooden crate", "sandbag", "#e9c79f", "#e4cfaa", "crate", "bag"),
    ("scenario 1", 1): ("brass block", "steel weight", "#edda95", "#c2ccd3", "plain", "weight"),
    ("scenario 1", 2): ("concrete paver", "gravel bucket", "#d3d8dc", "#c4cbd0", "concrete", "bucket"),
    ("scenario 1", 3): ("scenery block", "stage counterweight", "#d8cde0", "#c4cbd0", "felt", "weight"),
    ("scenario 2", 0): ("wooden block", "hanging mass", "#e9c79f", "#c2ccd3", "plain", "weight"),
    ("scenario 2", 1): ("packing crate", "sandbag", "#e9c79f", "#e4cfaa", "crate", "bag"),
    ("scenario 2", 2): ("rubber specimen block", "weight pouch", "#bfd8d2", "#d8c9b5", "rubber", "bag"),
    ("scenario 2", 3): ("wooden stage prop", "counterweight", "#d8cde0", "#c4cbd0", "plain", "weight"),
}

STATE_TEXT = {
    "uphill_speeding_up": "Moving uphill; speeding up",
    "uphill_slowing_down": "Moving uphill; slowing down",
    "downhill_speeding_up": "Moving downhill; speeding up",
    "downhill_slowing_down": "Moving downhill; slowing down",
}


def drawing_requests(bank: dict) -> list[dict]:
    axes = bank["variation_axes"]
    requests = []
    for scenario in bank["scenarios"]:
        all_axes = axes["common"] + axes["by_scenario"][scenario["id"]]
        drawing_axes = [axis for axis in all_axes if axis["changes_drawing"]]
        for scene_index, scene in enumerate(scenario["scenes"]):
            if scene["status"] != "kept":
                continue
            for values in itertools.product(*(axis["values"] for axis in drawing_axes)):
                requests.append({
                    "scenario": scenario["id"],
                    "scene_index": scene_index,
                    "drawing": dict(zip((axis["id"] for axis in drawing_axes), values)),
                })
    return requests


def state_signs(scenario: str, state: str) -> tuple[int, int]:
    uphill_sign = 1 if scenario == "scenario 1" else -1
    velocity = uphill_sign if state.startswith("uphill") else -uphill_sign
    acceleration = velocity if state.endswith("speeding_up") else -velocity
    if scenario == "scenario 2" and state.startswith("uphill"):
        raise ValueError("Uphill motion on the right-falling incline is excluded from this bank.")
    return velocity, acceleration


def text(ax, point, label, size=21, color=INK, **kwargs):
    return ax.text(*point, label, fontsize=size, color=color, ha="center", va="center", **kwargs)


def arrow(ax, start, end, *, color, dashed=False, width=2.1, scale=19, zorder=9):
    patch = FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=scale,
        linewidth=width, color=color, shrinkA=0, shrinkB=0,
        linestyle=(0, (5, 3.2)) if dashed else "-",
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def draw_hanging(ax, center, kind, fill):
    width, height = 0.78, 0.92
    cx, cy = center
    if kind == "bag":
        vertices = np.array([
            [-0.10, height/2], [0.10, height/2],
            [width/2, height*0.26], [width/2, -height*0.32],
            [width*0.28, -height/2], [-width*0.28, -height/2],
            [-width/2, -height*0.32], [-width/2, height*0.26],
        ]) + center
    elif kind == "bucket":
        vertices = np.array([
            [-width/2, height/2], [width/2, height/2],
            [width*0.34, -height/2], [-width*0.34, -height/2],
        ]) + center
    else:
        vertices = np.array([
            [-width/2, height/2], [width/2, height/2],
            [width/2, -height/2], [-width/2, -height/2],
        ]) + center
    patch = Polygon(vertices, closed=True, facecolor=fill, edgecolor=INK, linewidth=1.8, zorder=5)
    ax.add_patch(patch)
    if kind == "bucket":
        ax.plot([cx-width/2, cx+width/2], [cy+height*0.33]*2, color=INK, linewidth=1.0, zorder=6)
    text(ax, center + np.array([0.0, -0.07 if kind == "bucket" else 0.0]), r"$B$", size=22, zorder=7)
    return vertices, center + np.array([0, height/2])


def draw_one(request: dict, out: Path) -> dict:
    scenario = request["scenario"]
    index = request["scene_index"]
    alpha = math.radians(24 if scenario == "scenario 1" else -24)
    tangent = np.array([math.cos(alpha), math.sin(alpha)])
    normal = np.array([-math.sin(alpha), math.cos(alpha)])
    origin = np.array([0.0, 3.4])
    slope_point = lambda s: origin + s*tangent
    p0, p1 = slope_point(-3.75), slope_point(3.13)

    a_name, b_name, a_color, b_color, a_kind, b_kind = OBJECTS[(scenario, index)]
    block_width, block_height = 1.14, 0.78
    center = slope_point(-1.40) + block_height/2*normal
    corners = np.array([
        center-block_width/2*tangent-block_height/2*normal,
        center+block_width/2*tangent-block_height/2*normal,
        center+block_width/2*tangent+block_height/2*normal,
        center-block_width/2*tangent+block_height/2*normal,
    ])
    attachment_offset = 0.22
    anchor = center + block_width/2*tangent + attachment_offset*normal
    pulley_radius = 0.255
    contact = slope_point(3.61) + (block_height/2+attachment_offset)*normal
    pulley = contact - pulley_radius*normal
    exit_point = pulley + np.array([pulley_radius, 0.0])
    hanging_center = exit_point + np.array([0.0, -2.06])

    fig, ax = plt.subplots(figsize=(9.2, 6.0), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")
    ax.set_aspect("equal")
    plt.subplots_adjust(left=0.025, right=0.975, bottom=0.025, top=0.975)

    baseline = min(p0[1], p1[1])-0.40
    support = Polygon(
        [p0, p1, [p1[0], baseline], [p0[0], baseline]],
        closed=True, facecolor=SURFACE, edgecolor="#a2adb5", linewidth=1.05, zorder=1,
    )
    ax.add_patch(support)
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=INK, linewidth=2.7, zorder=3)
    for s in np.arange(-3.60, 3.08, 0.30):
        point = slope_point(s)
        tick = point-0.11*normal-0.07*tangent
        ax.plot([point[0], tick[0]], [point[1], tick[1]], color="#82919c", linewidth=0.8, zorder=2)

    # A fixed bracket visibly supports the axle without touching the hanging rope.
    bracket_base = pulley + np.array([0.0, -0.53])
    ax.plot(
        [p1[0], bracket_base[0], pulley[0]],
        [p1[1]-0.12, bracket_base[1], pulley[1]],
        color="#7e8e99", linewidth=3.2, solid_capstyle="round", zorder=2,
    )

    block = Polygon(corners, closed=True, facecolor=a_color, edgecolor=INK, linewidth=1.8, zorder=5)
    ax.add_patch(block)
    if a_kind == "crate":
        for point_a, point_b in [(corners[0], corners[2]), (corners[1], corners[3])]:
            line, = ax.plot([point_a[0], point_b[0]], [point_a[1], point_b[1]],
                            color="#c49a70", linewidth=1.1, zorder=5.1)
            line.set_clip_path(block)
    elif a_kind == "concrete":
        for st, sn in [(-.36,.19),(.36,.22),(-.34,-.21),(.36,-.18),(.02,.24)]:
            point = center+st*tangent+sn*normal
            ax.add_patch(Circle(point, radius=.018, facecolor="#8d989f", edgecolor="none", zorder=5.1))
    elif a_kind in {"felt", "rubber"}:
        low_left = center-block_width/2*tangent-block_height/2*normal
        low_right = center+block_width/2*tangent-block_height/2*normal
        ax.plot([low_left[0], low_right[0]], [low_left[1], low_right[1]], color="#516267", linewidth=3.5, zorder=5.1)

    # Entry tangent follows +x; the clockwise wrap exits vertically downward.
    ax.plot([anchor[0], contact[0]], [anchor[1], contact[1]], color=ROPE, linewidth=2.0, zorder=6)
    ax.add_patch(Circle(pulley, radius=pulley_radius, facecolor="#f8f9fa", edgecolor=INK, linewidth=1.7, zorder=4))
    entry_angle = math.degrees(math.atan2(normal[1], normal[0]))
    ax.add_patch(Arc(pulley, width=2*pulley_radius, height=2*pulley_radius,
                     theta1=0, theta2=entry_angle, color=ROPE, linewidth=2.0, zorder=6))
    ax.add_patch(Circle(pulley, radius=0.046, facecolor=INK, edgecolor=INK, zorder=7))
    hanging_vertices, hanging_top = draw_hanging(ax, hanging_center, b_kind, b_color)
    ax.plot([exit_point[0], hanging_top[0]], [exit_point[1], hanging_top[1]], color=ROPE, linewidth=2.0, zorder=6)

    # Coordinate origin is at A. The rope is offset above the +x axis.
    arrow(ax, center, center+1.78*tangent, color=AXIS)
    arrow(ax, center, center+1.34*normal, color=AXIS)
    ax.add_patch(Circle(center, radius=0.027, facecolor=AXIS, edgecolor=AXIS, zorder=10))
    text(ax, center+1.90*tangent-0.17*normal, r"$+x$", size=21, color=AXIS, zorder=11)
    text(ax, center+1.49*normal-0.15*tangent, r"$+y$", size=21, color=AXIS, zorder=11)
    text(ax, center-0.28*tangent-0.12*normal, r"$A$", size=22, zorder=11,
         bbox=dict(facecolor=a_color, edgecolor="none", pad=0.25))

    # Angle is measured relative to a horizontal reference, for either slope.
    reference_end = p0+np.array([1.43, 0.0])
    ax.plot([p0[0], reference_end[0]], [p0[1], reference_end[1]], color="#798894",
            linewidth=1.1, linestyle=(0, (4, 3)), zorder=4)
    ax.add_patch(Arc(p0, width=1.76, height=1.76,
                     theta1=min(0, math.degrees(alpha)), theta2=max(0, math.degrees(alpha)),
                     color=INK, linewidth=1.25, zorder=5))
    theta_location = p0 + 1.12*np.array([math.cos(alpha/2), math.sin(alpha/2)])
    text(ax, theta_location, r"$\theta$", size=21, zorder=6)

    extent = np.vstack([
        corners, hanging_vertices, p0, p1,
        center+2.1*tangent, center+1.7*normal,
        pulley+np.array([0.44, 0.44]), [p0[0], baseline], [p1[0], baseline],
    ])
    low, high = extent.min(axis=0), extent.max(axis=0)
    ax.set_xlim(low[0]-0.45, high[0]+0.46)
    ax.set_ylim(low[1]-0.35, high[1]+0.38)

    prefix = "U" if scenario == "scenario 1" else "D"
    scene_id = f"{prefix}{index}"
    file_id = scene_id
    angle_word = "upward" if scenario == "scenario 1" else "downward"
    pulley_word = "upper" if scenario == "scenario 1" else "lower"
    alt = (
        f"Object A, a {a_name}, is on the left on a rough incline sloping {angle_word} to the right. "
        f"A rope runs parallel to the incline to a fixed pulley at the {pulley_word} right end, "
        f"then vertically down to object B, a freely hanging {b_name}, on the right. "
        "The angle theta is marked between the surface and a horizontal reference. "
        "The axes originate on A: positive x points right along the incline and positive y points "
        "perpendicular to and outward from the surface."
    )
    png_path = out/"Figures"/f"{file_id}.png"
    svg_path = out/"Vectors"/f"{file_id}.svg"
    fig.savefig(png_path, dpi=170, facecolor="white",
                metadata={"Title": "Inclined-plane pulley geometry", "Description": alt})
    fig.savefig(svg_path, facecolor="white",
                metadata={"Title": "Inclined-plane pulley geometry", "Description": alt})
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    figure_bbox = fig.bbox
    for label in ax.texts:
        bb = label.get_window_extent(renderer)
        if not (figure_bbox.x0 <= bb.x0 <= bb.x1 <= figure_bbox.x1
                and figure_bbox.y0 <= bb.y0 <= bb.y1 <= figure_bbox.y1):
            raise ValueError(f"Label outside figure: {file_id}, {label.get_text()}")
    plt.close(fig)

    # Geometry checks are independent of the rendered appearance.
    assert abs(np.dot(tangent, normal)) < 1e-12
    assert tangent[0] > 0 and normal[1] > 0
    assert abs(np.dot(contact-anchor, normal)) < 1e-12, "Rope must parallel the incline"
    assert abs(np.linalg.norm(contact-pulley)-pulley_radius) < 1e-12
    assert abs(np.dot(contact-pulley, tangent)) < 1e-12, "Entry rope must be tangent"
    assert abs(exit_point[0]-hanging_top[0]) < 1e-12, "Hanging rope must be vertical"
    assert hanging_top[1] < exit_point[1], "B must hang below the pulley"
    assert hanging_vertices[:, 0].min() > p1[0], "B must clear the ramp"
    return {
        **request, "scene_id": scene_id,
        "scene_caption": f"{a_name.capitalize()} / {b_name}",
        "figure": f"Figures/{file_id}.png", "vector_figure": f"Vectors/{file_id}.svg",
        "alt_text": alt,
    }


def item_mappings(bank: dict, figures: list[dict]) -> list[dict]:
    """Map the full question grid to the reusable scene figures."""
    lookup = {
        (entry["scenario"], entry["scene_index"], tuple(sorted(entry["drawing"].items()))): entry
        for entry in figures
    }
    items = []
    for scenario in bank["scenarios"]:
        axes = bank["variation_axes"]["common"] + bank["variation_axes"]["by_scenario"][scenario["id"]]
        for scene_index, scene in enumerate(scenario["scenes"]):
            if scene["status"] != "kept":
                continue
            for combination in itertools.product(*(axis["values"] for axis in axes)):
                values = dict(zip((axis["id"] for axis in axes), combination))
                drawing = {axis["id"]: values[axis["id"]] for axis in axes if axis["changes_drawing"]}
                figure = lookup[(scenario["id"], scene_index, tuple(sorted(drawing.items())))]
                velocity, acceleration = state_signs(scenario["id"], values["kinematic_state"])
                items.append({
                    "scenario": scenario["id"], "scene_index": scene_index,
                    "scene_id": figure["scene_id"], "values": values,
                    "motion_description": STATE_TEXT[values["kinematic_state"]],
                    "figure": figure["figure"], "alt_text": figure["alt_text"],
                    "velocity_sign_x": velocity, "acceleration_sign_x": acceleration,
                })
    return items


def font(size: int, bold=False):
    base = Path("/usr/share/fonts/truetype/dejavu")
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(str(base/name), size=size)
    except OSError:
        return ImageFont.load_default(size=size)


def contact_sheet(entries: list[dict], out: Path, name: str, title: str, columns: int):
    rows = math.ceil(len(entries)/columns)
    cell_width, cell_height = 850, 605
    top = 108
    sheet = Image.new("RGB", (columns*cell_width+40, rows*cell_height+top+30), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text((30, 19), title, font=font(32, bold=True), fill=INK)
    draw.text((30, 63), "Students infer acceleration direction from each word problem.",
              font=font(20), fill="#596975")
    for cell, entry in enumerate(entries):
        column, row = cell % columns, cell // columns
        x, y = 20+column*cell_width, top+row*cell_height
        caption = f"{entry['scene_id']}  |  {entry['scene_caption']}"
        draw.text((x+17, y+10), caption, font=font(22, bold=True), fill=INK)
        with Image.open(out/entry["figure"]) as original:
            thumbnail = original.convert("RGB")
            thumbnail.thumbnail((cell_width-25, cell_height-60), Image.Resampling.LANCZOS)
        sheet.paste(thumbnail, (x+(cell_width-thumbnail.width)//2, y+48))
        draw.rectangle((x+4, y+2, x+cell_width-6, y+cell_height-8), outline="#d9e0e5", width=2)
    destination = out/name
    sheet.save(destination, optimize=True)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", type=Path, default=Path(__file__).with_name("input-inclined-plane-confirmed.mcq.yaml"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("inclined-plane-figures"))
    args = parser.parse_args()
    bank = yaml.safe_load(args.bank.read_text(encoding="utf-8"))
    out = args.output.resolve()
    for folder in ["Figures", "Vectors"]:
        (out/folder).mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
        "svg.fonttype": "none", "path.simplify": False,
    })
    requests = drawing_requests(bank)
    manifest_path = out/"figure-manifest.json"
    previous = json.loads(manifest_path.read_text())["figures"] if manifest_path.exists() else []
    manifest = [draw_one(request, out) for request in requests]
    items = item_mappings(bank, manifest)
    current_paths = {entry[key] for entry in manifest for key in ["figure", "vector_figure"]}
    for entry in previous:
        for key in ["figure", "vector_figure"]:
            if entry[key] not in current_paths:
                (out/entry[key]).unlink(missing_ok=True)
    manifest_path.write_text(json.dumps({"figures": manifest, "items": items}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (out/"figure-requests.json").write_text(json.dumps({"figures": requests}, indent=2)+"\n", encoding="utf-8")
    first = [entry for entry in manifest if entry["scenario"] == "scenario 1"]
    second = [entry for entry in manifest if entry["scenario"] == "scenario 2"]
    up_sheet = contact_sheet(first, out, "inclined-plane-rising-review.png",
                              "Incline rises to the right — all selected scenes", columns=2)
    down_sheet = contact_sheet(second, out, "inclined-plane-falling-review.png",
                                "Incline falls to the right — all selected scenes", columns=2)
    examples = [next(entry for entry in manifest if entry["scene_id"] == scene_id)
                for scene_id in ["U0", "D0"]]
    preview = contact_sheet(examples, out, "inclined-plane-figure-preview.png",
                              "Revised figures: geometry and coordinate axes", columns=2)
    print(json.dumps({
        "questions": len(items), "figures": len(manifest), "png_figures": len(list((out/"Figures").glob("*.png"))),
        "svg_figures": len(list((out/"Vectors").glob("*.svg"))),
        "preview": str(preview), "rising_review": str(up_sheet), "falling_review": str(down_sheet),
        "geometry_and_label_checks": "passed",
    }, indent=2))


if __name__ == "__main__":
    main()
