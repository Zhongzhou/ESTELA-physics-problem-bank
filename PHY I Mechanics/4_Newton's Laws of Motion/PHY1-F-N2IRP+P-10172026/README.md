# Newton’s Second Law on Rough Inclines

Bank ID: PHY1-F-N2LI-10172026. Author: O. Moussa.
Learning objective: N2D. There are 24 multiple-choice questions worth 1 point each.

The bank contains 16 questions on inclines that rise to the right and 8 on
inclines that fall to the right. Falling-right cases include downhill motion
only. The question figures show geometry and axes; students infer acceleration
from the motion described in each question.

Each question’s general feedback includes a free-body diagram of A, axes
originating on A, and theta between the negative y direction and gravity.
A solid velocity arrow and a dashed acceleration arrow appear above A.
The feedback also gives force components and the correct vector equation.
The force-component tables have thin borders between cells. Explanations of
incorrect choices appear only in the feedback for the corresponding choice.

## Files and use

- PHY1-F-N2LI-10172026.yaml: final bank with HTML blocks and MathJax mathematics.
- PHY1-F-N2LI-10172026-QTI.zip: regenerated package for import into Canvas.
- media/: all 14 PNG assets (8 question figures and 6 feedback diagrams).
- inclined-plane-bank-review.md: portable full question and feedback review.
- inclined-plane-items.json: presentation fields, answer keys, and media mappings.
- Sources/: confirmed workflow input, settings, reusable Python scripts, and SVG figures.
- yaml-validation.json, content-validation.json, physics-validation.json, item-review.json, qti-package-verification.json, and conversion-provenance.json: validation, review, and converter information.

To import into Canvas, extract this bundle and select
PHY1-F-N2LI-10172026-QTI.zip as the QTI import file.

Keep the YAML and media folder together. When converting with yaml-to-qti,
provide the media folder as the figure/media directory. General-feedback
images use package references such as
`$IMS-CC-FILEBASE$/media/fbd-U-uphill-speeding-up.png`.
Retain the HTML and MathJax delimiters in all presentation fields.

## Validation

The YAML, presentation fields, and local media passed validation without
issues. The independent item review found no minor or major issues, including
after the final axes and angle revision. All 24 answer keys were checked by
evaluating the actual LaTeX choices under 72 physically possible two-body
parameter sets.

The QTI package was generated with the unmodified omoussa/yaml-to-qti
converter at revision 0b1cfc0636e3b5422119b35780916afa3220ef87. Its 24 answer
keys, feedback links, preserved HTML/MathJax, table borders, and 14 packaged
images were checked. A real Canvas import was not tested. After import,
verify the general-feedback rendering and one-point question values: the
converter labels general feedback as text/plain and omits points_possible metadata.

## Regenerate the bank

Use Python with matplotlib, numpy, Pillow, and PyYAML. From Sources, run:

    python draw_inclined_plane_bank.py
    python draw_inclined_plane_feedback.py
    python build_inclined_plane_bank.py --output ../regenerated --settings inclined-plane-bank-settings.yaml

The settings preserve the original bank metadata and revision history.
Review the physics if changing the supplied choices, answer keys, or variation rules.
