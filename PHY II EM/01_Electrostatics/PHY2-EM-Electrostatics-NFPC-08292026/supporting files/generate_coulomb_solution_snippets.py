#!/usr/bin/env python3
"""Generate validated HTML solution strings for the 12 Coulomb-law scenarios."""

from __future__ import annotations

import math
from pathlib import Path

import yaml

from coulomb_problem_bank_diagrams import ELEMENTARY_CHARGE, SCENARIOS, Scenario


COULOMB_CONSTANT = 8.987_551_792_3e9
OUTPUT_PATH = Path(__file__).resolve().parent / "coulomb_solution_snippets.yaml"
UNIT_SCALE = {"nm": 1e-9, "um": 1e-6, "mm": 1e-3, "cm": 1e-2}
D_SI_TEX = {
    1: r"2.0\times10^{-8}\ \mathrm{m}",
    2: r"4.5\times10^{-8}\ \mathrm{m}",
    3: r"2.0\times10^{-6}\ \mathrm{m}",
    4: r"3.5\times10^{-5}\ \mathrm{m}",
    5: r"6.0\times10^{-4}\ \mathrm{m}",
    6: r"1.5\times10^{-3}\ \mathrm{m}",
    7: r"1.2\times10^{-2}\ \mathrm{m}",
    8: r"3.0\times10^{-2}\ \mathrm{m}",
    9: r"8.0\times10^{-3}\ \mathrm{m}",
    10: r"1.5\times10^{-2}\ \mathrm{m}",
    11: r"2.5\times10^{-2}\ \mathrm{m}",
    12: r"4.0\times10^{-2}\ \mathrm{m}",
}


class LiteralString(str):
    """Marker that tells PyYAML to emit a literal block scalar."""


def represent_literal_string(dumper: yaml.SafeDumper, value: LiteralString):
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")


yaml.SafeDumper.add_representer(LiteralString, represent_literal_string)


def index(label: str) -> str:
    return label.removeprefix("q")


def signed_number(value: float, decimals: int | None = None) -> str:
    if decimals is None:
        body = str(int(round(abs(value))))
    else:
        body = f"{abs(value):.{decimals}f}"
    return ("+" if value >= 0 else "-") + body


def charge_tex(scenario: Scenario, label: str) -> str:
    value = next(q for name, q, _xy in scenario.charges if name == label)
    if scenario.number <= 4:
        return signed_number(value / ELEMENTARY_CHARGE) + "e"
    if scenario.number <= 8:
        return signed_number(value / 1e-9) + r"\ \mathrm{nC}"
    return signed_number(value / 1e-6, decimals=1) + r"\ \mu\mathrm{C}"


def charge_si_tex(value: float) -> str:
    return scientific_tex(value, 3) + r"\ \mathrm{C}"


def d_in_meters(scenario: Scenario) -> float:
    value_text, unit = scenario.d_label.split()
    return float(value_text) * UNIT_SCALE[unit]


def scientific_tex(value: float, significant_digits: int) -> str:
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    exponent = math.floor(math.log10(magnitude))
    mantissa = magnitude / (10**exponent)
    decimals = max(significant_digits - 1, 0)
    rounded = round(mantissa, decimals)
    if rounded >= 10:
        rounded /= 10
        exponent += 1
    mantissa_text = f"{rounded:.{decimals}f}"
    return rf"{sign}{mantissa_text}\times10^{{{exponent}}}"


def d_display_tex(scenario: Scenario) -> str:
    value, unit = scenario.d_label.split()
    if unit == "um":
        unit_tex = r"\mu\mathrm{m}"
    else:
        unit_tex = rf"\mathrm{{{unit}}}"
    return rf"{value}\ {unit_tex}"


def displacement_tex(dx: int, dy: int) -> str:
    terms: list[tuple[int, str]] = []
    if dx:
        terms.append((dx, r"d\hat{i}"))
    if dy:
        terms.append((dy, r"d\hat{j}"))
    return join_integer_terms(terms)


def join_integer_terms(terms: list[tuple[int, str]]) -> str:
    pieces: list[str] = []
    for coefficient, symbol in terms:
        magnitude = abs(coefficient)
        term = symbol if magnitude == 1 else f"{magnitude}{symbol}"
        if not pieces:
            pieces.append(("-" if coefficient < 0 else "") + term)
        else:
            pieces.append((" - " if coefficient < 0 else " + ") + term)
    return "".join(pieces) if pieces else "0"


def unit_vector_tex(dx: int, dy: int, multiplier: int = 1) -> str:
    dx *= multiplier
    dy *= multiplier
    norm_squared = dx * dx + dy * dy
    root = math.isqrt(norm_squared)

    def coefficient_tex(component: int) -> str:
        magnitude = abs(component)
        if root * root == norm_squared:
            denominator = root
            divisor = math.gcd(magnitude, denominator)
            numerator = magnitude // divisor
            denominator //= divisor
            if denominator == 1:
                return "" if numerator == 1 else str(numerator)
            numerator_text = "1" if numerator == 1 else str(numerator)
            return rf"\frac{{{numerator_text}}}{{{denominator}}}"
        numerator_text = "1" if magnitude == 1 else str(magnitude)
        return rf"\frac{{{numerator_text}}}{{\sqrt{{{norm_squared}}}}}"

    pieces: list[str] = []
    for component, axis in ((dx, "i"), (dy, "j")):
        if component == 0:
            continue
        body = coefficient_tex(component) + rf"\hat{{{axis}}}"
        if not pieces:
            pieces.append(("-" if component < 0 else "") + body)
        else:
            pieces.append((" - " if component < 0 else " + ") + body)
    return "".join(pieces)


def numeric_vector_tex(x_component: float, y_component: float, sig: int = 3) -> str:
    reference = max(abs(x_component), abs(y_component), 1e-300)
    tolerance = reference * 1e-12
    components: list[tuple[float, str]] = []
    if abs(x_component) > tolerance:
        components.append((x_component, "i"))
    if abs(y_component) > tolerance:
        components.append((y_component, "j"))
    if not components:
        return r"0\ \mathrm{N}"

    pieces: list[str] = []
    for value, axis in components:
        magnitude_text = scientific_tex(abs(value), sig)
        body = rf"{magnitude_text}\hat{{{axis}}}"
        if not pieces:
            pieces.append(("-" if value < 0 else "") + body)
        else:
            pieces.append((" - " if value < 0 else " + ") + body)
    return rf"\left({''.join(pieces)}\right)\ \mathrm{{N}}"


def force_data(scenario: Scenario, source: str) -> dict[str, object]:
    by_label = {label: (q, xy) for label, q, xy in scenario.charges}
    target = scenario.target
    q_source, source_xy = by_label[source]
    q_target, target_xy = by_label[target]
    dx = target_xy[0] - source_xy[0]
    dy = target_xy[1] - source_xy[1]
    n = dx * dx + dy * dy
    distance = math.sqrt(n) * d_in_meters(scenario)
    scalar = COULOMB_CONSTANT * q_source * q_target / distance**2
    unit_x = dx / math.sqrt(n)
    unit_y = dy / math.sqrt(n)
    force_x = scalar * unit_x
    force_y = scalar * unit_y
    return {
        "source": source,
        "target": target,
        "q_source": q_source,
        "q_target": q_target,
        "dx": dx,
        "dy": dy,
        "n": n,
        "force_x": force_x,
        "force_y": force_y,
        "magnitude": math.hypot(force_x, force_y),
        "product_sign": 1 if q_source * q_target > 0 else -1,
    }


def force_name(data: dict[str, object], vector: bool = True) -> str:
    prefix = r"\vec{F}" if vector else "F"
    return rf"{prefix}_{{q_{index(str(data['source']))}\text{{ on }}q_{index(str(data['target']))}}}"


def conversion_paragraph(scenario: Scenario) -> str:
    d_si = D_SI_TEX[scenario.number]
    if scenario.number <= 4:
        return (
            '<p>For numerical evaluation, use '
            r"\(k=8.99\times10^9\ \mathrm{N\,m^2/C^2}\), "
            r"\(e=1.602\times10^{-19}\ \mathrm{C}\), and "
            rf"\(d={d_si}\).</p>"
        )

    conversions = []
    for label, value, _xy in scenario.charges:
        conversions.append(rf"q_{index(label)}={charge_si_tex(value)}")
    joined = r",\quad ".join(conversions)
    return (
        '<p>For numerical evaluation, use '
        r"\(k=8.99\times10^9\ \mathrm{N\,m^2/C^2}\) and convert all quantities to SI units: "
        rf"\({joined},\quad d={d_si}\).</p>"
    )


def force_section(scenario: Scenario, data: dict[str, object], introductory: str) -> str:
    source = str(data["source"])
    target = str(data["target"])
    source_i = index(source)
    target_i = index(target)
    dx = int(data["dx"])
    dy = int(data["dy"])
    n = int(data["n"])
    sign = int(data["product_sign"])
    relationship = "repel" if sign > 0 else "attract"
    direction_relation = "along" if sign > 0 else "opposite"
    distance_squared = "d^2" if n == 1 else rf"{n}d^2"
    vector_name = force_name(data)
    source_q = charge_tex(scenario, source)
    target_q = charge_tex(scenario, target)
    numeric_vector = numeric_vector_tex(float(data["force_x"]), float(data["force_y"]))

    return rf"""<p><strong>{introductory} the force of \(q_{source_i}\) on \(q_{target_i}\):</strong></p>
<p style="padding-left: 40px;">The displacement from source \(q_{source_i}\) to target \(q_{target_i}\) is \(\vec{{r}}_{{{source_i}{target_i}}}={displacement_tex(dx, dy)}\), so \(r_{{{source_i}{target_i}}}^2={distance_squared}\) and \(\hat{{r}}_{{{source_i}{target_i}}}={unit_vector_tex(dx, dy)}\).</p>
<p style="padding-left: 40px;">\(\begin{{aligned}}
{vector_name}&amp;=k\frac{{q_{source_i}q_{target_i}}}{{r_{{{source_i}{target_i}}}^2}}\hat{{r}}_{{{source_i}{target_i}}}\\
&amp;=k\frac{{({source_q})({target_q})}}{{{distance_squared}}}\left({unit_vector_tex(dx, dy)}\right)\\
&amp;={numeric_vector}
\end{{aligned}}\)</p>
<p style="padding-left: 40px;">Because \(q_{source_i}q_{target_i}\) is {'positive' if sign > 0 else 'negative'}, the charges {relationship}; therefore, the force is {direction_relation} \(\hat{{r}}_{{{source_i}{target_i}}}\).</p>"""


def option_two_force_paragraph(data: dict[str, object]) -> str:
    source_i = index(str(data["source"]))
    target_i = index(str(data["target"]))
    n = int(data["n"])
    sign = int(data["product_sign"])
    distance_squared = "d^2" if n == 1 else rf"{n}d^2"
    direction = unit_vector_tex(int(data["dx"]), int(data["dy"]), multiplier=sign)
    relationship = "repulsion" if sign > 0 else "attraction"
    magnitude = scientific_tex(float(data["magnitude"]), 3)
    scalar_name = force_name(data, vector=False)
    return (
        rf"<p>The force of \(q_{source_i}\) on \(q_{target_i}\) has magnitude "
        rf"\({scalar_name}=k\frac{{\left|q_{source_i}q_{target_i}\right|}}{{{distance_squared}}}"
        rf"={magnitude}\ \mathrm{{N}}\). Its direction is \({direction}\) because of {relationship}.</p>"
    )


def build_solution(scenario: Scenario) -> str:
    target_i = index(scenario.target)
    sources = sorted(label for label, _q, _xy in scenario.charges if label != scenario.target)
    first = force_data(scenario, sources[0])
    second = force_data(scenario, sources[1])

    net_x = float(first["force_x"]) + float(second["force_x"])
    net_y = float(first["force_y"]) + float(second["force_y"])
    net_magnitude = math.hypot(net_x, net_y)
    angle = math.degrees(math.atan2(net_y, net_x)) % 360

    first_vector = numeric_vector_tex(float(first["force_x"]), float(first["force_y"]))
    second_vector = numeric_vector_tex(float(second["force_x"]), float(second["force_y"]))
    net_vector = numeric_vector_tex(net_x, net_y)
    magnitude_tex = scientific_tex(net_magnitude, 2)
    x_tex = scientific_tex(net_x, 3)
    y_tex = scientific_tex(net_y, 3)

    return rf"""<h4><span style="text-decoration: underline;">Option 1: Use the vector equation for electrostatic force (recommended).</span></h4>
<p><strong>First, calculate the contribution from each source charge acting on \(q_{target_i}\).</strong></p>
{conversion_paragraph(scenario)}
{force_section(scenario, first, 'First, calculate')}
{force_section(scenario, second, 'Similarly, calculate')}
<p><strong>Now combine both contributions by adding the \(\hat{{i}}\) and \(\hat{{j}}\) components separately:</strong></p>
<p style="padding-left: 40px;">\(\begin{{aligned}}
\sum\vec{{F}}_{{\text{{on }}q_{target_i}}}&amp;={force_name(first)}+{force_name(second)}\\
&amp;={first_vector}+{second_vector}\\
&amp;={net_vector}
\end{{aligned}}\)</p>
<p><strong>Find the magnitude and direction of the resulting vector:</strong></p>
<p style="padding-left: 40px;">\(\begin{{aligned}}
\left|\sum\vec{{F}}_{{\text{{on }}q_{target_i}}}\right|&amp;=\sqrt{{F_x^2+F_y^2}}\\
&amp;=\sqrt{{\left({x_tex}\right)^2+\left({y_tex}\right)^2}}\\
&amp;=\boxed{{{magnitude_tex}\ \mathrm{{N}}}}
\end{{aligned}}\)</p>
<p style="padding-left: 40px;">Using \(\operatorname{{atan2}}(F_y,F_x)\) to select the correct quadrant, \(\theta={angle:.1f}^\circ\), measured counterclockwise from the \(+x\)-axis.</p>
<hr />
<h4><span style="text-decoration: underline;">Option 2: Find each magnitude and direction separately.</span></h4>
<p>Calculate the magnitude of each source-charge force with Coulomb's law, determine its direction from attraction or repulsion, and then add the forces as vectors.</p>
{option_two_force_paragraph(first)}
{option_two_force_paragraph(second)}
<p>Resolve these forces into components and add the x-components and y-components separately. This gives \(\sum\vec{{F}}_{{\text{{on }}q_{target_i}}}={net_vector}\), with magnitude \(\boxed{{{magnitude_tex}\ \mathrm{{N}}}}\) and direction \({angle:.1f}^\circ\) counterclockwise from the \(+x\)-axis.</p>
<hr />
"""


def validate_solution(scenario: Scenario, html: str) -> None:
    if html.count("<h4>") != 2 or html.count("</h4>") != 2:
        raise ValueError(f"Scenario {scenario.number}: heading mismatch")
    if html.count("<p") != html.count("</p>"):
        raise ValueError(f"Scenario {scenario.number}: paragraph mismatch")
    if html.count(r"\(") != html.count(r"\)"):
        raise ValueError(f"Scenario {scenario.number}: math delimiter mismatch")
    if "\\vec{F}" not in html or "\\boxed{" not in html:
        raise ValueError(f"Scenario {scenario.number}: required solution content missing")


def main() -> None:
    entries = []
    for scenario in SCENARIOS:
        solution = build_solution(scenario)
        validate_solution(scenario, solution)
        entries.append({"id": f"q{scenario.number}", "html": LiteralString(solution)})

    payload = {"solution_snippets": entries}
    rendered = yaml.safe_dump(
        payload,
        sort_keys=False,
        allow_unicode=True,
        width=10_000,
    )
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"Created {len(entries)} solution snippets: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
