#!/usr/bin/env python3
"""Build the 24-item review; export YAML only with explicit bank settings."""
from __future__ import annotations

import argparse
from datetime import datetime
import html
import itertools
import json
from pathlib import Path
import re
import shutil
from zoneinfo import ZoneInfo

import yaml

from draw_inclined_plane_bank import state_signs

BASE = Path(__file__).resolve().parent
GLOSSARY = r"""Let \(T\) be the rope-tension magnitude, \(N\) the normal-force magnitude on A, \(g\) the magnitude of gravitational acceleration, and \(a_A>0\) the magnitude of A’s acceleration. The unit vectors \(\hat{\imath}\) and \(\hat{\jmath}\) point along the positive \(x\) and \(y\) axes shown in the figure."""
ASK = "Which equation correctly expresses Newton’s second law for object A in the coordinate system shown?"
CONTEXTS = {
    "U1": ("brass block", "block", "board", "In a physics laboratory, a brass block A of mass "+r"\(m_A\)"+" slides on a rough inclined board on a laboratory bench.", "steel weight", "upper", True),
    "U2": ("concrete paver", "paver", "panel", "At a building-materials testing station, a concrete paver A of mass "+r"\(m_A\)"+" slides on a rough test panel.", "bucket of gravel", "upper", True),
    "U3": ("felt-bottomed scenery block", "block", "platform", "In a theater workshop, a felt-bottomed scenery block A of mass "+r"\(m_A\)"+" slides on a rough sloping platform.", "stage counterweight", "upper", True),
    "D1": ("small packing crate", "crate", "ramp", "At a loading platform, a small packing crate A of mass "+r"\(m_A\)"+" slides on a rough loading ramp.", "sandbag", "lower", False),
    "D2": ("rubber specimen block", "block", "panel", "In a materials laboratory, a rubber specimen block A of mass "+r"\(m_A\)"+" slides on a rough test panel.", "weight pouch", "lower", False),
    "D3": ("wooden stage prop", "prop", "ramp", "In a theater workshop, a wooden stage prop A of mass "+r"\(m_A\)"+" slides on a rough scenic ramp above an open backstage pit.", "counterweight", "lower", False),
}


def inline(text):
    """Only the accepted bold emphasis is Markdown; preserve all MathJax."""
    chunks = re.split(r"(\*\*.*?\*\*)", text)
    return "".join("<strong>"+html.escape(x[2:-2])+"</strong>" if x.startswith("**") else html.escape(x) for x in chunks)


def paragraphs(text):
    return "\n".join("<p>"+inline(p)+"</p>" for p in text.split("\n\n"))


def display(equation):
    return "<div>\\["+html.escape(equation)+"\\]</div>"


def signed(value, term):
    return ("+" if value > 0 else "-")+term


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=BASE)
    parser.add_argument("--output", type=Path, default=BASE/"inclined-plane-bank")
    parser.add_argument("--settings", type=Path, help="Explicit user-confirmed settings; required for YAML export.")
    args = parser.parse_args()
    source, out = args.source_root.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    media = out/"media"
    media.mkdir(exist_ok=True)
    bank = yaml.safe_load((source/"input-inclined-plane-confirmed.mcq.yaml").read_text())
    samples = json.loads((source/"inclined-plane-sample-items.json").read_text())["items"]
    sample_by_scene = {("U0" if i["scenario"] == "scenario 1" else "D0"): i for i in samples}
    geometries = json.loads((source/"inclined-plane-figures/figure-manifest.json").read_text())["figures"]
    geometry_lookup = {(i["scenario"], i["scene_index"]): i for i in geometries}
    fbd_data = json.loads((source/"inclined-plane-feedback/feedback-figure-manifest.json").read_text())["figures"]
    fbd_lookup = {(i["scenario"], i["values"]["kinematic_state"]): i for i in fbd_data}
    for figure in geometries:
        shutil.copyfile(source/"inclined-plane-figures"/figure["figure"], media/Path(figure["figure"]).name)
    for figure in fbd_data:
        shutil.copyfile(source/"inclined-plane-feedback"/figure["figure"], media/Path(figure["figure"]).name)

    items = []
    markdown = [
        "# Newton’s Second Law on Rough Inclines: complete bank review", "",
        "The selected grid contains 24 conceptual multiple-choice questions. Every question has six choices. General feedback includes the free-body diagram of A, a solid velocity arrow, a dashed acceleration arrow, a bordered force-component table, and the correct vector equation. Feedback for each choice is listed separately.", "",
        "Question figures show only geometry and coordinate axes. Falling-right inclines include downhill motion only. Feedback diagrams place the axes on A and mark theta between negative y and gravity.", "",
    ]
    for scenario in bank["scenarios"]:
        sid = scenario["id"]
        rising = sid == "scenario 1"
        axes = bank["variation_axes"]["common"]+bank["variation_axes"]["by_scenario"][sid]
        for scene_index, scene in enumerate(scenario["scenes"]):
            if scene["status"] != "kept":
                continue
            scene_id = ("U" if rising else "D")+str(scene_index)
            geometry = geometry_lookup[(sid, scene_index)]
            geometry_alt = geometry["alt_text"].replace("a freely hanging hanging mass", "a freely hanging mass")
            if scene_id in sample_by_scene:
                context = sample_by_scene[scene_id]["stem_markdown"].split("\n\n")[0]
                short_noun = "crate" if rising else "block"
                surface = "ramp" if rising else "board"
                object_name = "Wooden crate" if rising else "Wooden block"
            else:
                object_name, short_noun, surface, opener, hanging, pulley_position, _ = CONTEXTS[scene_id]
                slope = "rises" if rising else "falls"
                relation = "above" if rising else "below"
                context = (
                    opener+" The "+surface+" "+slope+r" to the right at an angle \(\theta\) "+relation+" the horizontal. "
                    "A taut, massless, inextensible rope runs parallel to the "+surface+" from A, passes over a fixed, frictionless, massless pulley at the "
                    +pulley_position+" right end, and then runs vertically downward to a freely hanging "+hanging+r" B of mass \(m_B\)."
                )
                if not rising:
                    context += " The hanging rope and object B clear the "+surface+" and its support."
            for combination in itertools.product(*(a["values"] for a in axes)):
                values = dict(zip((a["id"] for a in axes), combination))
                state = values["kinematic_state"]
                velocity, acceleration = state_signs(sid, state)
                speeding = state.endswith("speeding_up")
                uphill = state.startswith("uphill")
                motion_word = "moving up" if uphill else "sliding down"
                speed_word = "speeding up" if speeding else "slowing down"
                motion_text = f"At the instant shown, the {short_noun} is {motion_word} the incline and {speed_word}."
                friction_sentence = f"The coefficient of kinetic friction between the {short_noun} and the {surface} is "+r"\(\mu_k\)."
                stem_md = context+"\n\n"+friction_sentence+" **"+motion_text+"** It remains in contact with the "+surface+"."
                stem_html = paragraphs(stem_md)+"\n"+paragraphs(GLOSSARY)+"\n<p><strong>"+ASK+"</strong></p>"
                gravity = -1 if rising else 1
                gx = signed(gravity, r"m_A g\sin\theta")
                fx = signed(-velocity, r"\mu_k N")
                normal = r"\left(N-m_A g\cos\theta\right)\hat{\jmath}"
                lhs = rf"\left(T{gx}{fx}\right)\hat{{\imath}}+{normal}"
                rhs = ("" if acceleration > 0 else "-")+r"m_A a_A\hat{\imath}"
                correct_equation = lhs+"="+rhs
                opposite_gx = signed(-gravity, r"m_A g\sin\theta")
                opposite_fx = signed(velocity, r"\mu_k N")
                choices = [
                    lhs+r"=m_A a_A\hat{\imath}",
                    lhs+r"=-m_A a_A\hat{\imath}",
                    rf"\left(T{fx}\right)\hat{{\imath}}+{normal}={rhs}",
                    lhs+"="+("" if acceleration > 0 else "-")+r"m_A a_A\left(\cos\theta\,\hat{\imath}+\sin\theta\,\hat{\jmath}\right)",
                    rf"\left(T{opposite_gx}{fx}\right)\hat{{\imath}}+{normal}={rhs}",
                    rf"\left(T{gx}{opposite_fx}\right)\hat{{\imath}}+{normal}={rhs}",
                ]
                correct = 0 if acceleration > 0 else 1
                fbd = fbd_lookup[(sid, state)]
                figure = "media/"+Path(geometry["figure"]).name
                feedback_figure = "media/"+Path(fbd["figure"]).name
                hill_motion = "uphill" if uphill else "downhill"
                hill_acceleration = hill_motion if speeding else ("downhill" if uphill else "uphill")
                axis_v = "+x" if velocity > 0 else "-x"
                axis_a = "+x" if acceleration > 0 else "-x"
                axis_f = "-x" if velocity > 0 else "+x"
                axis_g = "-x" if rising else "+x"
                v_expression = ("" if velocity > 0 else "-")+r"v_A\hat{\imath}"
                a_expression = ("" if acceleration > 0 else "-")+r"a_A\hat{\imath}"
                inference = (
                    "A moves "+hill_motion+r", along \("+axis_v+r"\), and is "+speed_word+". "
                    "Its acceleration therefore points "+hill_acceleration+r", along \("+axis_a+r"\). "
                    r"Let \(v_A>0\) denote its speed."
                )
                motion_equation = r"\vec{v}_A="+v_expression+r",\qquad\vec{a}_A="+a_expression+"."
                force_text = (
                    r"Tension points toward the pulley, along \(+x\). "
                    r"Gravity’s parallel component points downhill, along \("+axis_g+r"\). "
                    r"Kinetic friction opposes the velocity and points along \("+axis_f+r"\). "
                    r"The normal force points along \(+y\), while gravity’s perpendicular component points along \(-y\)."
                    r" The angle between gravity and \(-y\) is \(\theta\), giving \(F_{g,y}=-m_A g\cos\theta\)."
                )
                accel_error = (
                    "The acceleration sign is reversed. A is "+("moving up" if uphill else "moving down")
                    +" the incline and "+speed_word+r", so \(\vec{a}_A="+a_expression+r"\)."
                )
                feedback = [
                    "", "",
                    r"The parallel component of gravity is missing. Its \(x\) component is \("+gx+r"\).",
                    r"The acceleration has been projected using the incline angle even though the axes are already aligned with the incline. A stays on the straight surface, so \(a_y=0\).",
                    r"The parallel component of gravity has the wrong sign. Gravity points downhill, along \("+axis_g+r"\), giving \(F_{g,x}="+gx+r"\).",
                    r"The friction sign is reversed. Kinetic friction opposes A’s velocity, so it points along \("+axis_f+r"\), with \(f_{k,x}="+fx+r"\).",
                ]
                feedback[correct] = (
                    r"Correct. Tension is along \(+x\), parallel gravity is along \("+axis_g
                    +r"\), friction is along \("+axis_f+r"\), and acceleration is along \("+axis_a+r"\)."
                )
                feedback[1-correct] = accel_error
                force_rows = [
                    ("Tension", r"+T", "0"),
                    ("Weight", gx, r"-m_A g\cos\theta"),
                    ("Normal force", "0", "+N"),
                    ("Kinetic friction", fx, "0"),
                ]
                table_html = '<table><thead><tr><th scope="col">Force on A</th><th scope="col">x component</th><th scope="col">y component</th></tr></thead><tbody>'
                for name, x, y in force_rows:
                    table_html += '<tr><th scope="row">'+name+r"</th><td>\("+x+r"\)</td><td>\("+y+r"\)</td></tr>"
                table_html += "</tbody></table>"
                table_html = table_html.replace('<table>', '<table style="border-collapse: collapse; border: 1px solid #777;">')
                table_html = re.sub(r'<(th|td)(\s[^>]*)?>',
                                    lambda match: '<'+match.group(1)+(match.group(2) or '')+' style="border: 1px solid #777; padding: 4px 8px;">',
                                    table_html)
                picture_html = (
                    '<figure><img src="$IMS-CC-FILEBASE$/'+feedback_figure+'" alt="'+html.escape(fbd["alt_text"], quote=True)
                    +'" width="640" /><figcaption>Solid arrow: velocity. Dashed arrow: acceleration. Arrow lengths are schematic.</figcaption></figure>'
                )
                normal_text = r"The straight surface constrains the perpendicular acceleration to zero: \(a_y=0\)."
                normal_equation = r"N-m_A g\cos\theta=m_A a_y=0."
                component_equation = "T"+gx+fx+"="+("" if acceleration > 0 else "-")+r"m_A a_A,\qquad N-m_A g\cos\theta=0."
                general_html = "\n".join([
                    "<h3>Free-body diagram and motion</h3>",
                    "<p>The four force arrows act on A. The solid arrow above A shows its velocity; the dashed arrow shows its acceleration.</p>",
                    picture_html, paragraphs(inference), display(motion_equation),
                    "<h3>Force components and Newton’s second law</h3>", paragraphs(force_text),
                    table_html, paragraphs(normal_text), display(normal_equation),
                    "<p>Summing the external force vectors gives</p>", display(correct_equation),
                    "<p>The component equations are</p>", display(component_equation),
                ])
                item = {
                    "id": f"q-{scene_id}-{state.replace('_','-')}",
                    "title": f"{scene_id}: {object_name.capitalize()} — {hill_motion}, {speed_word}",
                    "scenario": sid, "scene_index": scene_index, "values": values,
                    "choices": choices, "correct_index": correct,
                    "choice_symbols": ["T","m_A","g","theta","mu_k","N","a_A","i_hat","j_hat"],
                    "defines_symbols": ["T","m_A","m_B","g","theta","mu_k","N","a_A","i_hat","j_hat"],
                    "figure": figure, "figure_alt": geometry_alt,
                    "feedback_figure": feedback_figure, "feedback_figure_alt": fbd["alt_text"],
                    "text_html": stem_html, "choice_html": [display(eq) for eq in choices],
                    "choice_feedback_html": [paragraphs(text) for text in feedback],
                    "general_feedback_html": general_html,
                    "velocity_sign_x": velocity, "acceleration_sign_x": acceleration,
                }
                items.append(item)
                markdown.extend([
                    f"## {len(items)}. {item['title']}", "", stem_md, "",
                    f"![{geometry_alt}](sandbox:{out/figure})", "", GLOSSARY, "",
                    "**"+ASK+"**", "",
                ])
                for letter, eq in zip("ABCDEF", choices):
                    markdown.extend(["**"+letter+".**", "", r"\[", eq, r"\]", ""])
                markdown.extend([
                    "### General feedback", "",
                    "**Instructor key: "+("ABCDEF"[correct])+".**", "",
                    f"![{fbd['alt_text']}](sandbox:{out/feedback_figure})", "",
                    "*Solid arrow: velocity. Dashed arrow: acceleration. Arrow lengths are schematic.*", "",
                    inference, "", r"\["+motion_equation+r"\]", "", force_text, "",
                    table_html,
                ])
                markdown.extend(["", normal_text, "", r"\["+normal_equation+r"\]", "",
                                 r"\["+correct_equation+r"\]", "", r"\["+component_equation+r"\]", "",
                                 "### Feedback for each choice", "", "| Choice | Feedback |", "|---|---|"])
                for letter, reason in zip("ABCDEF", feedback):
                    markdown.append("| "+letter+" | "+reason+" |")
                markdown.append("")
    (out/"inclined-plane-items.json").write_text(json.dumps({"items": items}, ensure_ascii=False, indent=2)+"\n")
    (out/"inclined-plane-bank-review.md").write_text("\n".join(markdown))

    if args.settings:
        settings = yaml.safe_load(args.settings.read_text())
        for key in ["bank_id", "title", "authors", "learning objectives", "points"]:
            if key not in settings:
                raise ValueError("Missing explicit bank setting: "+key)
        if not isinstance(settings["points"], (int, float)) or isinstance(settings["points"], bool) or settings["points"] <= 0:
            raise ValueError("Question points must be positive")
        if not settings["authors"] or not settings["bank_id"]:
            raise ValueError("Bank ID and authors must be supplied")
        date = datetime.now(ZoneInfo("America/New_York")).strftime("%m-%d-%Y")
        questions = []
        for item in items:
            questions.append({"multiple_choice": {
                "id": item["id"], "title": item["title"], "points": settings["points"],
                "text": item["text_html"], "figure": item["figure"], "figure_alt": item["figure_alt"],
                "answers": [{"answer": {
                    "text": item["choice_html"][i], "correct": i == item["correct_index"],
                    "feedback": item["choice_feedback_html"][i],
                }} for i in range(len(item["choices"]))],
                "feedback": {"general": item["general_feedback_html"]},
            }})
        data = {"bank_info": {
            "title": settings["title"], "bank_id": settings["bank_id"],
            "description": "Choose vector forms of Newton’s second law for a sliding object on a rough incline connected to a hanging object. Infer acceleration from the motion description.",
            "date created": date, "learning objectives": settings["learning objectives"],
            "generation prompts": [
                {"workflow": "multiple-choice-questions; eight accepted scenes; 24 motion variants"},
                {"formatting": "HTML block fragments with MathJax delimiters in every presentation field"},
                {"feedback": "FBD of A with axes on A, theta between negative y and gravity, a solid velocity arrow, and a dashed acceleration arrow"},
            ],
            "updates": [{"update 1": date+": Initial bank; falling-right uphill motion excluded."}],
            "associated data": [
                {"input": "Sources/input-inclined-plane-confirmed.yaml"},
                {"workflow": "Sources/input-inclined-plane-confirmed.mcq.yaml"},
                {"markdown source": "inclined-plane-bank-review.md"},
                {"question diagram script": "Sources/draw_inclined_plane_bank.py"},
                {"feedback diagram script": "Sources/draw_inclined_plane_feedback.py"},
                {"bank builder": "Sources/build_inclined_plane_bank.py"},
                {"bank settings": "Sources/inclined-plane-bank-settings.yaml"},
            ],
            "generation details": {"model": "Codex", "bank version": "1.0.0", "last updated": date},
            "authors": settings["authors"],
        }, "questions": questions}
        if "bank_info" in settings:
            saved_metadata = settings["bank_info"]
            if not isinstance(saved_metadata, dict):
                raise ValueError("Saved bank_info must be a mapping")
            for key in ["title", "bank_id", "authors", "learning objectives"]:
                if saved_metadata.get(key) != settings[key]:
                    raise ValueError("Saved bank_info differs from explicit setting: "+key)
            data["bank_info"] = saved_metadata
        class Block(str):
            pass
        def represent(dumper, value):
            return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")
        yaml.SafeDumper.add_representer(Block, represent)
        for entry in questions:
            q = entry["multiple_choice"]
            q["text"] = Block(q["text"])
            q["feedback"]["general"] = Block(q["feedback"]["general"])
            for wrapper in q["answers"]:
                wrapper["answer"]["text"] = Block(wrapper["answer"]["text"])
                wrapper["answer"]["feedback"] = Block(wrapper["answer"]["feedback"])
        (out/(settings["bank_id"]+".yaml")).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000))
    print(json.dumps({"items": len(items), "review": str(out/"inclined-plane-bank-review.md"),
                      "items_json": str(out/"inclined-plane-items.json"),
                      "media_files": len(list(media.glob("*.png"))),
                      "yaml_exported": bool(args.settings)}, indent=2))


if __name__ == "__main__":
    main()
