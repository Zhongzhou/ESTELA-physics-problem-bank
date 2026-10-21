#!/usr/bin/env python3
"""Generate reusable electrostatics charge and pairwise-force diagrams.

The charge locations and values are defined once in ``example_configuration``.
The same configuration is then used to create a geometry diagram and one force
diagram for every charge pair.  Both clean typeset and hand-drawn approximation
styles are supported.
"""

from __future__ import annotations

import argparse
import math
import re
from contextlib import contextmanager
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Literal, Sequence

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch


COULOMB_CONSTANT = 8.987_551_792_3e9
StyleName = Literal["typeset", "handdrawn"]
ArrowMode = Literal["normalized", "magnitude"]


@dataclass(frozen=True)
class Charge:
    """A point charge and its display settings."""

    label: str
    q: float
    xy: tuple[float, float]
    color: str
    label_offset: tuple[float, float] = (10.0, 5.0)


@dataclass(frozen=True)
class Dimension:
    """A dimension line joining two charges.

    ``offset`` is measured in data-coordinate units, perpendicular to the
    start-to-end direction. Positive offset is to the left when moving from
    the start charge to the end charge; negative offset is to the right.
    """

    start_charge: str
    end_charge: str
    label: str
    offset: float


@dataclass
class DiagramOptions:
    """Visual and export options for a complete diagram set."""

    style: StyleName = "typeset"
    show_force_labels: bool = True
    show_dimensions: bool = True
    show_charge_values: bool = False
    arrow_mode: ArrowMode = "normalized"
    normalized_arrow_fraction: float = 0.18
    minimum_magnitude_arrow_fraction: float = 0.07
    maximum_magnitude_arrow_fraction: float = 0.28
    charge_marker_size: float = 245.0
    force_color: str = "#E31A1C"
    axis_color: str = "#252525"
    dimension_color: str = "#A8A8A8"
    background_color: str = "white"
    figure_size: tuple[float, float] = (6.4, 4.2)
    dpi: int = 180
    formats: tuple[str, ...] = field(default_factory=lambda: ("png", "svg"))


@dataclass(frozen=True)
class SceneBounds:
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    @property
    def span(self) -> float:
        return max(self.x_max - self.x_min, self.y_max - self.y_min)


def example_configuration() -> tuple[list[Charge], list[Dimension]]:
    """Return the example requested in the conversation."""

    charges = [
        Charge(label="q1", q=+2.0e-6, xy=(0.0, 1.0), color="#0068A6"),
        Charge(label="q2", q=-3.0e-6, xy=(0.0, 0.0), color="#990000"),
        Charge(label="q3", q=+1.0e-6, xy=(2.0, 0.0), color="#00864A"),
    ]
    dimensions = [
        Dimension("q2", "q1", "d", offset=+0.28),
        Dimension("q2", "q3", "2d", offset=-0.24),
    ]
    return charges, dimensions


def force_on_target(target: Charge, source: Charge) -> np.ndarray:
    """Return the Coulomb-force vector on ``target`` due to ``source``."""

    displacement = np.asarray(target.xy, dtype=float) - np.asarray(source.xy, dtype=float)
    separation = float(np.linalg.norm(displacement))
    if separation == 0.0:
        raise ValueError(f"Charges {target.label!r} and {source.label!r} are coincident.")
    return (
        COULOMB_CONSTANT
        * target.q
        * source.q
        * displacement
        / separation**3
    )


def _validate_configuration(charges: Sequence[Charge], dimensions: Sequence[Dimension]) -> None:
    if len(charges) < 2:
        raise ValueError("At least two charges are required.")
    labels = [charge.label for charge in charges]
    if len(labels) != len(set(labels)):
        raise ValueError("Every charge label must be unique.")
    if any(charge.q == 0.0 for charge in charges):
        raise ValueError("Each charge must be nonzero for pairwise-force diagrams.")
    known = set(labels)
    for dimension in dimensions:
        if dimension.start_charge not in known or dimension.end_charge not in known:
            raise ValueError(f"Dimension {dimension!r} refers to an unknown charge.")
        if dimension.start_charge == dimension.end_charge:
            raise ValueError("A dimension must join two different charges.")
    for first, second in combinations(charges, 2):
        if np.allclose(first.xy, second.xy, rtol=0.0, atol=0.0):
            raise ValueError(f"Charges {first.label!r} and {second.label!r} are coincident.")


def _charge_map(charges: Sequence[Charge]) -> dict[str, Charge]:
    return {charge.label: charge for charge in charges}


def _dimension_points(
    dimension: Dimension, by_label: dict[str, Charge]
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    start = np.asarray(by_label[dimension.start_charge].xy, dtype=float)
    end = np.asarray(by_label[dimension.end_charge].xy, dtype=float)
    direction = end - start
    length = float(np.linalg.norm(direction))
    if length == 0.0:
        raise ValueError("A dimension cannot join coincident charges.")
    normal = np.array([-direction[1], direction[0]]) / length
    offset = dimension.offset * normal
    return start, end, start + offset, end + offset


def _scene_bounds(
    charges: Sequence[Charge],
    dimensions: Sequence[Dimension],
    show_dimensions: bool,
    force_diagram: bool = False,
) -> SceneBounds:
    points = [np.asarray(charge.xy, dtype=float) for charge in charges]
    points.append(np.array([0.0, 0.0]))
    if show_dimensions:
        by_label = _charge_map(charges)
        for dimension in dimensions:
            _, _, dim_start, dim_end = _dimension_points(dimension, by_label)
            points.extend((dim_start, dim_end))
    coordinates = np.vstack(points)
    x_range = float(np.ptp(coordinates[:, 0])) or 1.0
    y_range = float(np.ptp(coordinates[:, 1])) or 1.0
    base_span = max(x_range, y_range, 1.0)
    x_padding_fraction = 0.34 if force_diagram else 0.26
    y_padding_fraction = 0.31 if force_diagram else 0.24
    x_pad = max(x_padding_fraction * base_span, 0.2)
    y_pad = max(y_padding_fraction * base_span, 0.2)
    return SceneBounds(
        x_min=float(coordinates[:, 0].min() - x_pad),
        x_max=float(coordinates[:, 0].max() + x_pad),
        y_min=float(coordinates[:, 1].min() - y_pad),
        y_max=float(coordinates[:, 1].max() + y_pad),
    )


@contextmanager
def _style_context(style: StyleName) -> Iterator[None]:
    common = {
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "mathtext.fontset": "stix",
        "axes.unicode_minus": False,
    }
    if style == "handdrawn":
        # Matplotlib's xkcd context adds deterministic-looking sketch effects.
        # DejaVu Sans is deliberately retained so no external font is required.
        with plt.xkcd(scale=0.72, length=85.0, randomness=1.35):
            with mpl.rc_context(
                {
                    **common,
                    "font.family": "DejaVu Sans",
                    "font.style": "oblique",
                    "path.sketch": (0.72, 85.0, 1.35),
                }
            ):
                yield
    else:
        with mpl.rc_context({**common, "font.family": "DejaVu Sans"}):
            yield


def _subscript(text: str) -> str:
    return text.translate(str.maketrans("0123456789+-", "₀₁₂₃₄₅₆₇₈₉₊₋"))


def _charge_index(label: str) -> str:
    match = re.search(r"(\d+)$", label)
    return match.group(1) if match else label


def _charge_text(charge: Charge, style: StyleName, include_value: bool) -> str:
    index = _charge_index(charge.label)
    if style == "typeset":
        base = rf"$q_{{{index}}}$"
        return f"{base}  {_format_charge_value(charge.q)}" if include_value else base
    base = f"q{_subscript(index)}"
    return f"{base}  {_format_charge_value(charge.q)}" if include_value else base


def _force_text(target: Charge, source: Charge, style: StyleName) -> str:
    target_index = _charge_index(target.label)
    source_index = _charge_index(source.label)
    if style == "typeset":
        return rf"$\vec{{F}}_{{{source_index}\,\mathrm{{on}}\,{target_index}}}$"
    return f"F⃗{_subscript(source_index)} on {_subscript(target_index)}"


def _axis_text(axis: str, style: StyleName) -> str:
    return rf"$+{axis}$" if style == "typeset" else f"+{axis}"


def _dimension_text(label: str, style: StyleName) -> str:
    return rf"${label}$" if style == "typeset" else label


def _format_charge_value(value: float) -> str:
    magnitude = abs(value)
    units = ((1e-3, "mC"), (1e-6, "μC"), (1e-9, "nC"), (1e-12, "pC"))
    sign = "+" if value > 0 else "−"
    for scale, unit in units:
        if magnitude >= scale:
            return f"{sign}{magnitude / scale:.3g} {unit}"
    return f"{value:.3g} C"


def _new_figure(options: DiagramOptions, bounds: SceneBounds) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=options.figure_size)
    fig.patch.set_facecolor(options.background_color)
    ax.set_facecolor(options.background_color)
    ax.set_xlim(bounds.x_min, bounds.x_max)
    ax.set_ylim(bounds.y_min, bounds.y_max)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    return fig, ax


def _draw_axes(ax: Axes, bounds: SceneBounds, options: DiagramOptions) -> None:
    arrow_properties = dict(
        arrowstyle="->",
        mutation_scale=13,
        linewidth=1.15,
        color=options.axis_color,
        shrinkA=0,
        shrinkB=0,
        zorder=1,
    )
    ax.add_patch(
        FancyArrowPatch(
            (bounds.x_min, 0.0),
            (bounds.x_max - 0.06 * (bounds.x_max - bounds.x_min), 0.0),
            **arrow_properties,
        )
    )
    ax.add_patch(
        FancyArrowPatch(
            (0.0, bounds.y_min),
            (0.0, bounds.y_max - 0.06 * (bounds.y_max - bounds.y_min)),
            **arrow_properties,
        )
    )
    ax.annotate(
        _axis_text("x", options.style),
        (bounds.x_max - 0.06 * (bounds.x_max - bounds.x_min), 0.0),
        xytext=(-1, -8),
        textcoords="offset points",
        ha="right",
        va="top",
        fontsize=13,
        color=options.axis_color,
    )
    ax.annotate(
        _axis_text("y", options.style),
        (0.0, bounds.y_max - 0.06 * (bounds.y_max - bounds.y_min)),
        xytext=(5, -1),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=13,
        color=options.axis_color,
    )


def _draw_charges(ax: Axes, charges: Sequence[Charge], options: DiagramOptions) -> None:
    for charge in charges:
        ax.scatter(
            [charge.xy[0]],
            [charge.xy[1]],
            s=options.charge_marker_size,
            color=charge.color,
            edgecolor="white",
            linewidth=1.1,
            zorder=5,
        )
        ax.annotate(
            _charge_text(charge, options.style, options.show_charge_values),
            charge.xy,
            xytext=charge.label_offset,
            textcoords="offset points",
            ha="left",
            va="bottom",
            fontsize=14,
            color=options.axis_color,
            zorder=6,
        )


def _draw_dimensions(
    ax: Axes,
    charges: Sequence[Charge],
    dimensions: Sequence[Dimension],
    options: DiagramOptions,
) -> None:
    if not options.show_dimensions:
        return
    by_label = _charge_map(charges)
    for dimension in dimensions:
        start, end, dim_start, dim_end = _dimension_points(dimension, by_label)
        extension_vector = dim_start - start
        extension_length = float(np.linalg.norm(extension_vector))
        extension_unit = extension_vector / extension_length
        small_extension = 0.035 * max(float(np.linalg.norm(end - start)), 1.0)
        for anchor, dimension_point in ((start, dim_start), (end, dim_end)):
            extension_end = dimension_point + small_extension * extension_unit
            ax.plot(
                [anchor[0], extension_end[0]],
                [anchor[1], extension_end[1]],
                color=options.dimension_color,
                linewidth=0.8,
                alpha=0.72,
                zorder=0,
            )
        ax.add_patch(
            FancyArrowPatch(
                dim_start,
                dim_end,
                arrowstyle="<->",
                mutation_scale=11,
                linewidth=0.9,
                color=options.dimension_color,
                shrinkA=0,
                shrinkB=0,
                zorder=1,
            )
        )
        midpoint = 0.5 * (dim_start + dim_end)
        direction = dim_end - dim_start
        angle = math.degrees(math.atan2(direction[1], direction[0]))
        if angle > 90 or angle < -90:
            angle += 180
        ax.annotate(
            _dimension_text(dimension.label, options.style),
            midpoint,
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            rotation=angle,
            rotation_mode="anchor",
            fontsize=13,
            color=options.axis_color,
            zorder=2,
        )


def _arrow_length(
    force_magnitude: float,
    maximum_force_magnitude: float,
    bounds: SceneBounds,
    options: DiagramOptions,
) -> float:
    if options.arrow_mode == "normalized":
        return options.normalized_arrow_fraction * bounds.span
    relative = force_magnitude / maximum_force_magnitude
    fraction = max(
        options.minimum_magnitude_arrow_fraction,
        options.maximum_magnitude_arrow_fraction * relative,
    )
    return fraction * bounds.span


def _draw_force_arrow(
    ax: Axes,
    target: Charge,
    source: Charge,
    force: np.ndarray,
    arrow_length: float,
    bounds: SceneBounds,
    options: DiagramOptions,
) -> None:
    force_magnitude = float(np.linalg.norm(force))
    unit_force = force / force_magnitude
    separation = float(
        np.linalg.norm(np.asarray(target.xy, dtype=float) - np.asarray(source.xy, dtype=float))
    )
    # Prevent arrows at a short separation from crossing or hiding one another.
    arrow_length = min(arrow_length, 0.36 * separation)
    marker_clearance = min(0.035 * bounds.span, 0.08 * separation)
    start = np.asarray(target.xy, dtype=float) + marker_clearance * unit_force
    end = start + arrow_length * unit_force
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="->",
            mutation_scale=17,
            linewidth=2.6,
            color=options.force_color,
            shrinkA=0,
            shrinkB=0,
            zorder=4,
        )
    )
    if options.show_force_labels:
        midpoint = start + 0.56 * arrow_length * unit_force
        normal = np.array([-unit_force[1], unit_force[0]])
        # Choose the side farther from the origin to reduce collisions with axes.
        if float(np.dot(midpoint, normal)) < 0:
            normal *= -1
        label_position = midpoint + 0.065 * bounds.span * normal
        ax.text(
            label_position[0],
            label_position[1],
            _force_text(target, source, options.style),
            ha="center",
            va="center",
            fontsize=12.5,
            color=options.force_color,
            zorder=7,
        )


def _maximum_pair_force(charges: Sequence[Charge]) -> float:
    return max(
        float(np.linalg.norm(force_on_target(first, second)))
        for first, second in combinations(charges, 2)
    )


def draw_geometry_diagram(
    charges: Sequence[Charge],
    dimensions: Sequence[Dimension],
    options: DiagramOptions,
) -> Figure:
    """Create the charge-location diagram without force arrows."""

    bounds = _scene_bounds(charges, dimensions, options.show_dimensions)
    fig, ax = _new_figure(options, bounds)
    _draw_axes(ax, bounds, options)
    _draw_dimensions(ax, charges, dimensions, options)
    _draw_charges(ax, charges, options)
    return fig


def draw_pair_force_diagram(
    charges: Sequence[Charge],
    first: Charge,
    second: Charge,
    options: DiagramOptions,
    maximum_force_magnitude: float,
) -> Figure:
    """Create a diagram showing the equal-and-opposite force pair."""

    bounds = _scene_bounds(charges, (), False, force_diagram=True)
    fig, ax = _new_figure(options, bounds)
    _draw_axes(ax, bounds, options)
    _draw_charges(ax, charges, options)
    for target, source in ((first, second), (second, first)):
        force = force_on_target(target, source)
        length = _arrow_length(
            float(np.linalg.norm(force)), maximum_force_magnitude, bounds, options
        )
        _draw_force_arrow(ax, target, source, force, length, bounds, options)
    return fig


def _save_figure(
    fig: Figure,
    output_stem: Path,
    formats: Iterable[str],
    dpi: int,
    title: str,
    description: str,
) -> list[Path]:
    paths: list[Path] = []
    for image_format in formats:
        normalized_format = image_format.lower().lstrip(".")
        path = output_stem.with_suffix(f".{normalized_format}")
        if normalized_format == "pdf":
            metadata = {
                "Title": title,
                "Subject": description,
                "Creator": "charge_diagram_generator.py",
            }
        else:
            metadata = {"Title": title, "Description": description}
            if normalized_format == "png":
                metadata["Software"] = "Matplotlib charge_diagram_generator.py"
        fig.savefig(
            path,
            format=normalized_format,
            dpi=dpi,
            bbox_inches="tight",
            pad_inches=0.08,
            metadata=metadata,
        )
        paths.append(path)
    plt.close(fig)
    return paths


def generate_diagram_set(
    charges: Sequence[Charge],
    dimensions: Sequence[Dimension],
    output_directory: Path | str,
    options: DiagramOptions,
) -> list[Path]:
    """Generate the geometry image and one image per unique charge pair."""

    _validate_configuration(charges, dimensions)
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    geometry = draw_geometry_diagram(charges, dimensions, options)
    created.extend(
        _save_figure(
            geometry,
            output_directory / f"geometry_{options.style}",
            options.formats,
            options.dpi,
            "Three-charge geometry diagram",
            "Three point charges on coordinate axes with labeled separation distances.",
        )
    )

    maximum_force = _maximum_pair_force(charges)
    for first, second in combinations(charges, 2):
        figure = draw_pair_force_diagram(
            charges, first, second, options, maximum_force
        )
        stem = f"forces_{first.label}_{second.label}_{options.style}"
        description = (
            f"Pairwise Coulomb-force vectors between {first.label} and {second.label}; "
            "all three charges and coordinate axes remain visible."
        )
        created.extend(
            _save_figure(
                figure,
                output_directory / stem,
                options.formats,
                options.dpi,
                f"Forces between {first.label} and {second.label}",
                description,
            )
        )
    return created


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate geometry and pairwise-force diagrams for point charges."
    )
    parser.add_argument(
        "--style",
        choices=("typeset", "handdrawn", "both"),
        default="typeset",
        help="Label/line style to generate (default: typeset).",
    )
    parser.add_argument(
        "--arrow-mode",
        choices=("normalized", "magnitude"),
        default="normalized",
        help="Use equal display lengths or scale arrows by force magnitude.",
    )
    parser.add_argument(
        "--show-charge-values",
        action="store_true",
        help="Append charge values to q1, q2, ... labels.",
    )
    parser.add_argument(
        "--hide-force-labels",
        action="store_true",
        help="Omit force-vector labels while retaining the arrows.",
    )
    parser.add_argument(
        "--hide-dimensions",
        action="store_true",
        help="Omit dimension annotations from the geometry diagram.",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=("png", "svg", "pdf"),
        default=("png", "svg"),
        help="One or more output formats (default: png svg).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("generated_charge_diagrams"),
        help="Directory for generated files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    charges, dimensions = example_configuration()
    styles: tuple[StyleName, ...] = (
        ("typeset", "handdrawn") if args.style == "both" else (args.style,)
    )
    all_created: list[Path] = []
    for style in styles:
        options = DiagramOptions(
            style=style,
            show_force_labels=not args.hide_force_labels,
            show_dimensions=not args.hide_dimensions,
            show_charge_values=args.show_charge_values,
            arrow_mode=args.arrow_mode,
            formats=tuple(args.formats),
        )
        all_created.extend(
            generate_diagram_set(charges, dimensions, args.output_dir, options)
        )
    print(f"Created {len(all_created)} files in {args.output_dir.resolve()}")
    for path in all_created:
        print(path)


if __name__ == "__main__":
    main()
