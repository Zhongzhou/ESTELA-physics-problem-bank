# Magnetic Fields from a Straight Wire and a Circular Coil

Bank ID: `PHY2-EM-B-BWC-10182026`  
Author: O. Moussa  
Learning objective: `EM-B-Bnet`  
Created: October 18, 2026

The YAML contains 84 numerical questions. Each asks for the **magnitude of the
net magnetic field at P in microteslas**, with 1 point, a 2% numerical tolerance,
and a request for three significant figures. Turn counts are exact integers;
measured givens are displayed to three significant figures. Answers are positive
scalar values in microteslas. Units are not included in the machine-readable
answer field.

| Placement family | Questions | Count |
| --- | --- | ---: |
| Wire parallel to the coil axis | q001–q012 | 12 |
| Perpendicular wire shifted sideways at P's axial coordinate | q013–q036 | 24 |
| Perpendicular wire crossing the axis between the coil and P | q037–q060 | 24 |
| Perpendicular wire crossing the axis beyond P | q061–q084 | 24 |

There are 60 cases with perpendicular fields, 12 with parallel fields, and 12
with antiparallel fields. The coil is centered at the origin, P is on its positive
axis, and both current directions are included. Parallel wires use the next
positive transverse axis for their offset; sideways wires use the remaining
positive transverse axis. These are the 84 agreed configurations under those
placement conventions.

The number of turns, coil radius, currents, and distances vary. The wire-to-coil
field-magnitude ratio is between 0.599 and 1.61. Nearly cancelling antiparallel
fields are excluded. Net magnitudes range from 1.19 to 129 microteslas.

## Contents

- `PHY2-EM-B-BWC-10182026_QTI.zip`: converter-generated QTI import package,
  containing all 84 questions and all 168 images. Extract this inner ZIP from
  the complete bundle and select it when importing QTI into Canvas.
- `PHY2-EM-B-BWC-10182026.yaml`: questions, numerical grading data, and complete
  HTML/MathJax worked solutions.
- `PHY2-EM-B-BWC-10182026-Figures/`: 84 question PNGs and 84 feedback PNGs.
- `answer_key.csv`: three-significant-figure results, source fields and
  directions, unrounded net values, and grading bounds.
- `configurations.json`: all source geometries, currents, and camera settings
  in SI units.
- `alt_text.json`: separate plain descriptions for question and feedback images.
- `science_validation.json`: independent Biot–Savart checks for all 84 questions.
- `validation_report.json`: complete YAML/HTML/MathJax/media/converter check report.
- `validation_summary.json`: concise check results and grouped converter warnings.
- `qti_package_validation.json`: checks performed on the delivered QTI ZIP,
  including its manifest, media bytes, MathJax content, scoring, and tolerance.
- `source/`: reproducible bank and figure generators, with dependencies.

The attached source templates were used for the bank structure. Presentation
fields follow the agreed HTML and MathJax format, using literal YAML blocks and
`\(...\)` or `\[...\]` delimiters.

## Solutions and figures

Each solution gives the geometry and SI conversions, the coil's axial-field
formula, the wire's field formula, source-field vectors, and vector addition.
The wire-field cross product is followed by the alternative right-hand rule:
point the right thumb along the current, curl the fingers around the wire, and
state the resulting field direction at P for that particular configuration.

Question images contain source geometry and current directions. Feedback images
add the two labeled field arrows at P, with source colors. Sources are faded to
15% opacity in feedback. Field-arrow lengths are schematic. The question images
contain no field-direction overlays or answers. Each image has descriptive alt
text; the two fields also have distinct source labels.

The accepted figure conventions are preserved: no rho label, no O label, nearby
P/Q labels, Ic below the coil-current arrow, R interrupting the radius arrow,
axis labels beyond arrowheads, and a dashed PQ segment only when it does not
coincide with an axis.

## Converter compatibility

Inspected repository: [omoussa/yaml-to-qti](https://github.com/omoussa/yaml-to-qti/),
revision `0b1cfc0636e3b5422119b35780916afa3220ef87`.

Question and feedback images are embedded in complete HTML `<div>` blocks using
the converter's packaged-media path:
`$IMS-CC-FILEBASE$/media/mag_001.png`, for example. During conversion, supply the
entire `PHY2-EM-B-BWC-10182026-Figures` folder as the media directory. The question
image is already in the question's HTML; there is no additional `figure` field.

The YAML, HTML fragments, MathJax content, and all 168 image files passed
validation. A disposable QTI conversion preserved the equations and images.
Every exported numerical interval was checked to equal the stated answer plus
or minus 2%, and every numerical score was checked to equal 1 point.

The inspected converter produces four warnings for each numerical question:

- General feedback containing HTML is marked `text/plain`.
- General feedback has no `displayfeedback` link.
- A generated feedback link targets a missing `correct` node.
- `points_possible` metadata is omitted, although numerical scoring uses 1 point.

The YAML and the delivered QTI retain the full solutions and images. These
converter issues should be addressed or checked when importing, especially
whether the general feedback is displayed. The converter was not modified.
No Canvas import was performed.

The QTI ZIP was generated with the converter's `app.create_imscc.main`, using
the YAML and the full Figures directory. The delivered ZIP passed archive and
manifest checks. Its 168 packaged PNGs are byte-for-byte identical to the
supplied figures; all equations and MathJax delimiters were preserved. Actual
QTI grading bounds and numerical scores were checked for every question.

## Scientific validation

All 84 analytical source-field vectors and their net magnitudes were checked
against independent numerical integration of the Biot–Savart law, integrating
the circular current path and the infinite straight-wire path directly. The
maximum relative difference was below 4 × 10⁻¹⁵. Topology/sign coverage, geometric
constraints, field relationships, and current reversal were also checked.

The answers use the explicitly supplied classroom value
`mu_0 = 4*pi*10^-7 T m/A`. Calculations retain full intermediate precision;
feedback displays intermediate and final results to three significant figures.
Percentage grading bounds are centered on the three-significant-figure answer.

## Rebuild

Use Python 3.10 or newer:

```bash
python -m pip install -r source/requirements.txt
python source/generate_bank.py
```

This recreates the YAML, numerical answer key, geometry data, scientific checks,
and 168 PNGs with random seed `10182026`. It preserves an existing bank's
creation date. To rebuild text and grading data while keeping existing images:

```bash
python source/generate_bank.py --no-render
```

The figure generator also supports SVG and PDF export and an adjustable
`--feedback-source-alpha` argument. The bank-generation script uses 0.15 for the
feedback source opacity. YAML/QTI validation reports describe the checks run
during this delivery; rerun the validation workflow after making later changes.
