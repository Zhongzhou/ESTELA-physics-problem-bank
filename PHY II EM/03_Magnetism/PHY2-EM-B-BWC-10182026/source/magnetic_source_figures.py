#!/usr/bin/env python3
"""Draw a circular N-turn coil, a long straight wire, and an axial point.

Requires Python 3.10+, NumPy, and Matplotlib. All geometry is in metres.
Only NumPy and Matplotlib are needed; no TeX installation is required.

Examples:
    python magnetic_source_figures.py --demo --output-dir figures
    python magnetic_source_figures.py --all-84 --output-dir figures
    python magnetic_source_figures.py --all-84 --with-fields --output-dir figures
    python magnetic_source_figures.py --config my_config.json --output-dir figures
    python magnetic_source_figures.py --validate-only

The coil is a single circle representing N coincident turns, not a solenoid.
An explicit orthographic projection feeds Matplotlib's 2D drawing tools so
annotation positions and vector exports remain predictable. Conductor strokes
are subdivided and ordered by camera depth at apparent crossings.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath

AXES = "xyz"
UNIT = np.eye(3)
COIL_COLOR = "#AC4F24"
WIRE_COLOR = "#006B80"
INK = "#26313A"
GUIDE = "#76838C"
FAMILIES = ("parallel", "sideways", "crossing_near", "crossing_far")
FAMILY_NAMES = {
    "parallel": "Parallel wire",
    "sideways": "Sideways-offset perpendicular wire",
    "crossing_near": "Intersecting wire: between coil and P",
    "crossing_far": "Intersecting wire: beyond P",
}


@dataclass(frozen=True)
class DiagramConfig:
    identifier: str = "example"
    family: str = "sideways"
    coil_axis: str = "z"
    coil_sense: str = "ccw"  # Viewed from the positive axis toward the origin.
    coil_radius: float = 0.060
    coil_turns: int = 20
    coil_current: float = 0.40
    wire_axis: str = "x"
    wire_sign: int = 1
    wire_current: float = 8.0
    wire_point: tuple[float, float, float] = (0.0, 0.090, 0.140)
    observation: tuple[float, float, float] = (0.0, 0.0, 0.140)
    azimuth_deg: float = 43.0
    elevation_deg: float = 27.0

    @classmethod
    def from_dict(cls, value: dict) -> "DiagramConfig":
        value = dict(value)
        for key in ("wire_point", "observation"):
            if key in value:
                value[key] = tuple(value[key])
        return cls(**value)


def coil_basis(axis: str) -> tuple[np.ndarray, np.ndarray]:
    """Right-handed in-plane basis: u cross v = positive coil axis."""
    k = AXES.index(axis)
    return UNIT[(k + 1) % 3], UNIT[(k + 2) % 3]


def source_geometry(cfg: DiagramConfig) -> dict:
    k, j = AXES.index(cfg.coil_axis), AXES.index(cfg.wire_axis)
    point, p = np.asarray(cfg.wire_point, float), np.asarray(cfg.observation, float)
    foot = point + np.dot(p - point, UNIT[j]) * UNIT[j]
    radial = p - foot
    rho = float(np.linalg.norm(radial))
    if rho == 0:
        raise ValueError("Observation point lies on the straight wire.")
    coil_dir = (1 if cfg.coil_sense == "ccw" else -1) * UNIT[k]
    wire_dir = np.cross(cfg.wire_sign * UNIT[j], radial / rho)
    cosine = float(np.dot(coil_dir, wire_dir))
    if np.isclose(abs(cosine), 1.0, atol=1e-9):
        relation = "parallel" if cosine > 0 else "antiparallel"
    elif np.isclose(cosine, 0.0, atol=1e-9):
        relation = "perpendicular"
    else:
        relation = "oblique"
    return dict(foot=foot, radial=radial, rho=rho, coil_direction=coil_dir,
                wire_direction=wire_dir, relationship=relation)


def validate_config(cfg: DiagramConfig) -> dict:
    if cfg.coil_axis not in tuple(AXES) or cfg.wire_axis not in tuple(AXES):
        raise ValueError("Coil and wire axes must each be x, y, or z.")
    if cfg.coil_sense not in ("cw", "ccw") or cfg.wire_sign not in (-1, 1):
        raise ValueError("Use coil_sense cw/ccw and wire_sign +1/-1.")
    if cfg.family not in FAMILIES:
        raise ValueError(f"Unknown family: {cfg.family}")
    scalars = [cfg.coil_radius, cfg.coil_current, cfg.wire_current,
               cfg.azimuth_deg, cfg.elevation_deg]
    if not np.all(np.isfinite(scalars)):
        raise ValueError("Dimensions, currents, and view angles must be finite.")
    if min(cfg.coil_radius, cfg.coil_current, cfg.wire_current) <= 0:
        raise ValueError("Radius and current magnitudes must be positive.")
    if not isinstance(cfg.coil_turns, int) or isinstance(cfg.coil_turns, bool) or cfg.coil_turns < 1:
        raise ValueError("The coil must have a positive integer number of turns.")
    p, q = np.asarray(cfg.observation, float), np.asarray(cfg.wire_point, float)
    if p.shape != (3,) or q.shape != (3,) or not np.all(np.isfinite([p, q])):
        raise ValueError("Point coordinates must be finite three-element lists.")
    k, j = AXES.index(cfg.coil_axis), AXES.index(cfg.wire_axis)
    tol = 1e-9 * max(cfg.coil_radius, np.linalg.norm(p), np.linalg.norm(q), 1e-3)
    if not np.allclose(p - p[k] * UNIT[k], 0, atol=tol, rtol=0):
        raise ValueError("P must lie on the coil axis.")
    geometry = source_geometry(cfg)
    if geometry["rho"] <= tol:
        raise ValueError("P is too close to the idealized straight wire.")
    if geometry["relationship"] == "oblique":
        raise ValueError("This bank allows only collinear or perpendicular fields.")
    if cfg.family == "parallel" and j != k:
        raise ValueError("The parallel family needs parallel source axes.")
    if cfg.family != "parallel" and j == k:
        raise ValueError("This family needs perpendicular source axes.")
    if cfg.family == "sideways" and not np.isclose(q[k], p[k], atol=tol, rtol=0):
        raise ValueError("The sideways wire must have P's axial coordinate.")
    if cfg.family.startswith("crossing"):
        other = 3 - k - j
        if abs(q[other]) > tol:
            raise ValueError("The crossing wire must intersect the coil axis.")
        if p[k] <= 0:
            raise ValueError("Near/far conventions use P on the positive coil axis.")
        if cfg.family == "crossing_near" and not 0 < q[k] < p[k]:
            raise ValueError("The near intersection must be between O and P.")
        if cfg.family == "crossing_far" and not q[k] > p[k]:
            raise ValueError("The far intersection must be beyond P.")
    # Reject contact between a zero-thickness wire and the circular winding.
    if j == k:
        transverse = q - q[k] * UNIT[k]
        touching = np.isclose(np.linalg.norm(transverse), cfg.coil_radius, atol=tol, rtol=0)
    else:
        other = 3 - k - j
        touching = abs(q[k]) <= tol and abs(q[other]) <= cfg.coil_radius + tol
    if touching:
        raise ValueError("The straight wire would intersect the coil winding.")
    return geometry


def enumerate_84(radius: float = 0.060, axial_distance: float = 0.140,
                 lateral_shift: float = 0.090) -> list[DiagramConfig]:
    """The 84 chosen conventions, not an exhaustive count of all placements.

    P is on the positive coil axis. Parallel wires use the next positive
    transverse axis as their offset. Sideways wires use the remaining positive
    axis. Near/far intersections are on the positive coil axis.
    Counts: parallel 12; sideways 24; crossing_near 24; crossing_far 24.
    """
    result = []
    for family in FAMILIES:
        for k, c_axis in enumerate(AXES):
            wire_axes = [k] if family == "parallel" else [j for j in range(3) if j != k]
            for j in wire_axes:
                for sense in ("ccw", "cw"):
                    for sign in (1, -1):
                        p = axial_distance * UNIT[k]
                        if family == "parallel":
                            q = lateral_shift * UNIT[(k + 1) % 3]
                        elif family == "sideways":
                            q = p + lateral_shift * UNIT[3 - k - j]
                        elif family == "crossing_near":
                            q = 0.45 * axial_distance * UNIT[k]
                        else:
                            q = 1.45 * axial_distance * UNIT[k]
                        identifier = f"mag_{len(result) + 1:03d}"
                        result.append(DiagramConfig(
                            identifier=identifier, family=family, coil_axis=c_axis,
                            coil_sense=sense, coil_radius=radius, wire_axis=AXES[j],
                            wire_sign=sign, wire_point=tuple(q), observation=tuple(p)))
    return result


def camera_basis(azimuth_deg: float, elevation_deg: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    az, el = np.deg2rad([azimuth_deg, elevation_deg])
    eye = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    right = np.array([-np.sin(az), np.cos(az), 0.0])
    up = np.cross(eye, right)
    return right, up, eye


def project(points: np.ndarray, camera: tuple) -> np.ndarray:
    points = np.asarray(points, float)
    return np.stack([points @ camera[0], points @ camera[1]], axis=-1)


def _camera_score(cfg: DiagramConfig, camera: tuple) -> float:
    """Avoid edge-on coils, foreshortened wires, and P hidden by the coil."""
    k, j = AXES.index(cfg.coil_axis), AXES.index(cfg.wire_axis)
    u, v = coil_basis(cfg.coil_axis)
    t = np.linspace(0, 2 * np.pi, 180)
    ring = cfg.coil_radius * (np.cos(t)[:, None] * u + np.sin(t)[:, None] * v)
    p2, r2 = project(np.array(cfg.observation), camera), project(ring, camera)
    separation = np.min(np.linalg.norm(r2 - p2, axis=1)) / cfg.coil_radius
    face = abs(np.dot(UNIT[k], camera[2]))
    wire_length = np.linalg.norm(project(UNIT[j], camera))
    return 0.8 * min(separation, 1.5) + 1.2 * min(face, 0.8) + 0.6 * wire_length


def choose_camera(cfg: DiagramConfig) -> tuple:
    candidates = [(cfg.azimuth_deg, cfg.elevation_deg), (35, 33), (56, 27), (43, 40)]
    bases = [camera_basis(*candidate) for candidate in candidates]
    return max(bases, key=lambda camera: _camera_score(cfg, camera))


class LabelPlacer:
    """Small greedy label placement using display-space collision scores."""

    def __init__(self, fig, ax, geometry_xy):
        self.fig, self.ax = fig, ax
        self.renderer = fig.canvas.get_renderer()
        self.boxes = []
        self.points = ax.transData.transform(geometry_xy)

    def add(self, xy, text, *, color=INK, size=12, preferred=(12, 10), leader=False,
            candidates=None):
        choices = candidates if candidates is not None else [preferred] + [
            (r * x, r * y) for r in (12, 20, 30)
            for x, y in ((1, 1), (-1, 1), (1, -1), (-1, -1),
                         (1.4, 0), (-1.4, 0), (0, 1.4), (0, -1.4))]
        best = None
        for dx, dy in choices:
            artist = self.ax.annotate(
                text, xy=xy, xytext=(dx, dy), textcoords="offset points",
                ha="center" if dx == 0 else ("left" if dx > 0 else "right"),
                va="center" if dy == 0 else ("bottom" if dy > 0 else "top"),
                fontsize=size, color=color, zorder=100,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.96, pad=1.0),
                annotation_clip=False)
            box = artist.get_window_extent(self.renderer).expanded(1.05, 1.12)
            overlap = sum(max(0, min(box.x1, b.x1) - max(box.x0, b.x0)) *
                          max(0, min(box.y1, b.y1) - max(box.y0, b.y0)) for b in self.boxes)
            occupied = np.sum((self.points[:, 0] >= box.x0) & (self.points[:, 0] <= box.x1) &
                              (self.points[:, 1] >= box.y0) & (self.points[:, 1] <= box.y1))
            outside = not self.ax.bbox.contains(box.x0, box.y0) or not self.ax.bbox.contains(box.x1, box.y1)
            score = overlap * 10 + occupied * 8 + math.hypot(dx, dy) * 0.18 + 10000 * outside
            if best is None or score < best[0]:
                if best is not None:
                    best[1].remove()
                best = (score, artist, box, dx, dy)
            else:
                artist.remove()
        _, artist, box, dx, dy = best
        self.boxes.append(box)
        if leader and math.hypot(dx, dy) > 22:
            self.ax.annotate("", xy=xy, xytext=(dx, dy), textcoords="offset points",
                             arrowprops=dict(arrowstyle="-", color=color, lw=0.65), zorder=95)
        return artist


    def fixed(self, xy, text, *, offset=(0, 0), color=INK, size=12,
              ha="center", va="center", pad=1.0):
        """Reserve exact placement for labels that must stay attached to arrows."""
        artist = self.ax.annotate(
            text, xy=xy, xytext=offset, textcoords="offset points",
            ha=ha, va=va, fontsize=size, color=color, zorder=100,
            bbox=dict(facecolor="white", edgecolor="none", alpha=1.0, pad=pad),
            annotation_clip=False)
        self.boxes.append(artist.get_window_extent(self.renderer).expanded(1.05, 1.12))
        return artist


def segment_on_coordinate_axis(start, end) -> bool:
    """Coincidence with an axis, rather than merely parallel to that axis."""
    points = np.asarray([start, end], float)
    tol = 1e-9 * max(float(np.max(np.abs(points))), 1e-3)
    return any(np.all(np.abs(np.delete(points, i, axis=1)) <= tol) for i in range(3))


def _arrow(ax, points2, color, *, width=2.3, head=13, zorder=25, halo=True):
    path = MplPath(points2, [MplPath.MOVETO] + [MplPath.LINETO] * (len(points2) - 1))
    arrow = FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=head,
                            color=color, linewidth=width, zorder=zorder,
                            capstyle="round", joinstyle="round")
    if halo:
        arrow.set_path_effects([pe.Stroke(linewidth=width + 2, foreground="white"), pe.Normal()])
    ax.add_patch(arrow)
    return arrow


def feedback_arrows(cfg: DiagramConfig, geometry: dict, camera: tuple, scene_points) -> list[dict]:
    """Schematic direction arrows: true 3D directions, legible projected lengths.

    Co-directed arrows share the exact origin and direction. A longer, wider
    coil arrow surrounds a shorter, narrower wire arrow so both remain visible.
    Lengths do not encode magnetic-field magnitudes.
    """
    projected_span = float(np.ptp(project(scene_points, camera), axis=0).max())
    length = max(0.18 * projected_span, 0.8 * cfg.coil_radius)
    co_directed = geometry["relationship"] == "parallel"
    p = np.asarray(cfg.observation, float)
    arrows = []
    for source, label, color, direction in (
        ("coil", r"$\vec{B}_c$", COIL_COLOR, geometry["coil_direction"]),
        ("wire", r"$\vec{B}_w$", WIRE_COLOR, geometry["wire_direction"]),
    ):
        factor = (1.14 if source == "coil" else 0.76) if co_directed else 1.0
        projected_direction = project(direction, camera)
        projection_length = float(np.linalg.norm(projected_direction))
        if projection_length < 1e-8:
            raise ValueError("A field points along the viewing direction; choose another camera.")
        end = p + (factor * length / projection_length) * direction
        points3 = np.array([p, end])
        arrows.append(dict(
            source=source, label=label, color=color, points3=points3,
            points2=project(points3, camera),
            width=(5.2 if source == "coil" else 2.4) if co_directed else 3.3,
            halo=not (co_directed and source == "wire")))
    return arrows


def _coordinate_text(point: Sequence[float]) -> str:
    return "(" + ", ".join(f"{100 * x:.3g}" if abs(x) > 1e-12 else "0" for x in point) + ") cm"


def draw_diagram(cfg: DiagramConfig, output_stem: str | Path, *, dpi: int = 180,
                 formats: Sequence[str] = ("png", "svg"), show_title: bool = False,
                 with_fields: bool = False, feedback_source_alpha: float = 0.15) -> list[Path]:
    """Write question figures and, optionally, matched *_feedback field figures.

    Both versions use the same camera, axes, scale, and source-label positions.
    Field arrows originate at P and show directions rather than magnitudes.
    Feedback sources are faint context; their opacity defaults to 15 percent.
    """
    if not 0 <= feedback_source_alpha <= 1:
        raise ValueError("feedback_source_alpha must be between 0 and 1.")
    geometry = validate_config(cfg)
    r, k, j = cfg.coil_radius, AXES.index(cfg.coil_axis), AXES.index(cfg.wire_axis)
    p, q = np.array(cfg.observation), np.array(cfg.wire_point)
    foot = geometry["foot"]
    camera = choose_camera(cfg)
    u, v = coil_basis(cfg.coil_axis)
    angles = np.linspace(0, 2 * np.pi, 361)
    ring = r * (np.cos(angles)[:, None] * u + np.sin(angles)[:, None] * v)
    # Cropped wire endpoints indicate a very long segment, not physical ends.
    t0, t1 = min(-1.5 * r, p[j] - 1.4 * r), max(1.5 * r, p[j] + 1.4 * r)
    wire = q + np.linspace(t0, t1, 181)[:, None] * UNIT[j]
    sources = np.vstack([ring, wire, p[None, :], np.zeros((1, 3))])
    fields = feedback_arrows(cfg, geometry, camera, sources) if with_fields else []
    layout_points = np.vstack([sources] + [arrow["points3"] for arrow in fields])
    lo, hi = layout_points.min(axis=0), layout_points.max(axis=0)
    axis_lo = np.minimum(lo - 0.2 * r, -1.2 * r)
    axis_hi = np.maximum(hi + 0.4 * r, 1.55 * r)
    axis_points = np.vstack([axis_lo[i] * UNIT[i] for i in range(3)] +
                            [axis_hi[i] * UNIT[i] for i in range(3)])
    all_projected = project(np.vstack([layout_points, axis_points]), camera)
    min2, max2 = all_projected.min(axis=0), all_projected.max(axis=0)
    margin = 0.55 * r

    with plt.rc_context({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
                         "svg.fonttype": "none", "font.size": 11}):
        fig, ax = plt.subplots(figsize=(7.4, 6.8), facecolor="white")
        fig.subplots_adjust(left=0.045, right=0.955, bottom=0.18, top=0.91)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(min2[0] - margin, max2[0] + margin)
        ax.set_ylim(min2[1] - margin, max2[1] + margin)
        ax.set_axis_off()
        # Uncluttered reference axes: dashed negative portions, positive arrows.
        for i in range(3):
            neg = project(np.array([axis_lo[i] * UNIT[i], np.zeros(3)]), camera)
            pos = project(np.array([np.zeros(3), axis_hi[i] * UNIT[i]]), camera)
            ax.plot(neg[:, 0], neg[:, 1], color="#A7AFB4", lw=0.8, ls=(0, (3, 3)), zorder=1)
            ax.add_patch(FancyArrowPatch(pos[0], pos[1], arrowstyle="-|>",
                                        mutation_scale=10, color="#8A949B", lw=0.95, zorder=1))
        # Draw PQ only when it is not already represented by a coordinate axis.
        # The right-angle symbol remains useful even when PQ is an axis segment.
        guide2 = project(np.array([p, foot]), camera)
        show_guide = not segment_on_coordinate_axis(p, foot)
        if show_guide:
            ax.plot(guide2[:, 0], guide2[:, 1], color=GUIDE, lw=1.2, ls=(0, (3, 3)), zorder=2)
        side = cfg.wire_sign * UNIT[j]
        radial_unit = geometry["radial"] / geometry["rho"]
        corner = foot + 0.16 * r * radial_unit
        corner_path = np.array([corner, corner + 0.16 * r * side, foot + 0.16 * r * side])
        corner2 = project(corner_path, camera)
        ax.plot(corner2[:, 0], corner2[:, 1], color=GUIDE, lw=0.8, zorder=2)
        # Order short conductor strokes from back to front. This avoids one
        # global z-order value for each whole crossing conductor.
        segments, colors, widths, depths = [], [], [], []
        for points, color, width in ((ring, COIL_COLOR, 2.7), (wire, WIRE_COLOR, 3.0)):
            for start, end in zip(points[:-1], points[1:]):
                segments.append(project(np.array([start, end]), camera))
                colors.append(color)
                widths.append(width)
                depths.append(float(np.dot((start + end) / 2, camera[2])))
        order = np.argsort(depths, kind="stable")
        collection = LineCollection(np.array(segments)[order], colors=np.array(colors)[order],
                                    linewidths=np.array(widths)[order], capstyle="round", zorder=5)
        collection.set_path_effects([pe.Stroke(linewidth=5.0, foreground="white"), pe.Normal()])
        ax.add_collection(collection)
        # Coil current follows increasing theta for CCW viewed from +axis.
        near_theta = math.atan2(np.dot(camera[2], v), np.dot(camera[2], u))
        sign = 1 if cfg.coil_sense == "ccw" else -1
        arrow_angles = near_theta + sign * np.linspace(-0.28, 0.28, 35)
        coil_arrow3 = r * (np.cos(arrow_angles)[:, None] * u + np.sin(arrow_angles)[:, None] * v)
        coil_arrow2 = project(coil_arrow3, camera)
        coil_current_arrow = _arrow(ax, coil_arrow2, COIL_COLOR, width=2.8, head=15)
        # The current arrow lies on the wire and is positioned away from Q.
        arrow_center_t = t0 + 0.23 * (t1 - t0)
        arrow_ts = arrow_center_t + cfg.wire_sign * np.array([-0.34, 0.34]) * r
        wire_arrow3 = q + arrow_ts[:, None] * UNIT[j]
        wire_current_arrow = _arrow(ax, project(wire_arrow3, camera), WIRE_COLOR, width=3.0, head=15)
        # Radius annotation, kept on the opposite half from the current arrow.
        radius_theta = near_theta + 2.3
        radius_tip = r * (math.cos(radius_theta) * u + math.sin(radius_theta) * v)
        radius2 = project(np.array([np.zeros(3), radius_tip]), camera)
        radius_arrow = FancyArrowPatch(radius2[0], radius2[1], arrowstyle="-|>",
                                      mutation_scale=9, color=COIL_COLOR, lw=0.9, zorder=3)
        ax.add_patch(radius_arrow)
        p2, foot2, o2 = project(np.array([p, foot, np.zeros(3)]), camera)
        ax.scatter(*foot2, s=30, facecolors="white", edgecolors=WIRE_COLOR, linewidths=1.1, zorder=35)
        ax.scatter(*o2, s=19, color=INK, zorder=35)
        ax.scatter(*p2, s=67, facecolors=INK, edgecolors="white", linewidths=1.1, zorder=40)
        fig.canvas.draw()
        reference_axes = np.vstack([
            np.linspace(axis_lo[i], axis_hi[i], 100)[:, None] * UNIT[i]
            for i in range(3)])
        label_geometry = np.vstack([ring[::3], wire[::3], reference_axes, corner_path])
        if fields:
            # Reserve overlay paths in both versions so source labels stay put.
            label_geometry = np.vstack([label_geometry] + [
                np.linspace(arrow["points3"][0], arrow["points3"][1], 50)
                for arrow in fields])
        placer = LabelPlacer(fig, ax, project(label_geometry, camera))
        origin_display = ax.transData.transform(o2)
        for i in range(3):
            tip = project(axis_hi[i] * UNIT[i], camera)
            direction2 = ax.transData.transform(tip) - origin_display
            direction2 /= np.linalg.norm(direction2)
            # Center each axis letter beyond the arrowhead, never on its shaft.
            placer.fixed(tip, f"${AXES[i]}$", size=14, offset=tuple(13 * direction2))
        # R interrupts the radius line; Ic sits directly below the current arrow.
        radius_label = placer.fixed(radius2.mean(axis=0), "$R$", color=COIL_COLOR, size=12, pad=1.6)
        below_coil_arrow = np.array([coil_arrow2[:, 0].mean(), coil_arrow2[:, 1].min()])
        coil_current_label = placer.fixed(below_coil_arrow, "$I_c$", offset=(0, -8),
                                          color=COIL_COLOR, size=14, va="top")
        placer.add(p2, "$P$", size=15,
                   candidates=[(6, 0), (-6, 0), (0, 6), (0, -6),
                               (6, -2), (-6, 2), (6, 2), (-6, -2)])
        placer.add(foot2, "$Q$", size=12, color=WIRE_COLOR,
                   candidates=[(4.5, 0), (-4.5, 0), (0, 4.5), (0, -4.5),
                               (5, -2), (-5, 2), (5, 2), (-5, -2)])
        wire_current_label = placer.add(project(np.mean(wire_arrow3, axis=0), camera), "$I_w$",
                                        color=WIRE_COLOR, size=14, preferred=(14, 3))
        fig.text(0.065, 0.954, "N-turn circular coil", color=COIL_COLOR, fontsize=12, weight="semibold")
        fig.text(0.57, 0.954, "Long straight wire", color=WIRE_COLOR, fontsize=12, weight="semibold")
        if show_title:
            fig.text(0.065, 0.922, FAMILY_NAMES[cfg.family], fontsize=10, color=GUIDE)
        direction = "+" if cfg.wire_sign > 0 else "−"
        footer = (f"Coil: {cfg.coil_sense.upper()}, viewed from +{cfg.coil_axis} toward origin"
                  f"    |    Wire current: {direction}{cfg.wire_axis}")
        fig.text(0.065, 0.125, footer, fontsize=9, color=INK)
        fig.text(0.065, 0.085, f"P = {_coordinate_text(p)}    |    Q = {_coordinate_text(foot)}",
                 fontsize=9, color=INK)
        fig.text(0.065, 0.045, "The coil is centered at the origin. PQ is perpendicular to the wire.",
                 fontsize=8.6, color=GUIDE)
        stem = Path(output_stem)
        stem.parent.mkdir(parents=True, exist_ok=True)
        paths = []
        for fmt in formats:
            if fmt not in ("png", "svg", "pdf"):
                raise ValueError("Supported output formats: png, svg, pdf.")
            path = stem.with_suffix("." + fmt)
            fig.savefig(path, dpi=dpi, facecolor="white")
            paths.append(path)
        if with_fields:
            # Add the overlay only after exporting the answer-free question.
            # Continuous shadow paths avoid opacity accumulating where short,
            # depth-sorted conductor strokes meet. No white occlusion halos:
            # these faint sources provide context for the full-color vectors.
            if feedback_source_alpha < 1:
                collection.set_visible(False)
                for points, color, width in ((ring, COIL_COLOR, 2.7), (wire, WIRE_COLOR, 3.0)):
                    shadow = project(points, camera)
                    ax.plot(shadow[:, 0], shadow[:, 1], color=color, lw=width,
                            alpha=feedback_source_alpha, solid_capstyle="round",
                            solid_joinstyle="round", zorder=5)
                for artist in (coil_current_arrow, wire_current_arrow, radius_arrow):
                    artist.set_alpha(feedback_source_alpha)
                    artist.set_path_effects([])
                for artist in (radius_label, coil_current_label, wire_current_label):
                    artist.set_alpha(min(1, 2 * feedback_source_alpha))
            # The dot at P stays on top of the common arrow origins.
            for arrow in fields:
                _arrow(ax, arrow["points2"], arrow["color"], width=arrow["width"],
                       head=17, zorder=30, halo=arrow["halo"])
            fig.canvas.draw()
            placer.renderer = fig.canvas.get_renderer()
            for arrow in fields:
                start, end = arrow["points2"]
                direction2 = (end - start) / np.linalg.norm(end - start)
                normal2 = np.array([-direction2[1], direction2[0]])
                side = 1 if arrow["source"] == "coil" else -1
                preferred = tuple(side * 10 * normal2 + 3 * direction2)
                placer.add(end, arrow["label"], color=arrow["color"], size=14,
                           preferred=preferred)
            fig.text(0.065, 0.018,
                     "Field arrows show direction only; lengths are schematic.",
                     fontsize=8.5, color=GUIDE)
            feedback_stem = stem.with_name(stem.name + "_feedback")
            for fmt in formats:
                path = feedback_stem.with_suffix("." + fmt)
                fig.savefig(path, dpi=dpi, facecolor="white")
                paths.append(path)
        plt.close(fig)
    return paths


def alt_text(cfg: DiagramConfig, *, with_fields: bool = False) -> str:
    """Describe sources; include field directions only for feedback versions."""
    g = source_geometry(cfg)
    direction = "positive" if cfg.wire_sign > 0 else "negative"
    sense = "counterclockwise" if cfg.coil_sense == "ccw" else "clockwise"
    guide_description = ("Segment PQ lies on a coordinate axis. "
                         if segment_on_coordinate_axis(cfg.observation, g["foot"])
                         else "A dashed segment PQ marks the perpendicular distance from P to the wire. ")
    description = (f"Three-dimensional coordinate diagram. A circular N-turn coil of radius R is centered "
            f"at the origin with its axis along {cfg.coil_axis}. Its current is {sense} when "
            f"viewed from the positive {cfg.coil_axis} axis toward the origin. A long straight wire is "
            f"parallel to the {cfg.wire_axis} axis and passes through "
            f"{_coordinate_text(cfg.wire_point)}. Wire current flows in the {direction} "
            f"{cfg.wire_axis} direction. Observation point P is at {_coordinate_text(cfg.observation)}. "
            f"Q, the closest point on the wire to P, is at {_coordinate_text(g['foot'])}. "
            f"{guide_description}"
            f"One drawn circle represents N coincident circular turns.")
    if with_fields:
        def direction_description(vector):
            active = np.flatnonzero(np.abs(vector) > 1e-9)
            if len(active) == 1:
                i = active[0]
                return f"the {'positive' if vector[i] > 0 else 'negative'} {AXES[i]} direction"
            components = ", ".join(f"{value:.3g}" for value in vector)
            return f"the direction of unit vector ({components})"
        description += (
            f" The sources are faint background outlines. Both magnetic-field arrows "
            f"originate at P. The coil-colored arrow, labeled "
            f"vector B subscript c, points in {direction_description(g['coil_direction'])}. "
            f"The wire-colored arrow, labeled vector B subscript w, points in "
            f"{direction_description(g['wire_direction'])}. "
            f"Arrow lengths are schematic and indicate directions only.")
    return description


def validate_bank(configs: Sequence[DiagramConfig]) -> dict:
    if len(configs) != 84:
        raise AssertionError(f"Expected 84 configurations, found {len(configs)}")
    family_counts, relations, signatures = Counter(), Counter(), set()
    for cfg in configs:
        g = validate_config(cfg)
        family_counts[cfg.family] += 1
        relations[g["relationship"]] += 1
        signature = (cfg.coil_axis, cfg.coil_sense, cfg.wire_axis, cfg.wire_sign,
                     tuple(cfg.wire_point), tuple(cfg.observation))
        if signature in signatures:
            raise AssertionError("Duplicate source geometry and currents")
        signatures.add(signature)
        reversed_wire = validate_config(replace(cfg, wire_sign=-cfg.wire_sign))
        if not np.allclose(g["wire_direction"], -reversed_wire["wire_direction"]):
            raise AssertionError("Wire-current reversal did not reverse its magnetic field")
        reversed_coil = validate_config(replace(cfg, coil_sense="cw" if cfg.coil_sense == "ccw" else "ccw"))
        if not np.allclose(g["coil_direction"], -reversed_coil["coil_direction"]):
            raise AssertionError("Coil-current reversal did not reverse its magnetic field")
    if dict(family_counts) != {"parallel": 12, "sideways": 24, "crossing_near": 24, "crossing_far": 24}:
        raise AssertionError(f"Incorrect family counts: {family_counts}")
    if dict(relations) != {"perpendicular": 60, "parallel": 12, "antiparallel": 12}:
        raise AssertionError(f"Incorrect field relationships: {relations}")
    return {"configurations": len(configs), "families": dict(family_counts),
            "field_relationships": dict(relations), "current_reversals": "passed",
            "unique_source_configurations": len(signatures)}


def demo_configs() -> list[DiagramConfig]:
    """Use one common coil orientation to make placement differences visible."""
    configs = enumerate_84()
    selected = []
    for family in FAMILIES:
        cfg = next(c for c in configs if c.family == family and c.coil_axis == "z"
                   and c.coil_sense == "ccw" and c.wire_sign == 1
                   and c.wire_axis == ("z" if family == "parallel" else "x"))
        selected.append(replace(cfg, identifier="demo_" + family))
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--demo", action="store_true", help="Render four representative layouts (default).")
    group.add_argument("--all-84", action="store_true", help="Render all 84 chosen source configurations.")
    group.add_argument("--config", type=Path, help="Read one configuration or a list from JSON.")
    group.add_argument("--validate-only", action="store_true", help="Check all 84 geometries without drawing.")
    parser.add_argument("--output-dir", type=Path, default=Path("figures"))
    parser.add_argument("--formats", nargs="+", choices=["png", "svg", "pdf"], default=["png", "svg"])
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--with-fields", action="store_true",
                        help="Also write *_feedback images with labeled field-direction arrows from P.")
    parser.add_argument("--feedback-source-alpha", type=float, default=0.15,
                        help="Source opacity in feedback images, from 0 to 1 (default: 0.15).")
    args = parser.parse_args()
    if args.dpi < 30:
        parser.error("--dpi must be at least 30")
    if not 0 <= args.feedback_source_alpha <= 1:
        parser.error("--feedback-source-alpha must be between 0 and 1")
    report = validate_bank(enumerate_84())
    if args.validate_only:
        print(json.dumps(report, indent=2))
        return
    if args.config:
        values = json.loads(args.config.read_text(encoding="utf-8"))
        values = values if isinstance(values, list) else [values]
        configs = [DiagramConfig.from_dict(value) for value in values]
    else:
        configs = enumerate_84() if args.all_84 else demo_configs()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for cfg in configs:
        # Restrict identifiers to a basename, including when reading external JSON.
        if not cfg.identifier or Path(cfg.identifier).name != cfg.identifier or cfg.identifier in (".", ".."):
            parser.error("Each configuration identifier must be a plain filename stem.")
        draw_diagram(cfg, args.output_dir / cfg.identifier, dpi=args.dpi,
                     formats=args.formats, show_title=True, with_fields=args.with_fields,
                     feedback_source_alpha=args.feedback_source_alpha)
    (args.output_dir / "configurations.json").write_text(
        json.dumps([asdict(c) for c in configs], indent=2) + "\n", encoding="utf-8")
    descriptions = {c.identifier: alt_text(c) for c in configs}
    if args.with_fields:
        descriptions.update({c.identifier + "_feedback": alt_text(c, with_fields=True) for c in configs})
    (args.output_dir / "alt_text.json").write_text(
        json.dumps(descriptions, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    versions = len(configs) * (2 if args.with_fields else 1)
    print(f"Rendered {len(configs)} configurations ({versions} image versions) to {args.output_dir.resolve()}")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
