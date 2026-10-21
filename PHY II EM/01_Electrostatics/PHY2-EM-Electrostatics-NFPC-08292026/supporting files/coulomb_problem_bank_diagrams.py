#!/usr/bin/env python3
"""Generate 36 typeset diagrams for the Coulomb's-law problem bank.

This batch driver imports the drawing components from
``charge_diagram_generator.py``.  For each scenario, it creates one geometry
diagram and the two source-target pair-force diagrams needed in the solution.
Every image is resized to exactly 400 pixels wide while preserving its aspect
ratio, and all 36 PNG files are packaged into a ZIP archive.
"""

from __future__ import annotations

import argparse
import math
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
GENERATOR_CANDIDATES = (
    SCRIPT_DIRECTORY / "charge_diagram_generator.py",
    SCRIPT_DIRECTORY / "upload" / "charge_diagram_generator.py",
)

for candidate in GENERATOR_CANDIDATES:
    if candidate.is_file():
        sys.path.insert(0, str(candidate.parent))
        break
else:
    raise FileNotFoundError(
        "Place charge_diagram_generator.py beside this script or in an "
        "'upload' subdirectory."
    )

from charge_diagram_generator import (  # noqa: E402
    Charge,
    DiagramOptions,
    SceneBounds,
    _draw_axes,
    _draw_charges,
    _new_figure,
    draw_pair_force_diagram,
)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402


ELEMENTARY_CHARGE = 1.602_176_634e-19
CHARGE_COLORS = {
    "q1": "#0068A6",
    "q2": "#990000",
    "q3": "#00864A",
}


@dataclass(frozen=True)
class Scenario:
    number: int
    d_label: str
    target: str
    # Charge values are stored in coulombs; coordinates are stored in units of d.
    charges: tuple[tuple[str, float, tuple[int, int]], ...]


SCENARIOS = (
    Scenario(1, "20 nm", "q2", (("q1", +2 * ELEMENTARY_CHARGE, (-2, 1)), ("q2", -3 * ELEMENTARY_CHARGE, (0, 1)), ("q3", -5 * ELEMENTARY_CHARGE, (1, -1)))),
    Scenario(2, "45 nm", "q1", (("q1", -4 * ELEMENTARY_CHARGE, (-1, 0)), ("q2", +7 * ELEMENTARY_CHARGE, (2, -1)), ("q3", +3 * ELEMENTARY_CHARGE, (-1, 2)))),
    Scenario(3, "2.0 um", "q3", (("q1", +6 * ELEMENTARY_CHARGE, (-2, 0)), ("q2", -2 * ELEMENTARY_CHARGE, (1, 1)), ("q3", +5 * ELEMENTARY_CHARGE, (1, -2)))),
    Scenario(4, "35 um", "q2", (("q1", -7 * ELEMENTARY_CHARGE, (0, 2)), ("q2", -4 * ELEMENTARY_CHARGE, (-2, -1)), ("q3", +3 * ELEMENTARY_CHARGE, (2, -1)))),
    Scenario(5, "0.60 mm", "q1", (("q1", +250e-9, (2, 1)), ("q2", -400e-9, (2, -2)), ("q3", +650e-9, (-1, 0)))),
    Scenario(6, "1.5 mm", "q3", (("q1", -180e-9, (-2, 0)), ("q2", +320e-9, (1, 2)), ("q3", -540e-9, (0, 0)))),
    Scenario(7, "1.2 cm", "q2", (("q1", +750e-9, (-1, 2)), ("q2", +300e-9, (1, 2)), ("q3", -500e-9, (0, -1)))),
    Scenario(8, "3.0 cm", "q1", (("q1", -220e-9, (0, -2)), ("q2", +680e-9, (-2, 0)), ("q3", +450e-9, (0, 1)))),
    Scenario(9, "8.0 mm", "q3", (("q1", +1.5e-6, (0, -2)), ("q2", -2.5e-6, (2, 1)), ("q3", +4.0e-6, (-1, 1)))),
    Scenario(10, "1.5 cm", "q1", (("q1", -3.0e-6, (1, 0)), ("q2", +5.5e-6, (1, 2)), ("q3", -1.8e-6, (-2, -1)))),
    Scenario(11, "2.5 cm", "q2", (("q1", +6.0e-6, (1, 2)), ("q2", -2.0e-6, (0, -1)), ("q3", -4.5e-6, (-2, -1)))),
    Scenario(12, "4.0 cm", "q3", (("q1", -7.5e-6, (-1, 2)), ("q2", +3.5e-6, (0, -2)), ("q3", +5.0e-6, (2, 2)))),
)


def validate_scenario(scenario: Scenario) -> None:
    """Verify distinct grid nodes and the required source-charge geometry."""

    positions = {label: xy for label, _value, xy in scenario.charges}
    if set(positions) != {"q1", "q2", "q3"}:
        raise ValueError(f"Scenario {scenario.number}: expected q1, q2, and q3.")
    if len(set(positions.values())) != 3:
        raise ValueError(f"Scenario {scenario.number}: charge locations must differ.")
    if any(coordinate not in {-2, -1, 0, 1, 2} for xy in positions.values() for coordinate in xy):
        raise ValueError(f"Scenario {scenario.number}: a charge is outside the grid.")

    target_x, target_y = positions[scenario.target]
    sources = [label for label in positions if label != scenario.target]
    aligned = [
        label
        for label in sources
        if positions[label][0] == target_x or positions[label][1] == target_y
    ]
    diagonal = [
        label
        for label in sources
        if positions[label][0] != target_x and positions[label][1] != target_y
    ]
    if len(aligned) != 1 or len(diagonal) != 1:
        raise ValueError(
            f"Scenario {scenario.number}: expected one aligned and one diagonal source."
        )


def resize_to_width(path: Path, width: int) -> tuple[int, int]:
    """Resize a PNG to ``width`` pixels while preserving aspect ratio."""

    with Image.open(path) as image:
        height = max(1, math.floor(image.height * width / image.width + 0.5))
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        resized.save(path, format="PNG", optimize=True, dpi=(180, 180))
    return width, height


def draw_gridded_geometry(charges: list[Charge], options: DiagramOptions) -> Figure:
    """Draw the complete -2d to +2d grid with one x- and y-spacing label."""

    bounds = SceneBounds(-2.72, 2.72, -2.72, 2.72)
    figure, axes = _new_figure(options, bounds)

    grid_color = "#C9CED3"
    for coordinate in range(-2, 3):
        axes.plot(
            [-2, 2],
            [coordinate, coordinate],
            color=grid_color,
            linewidth=0.8,
            zorder=0,
        )
        axes.plot(
            [coordinate, coordinate],
            [-2, 2],
            color=grid_color,
            linewidth=0.8,
            zorder=0,
        )

    _draw_axes(axes, bounds, options)
    _draw_charges(axes, charges, options)

    dimension_color = "#555555"
    arrow_properties = dict(
        arrowstyle="<->",
        mutation_scale=10,
        linewidth=1.0,
        color=dimension_color,
        shrinkA=0,
        shrinkB=0,
        zorder=3,
    )

    # One horizontal cell width: Delta x = d.
    axes.add_patch(FancyArrowPatch((0, -2.38), (1, -2.38), **arrow_properties))
    axes.text(
        0.5,
        -2.48,
        r"$d$",
        ha="center",
        va="top",
        fontsize=12.5,
        color=dimension_color,
        zorder=4,
    )

    # One vertical cell height: Delta y = d.
    axes.add_patch(FancyArrowPatch((-2.38, 0), (-2.38, 1), **arrow_properties))
    axes.text(
        -2.48,
        0.5,
        r"$d$",
        ha="right",
        va="center",
        fontsize=12.5,
        color=dimension_color,
        zorder=4,
    )
    return figure


def save_and_resize(
    figure: Figure,
    output_path: Path,
    width: int,
    title: str,
    description: str,
    dpi: int,
) -> None:
    """Save one Matplotlib figure, close it, and resize the PNG."""

    figure.savefig(
        output_path,
        format="png",
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.08,
        metadata={
            "Title": title,
            "Description": description,
            "Software": "charge_diagram_generator.py with batch driver",
        },
    )
    plt.close(figure)
    resize_to_width(output_path, width)


def expand_force_diagram_bounds(figure: Figure, fraction: float = 0.14) -> None:
    """Add breathing room so diagonal arrows and labels are not clipped."""

    axes = figure.axes[0]
    x_min, x_max = axes.get_xlim()
    y_min, y_max = axes.get_ylim()
    x_margin = fraction * (x_max - x_min)
    y_margin = fraction * (y_max - y_min)
    axes.set_xlim(x_min - x_margin, x_max + x_margin)
    axes.set_ylim(y_min - y_margin, y_max + y_margin)


def generate(output_directory: Path, zip_path: Path, width: int = 400) -> list[Path]:
    """Render, resize, and archive three diagrams for every scenario."""

    output_directory.mkdir(parents=True, exist_ok=True)
    options = DiagramOptions(
        style="typeset",
        show_force_labels=True,
        show_dimensions=False,
        show_charge_values=False,
        figure_size=(6.4, 4.2),
        dpi=180,
        formats=("png",),
    )

    created: list[Path] = []
    for scenario in SCENARIOS:
        validate_scenario(scenario)
        charges = [
            Charge(
                label=label,
                q=value,
                xy=xy,
                color=CHARGE_COLORS[label],
                # Keep labels at positive y-axis nodes clear of the +y marker.
                label_offset=(-28.0, 5.0) if xy[0] == 0 and xy[1] > 0 else (10.0, 5.0),
            )
            for label, value, xy in scenario.charges
        ]
        geometry_path = output_directory / f"coulomb_problem_{scenario.number:02d}.png"
        save_and_resize(
            draw_gridded_geometry(charges, options),
            geometry_path,
            width,
            f"Coulomb's law problem {scenario.number}: geometry",
            (
                f"Three-charge coordinate diagram on a d by d grid; "
                f"force target {scenario.target}; d = {scenario.d_label}."
            ),
            options.dpi,
        )
        created.append(geometry_path)

        by_label = {charge.label: charge for charge in charges}
        target = by_label[scenario.target]
        source_labels = sorted(label for label in by_label if label != scenario.target)
        for source_label in source_labels:
            source = by_label[source_label]
            force_path = output_directory / (
                f"coulomb_problem_{scenario.number:02d}_"
                f"force_{source_label}_on_{scenario.target}.png"
            )
            force_figure = draw_pair_force_diagram(
                charges,
                target,
                source,
                options,
                maximum_force_magnitude=1.0,
            )
            expand_force_diagram_bounds(force_figure)
            save_and_resize(
                force_figure,
                force_path,
                width,
                (
                    f"Coulomb's law problem {scenario.number}: "
                    f"{source_label} and {scenario.target} force pair"
                ),
                (
                    f"Pairwise Coulomb-force vectors between {source_label} and "
                    f"target {scenario.target}."
                ),
                options.dpi,
            )
            created.append(force_path)

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for image_path in created:
            archive.write(image_path, arcname=image_path.name)
    return created


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SCRIPT_DIRECTORY / "coulomb_problem_diagrams_400px",
    )
    parser.add_argument(
        "--zip-file",
        type=Path,
        default=SCRIPT_DIRECTORY / "coulomb_problem_diagrams_400px.zip",
    )
    parser.add_argument("--width", type=int, default=400)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.width <= 0:
        raise ValueError("Image width must be a positive integer.")
    files = generate(arguments.output_dir, arguments.zip_file, arguments.width)
    print(f"Created {len(files)} diagrams in {arguments.output_dir.resolve()}")
    print(f"Created ZIP archive: {arguments.zip_file.resolve()}")
    for path in files:
        with Image.open(path) as image:
            print(f"{path.name}: {image.width} x {image.height} px")


if __name__ == "__main__":
    main()
