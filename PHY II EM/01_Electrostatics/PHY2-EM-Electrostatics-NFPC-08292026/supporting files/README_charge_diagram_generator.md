# Charge Diagram Generator

`charge_diagram_generator.py` generates a charge-location diagram and one
pairwise Coulomb-force diagram for each unique pair of charges. It exports
publication-quality SVG graphics and Canvas-ready PNG graphics.

## Requirements

- Python 3.10 or newer
- Matplotlib
- NumPy

Install the dependencies if necessary:

```bash
python -m pip install matplotlib numpy
```

## Basic use

Generate clean typeset diagrams:

```bash
python charge_diagram_generator.py --style typeset
```

Generate the hand-drawn approximation:

```bash
python charge_diagram_generator.py --style handdrawn
```

Generate both styles in one run:

```bash
python charge_diagram_generator.py --style both
```

The default output directory is `generated_charge_diagrams`. Use a different
directory with `--output-dir DIRECTORY`.

## Changing the charges

Edit `example_configuration()` in the Python file. Each charge is defined by
its label, signed charge in coulombs, coordinate, color, and optional label
offset:

```python
charges = [
    Charge(label="q1", q=+2.0e-6, xy=(0.0, 1.0), color="#0068A6"),
    Charge(label="q2", q=-3.0e-6, xy=(0.0, 0.0), color="#990000"),
    Charge(label="q3", q=+1.0e-6, xy=(2.0, 0.0), color="#00864A"),
]
```

Force directions are recalculated automatically from the coordinates and
signed charge values.

Dimensions identify their endpoint charges and use a signed perpendicular
offset:

```python
dimensions = [
    Dimension("q2", "q1", "d", offset=+0.28),
    Dimension("q2", "q3", "2d", offset=-0.24),
]
```

## Useful flags

```text
--style typeset|handdrawn|both
--arrow-mode normalized|magnitude
--show-charge-values
--hide-force-labels
--hide-dimensions
--formats png svg pdf
--output-dir DIRECTORY
```

`normalized` arrows emphasize direction and use equal displayed lengths.
`magnitude` arrows are scaled relative to the largest pairwise force in the
diagram set, with a minimum length so small forces remain visible.

## Using the generator from another Python program

Import `Charge`, `Dimension`, `DiagramOptions`, and `generate_diagram_set`:

```python
from pathlib import Path

from charge_diagram_generator import (
    Charge,
    DiagramOptions,
    Dimension,
    generate_diagram_set,
)

charges = [
    Charge("q1", +2e-6, (0, 1), "#0068A6"),
    Charge("q2", -3e-6, (0, 0), "#990000"),
    Charge("q3", +1e-6, (2, 0), "#00864A"),
]

dimensions = [
    Dimension("q2", "q1", "d", +0.28),
    Dimension("q2", "q3", "2d", -0.24),
]

options = DiagramOptions(
    style="typeset",
    arrow_mode="normalized",
    show_force_labels=True,
    show_dimensions=True,
    show_charge_values=False,
    formats=("png", "svg"),
)

generate_diagram_set(charges, dimensions, Path("my_diagrams"), options)
```

The SVG files are best for resizing and printed materials. The PNG files are
convenient for Canvas uploads; include meaningful alternative text when adding
them to a Canvas page.
