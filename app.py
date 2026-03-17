"""
ESTELA Physics Problem Bank Visualizer — Flask edition
Run:  uv run python app.py
      then open http://localhost:5174
"""

import json
import os
import re
import threading
import webbrowser
from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml
from flask import Flask, Response, jsonify, request, send_file

app = Flask(__name__, static_folder=None)

# ══════════════════════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════════════════════

SKIP_DIRS = {
    "Old", "old", "Archive", "archive", "Older versions", "Older Versions",
    "Drafts", "drafts", "Temporary", "temporary", "venv", "__pycache__",
    ".git", "Scripts", "scripts", "Figure Creation", "figure_creation",
}
SKIP_COURSES = {"venv", "Templates", "Bank Statistics", ".git"}

QTYPES = [
    "numerical", "multiple_choice", "true_false", "multiple_answers",
    "essay", "categorization", "ordering", "fill_in_multiple_blanks",
    "formula", "file_upload", "hot_spot",
]
TYPE_SHORT = {
    "numerical": "NUM", "multiple_choice": "MC", "multiple_answers": "MA",
    "true_false": "T/F", "essay": "ESS", "categorization": "CAT",
    "ordering": "ORD", "fill_in_multiple_blanks": "FIB",
    "formula": "FRM", "file_upload": "FILE", "hot_spot": "HOT",
}
TYPE_LABEL = {
    "numerical": "Numerical", "multiple_choice": "Multiple Choice",
    "multiple_answers": "Multiple Answer", "true_false": "True / False",
    "essay": "Essay", "formula": "Formula", "categorization": "Categorization",
    "fill_in_multiple_blanks": "Fill-in-the-Blank", "ordering": "Ordering",
    "hot_spot": "Hot Spot",
}


# ══════════════════════════════════════════════════════════════════════════════
# Core logic
# ══════════════════════════════════════════════════════════════════════════════

def latex_to_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(
        r"<latex>\s*\n(.*?)\n\s*</latex>",
        lambda m: f"$$\n{m.group(1)}\n$$",
        text, flags=re.DOTALL,
    )
    text = re.sub(r"<latex>(.*?)</latex>", r"$\1$", text, flags=re.DOTALL)
    # markdown bold (**text**) → <strong>
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text, flags=re.DOTALL)
    return text


def get_qtype(q: dict) -> str:
    for k in QTYPES:
        if k in q:
            return k
    keys = list(q.keys())
    return keys[0] if keys else "unknown"


def load_yaml_file(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def is_bank(data) -> bool:
    return isinstance(data, dict) and "questions" in data and isinstance(data["questions"], list)


def _strip_tags(text: str) -> str:
    """Strip XML/HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def bank_meta(data: dict) -> dict:
    info = data.get("bank_info") or {}
    qs = data.get("questions") or []
    type_counts: dict = {}
    for q in qs:
        if isinstance(q, dict):
            t = get_qtype(q)
            type_counts[t] = type_counts.get(t, 0) + 1
    # first-question text snippet for card thumbnail
    preview = ""
    if qs and isinstance(qs[0], dict):
        q0 = qs[0]
        qtype = get_qtype(q0)
        text = (q0.get(qtype) or {}).get("text") or ""
        clean = _strip_tags(str(text))
        preview = clean[:220] + ("…" if len(clean) > 220 else "")
    return {
        "title": info.get("title") or "Untitled Bank",
        "bank_id": info.get("bank_id") or "",
        "description": info.get("description") or "",
        "authors": info.get("authors") or [],
        "date_created": info.get("date created") or info.get("date_created") or "",
        "lo": info.get("learning objectives") or info.get("learning_objectives") or [],
        "q_count": len(qs),
        "q_types": type_counts,
        "preview": preview,
    }


@lru_cache(maxsize=8)
def scan_repo(root: str) -> dict:
    result: dict = {}
    if not root or not os.path.isdir(root):
        return result
    for course_e in sorted(os.scandir(root), key=lambda e: e.name):
        if not course_e.is_dir() or course_e.name in SKIP_COURSES or course_e.name.startswith("."):
            continue
        course_topics: dict = {}
        for topic_e in sorted(os.scandir(course_e.path), key=lambda e: e.name):
            if not topic_e.is_dir() or topic_e.name.startswith("."):
                continue
            banks = []
            for root2, dirs, files in os.walk(topic_e.path):
                dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
                for f in sorted(files):
                    if not f.endswith((".yaml", ".yml")):
                        continue
                    rel_parts = set(Path(root2).relative_to(topic_e.path).parts)
                    if rel_parts & SKIP_DIRS:
                        continue
                    fp = os.path.join(root2, f)
                    data = load_yaml_file(fp)
                    if data and is_bank(data):
                        banks.append({"path": fp, "meta": bank_meta(data)})
            if banks:
                course_topics[topic_e.name] = banks
        if course_topics:
            result[course_e.name] = course_topics
    return result


def extract_mc_answers(answers: list) -> list:
    result = []
    for j, a in enumerate(answers):
        if not isinstance(a, dict):
            result.append((j, str(a), False))
            continue
        inner = a.get("answer")
        if isinstance(inner, dict):
            text = str(inner.get("text") or "")
            correct = bool(inner.get("correct", False))
        elif "text" in a:
            text = str(a.get("text") or "")
            correct = bool(a.get("correct", False))
        else:
            text = str(a)
            correct = False
        result.append((j, text, correct))
    return result


def _html2tex(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<latex>\s*\n(.*?)\n\s*</latex>", r"\\[\n\1\n\\]", text, flags=re.DOTALL)
    text = re.sub(r"<latex>(.*?)</latex>", r"\\(\1\\)", text, flags=re.DOTALL)
    text = re.sub(r"<strong>(.*?)</strong>", r"\\textbf{\1}", text, flags=re.DOTALL)
    text = re.sub(r"<b>(.*?)</b>", r"\\textbf{\1}", text, flags=re.DOTALL)
    text = re.sub(r"<em>(.*?)</em>", r"\\textit{\1}", text, flags=re.DOTALL)
    text = re.sub(r"<sup>(.*?)</sup>", r"$^{\1}$", text, flags=re.DOTALL)
    text = re.sub(r"<sub>(.*?)</sub>", r"$_{\1}$", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def _tol_str(tol, margin_type: str) -> str:
    if not tol:
        return ""
    pct = r"\%" if margin_type == "percent" else ""
    return rf" \pm {tol}{pct}"


def q_to_latex(q: dict, num: int) -> str:
    qtype = get_qtype(q)
    qdata = q.get(qtype) or {}
    body = _html2tex(str(qdata.get("text") or ""))
    out = [f"\\question[3] % Q{num}", body, ""]
    if qtype == "numerical":
        ans = qdata.get("answer") or {}
        val = ans.get("value", "")
        ts = _tol_str(ans.get("tolerance", ""), ans.get("margin_type", ""))
        val_str = f", ${val}{ts}$" if val != "" else ""
        out += [f"\\vspace{{4mm}}\\underline{{\\hspace{{4cm}}}} \\textit{{(Numerical{val_str})}}", ""]
    elif qtype in ("multiple_choice", "multiple_answers"):
        out.append("\\begin{choices}")
        for _, atxt, correct in extract_mc_answers(qdata.get("answers") or []):
            cmd = "\\CorrectChoice" if correct else "\\choice"
            out.append(f"  {cmd} {_html2tex(atxt)}")
        out.append("\\end{choices}")
    elif qtype == "true_false":
        out += ["\\begin{choices}", "  \\choice True", "  \\choice False", "\\end{choices}"]
    elif qtype == "essay":
        out.append("\\vspace{4cm}")
    out.append("")
    return "\n".join(out)


def build_exam_latex(cart: list, version: int, title: str) -> str:
    qs = []
    for item in cart:
        raw = item.get("rawData") or {}
        questions = raw.get("questions") or []
        if questions:
            qn = max(1, int(item.get("qn") or 1))
            n = len(questions)
            start = ((version - 1) * qn) % n
            for i in range(qn):
                qs.append(questions[(start + i) % n])
    body = "\n\n".join(q_to_latex(q, i + 1) for i, q in enumerate(qs))
    return rf"""\documentclass[12pt,addpoints]{{exam}}
\usepackage{{amsmath,amssymb,physics,geometry,microtype}}
\geometry{{margin=1in}}
%\printanswers  % uncomment to show answers (e.g. for instructor copy)

\begin{{document}}
\begin{{center}}
  {{\Large\bfseries {title}}}\\[4pt]
  Version {version} \quad \today
\end{{center}}
\vspace{{2mm}}\hrule\vspace{{2mm}}
Name:\underline{{\hspace{{8cm}}}} \hfill Score: \underline{{\hspace{{2cm}}}} / \numpoints
\vspace{{6mm}}
\begin{{questions}}
{body}
\end{{questions}}
\end{{document}}
"""


def build_key_latex(cart: list, version: int, title: str) -> str:
    rows = []
    for item in cart:
        raw = item.get("rawData") or {}
        questions = raw.get("questions") or []
        if not questions:
            continue
        qn = max(1, int(item.get("qn") or 1))
        n = len(questions)
        start = ((version - 1) * qn) % n
        for i in range(qn):
            q = questions[(start + i) % n]
            qtype = get_qtype(q)
            qdata = q.get(qtype) or {}
            if qtype == "numerical":
                ans = qdata.get("answer") or {}
                val = ans.get("value", "?")
                ts = _tol_str(ans.get("tolerance", ""), ans.get("margin_type", ""))
                rows.append(rf"  \item ${val}{ts}$")
            elif qtype in ("multiple_choice", "multiple_answers"):
                correct_letters = [
                    chr(65 + j)
                    for j, _, is_correct in extract_mc_answers(qdata.get("answers") or [])
                    if is_correct
                ]
                rows.append(rf"  \item {', '.join(correct_letters) or '?'}")
            elif qtype == "true_false":
                av = qdata.get("answer")
                rows.append(rf"  \item {'True' if av else 'False'}")
            else:
                rows.append(r"  \item [See rubric]")
    rows_str = "\n".join(rows)
    return rf"""\documentclass{{article}}
\usepackage{{amsmath,geometry}}
\geometry{{margin=1in}}
\begin{{document}}
\section*{{{title} --- Version {version} --- Answer Key}}
\begin{{enumerate}}
{rows_str}
\end{{enumerate}}
\end{{document}}
"""


def build_pdf_html(cart: list, version: int, title: str, include_answers: bool) -> str:
    parts = []
    q_num = 0
    for item in cart:
        raw = item.get("rawData") or {}
        questions = raw.get("questions") or []
        if not questions:
            continue
        qn = max(1, int(item.get("qn") or 1))
        n = len(questions)
        start = ((version - 1) * qn) % n
        for i in range(qn):
            q = questions[(start + i) % n]
            qtype = get_qtype(q)
            qdata = q.get(qtype) or {}
            body = latex_to_html(str(qdata.get("text") or ""))
            ans_html = ""
            if qtype in ("multiple_choice", "multiple_answers"):
                for j, atxt, correct in extract_mc_answers(qdata.get("answers") or []):
                    cls = "ans-ok" if (include_answers and correct) else "ans-opt"
                    ans_html += f'<div class="{cls}"><b>{chr(65+j)}.</b> {latex_to_html(atxt)}</div>'
            elif qtype == "numerical":
                if include_answers:
                    ans = qdata.get("answer") or {}
                    val = ans.get("value", "")
                    ts = ""
                    if ans.get("tolerance"):
                        pct = "%" if ans.get("margin_type") == "percent" else ""
                        ts = f" &plusmn; {ans['tolerance']}{pct}"
                    if val != "":
                        ans_html = f'<div class="ans-ok"><b>Answer:</b> {val}{ts}</div>'
                else:
                    ans_html = '<div class="ans-space"></div>'
            elif qtype == "true_false":
                if include_answers:
                    av = qdata.get("answer")
                    ans_html = f'<div class="ans-ok"><b>Answer:</b> {"True" if av else "False"}</div>'
                else:
                    ans_html = '<div class="ans-opt"><b>A.</b> True</div><div class="ans-opt"><b>B.</b> False</div>'
            else:
                if not include_answers:
                    ans_html = '<div class="ans-space" style="height:3cm"></div>'
            q_num += 1
            work = '' if include_answers else '<div class="work-area"><span class="work-lbl">Work</span></div>'
            parts.append(
                f'<div class="sheet">'
                f'<div class="q-num">Question {q_num}</div>'
                f'<div class="q-body">{body}</div>'
                f'<div class="ans-list">{ans_html}</div>'
                f'{work}'
                f'</div>'
            )
    label = " \u2014 Answer Key" if include_answers else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} \u2014 Version {version}{label}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}},{{left:'\\\\[',right:'\\\\]',display:true}},{{left:'\\\\(',right:'\\\\)',display:false}}],throwOnError:false}})">
</script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,600;9..40,700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'DM Sans',sans-serif;font-size:11pt;color:#1a1916;line-height:1.65;background:#eceae4;-webkit-font-smoothing:antialiased;}}
.sheet{{max-width:820px;margin:2rem auto;background:#fff;padding:2.2cm 2.6cm 2.4cm;box-shadow:0 2px 20px rgba(0,0,0,.08);}}
.sheet:first-child{{border-radius:6px 6px 0 0;margin-bottom:0;}}
.sheet+.sheet{{border-top:1px solid #e8e6df;margin-top:0;margin-bottom:0;}}
.sheet:last-child{{border-radius:0 0 6px 6px;margin-bottom:2rem;}}
.sheet:only-child{{border-radius:6px;margin-bottom:2rem;}}
h1{{font-size:18pt;font-weight:700;letter-spacing:-.02em;margin-bottom:.2cm;}}
.meta{{font-size:8.5pt;color:#999;margin-bottom:.5cm;}}
hr{{border:none;border-top:1.5px solid #e0ded6;margin:.5cm 0 .7cm;}}
.name-row{{display:flex;align-items:baseline;gap:.5cm;font-size:10pt;}}
.name-row .line{{border-bottom:1px solid #333;flex:1;height:1.3em;}}
.name-row .score{{border-bottom:1px solid #333;width:3cm;height:1.3em;}}
.q-num{{font-size:7.5pt;font-weight:600;color:#9b9890;text-transform:uppercase;letter-spacing:.09em;margin-bottom:.35cm;}}
.q-body{{font-size:11pt;line-height:1.75;margin-bottom:.45cm;}}
.ans-list{{display:flex;flex-direction:column;gap:.13cm;margin-bottom:.5cm;}}
.ans-opt{{padding:.15cm .38cm;border:1px solid #e8e6df;border-radius:5px;font-size:10pt;color:#3d3b35;}}
.ans-ok{{padding:.15cm .38cm;border:1px solid rgba(26,122,53,.35);background:rgba(26,122,53,.06);border-radius:5px;font-size:10pt;color:#1a7a35;}}
.ans-space{{border-bottom:1px solid #bbb;height:1.2cm;margin-bottom:.5cm;}}
.work-area{{border:1.5px dashed #d5d2c8;border-radius:7px;padding:.4cm .6cm;min-height:15cm;}}
.work-lbl{{font-size:7pt;color:#c5c2b8;text-transform:uppercase;letter-spacing:.1em;}}
.katex-display{{margin:.4cm 0;overflow-x:auto;}}
@media print{{
  body{{background:#fff;}}
  .sheet{{box-shadow:none;margin:0 !important;max-width:none;padding:2cm 2.4cm;border-radius:0 !important;border-top:none !important;break-after:page;page-break-after:always;}}
  .sheet:last-child{{break-after:auto;page-break-after:auto;}}
}}
</style>
</head>
<body>
<div class="sheet">
<h1>{title} \u2014 Version {version}{label}</h1>
<div class="meta">ESTELA Problem Bank Visualizer &middot; UCF / NSF-2421299</div>
<hr>
<div class="name-row">Name:&nbsp;<div class="line"></div>&nbsp;&nbsp;&nbsp;Score:&nbsp;<div class="score"></div></div>
</div>
{''.join(parts)}
</body>
</html>"""


def compile_pdf(cart: list, version: int, title: str, include_answers: bool):
    html = build_pdf_html(cart, version, title, include_answers)
    try:
        from weasyprint import HTML
        return HTML(string=html).write_pdf(), ""
    except ImportError:
        return None, "weasyprint_missing"
    except Exception as e:
        return None, str(e)


# ══════════════════════════════════════════════════════════════════════════════
# API routes
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/scan", methods=["POST"])
def api_scan():
    root = (request.json or {}).get("path", "").strip()
    if not root or not os.path.isdir(root):
        return jsonify({"error": "Path not found"}), 400
    scan_repo.cache_clear()
    data = scan_repo(root)
    out = {}
    for course, topics in data.items():
        out[course] = {}
        for topic, banks in topics.items():
            out[course][topic] = [{"path": b["path"], "meta": b["meta"]} for b in banks]
    return jsonify({"data": out})


@app.route("/api/bank", methods=["POST"])
def api_bank():
    path = (request.json or {}).get("path", "")
    data = load_yaml_file(path)
    if not data or not is_bank(data):
        return jsonify({"error": "Invalid bank"}), 400
    questions = []
    for q in data.get("questions") or []:
        qtype = get_qtype(q)
        qdata = q.get(qtype) or {}
        body = latex_to_html(str(qdata.get("text") or ""))
        answers = []
        if qtype in ("multiple_choice", "multiple_answers"):
            for j, atxt, correct in extract_mc_answers(qdata.get("answers") or []):
                answers.append({"label": chr(65+j), "text": latex_to_html(atxt), "correct": correct})
        elif qtype == "numerical":
            ans = qdata.get("answer") or {}
            val = ans.get("value", "")
            tol = ans.get("tolerance", "")
            mt  = ans.get("margin_type", "")
            ts  = f" ± {tol}{'%' if mt=='percent' else ''}" if tol else ""
            if val != "":
                answers.append({"label": "Answer", "text": f"{val}{ts}", "correct": True})
        elif qtype == "true_false":
            av = qdata.get("answer")
            answers.append({"label": "Answer", "text": "True" if av else "False", "correct": True})
        fb = qdata.get("feedback") or {}
        solution = latex_to_html(str(fb.get("general") or ""))
        fig = qdata.get("figure")
        fig_url = None
        if fig:
            bank_dir = str(Path(path).parent)
            for candidate in [
                os.path.join(bank_dir, fig),
                os.path.join(bank_dir, "Figures", os.path.basename(fig)),
            ]:
                if os.path.exists(candidate):
                    fig_url = f"/api/figure?path={candidate}"
                    break
        questions.append({
            "id": qdata.get("id") or f"q{len(questions)+1}",
            "title": qdata.get("title") or "",
            "type": qtype,
            "type_label": TYPE_LABEL.get(qtype, qtype),
            "body": body,
            "answers": answers,
            "solution": solution,
            "fig_url": fig_url,
        })
    return jsonify({
        "questions": questions,
        "meta": bank_meta(data),
        "rawData": data,
    })


@app.route("/api/figure")
def api_figure():
    path = request.args.get("path", "")
    if not path or not os.path.isfile(path):
        return "Not found", 404
    return send_file(path)


@app.route("/api/export/tex", methods=["POST"])
def api_export_tex():
    body = request.json or {}
    cart       = body.get("cart", [])
    version    = int(body.get("version", 1))
    title      = body.get("title", "Exam")
    kind       = body.get("kind", "exam")
    src = build_key_latex(cart, version, title) if kind == "key" else build_exam_latex(cart, version, title)
    fname = f"{'key' if kind=='key' else 'exam'}_v{version}.tex"
    return Response(src, mimetype="text/plain",
                    headers={"Content-Disposition": f'attachment; filename="{fname}"'})


@app.route("/api/export/html", methods=["POST"])
def api_export_html():
    body = request.json or {}
    cart       = body.get("cart", [])
    version    = int(body.get("version", 1))
    title      = body.get("title", "Exam")
    answers = bool(body.get("include_answers", False))
    html = build_pdf_html(cart, version, title, answers)
    return Response(html, mimetype="text/html")


@app.route("/api/export/pdf", methods=["POST"])
def api_export_pdf():
    body = request.json or {}
    cart    = body.get("cart", [])
    version = int(body.get("version", 1))
    title   = body.get("title", "Exam")
    answers = bool(body.get("include_answers", False))
    pdf, err = compile_pdf(cart, version, title, answers)
    if err == "weasyprint_missing":
        return jsonify({"error": "weasyprint_missing"}), 422
    if err:
        return jsonify({"error": err}), 500
    fname = f"{'key' if answers else 'exam'}_v{version}.pdf"
    return Response(pdf, mimetype="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{fname}"'})


# ══════════════════════════════════════════════════════════════════════════════
# UI — single HTML page
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return HTML_PAGE


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESTELA · Problem Bank</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,400;0,500;1,400&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
        onload="window._katexReady=true"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --bg:#fafaf8;--bg2:#f3f2ee;--bg3:#eeede8;--surface:#fff;
  --border:#d8d6ce;--border2:#e8e6df;
  --ink:#1a1916;--ink2:#3d3b35;--ink3:#6b6860;--ink4:#9b9890;
  --accent:#c8391a;--accent-dim:rgba(200,57,26,.07);
  --blue:#1a3cc8;--gold:#b8860b;--green:#1a7a35;
  --sidebar-w:264px;
  --font-d:'DM Serif Display',Georgia,serif;
  --font-b:'DM Sans',system-ui,sans-serif;
  --font-m:'DM Mono','Courier New',monospace;
  --r:7px;--r2:11px;
  --sh:0 1px 3px rgba(26,25,22,.07),0 4px 12px rgba(26,25,22,.04);
  --sh2:0 2px 8px rgba(26,25,22,.1),0 8px 28px rgba(26,25,22,.07);
}
[data-theme=dark]{
  --bg:#141412;--bg2:#1c1c19;--bg3:#242420;--surface:#1c1c19;
  --border:#38372f;--border2:#2e2e26;
  --ink:#f0ede4;--ink2:#c8c4b8;--ink3:#8a8780;--ink4:#5a5850;
  --accent:#e8522e;--accent-dim:rgba(232,82,46,.07);
  --blue:#4d6fe8;--gold:#d4a017;--green:#6de89a;
  --sh:0 1px 3px rgba(0,0,0,.3),0 4px 12px rgba(0,0,0,.2);
  --sh2:0 2px 8px rgba(0,0,0,.4),0 8px 28px rgba(0,0,0,.3);
}
html,body{height:100%;font-family:var(--font-b);background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased;}

/* ── Layout ── */
#shell{display:flex;height:100vh;overflow:hidden;}

/* ── Sidebar ── */
#sidebar{width:var(--sidebar-w);flex-shrink:0;background:var(--bg2);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
#sb-top{padding:1rem 1.1rem .8rem;border-bottom:1px solid var(--border);flex-shrink:0;}
.sb-wm{font-family:var(--font-d);font-size:1.1rem;color:var(--ink);letter-spacing:-.02em;}
.sb-wm em{font-style:normal;color:var(--accent);}
.sb-sub{font-family:var(--font-m);font-size:.57rem;color:var(--ink4);letter-spacing:.1em;text-transform:uppercase;margin-top:.18rem;}
#sb-scroll{flex:1;overflow-y:auto;padding:.75rem 1rem 1.2rem;}
.sb-sec{margin-bottom:.9rem;}
.sb-lbl{font-family:var(--font-m);font-size:.62rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--ink4);margin-bottom:.32rem;display:block;}

/* ── Controls ── */
.inp{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--ink);font-family:var(--font-m);font-size:.77rem;border-radius:var(--r);padding:.4rem .58rem;outline:none;transition:border-color .12s,box-shadow .12s;}
.inp:focus{border-color:var(--accent);box-shadow:0 0 0 2px rgba(200,57,26,.1);}
.inp-row{display:flex;gap:.35rem;margin-top:.35rem;}
.sel{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--ink);font-family:var(--font-m);font-size:.77rem;border-radius:var(--r);padding:.38rem .55rem;outline:none;cursor:pointer;margin-top:.28rem;}
.sel:focus{border-color:var(--accent);}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.3rem;background:var(--surface);border:1px solid var(--border);color:var(--ink2);font-family:var(--font-b);font-size:.77rem;font-weight:500;border-radius:var(--r);padding:.36rem .8rem;cursor:pointer;transition:background .1s,border-color .1s,box-shadow .1s;white-space:nowrap;line-height:1.3;}
.btn:hover{background:var(--bg3);border-color:var(--ink4);box-shadow:var(--sh);}
.btn:active{transform:scale(.98);}
.btn-p{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 1px 4px rgba(200,57,26,.28);}
.btn-p:hover{filter:brightness(1.07);background:var(--accent);border-color:var(--accent);}
.btn-sm{font-size:.72rem;padding:.28rem .62rem;}
.btn-xs{font-size:.68rem;padding:.22rem .48rem;}
.btn-full{width:100%;margin-top:.3rem;}
.btn-icon{padding:.3rem .42rem;}

/* ── Cart ── */
.cart-empty{font-family:var(--font-m);font-size:.7rem;color:var(--ink4);}
.ci-grp-label{font-family:var(--font-m);font-size:.6rem;color:var(--accent);text-transform:uppercase;letter-spacing:.06em;margin:.4rem 0 .12rem;}
.ci-row{display:flex;align-items:flex-start;gap:.35rem;padding:.3rem 0;border-bottom:1px solid var(--border2);}
.ci-row:last-of-type{border-bottom:none;}
.ci-info{flex:1;min-width:0;}
.ci-title{font-size:.75rem;font-weight:500;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.ci-n{font-family:var(--font-m);font-size:.62rem;color:var(--ink4);}
.ci-stepper{display:flex;align-items:center;gap:.2rem;margin-top:.18rem;}
.ci-step{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;border-radius:50%;border:1px solid var(--border);background:var(--bg3);color:var(--ink2);font-size:.8rem;cursor:pointer;line-height:1;padding:0;transition:background .1s,border-color .1s;}
.ci-step:hover{background:var(--accent);border-color:var(--accent);color:#fff;}
.ci-qval{font-family:var(--font-m);font-size:.72rem;font-weight:600;color:var(--ink);min-width:1.1rem;text-align:center;}
.cnt-badge{display:inline-flex;align-items:center;justify-content:center;background:var(--accent);color:#fff;font-family:var(--font-m);font-weight:700;font-size:.59rem;width:1.05rem;height:1.05rem;border-radius:50%;margin-left:.22rem;vertical-align:middle;}

/* ── Main ── */
#main{flex:1;display:flex;flex-direction:column;overflow:hidden;}
#topbar{display:flex;align-items:center;justify-content:space-between;padding:.65rem 1.6rem;border-bottom:1px solid var(--border);background:var(--surface);flex-shrink:0;box-shadow:var(--sh);}
.tb-wm{font-family:var(--font-d);font-size:1.2rem;color:var(--ink);letter-spacing:-.02em;}
.tb-wm em{font-style:normal;color:var(--accent);}
.tb-sub{font-family:var(--font-m);font-size:.6rem;color:var(--ink4);letter-spacing:.07em;text-transform:uppercase;margin-top:.1rem;}
#content{flex:1;overflow-y:auto;padding:1.3rem 1.8rem 3rem;}

/* ── Stats ── */
#stats{display:flex;border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;margin-bottom:1.4rem;background:var(--surface);box-shadow:var(--sh);}
.sc{flex:1;padding:.5rem .8rem;border-right:1px solid var(--border);}
.sc:last-child{border-right:none;}
.sv{font-family:var(--font-d);font-size:1.35rem;color:var(--ink);line-height:1;letter-spacing:-.03em;}
.sk{font-family:var(--font-m);font-size:.59rem;color:var(--ink4);text-transform:uppercase;letter-spacing:.08em;margin-top:.1rem;}

/* ── Export panel ── */
#export-panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:.9rem 1rem;margin-bottom:1.2rem;box-shadow:var(--sh);}
.ep-title{font-family:var(--font-m);font-size:.64rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--ink4);margin-bottom:.7rem;}
.ep-grid{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;}
.ep-group{background:var(--bg2);border:1px solid var(--border2);border-radius:var(--r);padding:.6rem .75rem;}
.ep-glbl{font-family:var(--font-m);font-size:.6rem;color:var(--ink4);text-transform:uppercase;letter-spacing:.07em;margin-bottom:.4rem;}
.ep-btns{display:flex;flex-wrap:wrap;gap:.28rem;}

/* ── Topic rule ── */
.topic-rule{display:flex;align-items:center;gap:.6rem;margin:1.7rem 0 .6rem;}
.tr-c{font-family:var(--font-d);font-size:.98rem;color:var(--ink);white-space:nowrap;}
.tr-t{font-family:var(--font-m);font-size:.63rem;color:var(--ink3);letter-spacing:.04em;white-space:nowrap;}
.tr-l{flex:1;height:1px;background:var(--border);}
.tr-n{font-family:var(--font-m);font-size:.61rem;color:var(--ink4);white-space:nowrap;}

/* ── Bank card ── */
.bank-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:.85rem 1rem .85rem 1.2rem;margin-bottom:.3rem;box-shadow:var(--sh);position:relative;transition:box-shadow .15s,transform .12s;}
.bank-card::before{content:'';position:absolute;left:0;top:16%;bottom:16%;width:3px;background:var(--border2);border-radius:0 2px 2px 0;transition:background .15s;}
.bank-card:hover{box-shadow:var(--sh2);transform:translateX(2px);}
.bank-card:hover::before{background:var(--ink4);}
.bank-card.incart::before{background:var(--accent);}
.bank-card.incart{border-color:rgba(200,57,26,.18);}
[data-theme=dark] .bank-card.incart{border-color:rgba(232,82,46,.26);}
.bc-row{display:flex;justify-content:space-between;align-items:flex-start;gap:.7rem;}
.bc-title{font-weight:600;font-size:.86rem;color:var(--ink);letter-spacing:-.01em;}
.bc-id{font-family:var(--font-m);font-size:.63rem;color:var(--ink4);margin-top:.05rem;}
.bc-right{font-family:var(--font-m);font-size:.64rem;color:var(--ink4);white-space:nowrap;flex-shrink:0;margin-top:.08rem;}
.bc-desc{font-size:.75rem;color:var(--ink3);margin-top:.28rem;line-height:1.5;}
.bc-preview{font-size:.73rem;color:var(--ink4);margin-top:.28rem;line-height:1.55;font-style:italic;border-left:2px solid var(--border);padding-left:.5rem;}
.bc-footer{display:flex;align-items:center;justify-content:space-between;margin-top:.55rem;}
.bc-badges{display:flex;flex-wrap:wrap;gap:0;}
.bc-actions{display:flex;gap:.3rem;flex-shrink:0;}

/* ── Badges ── */
.badge{display:inline-block;font-family:var(--font-m);font-size:.6rem;font-weight:500;padding:.09rem .36rem;border-radius:3px;margin:.12rem .08rem 0 0;letter-spacing:.03em;}
.bd-num{background:rgba(26,60,200,.07);color:var(--blue);border:1px solid rgba(26,60,200,.17);}
.bd-mc{background:rgba(184,134,11,.08);color:var(--gold);border:1px solid rgba(184,134,11,.19);}
.bd-gen{background:rgba(26,25,22,.05);color:var(--ink3);border:1px solid var(--border);}
.bd-ok{background:var(--accent);color:#fff;border:none;}
[data-theme=dark] .bd-num{background:rgba(77,111,232,.11);color:var(--blue);border-color:rgba(77,111,232,.24);}
[data-theme=dark] .bd-mc{background:rgba(212,160,23,.09);color:var(--gold);border-color:rgba(212,160,23,.22);}
[data-theme=dark] .bd-gen{background:rgba(255,255,255,.05);color:var(--ink3);}

/* ── Questions ── */
.q-panel{margin-top:.4rem;border:1px solid var(--border2);border-radius:var(--r);overflow:hidden;}
.q-ph{padding:.4rem .8rem;background:var(--bg2);border-bottom:1px solid var(--border2);font-family:var(--font-m);font-size:.63rem;color:var(--ink4);text-transform:uppercase;letter-spacing:.08em;}
.q-item{border-bottom:1px solid var(--border2);}
.q-item:last-child{border-bottom:none;}
.q-trigger{display:flex;align-items:center;gap:.55rem;padding:.45rem .8rem;cursor:pointer;background:var(--surface);border:none;width:100%;text-align:left;color:var(--ink);font-family:var(--font-b);font-size:.81rem;transition:background .1s;}
.q-trigger:hover,.q-trigger.open{background:var(--bg2);}
.q-nbadge{font-family:var(--font-m);font-size:.58rem;color:var(--ink4);background:var(--bg3);border:1px solid var(--border);border-radius:3px;padding:.05rem .3rem;flex-shrink:0;}
.q-type{font-family:var(--font-m);font-size:.57rem;color:var(--ink4);margin-left:auto;flex-shrink:0;}
.q-chev{font-size:.68rem;color:var(--ink4);transition:transform .17s;flex-shrink:0;}
.q-trigger.open .q-chev{transform:rotate(90deg);}
.q-body{display:none;padding:.65rem .8rem .8rem;background:var(--bg2);border-top:1px solid var(--border2);}
.q-body.open{display:block;}
.q-text{font-size:.84rem;line-height:1.72;color:var(--ink2);margin-bottom:.45rem;}
.ans-list{display:flex;flex-direction:column;gap:.13rem;margin-bottom:.38rem;}
.ans-opt{background:var(--surface);border:1px solid var(--border);border-radius:5px;padding:.3rem .62rem;font-size:.81rem;color:var(--ink2);}
.ans-ok{border-color:rgba(26,122,53,.35);background:rgba(26,122,53,.06);color:var(--green);}
.q-sol{border-left:3px solid var(--accent);padding:.48rem .72rem;background:var(--accent-dim);border-radius:0 5px 5px 0;font-size:.79rem;color:var(--ink2);line-height:1.65;margin-top:.38rem;}
.sol-lbl{font-family:var(--font-m);font-size:.59rem;font-weight:500;color:var(--accent);text-transform:uppercase;letter-spacing:.09em;margin-bottom:.2rem;}

/* ── Empty ── */
#empty{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;padding:2rem;text-align:center;color:var(--ink4);}
.e-icon{font-size:2.6rem;margin-bottom:.75rem;opacity:.4;}
.e-h{font-family:var(--font-d);font-size:1.35rem;color:var(--ink);margin-bottom:.38rem;}
.e-p{font-size:.83rem;color:var(--ink3);line-height:1.65;max-width:360px;}
.e-code{font-family:var(--font-m);font-size:.75rem;color:var(--accent);margin-top:.55rem;}

/* ── Toast ── */
#toast{position:fixed;bottom:1.3rem;right:1.3rem;background:var(--ink);color:var(--bg);font-family:var(--font-m);font-size:.73rem;padding:.45rem .9rem;border-radius:var(--r);box-shadow:var(--sh2);opacity:0;transform:translateY(5px);transition:opacity .18s,transform .18s;pointer-events:none;z-index:9999;}
#toast.show{opacity:1;transform:translateY(0);}

/* ── Scrollbars ── */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}

/* ── Loading spinner ── */
.spin{display:inline-block;width:11px;height:11px;border:2px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:_spin .55s linear infinite;vertical-align:middle;}
@keyframes _spin{to{transform:rotate(360deg);}}
</style>
</head>
<body>
<div id="shell">

  <!-- Sidebar -->
  <aside id="sidebar">
    <div id="sb-top">
      <div class="sb-wm">E<em>S</em>TELA</div>
      <div class="sb-sub">Problem Bank Visualizer</div>
    </div>
    <div id="sb-scroll">

      <div class="sb-sec">
        <span class="sb-lbl">Repository</span>
        <input id="path-inp" class="inp" type="text" placeholder="/path/to/problem-bank" spellcheck="false"
               onkeydown="if(event.key==='Enter')loadRepo()">
        <div class="inp-row">
          <button class="btn btn-p" style="flex:1" onclick="loadRepo()">Load</button>
          <button class="btn btn-icon" onclick="clearAll()" title="Clear">✕</button>
        </div>
      </div>

      <div class="sb-sec" id="filter-sec" style="display:none">
        <span class="sb-lbl">Filter</span>
        <select id="fc" class="sel" onchange="onFilterChange()">
          <option value="">All courses</option>
        </select>
        <select id="ft" class="sel" style="display:none" onchange="renderBanks()">
          <option value="">All topics</option>
        </select>
      </div>

      <div class="sb-sec" id="search-sec" style="display:none">
        <span class="sb-lbl">Search</span>
        <input id="search-inp" class="inp" type="text" placeholder="Title, ID, topic, objective…"
               oninput="S.search=this.value.trim();renderBanks()">
      </div>

      <div class="sb-sec">
        <button class="btn btn-sm btn-full" id="theme-btn" onclick="toggleTheme()">🌙 Dark mode</button>
      </div>

      <div class="sb-sec">
        <span class="sb-lbl">Exam Cart <span id="cart-badge"></span></span>
        <div id="cart-body"><div class="cart-empty">No banks selected.</div></div>
      </div>

      <div class="sb-sec" id="build-sec" style="display:none">
        <span class="sb-lbl">Build Exam</span>
        <input id="exam-title" class="inp" type="text" value="PHY I Mechanics Exam" placeholder="Exam title…">
        <div style="display:flex;align-items:center;gap:.35rem;margin-top:.32rem;">
          <span style="font-family:var(--font-m);font-size:.7rem;color:var(--ink4)">Versions:</span>
          <button class="ci-step" onclick="adjustVersions(-1)">−</button>
          <span id="n-ver-display" style="font-family:var(--font-m);font-size:.72rem;font-weight:600;color:var(--ink);min-width:1.1rem;text-align:center">2</span>
          <input id="n-ver" type="hidden" value="2">
          <button class="ci-step" onclick="adjustVersions(1)">+</button>
          <span id="max-ver-hint" style="font-family:var(--font-m);font-size:.62rem;color:var(--ink4)"></span>
        </div>
        <div id="export-btns" style="margin-top:.5rem"></div>
      </div>

    </div>
  </aside>

  <!-- Main -->
  <div id="main">
    <div id="topbar">
      <div>
        <div class="tb-wm">Problem Bank <em>Visualizer</em></div>
        <div class="tb-sub">ESTELA · Isomorphic Physics Banks · UCF / NSF-2421299</div>
      </div>
    </div>
    <div id="content">
      <div id="empty">
        <div class="e-icon">⚛</div>
        <div class="e-h">Load a repository</div>
        <p class="e-p">Enter the path to your local clone of the ESTELA problem bank and click <b>Load</b>.</p>
        <div class="e-code">github.com/Zhongzhou/ESTELA-physics-problem-bank</div>
      </div>
      <div id="banks-view" style="display:none"></div>
    </div>
  </div>

</div>
<div id="toast"></div>

<script>
// ── State ──────────────────────────────────────────────────────────────────
const S = {
  repo: {},        // course → topic → [{path,meta}]
  cart: [],        // [{path,meta,topic,rawData}]
  expanded: new Set(),
  theme: localStorage.getItem('theme') || 'light',
  search: '',
};

// ── Theme ──────────────────────────────────────────────────────────────────
function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  document.getElementById('theme-btn').textContent = t === 'dark' ? '☀ Light mode' : '🌙 Dark mode';
}
function toggleTheme() {
  S.theme = S.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('theme', S.theme);
  applyTheme(S.theme);
}
applyTheme(S.theme);
// restore last used path
(function(){ const p = localStorage.getItem('estela_path'); if (p) document.getElementById('path-inp').value = p; })();

// ── Toast ──────────────────────────────────────────────────────────────────
let _tt;
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg; el.classList.add('show');
  clearTimeout(_tt); _tt = setTimeout(() => el.classList.remove('show'), 2000);
}

// ── KaTeX ──────────────────────────────────────────────────────────────────
function renderMath(el) {
  if (!window.renderMathInElement) { setTimeout(() => renderMath(el), 120); return; }
  renderMathInElement(el || document.body, {
    delimiters: [
      {left:'$$',right:'$$',display:true}, {left:'$',right:'$',display:false},
      {left:'\\[',right:'\\]',display:true}, {left:'\\(',right:'\\)',display:false},
    ],
    throwOnError: false,
  });
}

// ── Load repo ──────────────────────────────────────────────────────────────
async function loadRepo() {
  const path = document.getElementById('path-inp').value.trim();
  if (!path) return;
  try {
    const res = await fetch('/api/scan', {method:'POST',
      headers:{'Content-Type':'application/json'}, body: JSON.stringify({path})});
    if (!res.ok) { toast('Path not found'); return; }
    const {data} = await res.json();
    S.repo = data; S.cart = []; S.expanded = new Set(); S.search = '';
    document.getElementById('search-inp').value = '';
    populateFilters(); renderBanks(); renderCart();
    await restoreCart(data);
    toast('Loaded');
  } catch(e) { toast('Error: ' + e.message); }
}

function clearAll() {
  S.repo = {}; S.cart = []; S.expanded = new Set(); S.search = '';
  localStorage.removeItem('estela_cart');
  localStorage.removeItem('estela_path');
  document.getElementById('path-inp').value = '';
  document.getElementById('search-inp').value = '';
  document.getElementById('empty').style.display = 'flex';
  document.getElementById('banks-view').style.display = 'none';
  document.getElementById('filter-sec').style.display = 'none';
  document.getElementById('search-sec').style.display = 'none';
  document.getElementById('build-sec').style.display = 'none';
  renderCart();
}

// ── Filters ────────────────────────────────────────────────────────────────
function populateFilters() {
  const fc = document.getElementById('fc');
  fc.innerHTML = '<option value="">All courses</option>';
  Object.keys(S.repo).forEach(c => {
    const o = document.createElement('option'); o.value = c; o.textContent = c; fc.appendChild(o);
  });
  document.getElementById('filter-sec').style.display = 'block';
  document.getElementById('search-sec').style.display = 'block';
}

function onFilterChange() {
  const course = document.getElementById('fc').value;
  const ft = document.getElementById('ft');
  if (course && S.repo[course]) {
    ft.style.display = 'block';
    ft.innerHTML = '<option value="">All topics</option>';
    Object.keys(S.repo[course]).forEach(t => {
      const o = document.createElement('option'); o.value = t; o.textContent = t; ft.appendChild(o);
    });
  } else {
    ft.style.display = 'none';
  }
  renderBanks();
}

// ── Badge helpers ──────────────────────────────────────────────────────────
const TS = {numerical:'NUM',multiple_choice:'MC',multiple_answers:'MA',true_false:'T/F',
  essay:'ESS',categorization:'CAT',ordering:'ORD',fill_in_multiple_blanks:'FIB',
  formula:'FRM',file_upload:'FILE',hot_spot:'HOT'};

function bcls(t) {
  if (t==='numerical') return 'bd-num';
  if (t==='multiple_choice'||t==='multiple_answers') return 'bd-mc';
  return 'bd-gen';
}

// ── Render banks ───────────────────────────────────────────────────────────
function renderBanks() {
  const fc = document.getElementById('fc').value;
  const ft = document.getElementById('ft').value;
  const q = S.search.toLowerCase();
  let html = statsHTML();

  for (const [course, topics] of Object.entries(S.repo)) {
    if (fc && course !== fc) continue;
    for (const [topic, banks] of Object.entries(topics)) {
      if (ft && topic !== ft) continue;
      const filtered = q ? banks.filter(b => {
        const m = b.meta;
        return (m.title||'').toLowerCase().includes(q) ||
               (m.bank_id||'').toLowerCase().includes(q) ||
               (m.description||'').toLowerCase().includes(q) ||
               topic.toLowerCase().includes(q) ||
               (m.lo||[]).some(l => String(l).toLowerCase().includes(q));
      }) : banks;
      if (!filtered.length) continue;
      html += `<div class="topic-rule">
        <span class="tr-c">${course}</span>
        <span class="tr-t">${topic}</span>
        <span class="tr-l"></span>
        <span class="tr-n">${filtered.length} bank${filtered.length!==1?'s':''}</span>
      </div>`;
      html += filtered.map(b => bankCardHTML(b, topic)).join('');
    }
  }

  const v = document.getElementById('banks-view');
  v.innerHTML = html; v.style.display = 'block';
  document.getElementById('empty').style.display = 'none';
  S.expanded.forEach(p => loadQs(p));
}

function statsHTML() {
  let courses=0,topics=0,banks=0,qs=0;
  for (const tv of Object.values(S.repo)) {
    courses++;
    for (const bl of Object.values(tv)) { topics++; for (const b of bl) { banks++; qs+=b.meta.q_count; } }
  }
  return `<div id="stats">
    ${[['Courses',courses],['Topics',topics],['Banks',banks],['Questions',qs],['In Cart',S.cart.length]]
      .map(([k,v])=>`<div class="sc"><div class="sv">${v}</div><div class="sk">${k}</div></div>`).join('')}
  </div>`;
}

function bankCardHTML(b, topic) {
  const {path,meta} = b;
  const inCart = S.cart.some(c=>c.path===path);
  const isExp  = S.expanded.has(path);
  const badges = Object.entries(meta.q_types)
    .map(([t,n])=>`<span class="badge ${bcls(t)}">${TS[t]||t.slice(0,3).toUpperCase()} ×${n}</span>`)
    .join('') + (inCart?'<span class="badge bd-ok">✓ cart</span>':'');
  const desc = meta.description
    ? `<div class="bc-desc">${esc(meta.description).slice(0,145)}${meta.description.length>145?'…':''}</div>` : '';
  const preview = (!isExp && meta.preview)
    ? `<div class="bc-preview">${esc(meta.preview)}</div>` : '';
  const qSection = isExp
    ? `<div class="q-panel" id="qp-${slugify(path)}">
        <div class="q-ph">${esc(meta.title)} — ${meta.q_count} questions</div>
        <div id="ql-${slugify(path)}">
          <div style="padding:.65rem .8rem;font-family:var(--font-m);font-size:.7rem;color:var(--ink4)">
            <span class="spin"></span> Loading…
          </div>
        </div>
      </div>` : '';
  return `<div class="bank-card${inCart?' incart':''}" id="bc-${slugify(path)}">
    <div class="bc-row">
      <div style="flex:1;min-width:0">
        <div class="bc-title">${esc(meta.title)}</div>
        <div class="bc-id">${esc(meta.bank_id)}</div>
      </div>
      <div class="bc-right">${meta.q_count} q</div>
    </div>
    ${desc}
    ${preview}
    <div class="bc-footer">
      <div class="bc-badges">${badges}</div>
      <div class="bc-actions">
        <button class="btn btn-sm" onclick="toggleExp(${attr(path)},${attr(topic)})">
          ${isExp?'▾ Collapse':'▸ Preview'}
        </button>
        <button class="btn btn-sm${!inCart?' btn-p':''}"
                onclick="toggleCart(${attr(path)},${attr(topic)})">
          ${inCart?'− Remove':'+ Add'}
        </button>
      </div>
    </div>
    ${qSection}
  </div>`;
}

// ── Questions ──────────────────────────────────────────────────────────────
async function loadQs(path) {
  const container = document.getElementById(`ql-${slugify(path)}`);
  if (!container) return;
  const res = await fetch('/api/bank', {method:'POST',
    headers:{'Content-Type':'application/json'}, body:JSON.stringify({path})});
  if (!res.ok) { container.innerHTML = '<div style="padding:.5rem;color:var(--accent)">Failed to load</div>'; return; }
  const {questions, rawData} = await res.json();
  // store rawData for export if this bank is in cart
  const ci = S.cart.find(c=>c.path===path);
  if (ci) ci.rawData = rawData;
  container.innerHTML = questions.map((q,i)=>qHTML(q,i,path)).join('');
  renderMath(container);
}

function qHTML(q, i, bankPath) {
  const id = `q_${slugify(bankPath)}_${i}`;
  const answers = q.answers.map(a =>
    `<div class="ans-opt${a.correct?' ans-ok':''}">` +
    (a.label !== 'Answer' ? `<b>${a.label}.</b> ` : `<b>${a.label}:</b> `) +
    `${a.text}</div>`
  ).join('');
  const sol = q.solution
    ? `<div class="q-sol"><div class="sol-lbl">Solution</div>${q.solution}</div>` : '';
  const fig = q.fig_url
    ? `<img src="${q.fig_url}" style="max-width:360px;margin:.35rem 0;border-radius:5px;display:block;">` : '';
  return `<div class="q-item">
    <button class="q-trigger" id="qt-${id}" onclick="toggleQ('${id}')">
      <span class="q-nbadge">Q${i+1}</span>
      <span style="flex:1;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">
        ${esc(q.title||q.id)}
      </span>
      <span class="q-type">${q.type_label}</span>
      <span class="q-chev">›</span>
    </button>
    <div class="q-body" id="qb-${id}">
      <div class="q-text">${q.body}</div>
      ${fig}
      <div class="ans-list">${answers}</div>
      ${sol}
    </div>
  </div>`;
}

function toggleQ(id) {
  const t = document.getElementById(`qt-${id}`);
  const b = document.getElementById(`qb-${id}`);
  const open = b.classList.toggle('open');
  t.classList.toggle('open', open);
  if (open) renderMath(b);
}

// ── Cart ───────────────────────────────────────────────────────────────────
async function toggleCart(path, topic) {
  const idx = S.cart.findIndex(c=>c.path===path);
  if (idx !== -1) {
    S.cart.splice(idx,1); toast('Removed'); renderCart(); renderBanks(); return;
  }
  // find meta
  let meta = null;
  for (const tv of Object.values(S.repo))
    for (const bl of Object.values(tv))
      for (const b of bl)
        if (b.path===path) { meta = b.meta; break; }

  // fetch rawData for LaTeX export
  try {
    const res = await fetch('/api/bank', {method:'POST',
      headers:{'Content-Type':'application/json'}, body:JSON.stringify({path})});
    if (!res.ok) { toast('Failed to load bank'); return; }
    const {rawData, meta: apiMeta} = await res.json();
    S.cart.push({path, meta: meta||apiMeta, topic, rawData: rawData||{}, qn: 1});
    toast('Added to cart'); saveCart(); renderCart(); renderBanks();
  } catch(e) { toast('Error: ' + e.message); }
}

function removeFromCart(path) {
  S.cart = S.cart.filter(c=>c.path!==path);
  saveCart(); renderCart(); renderBanks();
}

function adjustVersions(delta) {
  const inp = document.getElementById('n-ver');
  const disp = document.getElementById('n-ver-display');
  const maxV = parseInt(inp.max) || 10;
  const cur = parseInt(inp.value) || 2;
  const next = Math.min(maxV, Math.max(1, cur + delta));
  inp.value = next;
  disp.textContent = next;
  updateExportBtns();
}

function adjustCartQn(path, delta) {
  const item = S.cart.find(c=>c.path===path);
  if (!item) return;
  item.qn = Math.min(item.meta.q_count, Math.max(1, (item.qn||1) + delta));
  saveCart(); renderCart();
}

function renderCart() {
  const el = document.getElementById('cart-body');
  const badge = document.getElementById('cart-badge');
  badge.innerHTML = S.cart.length
    ? `<span class="cnt-badge">${S.cart.length}</span>` : '';
  document.getElementById('build-sec').style.display = S.cart.length ? 'block' : 'none';

  // update max versions hint
  const hint = document.getElementById('max-ver-hint');
  const nver = document.getElementById('n-ver');
  const disp = document.getElementById('n-ver-display');
  if (hint && nver) {
    if (S.cart.length) {
      const maxV = Math.min(...S.cart.map(c => Math.max(1, Math.floor(c.meta.q_count / Math.max(1, c.qn||1)))));
      hint.textContent = `max ${maxV}`;
      nver.max = maxV;
      if (parseInt(nver.value) > maxV) { nver.value = maxV; if (disp) disp.textContent = maxV; }
    } else {
      hint.textContent = '';
      nver.max = 10;
    }
  }
  updateExportBtns();

  if (!S.cart.length) {
    el.innerHTML = '<div class="cart-empty">No banks selected.</div>'; return;
  }
  const byTopic = {};
  S.cart.forEach(c => (byTopic[c.topic||'?'] = byTopic[c.topic||'?']||[]).push(c));
  el.innerHTML = Object.entries(byTopic).map(([t,items]) =>
    `<div class="ci-grp-label">${esc(t)}</div>` +
    items.map(item=>`<div class="ci-row">
      <div class="ci-info">
        <div class="ci-title">${esc(item.meta.title)}</div>
        <div class="ci-stepper">
          <button class="ci-step" onclick="adjustCartQn(${attr(item.path)},-1)">−</button>
          <span class="ci-qval">${item.qn||1}</span>
          <button class="ci-step" onclick="adjustCartQn(${attr(item.path)},1)">+</button>
          <span class="ci-n">/ ${item.meta.q_count}</span>
        </div>
      </div>
      <button class="btn btn-xs btn-icon" onclick="removeFromCart(${attr(item.path)})" title="Remove">✕</button>
    </div>`).join('')
  ).join('');
}

// ── Expand ─────────────────────────────────────────────────────────────────
function toggleExp(path, topic) {
  if (S.expanded.has(path)) S.expanded.delete(path);
  else S.expanded.add(path);
  renderBanks();
}

// ── Export buttons (sidebar) ────────────────────────────────────────────────
function updateExportBtns() {
  const el = document.getElementById('export-btns');
  if (!el) return;
  if (!S.cart.length) { el.innerHTML = ''; return; }
  const nv = Math.max(1, parseInt(document.getElementById('n-ver')?.value||'2'));
  const vs = Array.from({length:nv},(_,i)=>i+1);
  const row = (label, btns) =>
    `<div style="margin-bottom:.3rem">
       <div style="font-family:var(--font-m);font-size:.6rem;color:var(--ink4);text-transform:uppercase;letter-spacing:.07em;margin-bottom:.18rem">${label}</div>
       <div style="display:flex;flex-wrap:wrap;gap:.22rem">${btns}</div>
     </div>`;
  el.innerHTML =
    row('Preview Exam', vs.map(v=>`<button class="btn btn-xs" onclick="doPreview(${v},false)">👁 v${v}</button>`).join('')) +
    row('Preview Key',  vs.map(v=>`<button class="btn btn-xs" onclick="doPreview(${v},true)">👁 v${v}</button>`).join('')) +
    row('Exam .tex',    vs.map(v=>`<button class="btn btn-xs" onclick="doTex(${v},${attr('exam')})">⬇ v${v}</button>`).join('')) +
    row('Key .tex',     vs.map(v=>`<button class="btn btn-xs" onclick="doTex(${v},${attr('key')})">⬇ v${v}</button>`).join(''));
}

// ── Export panel (kept for reference, no longer rendered in main content) ───
function exportPanelHTML() {
  const nv = parseInt(document.getElementById('n-ver')?.value||'2');
  const vs = Array.from({length:nv},(_,i)=>i+1);
  const row = (kind, icon) => vs.map(v =>
    `<button class="btn btn-xs" onclick="doTex(${v},${attr(kind)})">${icon} v${v}</button>`
  ).join('');
  const prow = (answers) => vs.map(v =>
    `<button class="btn btn-xs" onclick="doPDF(${v},${answers})">🖨 v${v}</button>`
  ).join('');
  return `<div id="export-panel">
    <div class="ep-title">Export</div>
    <div class="ep-grid">
      <div class="ep-group">
        <div class="ep-glbl">Exam .tex</div>
        <div class="ep-btns">${row('exam','⬇')}</div>
      </div>
      <div class="ep-group">
        <div class="ep-glbl">Key .tex</div>
        <div class="ep-btns">${row('key','⬇')}</div>
      </div>
      <div class="ep-group">
        <div class="ep-glbl">Exam PDF</div>
        <div class="ep-btns">${prow(false)}</div>
      </div>
      <div class="ep-group">
        <div class="ep-glbl">Key PDF</div>
        <div class="ep-btns">${prow(true)}</div>
      </div>
    </div>
  </div>`;
}

function _cartBody() {
  return S.cart.map(c=>({path:c.path, meta:c.meta, rawData:c.rawData||{}, qn:c.qn||1}));
}

async function doTex(version, kind) {
  const title = document.getElementById('exam-title').value || 'Exam';
  const body = {cart:_cartBody(), version, kind, title};
  const res = await fetch('/api/export/tex', {method:'POST',
    headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  if (!res.ok) { toast('Export failed'); return; }
  const fname = `${kind}_v${version}.tex`;
  dlBlob(await res.blob(), fname); toast('Downloaded ' + fname);
}

async function doPreview(version, includeAnswers) {
  toast('Building preview…');
  const title = document.getElementById('exam-title').value || 'Exam';
  const body = {cart:_cartBody(), version, title, include_answers:includeAnswers};
  try {
    const res = await fetch('/api/export/html', {method:'POST',
      headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    if (!res.ok) { toast('Preview failed'); return; }
    const html = await res.text();
    const blob = new Blob([html], {type:'text/html'});
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
    setTimeout(() => URL.revokeObjectURL(url), 120000);
  } catch(e) { toast('Error: ' + e.message); }
}

function dlBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), {href:url, download:name});
  document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(url); a.remove(); }, 800);
}

// ── Cart persistence ────────────────────────────────────────────────────────
function saveCart() {
  try {
    const payload = S.cart.map(c=>({path:c.path, meta:c.meta, topic:c.topic, qn:c.qn||1}));
    localStorage.setItem('estela_cart', JSON.stringify(payload));
    localStorage.setItem('estela_path', document.getElementById('path-inp').value.trim());
  } catch(e) {}
}

async function restoreCart(repoData) {
  try {
    const saved = localStorage.getItem('estela_cart');
    if (!saved) return;
    const items = JSON.parse(saved);
    if (!items.length) return;
    // verify paths still exist in loaded repo
    const allPaths = new Set();
    for (const tv of Object.values(repoData))
      for (const bl of Object.values(tv))
        for (const b of bl) allPaths.add(b.path);
    const valid = items.filter(c => allPaths.has(c.path));
    if (!valid.length) return;
    // fetch rawData for each restored item
    for (const item of valid) {
      try {
        const res = await fetch('/api/bank', {method:'POST',
          headers:{'Content-Type':'application/json'}, body:JSON.stringify({path:item.path})});
        if (!res.ok) continue;
        const {rawData} = await res.json();
        S.cart.push({...item, rawData: rawData||{}});
      } catch(e) {}
    }
    if (S.cart.length) { renderCart(); renderBanks(); toast(`Restored ${S.cart.length} cart item${S.cart.length>1?'s':''}`); }
  } catch(e) {}
}

// ── Utilities ──────────────────────────────────────────────────────────────
function esc(s) {
  return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function json(v) { return JSON.stringify(v); }
// safe for use inside double-quoted HTML attributes
function attr(v) { return JSON.stringify(v).replace(/&/g,'&amp;').replace(/"/g,'&quot;'); }
function slugify(s) { return String(s).replace(/[^a-zA-Z0-9]/g,'_'); }
</script>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════════════════════
# Entrypoint
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    PORT = 5174
    print(f"\n  ⚛  ESTELA Problem Bank Visualizer")
    print(f"     http://localhost:{PORT}\n")
    threading.Timer(0.9, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    app.run(port=PORT, debug=False)