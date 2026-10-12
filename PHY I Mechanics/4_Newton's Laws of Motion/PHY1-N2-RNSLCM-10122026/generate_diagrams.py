"""Draw the selected circular-motion scenario diagrams.

Backup scenarios are omitted. Horizontal figures are labeled "Top view".
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "diagrams"

OBJECT_COLOR = "#D35400"
FLOW_COLOR = "#1A5276"
TRACK_COLOR = "#1C2833"
FONT_SIZE = 14

# Unit circle positions. Side is the right-hand point. North is the top of a top view.
POSITIONS = {
    "top": (0.0, 1.0),
    "bottom": (0.0, -1.0),
    "side": (1.0, 0.0),
    "left": (-1.0, 0.0),
    "north": (0.0, 1.0),
    "right": (1.0, 0.0),
}


def _label(ax, x, y, text, dx, dy, ha, va):
    ax.text(
        x + dx,
        y + dy,
        text,
        ha=ha,
        va=va,
        fontsize=FONT_SIZE,
        color="black",
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none"},
        zorder=6,
    )


MARKER_SIZE = 13


def _marker(ax, x, y):
    ax.plot(
        x,
        y,
        "o",
        color=OBJECT_COLOR,
        markersize=MARKER_SIZE,
        markeredgecolor="black",
        markeredgewidth=0.8,
        zorder=5,
    )


def _marker_radius_data(ax, markersize):
    """Radius, in data coordinates, of a plot marker of the given point size."""
    ax.figure.canvas.draw()
    radius_px = (markersize / 2.0) * ax.figure.dpi / 72.0
    x0, y0 = ax.transData.transform((0.0, 0.0))
    x1, _y1 = ax.transData.inverted().transform((x0 + radius_px, y0))
    return abs(x1)


def _view_label(ax, text):
    ax.text(0, 1.62, text, ha="center", va="bottom", fontsize=FONT_SIZE, color="black", zorder=7)


def _object_legend(ax, name, y):
    ax.plot([-0.35], [y], "o", color=OBJECT_COLOR, markersize=11,
            markeredgecolor="black", markeredgewidth=0.8, zorder=5)
    ax.text(0.0, y, name, ha="left", va="center", fontsize=FONT_SIZE, zorder=6)


def _flow_column(ax, direction, name):
    """Stack horizontal arrows on the side the force comes from."""
    length = 0.5
    ys = (-0.9, -0.45, 0.0, 0.45, 0.9)
    if direction > 0:
        tail_x = -2.45
        head_x = tail_x + length
    else:
        tail_x = 2.45
        head_x = tail_x - length
    for y in ys:
        ax.annotate(
            "",
            xy=(head_x, y),
            xytext=(tail_x, y),
            arrowprops={
                "arrowstyle": "-|>",
                "color": FLOW_COLOR,
                "lw": 2.1,
                "mutation_scale": 15,
                "shrinkA": 0,
                "shrinkB": 0,
            },
            zorder=4,
        )
    ax.text((tail_x + head_x) / 2, ys[-1] + 0.18, name, ha="center", va="bottom", fontsize=FONT_SIZE, color=FLOW_COLOR)


def _gravity(ax):
    ax.annotate(
        "",
        xy=(-1.95, -0.55),
        xytext=(-1.95, 0.55),
        arrowprops={
            "arrowstyle": "-|>",
            "color": "black",
            "lw": 2.3,
            "mutation_scale": 16,
            "shrinkA": 0,
            "shrinkB": 0,
        },
        zorder=4,
    )
    ax.text(-1.95, 0.72, "gravity", ha="center", va="bottom", fontsize=FONT_SIZE)


def _radii(ax, keys, style):
    for key in keys:
        x, y = POSITIONS[key]
        line, = ax.plot(
            [0, x],
            [0, y],
            color="black",
            linewidth=2.2 if style == "-" else 1.6,
            solid_capstyle="round",
            zorder=2,
        )
        if style == "-":
            line.set_linestyle("-")
        else:
            line.set_linestyle((0, (5, 3.5)))
    ax.plot(0, 0, "o", color="black", markersize=4.5, zorder=4)


def _crop_margin(path, pad_px=10):
    image = plt.imread(path)
    rgb = image[:, :, :3]
    if rgb.dtype != np.uint8:
        rgb = np.clip(np.rint(rgb * 255), 0, 255).astype(np.uint8)
    ink = np.any(rgb < 248, axis=2)
    rows = np.flatnonzero(ink.any(axis=1))
    cols = np.flatnonzero(ink.any(axis=0))
    top = max(int(rows[0]) - pad_px, 0)
    bottom = min(int(rows[-1]) + pad_px + 1, image.shape[0])
    left = max(int(cols[0]) - pad_px, 0)
    right = min(int(cols[-1]) + pad_px + 1, image.shape[1])
    plt.imsave(path, image[top:bottom, left:right])


def _finish(fig, ax, filename):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-3.05, 3.05)
    ax.set_ylim(-2.05, 2.15)
    path = OUT / filename
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white", pad_inches=0.02)
    plt.close(fig)
    _crop_margin(path)


def draw_vertical_tension(spec):
    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    _view_label(ax, "Side view")
    circle = Circle((0, 0), 1, fill=False, linestyle=(0, (5, 4)), linewidth=1.8, color="black", zorder=1)
    ax.add_patch(circle)
    keys = ("top", "side", "bottom")
    _radii(ax, keys, "-")
    for key in keys:
        _marker(ax, *POSITIONS[key])
    _label(ax, 0, 1, "1", 0, 0.16, "center", "bottom")
    _label(ax, 1, 0, "2", 0.16, 0, "left", "center")
    _label(ax, 0, -1, "3", 0, -0.16, "center", "top")
    _gravity(ax)
    _object_legend(ax, spec["object"], -1.72)
    _finish(fig, ax, spec["file"])


def draw_vertical_track(spec):
    """Place each object so its outer edge touches the inside of the track."""
    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    _view_label(ax, "Side view")
    track_radius = 1.0
    track = Circle(
        (0, 0),
        track_radius,
        fill=False,
        linestyle="-",
        linewidth=3.6,
        color=TRACK_COLOR,
        zorder=1,
    )
    ax.add_patch(track)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-3.05, 3.05)
    ax.set_ylim(-2.05, 2.15)
    # Center of the object sits one object-radius inside the track circle.
    inner = track_radius - _marker_radius_data(ax, MARKER_SIZE)
    for key in ("top", "side", "bottom"):
        x, y = POSITIONS[key]
        ax.plot(
            [0, inner * x],
            [0, inner * y],
            color="black",
            linewidth=1.6,
            linestyle=(0, (5, 3.5)),
            solid_capstyle="round",
            zorder=2,
        )
        _marker(ax, inner * x, inner * y)
    ax.plot(0, 0, "o", color="black", markersize=4.5, zorder=4)
    _label(ax, 0, 1, "1", 0, 0.18, "center", "bottom")
    _label(ax, 1, 0, "2", 0.18, 0, "left", "center")
    _label(ax, 0, -1, "3", 0, -0.18, "center", "top")
    _gravity(ax)
    _object_legend(ax, spec["object"], -1.72)
    _finish(fig, ax, spec["file"])


def draw_horizontal(spec, road):
    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    _view_label(ax, "Top view")
    _flow_column(ax, spec["direction"], spec["flow"])
    if road:
        ax.add_patch(Circle((0, 0), 1.12, fill=False, linestyle="-", linewidth=2.4, color=TRACK_COLOR, zorder=1))
        ax.add_patch(Circle((0, 0), 0.88, fill=False, linestyle="-", linewidth=2.4, color=TRACK_COLOR, zorder=1))
        _radii(ax, ("left", "north", "right"), "--")
    else:
        ax.add_patch(Circle((0, 0), 1, fill=False, linestyle=(0, (5, 4)), linewidth=1.8, color="black", zorder=1))
        _radii(ax, ("left", "north", "right"), "-")
    for key in ("left", "north", "right"):
        _marker(ax, *POSITIONS[key])
    _label(ax, -1, 0, "1", -0.16, 0, "right", "center")
    _label(ax, 0, 1, "2", 0, 0.18, "center", "bottom")
    _label(ax, 1, 0, "3", 0.16, 0, "left", "center")
    _object_legend(ax, spec["object"], -1.62)
    _finish(fig, ax, spec["file"])


SCENARIOS = [
    {"file": "01-bucket-of-water.png", "kind": "vertical-tension", "object": "bucket of water"},
    {"file": "02-steel-nut.png", "kind": "vertical-tension", "object": "steel nut"},
    {"file": "03-toy-car.png", "kind": "vertical-track", "object": "toy car"},
    {"file": "04-glass-marble.png", "kind": "vertical-track", "object": "glass marble"},
    {"file": "05-model-airplane.png", "kind": "horizontal-string", "object": "model airplane", "flow": "wind", "direction": 1},
    {"file": "06-model-boat.png", "kind": "horizontal-string", "object": "model boat", "flow": "current", "direction": 1},
    {"file": "07-model-car.png", "kind": "horizontal-string", "object": "model car", "flow": "wind", "direction": -1},
    {"file": "08-underwater-probe.png", "kind": "horizontal-string", "object": "underwater probe", "flow": "current", "direction": -1},
    {"file": "09-car.png", "kind": "horizontal-road", "object": "car", "flow": "wind", "direction": 1},
    {"file": "10-delivery-truck.png", "kind": "horizontal-road", "object": "delivery truck", "flow": "wind", "direction": 1},
    {"file": "11-bicycle.png", "kind": "horizontal-road", "object": "bicycle and rider", "flow": "wind", "direction": -1},
    {"file": "12-motorcycle.png", "kind": "horizontal-road", "object": "motorcycle and rider", "flow": "wind", "direction": -1},
]


def main():
    OUT.mkdir(exist_ok=True)
    for spec in SCENARIOS:
        kind = spec["kind"]
        if kind == "vertical-tension":
            draw_vertical_tension(spec)
        elif kind == "vertical-track":
            draw_vertical_track(spec)
        elif kind == "horizontal-string":
            draw_horizontal(spec, road=False)
        elif kind == "horizontal-road":
            draw_horizontal(spec, road=True)
        else:
            raise ValueError(kind)
        print(spec["file"])


if __name__ == "__main__":
    main()
