#!/usr/bin/env python3
"""Rebuild the 84-question wire/coil numerical bank and its paired figures."""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import asdict, replace
from datetime import datetime
from html import escape
import json
import math
from pathlib import Path
import random
from zoneinfo import ZoneInfo

import numpy as np
from scipy.integrate import quad_vec
import yaml

import magnetic_source_figures as fig

BANK_ID = "PHY2-EM-B-BWC-10182026"
TITLE = "Magnetic Fields from a Straight Wire and a Circular Coil"
CONVERTER_REVISION = "0b1cfc0636e3b5422119b35780916afa3220ef87"
SEED = 10182026
MU0 = 4 * math.pi * 1e-7
UNITS = (r"\hat{\mathbf{i}}", r"\hat{\mathbf{j}}", r"\hat{\mathbf{k}}")


class Literal(str):
    pass


class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


Dumper.add_representer(Literal, lambda d, v: d.represent_scalar("tag:yaml.org,2002:str", v, style="|"))


def sig(value: float, digits: int = 3) -> str:
    """Fixed decimal notation with exactly the requested significant digits."""
    if value == 0:
        return "0"
    places = digits - 1 - math.floor(math.log10(abs(value)))
    return f"{value:.{max(0, places)}f}"


def math_inline(content: str) -> str:
    return r"\(" + content + r"\)"


def equation(content: str) -> str:
    return r"<div>\[" + content + r"\]</div>"


def paragraph(content: str) -> str:
    return "<p>" + content + "</p>"


def coordinate(values, factor=100) -> str:
    return r"\left(" + r",\ ".join(sig(float(v) * factor) for v in values) + r"\right)"


def unit(vector) -> str:
    i = int(np.argmax(np.abs(vector)))
    return ("-" if vector[i] < 0 else "") + UNITS[i]


def direction(vector) -> str:
    i = int(np.argmax(np.abs(vector)))
    return ("-" if vector[i] < 0 else "+") + fig.AXES[i]


def direction_prose(vector) -> str:
    i = int(np.argmax(np.abs(vector)))
    return ("negative" if vector[i] < 0 else "positive") + "-" + math_inline(fig.AXES[i]) + " direction"


def vector_expression(vector) -> str:
    parts = []
    for i, val in enumerate(vector):
        if abs(val) < 1e-10:
            continue
        sign = "-" if val < 0 else ("+" if parts else "")
        parts.append(sign + sig(abs(float(val))) + r"\," + UNITS[i])
    return " ".join(parts) or "0"


def fields(cfg):
    g = fig.validate_config(cfg)
    a = float(np.linalg.norm(cfg.observation))
    bc = MU0 * cfg.coil_turns * cfg.coil_current * cfg.coil_radius**2 / (2 * (cfg.coil_radius**2 + a*a)**1.5)
    bw = MU0 * cfg.wire_current / (2 * math.pi * g["rho"])
    vc = bc * g["coil_direction"]
    vw = bw * g["wire_direction"]
    return g, bc, bw, vc, vw, float(np.linalg.norm(vc + vw))


def configurations():
    """Keep each agreed topology/sign combination; vary only numerical givens."""
    rng = random.Random(SEED)
    result = []
    for template in fig.enumerate_84():
        k, j = fig.AXES.index(template.coil_axis), fig.AXES.index(template.wire_axis)
        for _ in range(10000):
            r_cm = rng.choice([4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9])
            a_cm = rng.choice(list(range(7, 17)))
            if not 0.9 <= a_cm / r_cm <= 2.3:
                continue
            lateral_cm = rng.choice([3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])
            p = a_cm / 100 * fig.UNIT[k]
            if template.family == "parallel":
                if lateral_cm == r_cm:
                    continue
                q = p + lateral_cm / 100 * fig.UNIT[(k + 1) % 3]
            elif template.family == "sideways":
                q = p + lateral_cm / 100 * fig.UNIT[3 - k - j]
            elif template.family == "crossing_near":
                q = round(a_cm * rng.choice([0.4, 0.5, 0.6]), 2) / 100 * fig.UNIT[k]
            else:
                q = (a_cm + rng.choice([3, 4, 5, 6, 7, 8])) / 100 * fig.UNIT[k]
            n = rng.choice([12, 15, 16, 18, 20, 24, 25, 28, 30, 32, 36, 40])
            ic = rng.choice([0.180, 0.200, 0.240, 0.250, 0.300, 0.320, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.750, 0.800])
            candidate = replace(template, coil_radius=r_cm / 100, coil_turns=n,
                                coil_current=ic, observation=tuple(p), wire_point=tuple(q))
            g, bc, *_ = fields(candidate)
            ratio = rng.choice([0.600, 0.700, 0.800, 1.25, 1.40, 1.60])
            iw = float(f"{bc * ratio * 2 * math.pi * g['rho'] / MU0:.3g}")
            if not 0.500 <= iw <= 18.0:
                continue
            candidate = replace(candidate, wire_current=iw)
            g, bc, bw, vc, vw, bn = fields(candidate)
            if not 0.59 <= bw / bc <= 1.61:
                continue
            if not 3e-6 <= bc <= 100e-6 or not 0.18 * max(bc, bw) <= bn:
                continue
            result.append(candidate)
            break
        else:
            raise RuntimeError("No suitable numeric values for " + template.identifier)
    fig.validate_bank(result)
    return result


def question_head(cfg):
    k = fig.AXES.index(cfg.coil_axis)
    plane = "".join(fig.AXES[i] for i in range(3) if i != k)
    sense = "counterclockwise" if cfg.coil_sense == "ccw" else "clockwise"
    g = fig.source_geometry(cfg)
    a = paragraph(
        "A thin circular coil of " + math_inline(f"N={cfg.coil_turns}") + " turns and radius "
        + math_inline(f"R={sig(100 * cfg.coil_radius)}" + r"\ \mathrm{cm}")
        + " is centered at the origin and lies in the " + math_inline(plane) + " plane. "
        + "It carries a current of " + math_inline(f"I_c={sig(cfg.coil_current)}" + r"\ \mathrm{A}")
        + ", flowing " + sense + " when viewed from the positive " + math_inline(cfg.coil_axis)
        + " axis toward the origin. Model the coil as " + math_inline("N") + " coincident circular turns.")
    b = paragraph(
        "A long straight wire is parallel to the " + math_inline(cfg.wire_axis)
        + " axis and passes through " + math_inline("Q=" + coordinate(g["foot"]) + r"\ \mathrm{cm}")
        + ". It carries a current of " + math_inline("I_w=" + sig(cfg.wire_current) + r"\ \mathrm{A}")
        + " in the " + math_inline(direction(cfg.wire_sign * fig.UNIT[fig.AXES.index(cfg.wire_axis)]))
        + " direction. The wire is sufficiently long that end effects can be neglected.")
    c = paragraph(
        "The observation point is " + math_inline("P=" + coordinate(cfg.observation) + r"\ \mathrm{cm}")
        + ". <strong>Find the magnitude of the net magnetic field at " + math_inline("P")
        + ", in microteslas " + math_inline(r"(\mu\mathrm{T})") + ".</strong> Report your answer to three significant figures.")
    d = paragraph("Use " + math_inline(r"\mu_0=4\pi\times10^{-7}\ \mathrm{T\,m/A}")
                  + " and " + math_inline(r"1\ \mu\mathrm{T}=10^{-6}\ \mathrm{T}") + ".")
    image = ('<div><img src="$IMS-CC-FILEBASE$/media/' + cfg.identifier + '.png" alt="'
             + escape(fig.alt_text(cfg), quote=True)
             + '" width="740" style="max-width:100%;height:auto;" /></div>')
    return Literal("\n".join([a, b, c, d, image]))


def solution(cfg):
    g, bc, bw, vc, vw, bn = fields(cfg)
    bc_u, bw_u, bn_u = bc * 1e6, bw * 1e6, bn * 1e6
    k, j = fig.AXES.index(cfg.coil_axis), fig.AXES.index(cfg.wire_axis)
    a, rho = float(np.linalg.norm(cfg.observation)), g["rho"]
    tangent = cfg.wire_sign * fig.UNIT[j]
    radial = g["radial"] / rho
    out = ["<h3>1. Geometry and superposition</h3>", paragraph(
        "The requested quantity is the scalar magnitude " + math_inline(r"B_{\mathrm{net}}=|\vec B_c+\vec B_w|")
        + ". Let " + math_inline("a") + " be the distance from the coil center to " + math_inline("P")
        + " along its axis, and let " + math_inline(r"\rho=|\overrightarrow{QP}|")
        + " be the shortest distance from the wire to " + math_inline("P") + ". Convert distances to meters before substitution.")]
    givens = [
        ("Number of turns", "N", str(cfg.coil_turns) + r"\text{ (exact)}"),
        ("Coil current", "I_c", sig(cfg.coil_current) + r"\ \mathrm{A}"),
        ("Wire current", "I_w", sig(cfg.wire_current) + r"\ \mathrm{A}"),
        ("Coil radius", "R", sig(cfg.coil_radius * 100) + r"\ \mathrm{cm}=" + sig(cfg.coil_radius) + r"\ \mathrm{m}"),
        ("Axial distance", "a", sig(a * 100) + r"\ \mathrm{cm}=" + sig(a) + r"\ \mathrm{m}"),
        ("Distance to wire", r"\rho", sig(rho * 100) + r"\ \mathrm{cm}=" + sig(rho) + r"\ \mathrm{m}"),
    ]
    th = ' style="border:1px solid #777;padding:5px;"'
    out.append('<table style="border-collapse:collapse;"><thead><tr>' + ''.join('<th scope="col"' + th + '>' + v + '</th>' for v in ("Quantity", "Symbol", "Value")) + '</tr></thead><tbody>')
    for name, symbol, value in givens:
        out.append('<tr><th scope="row"' + th + '>' + name + '</th><td' + th + '>' + math_inline(symbol) + '</td><td' + th + '>' + math_inline(value) + '</td></tr>')
    out.append('</tbody></table>')
    out.append(equation(r"\overrightarrow{QP}=\vec r_P-\vec r_Q=" + coordinate(g["radial"]) + r"\ \mathrm{cm},\qquad \rho=" + sig(rho) + r"\ \mathrm{m}."))
    out.extend(["<h3>2. Magnetic field of the circular coil</h3>", paragraph(
        "At a point on the axis of a circular " + math_inline("N") + "-turn coil, the field magnitude is"),
        equation(r"B_c=\frac{\mu_0NI_cR^2}{2(R^2+a^2)^{3/2}}."),
        equation(r"B_c=\frac{(4\pi\times10^{-7}\ \mathrm{T\,m/A})(" + str(cfg.coil_turns)
                 + ")(" + sig(cfg.coil_current) + r"\ \mathrm{A})(" + sig(cfg.coil_radius)
                 + r"\ \mathrm{m})^2}{2\left[(" + sig(cfg.coil_radius) + r"\ \mathrm{m})^2+("
                 + sig(a) + r"\ \mathrm{m})^2\right]^{3/2}}=" + sig(bc_u) + r"\ \mu\mathrm{T}."),
        paragraph("Curl the fingers of your right hand in the direction of the coil current. Your thumb points along "
                  + math_inline(direction(g["coil_direction"])) + ", so the coil field at " + math_inline("P")
                  + " is in the " + direction_prose(g["coil_direction"]) + "."),
        equation(r"\vec B_c=\left(" + vector_expression(vc * 1e6) + r"\right)\ \mu\mathrm{T}."),
        "<h3>3. Magnetic field of the straight wire</h3>",
        paragraph("Let " + math_inline(r"\hat\ell_w") + " point along the wire current, and let "
                  + math_inline(r"\hat r_\perp") + " point from the wire toward " + math_inline("P") + ". The direction follows the cross product"),
        equation(r"\hat\ell_w=" + unit(tangent) + r",\qquad \hat r_\perp=" + unit(radial)
                 + r",\qquad \hat b_w=\hat\ell_w\times\hat r_\perp=(" + unit(tangent)
                 + r")\times(" + unit(radial) + ")=" + unit(g["wire_direction"]) + "."),
        paragraph("Alternatively, use the <strong>right-hand rule</strong>: line up your right thumb with the current, in the "
                  + math_inline(direction(tangent)) + " direction. Your remaining fingers curl around the wire in the direction of its magnetic field. At "
                  + math_inline("P") + ", which lies in the " + math_inline(direction(radial)) + " direction from "
                  + math_inline("Q") + ", your curled fingers point in the " + direction_prose(g["wire_direction"]) + "."),
        paragraph("For a long straight wire, the field magnitude is"),
        equation(r"B_w=\frac{\mu_0I_w}{2\pi\rho}."),
        equation(r"B_w=\frac{(4\pi\times10^{-7}\ \mathrm{T\,m/A})(" + sig(cfg.wire_current)
                 + r"\ \mathrm{A})}{2\pi(" + sig(rho) + r"\ \mathrm{m})}=" + sig(bw_u) + r"\ \mu\mathrm{T}."),
        equation(r"\vec B_w=\left(" + vector_expression(vw * 1e6) + r"\right)\ \mu\mathrm{T}."),
        "<h3>4. Add the fields as vectors</h3>",
        paragraph("The arrows below show directions only; their lengths do not represent relative field magnitudes."),
        '<div><img src="$IMS-CC-FILEBASE$/media/' + cfg.identifier + '_feedback.png" alt="'
        + escape(fig.alt_text(cfg, with_fields=True), quote=True) + '" width="740" style="max-width:100%;height:auto;" /></div>',
        equation(r"\vec B_{\mathrm{net}}=\vec B_c+\vec B_w=\left(" + vector_expression((vc + vw) * 1e6) + r"\right)\ \mu\mathrm{T}."),
    ])
    if g["relationship"] == "parallel":
        out.append(paragraph("The two fields point in the same direction, so their magnitudes add."))
        out.append(equation(r"B_{\mathrm{net}}=B_c+B_w=(" + sig(bc_u) + "+" + sig(bw_u) + r")\ \mu\mathrm{T}."))
    elif g["relationship"] == "antiparallel":
        out.append(paragraph("The fields point in opposite directions. The magnitude of their vector sum is the absolute difference of their magnitudes."))
        out.append(equation(r"B_{\mathrm{net}}=|B_c-B_w|=|" + sig(bc_u) + "-" + sig(bw_u) + r"|\ \mu\mathrm{T}."))
    else:
        out.append(paragraph("The two fields are perpendicular, so use the Pythagorean theorem for the magnitude."))
        out.append(equation(r"B_{\mathrm{net}}=\sqrt{B_c^2+B_w^2}=\sqrt{(" + sig(bc_u)
                            + r")^2+(" + sig(bw_u) + r")^2}\ \mu\mathrm{T}."))
    out.append(paragraph("Keep extra digits during the calculation; intermediate values above are rounded for display. The result to three significant figures is"))
    out.append(equation(r"\boxed{B_{\mathrm{net}}=" + sig(bn_u) + r"\ \mu\mathrm{T}}."))
    return Literal("\n".join(out))


def independent_field_check(cfg):
    """Integrate Biot-Savart directly, independent of the axial field formulas."""
    p = np.asarray(cfg.observation)
    k, j = fig.AXES.index(cfg.coil_axis), fig.AXES.index(cfg.wire_axis)
    # Explicit right-handed loop bases; derivative is with respect to angle.
    pairs = (([0, 1, 0], [0, 0, 1]), ([0, 0, 1], [1, 0, 0]), ([1, 0, 0], [0, 1, 0]))
    u, v = (np.array(x) for x in pairs[k])
    sense = 1 if cfg.coil_sense == "ccw" else -1
    def coil_integrand(theta):
        pos = cfg.coil_radius * (math.cos(theta) * u + math.sin(theta) * v)
        dl = sense * cfg.coil_radius * (-math.sin(theta) * u + math.cos(theta) * v)
        displacement = p - pos
        return np.cross(dl, displacement) / np.linalg.norm(displacement)**3
    bcoil, _ = quad_vec(coil_integrand, 0, 2 * math.pi, epsabs=1e-10, epsrel=1e-10)
    bcoil *= MU0 * cfg.coil_turns * cfg.coil_current / (4 * math.pi)
    axis = np.eye(3)[j]
    q = np.asarray(cfg.wire_point)
    rho = np.linalg.norm(np.cross(p - q, axis))
    def wire_integrand(t):
        displacement = p - (q + rho * t * axis)
        dl = cfg.wire_sign * rho * axis
        return np.cross(dl, displacement) / np.linalg.norm(displacement)**3
    bwire, _ = quad_vec(wire_integrand, -np.inf, np.inf, epsabs=1e-10, epsrel=1e-10)
    bwire *= MU0 * cfg.wire_current / (4 * math.pi)
    _, bc, bw, vc, vw, bn = fields(cfg)
    ec = float(np.linalg.norm(bcoil - vc) / bc)
    ew = float(np.linalg.norm(bwire - vw) / bw)
    en = float(abs(np.linalg.norm(bcoil + bwire) - bn) / bn)
    if max(ec, ew, en) > 1e-8:
        raise AssertionError(f"Independent field integration mismatch for {cfg.identifier}: {ec, ew, en}")
    return dict(coil_relative_error=ec, wire_relative_error=ew, net_relative_error=en)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--no-render", action="store_true", help="Reuse the paired PNG files already rendered.")
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()
    root = args.output_dir.resolve()
    root.mkdir(parents=True, exist_ok=True)
    media_name = BANK_ID + "-Figures"
    media = root / media_name
    media.mkdir(exist_ok=True)
    configs = configurations()
    today = datetime.now(ZoneInfo("America/New_York")).strftime("%m-%d-%Y")
    bank_path = root / (BANK_ID + ".yaml")
    if bank_path.exists():
        today = yaml.safe_load(bank_path.read_text())["bank_info"]["date created"]
    bank = {"bank_info": {
        "title": TITLE, "bank_id": BANK_ID,
        "description": Literal("84 numerical problems finding the magnitude of the net magnetic field from a long straight wire and a circular N-turn coil. Answers are in microteslas, with 1 point per question and a 2% numerical tolerance."),
        "date created": today, "status": "draft", "learning objectives": ["EM-B-Bnet"],
        "generation prompts": [
            {"configurations": "Coil centered at origin; P on its positive axis. Include the 84 agreed major-axis placements, current senses, and wire-current directions: 12 parallel-source-axis, 24 sideways, 24 crossing-near, 24 crossing-far."},
            {"numerical values": "Vary currents, turns, radii, and distances; keep the source fields comparable. Give measured values and final results to three significant figures; use exact integer turn counts."},
            {"question and solution": "Ask only for the magnitude of the net field, in microteslas. Provide HTML and MathJax worked solutions with vectors, a cross product, and the right-thumb/current and curled-finger/field rule at P."},
            {"figures": "Preserve the accepted question-diagram conventions. Feedback vectors begin at P and match source colors; sources are faded to 15% opacity in feedback only."},
        ],
        "updates": [{"initial generation": today + ": O. Moussa's approved bank settings and diagram conventions."}],
        "associated data": [
            {"geometry and parameters": "configurations.json"}, {"answer key": "answer_key.csv"},
            {"bank generator": "source/generate_bank.py"}, {"figure generator": "source/magnetic_source_figures.py"},
            {"independent physics checks": "science_validation.json"}, {"YAML and converter checks": "validation_report.json"},
        ],
        "generation details": {"model": "Codex (GPT-6)", "generator version": "1.0.0", "last updated": today,
                               "random seed": SEED, "converter repository": "https://github.com/omoussa/yaml-to-qti",
                               "converter revision inspected": CONVERTER_REVISION,
                               "numerical method": "Analytical coil and wire fields checked independently against direct Biot-Savart quadrature."},
        "authors": ["O. Moussa"],
    }, "questions": []}
    rows, alt, errors = [], {}, []
    for i, cfg in enumerate(configs, 1):
        g, bc, bw, vc, vw, bn = fields(cfg)
        result = float(sig(bn * 1e6))
        assert result > 0 and abs(result / (bn * 1e6) - 1) < 0.005
        check = independent_field_check(cfg)
        errors.append({"id": f"q{i:03}", **check})
        bank["questions"].append({"numerical": {
            "id": f"q{i:03}", "title": f"{BANK_ID} - Problem {i:03}", "points": 1,
            "calculator": "scientific", "text": question_head(cfg),
            "answer": {"value": result, "margin_type": "percent", "tolerance": 2},
            "feedback": {"general": solution(cfg)},
        }})
        rows.append({"question_id": f"q{i:03}", "family": cfg.family, "coil_axis": cfg.coil_axis,
                     "coil_sense": cfg.coil_sense, "wire_axis": cfg.wire_axis, "wire_current_sign": cfg.wire_sign,
                     "turns": cfg.coil_turns, "radius_cm": sig(cfg.coil_radius * 100),
                     "axial_distance_cm": sig(np.linalg.norm(cfg.observation) * 100), "rho_cm": sig(g["rho"] * 100),
                     "coil_current_A": sig(cfg.coil_current), "wire_current_A": sig(cfg.wire_current),
                     "coil_field_microtesla": sig(bc * 1e6), "coil_field_direction": direction(g["coil_direction"]),
                     "wire_field_microtesla": sig(bw * 1e6), "wire_field_direction": direction(g["wire_direction"]),
                     "field_relationship": g["relationship"], "net_field_microtesla": sig(bn * 1e6),
                     "net_field_unrounded_microtesla": f"{bn * 1e6:.12g}",
                     "grading_lower_microtesla": f"{0.98 * result:.12g}", "grading_upper_microtesla": f"{1.02 * result:.12g}"})
        alt[cfg.identifier] = fig.alt_text(cfg)
        alt[cfg.identifier + "_feedback"] = fig.alt_text(cfg, with_fields=True)
        if not args.no_render:
            fig.draw_diagram(cfg, media / cfg.identifier, dpi=args.dpi, formats=("png",),
                             with_fields=True, feedback_source_alpha=0.15, show_title=False)
        if i % 12 == 0:
            print(f"Completed {i}/84 questions and independent physics checks.", flush=True)
    bank_path.write_text(yaml.dump(bank, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=115), encoding="utf-8")
    (root / "configurations.json").write_text(json.dumps([asdict(c) for c in configs], indent=2) + "\n")
    (root / "alt_text.json").write_text(json.dumps(alt, indent=2) + "\n")
    with (root / "answer_key.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    ratios = [float(fields(c)[2] / fields(c)[1]) for c in configs]
    science = {**fig.validate_bank(configs), "direct_Biot_Savart_checks": len(errors),
               "maximum_relative_integration_error": max(max(e[k] for k in ("coil_relative_error", "wire_relative_error", "net_relative_error")) for e in errors),
               "wire_to_coil_field_ratio_range": [min(ratios), max(ratios)],
               "minimum_nonzero_net_microtesla": min(float(r["net_field_microtesla"]) for r in rows),
               "maximum_net_microtesla": max(float(r["net_field_microtesla"]) for r in rows),
               "rounded_answers_within_requested_tolerance": True, "per_question_integration_checks": errors}
    (root / "science_validation.json").write_text(json.dumps(science, indent=2) + "\n")
    print(str(bank_path), flush=True)
    print(json.dumps({k: v for k, v in science.items() if k != "per_question_integration_checks"}), flush=True)


if __name__ == "__main__":
    main()
