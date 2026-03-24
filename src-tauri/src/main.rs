// Prevents extra console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use base64::Engine as _;
use regex::Regex;
use serde_json::{json, Value};
use std::collections::HashMap;
use std::io::Read;
use std::path::{Path, PathBuf};

// ══════════════════════════════════════════════════════════════════════════════
// Constants
// ══════════════════════════════════════════════════════════════════════════════

const SKIP_DIRS: &[&str] = &[
    "Old", "old", "Archive", "archive", "Older versions", "Older Versions",
    "Drafts", "drafts", "Temporary", "temporary", "venv", "__pycache__",
    ".git", "Scripts", "scripts", "Figure Creation", "figure_creation",
];

const SKIP_COURSES: &[&str] = &["venv", "Templates", "Bank Statistics", ".git"];

const QTYPES: &[&str] = &[
    "numerical", "multiple_choice", "true_false", "multiple_answers",
    "essay", "categorization", "ordering", "fill_in_multiple_blanks",
    "formula", "file_upload", "hot_spot",
];

// ══════════════════════════════════════════════════════════════════════════════
// Helper functions
// ══════════════════════════════════════════════════════════════════════════════

fn get_qtype(q: &Value) -> String {
    if let Some(obj) = q.as_object() {
        for k in QTYPES {
            if obj.contains_key(*k) {
                return k.to_string();
            }
        }
        if let Some(first_key) = obj.keys().next() {
            return first_key.clone();
        }
    }
    "unknown".to_string()
}

fn strip_tags(text: &str) -> String {
    let mut s = text.to_string();
    // <latex>...</latex> blocks → strip entirely
    s = Regex::new(r"(?s)<latex>.*?</latex>").unwrap().replace_all(&s, " ").to_string();
    // strip HTML tags
    s = Regex::new(r"<[^>]+>").unwrap().replace_all(&s, " ").to_string();
    // \command{content} → content (e.g. \text{kg} → kg, \textbf{x} → x)
    let cmd_re = Regex::new(r"\\[a-zA-Z]+\{([^}]*)\}").unwrap();
    while cmd_re.is_match(&s) {
        s = cmd_re.replace_all(&s, "$1").to_string();
    }
    // $...$ and $$...$$ → content
    s = Regex::new(r"\$\$([^$]*)\$\$").unwrap().replace_all(&s, "$1").to_string();
    s = Regex::new(r"\$([^$]*)\$").unwrap().replace_all(&s, "$1").to_string();
    // remaining backslashes and markdown bold/italic
    s = s.replace("\\", " ").replace("**", "").replace('*', "");
    // collapse whitespace
    Regex::new(r"\s+").unwrap().replace_all(s.trim(), " ").to_string()
}

fn latex_to_html(text: &str) -> String {
    if text.is_empty() {
        return String::new();
    }
    // Block latex: <latex>\n...\n</latex> → $$\n...\n$$
    let block_re = Regex::new(r"(?s)<latex>\s*\n(.*?)\n\s*</latex>").unwrap();
    let result = block_re.replace_all(text, |caps: &regex::Captures| {
        format!("$$\n{}\n$$", &caps[1])
    });
    // Inline latex: <latex>...</latex> → $...$
    let inline_re = Regex::new(r"(?s)<latex>(.*?)</latex>").unwrap();
    let result = inline_re.replace_all(&result, |caps: &regex::Captures| {
        format!("${}", caps[1].to_string() + "$")
    });
    // markdown bold: **text** → <strong>text</strong>
    let bold_re = Regex::new(r"(?s)\*\*(.*?)\*\*").unwrap();
    bold_re.replace_all(&result, |caps: &regex::Captures| {
        format!("<strong>{}</strong>", &caps[1])
    }).to_string()
}

fn html2tex(text: &str) -> String {
    if text.is_empty() {
        return String::new();
    }
    // Block latex: <latex>\n...\n</latex> → \[\n...\n\]
    let block_re = Regex::new(r"(?s)<latex>\s*\n(.*?)\n\s*</latex>").unwrap();
    let result = block_re.replace_all(text, |caps: &regex::Captures| {
        format!("\\[\n{}\n\\]", &caps[1])
    });
    // Inline latex: <latex>...</latex> → \(...\)
    let inline_re = Regex::new(r"(?s)<latex>(.*?)</latex>").unwrap();
    let result = inline_re.replace_all(&result, |caps: &regex::Captures| {
        format!("\\({}\\)", &caps[1])
    });
    // <strong>...</strong> → \textbf{...}
    let strong_re = Regex::new(r"(?s)<strong>(.*?)</strong>").unwrap();
    let result = strong_re.replace_all(&result, |caps: &regex::Captures| {
        format!("\\textbf{{{}}}", &caps[1])
    });
    // <b>...</b> → \textbf{...}
    let b_re = Regex::new(r"(?s)<b>(.*?)</b>").unwrap();
    let result = b_re.replace_all(&result, |caps: &regex::Captures| {
        format!("\\textbf{{{}}}", &caps[1])
    });
    // <em>...</em> → \textit{...}
    let em_re = Regex::new(r"(?s)<em>(.*?)</em>").unwrap();
    let result = em_re.replace_all(&result, |caps: &regex::Captures| {
        format!("\\textit{{{}}}", &caps[1])
    });
    // <sup>...</sup> → $^{...}$
    let sup_re = Regex::new(r"(?s)<sup>(.*?)</sup>").unwrap();
    let result = sup_re.replace_all(&result, |caps: &regex::Captures| {
        format!("$^{{{}}}$", &caps[1])
    });
    // <sub>...</sub> → $_{{...}}$
    let sub_re = Regex::new(r"(?s)<sub>(.*?)</sub>").unwrap();
    let result = sub_re.replace_all(&result, |caps: &regex::Captures| {
        format!("$_{{{}}}$", &caps[1])
    });
    // strip remaining HTML tags
    let tag_re = Regex::new(r"<[^>]+>").unwrap();
    let result = tag_re.replace_all(&result, "").trim().to_string();
    // Escape bare < and > outside math delimiters as $<$ / $>$ so LaTeX renders them
    let mut out = String::with_capacity(result.len());
    let bytes = result.as_bytes();
    let mut i = 0;
    let mut in_math = false;
    while i < bytes.len() {
        // Detect \( \) \[ \] math boundaries
        if i + 1 < bytes.len() && bytes[i] == b'\\' {
            match bytes[i + 1] {
                b'(' | b'[' => { in_math = true;  out.push('\\'); out.push(bytes[i+1] as char); i += 2; continue; }
                b')' | b']' => { in_math = false; out.push('\\'); out.push(bytes[i+1] as char); i += 2; continue; }
                _ => {}
            }
        }
        if !in_math && bytes[i] == b'<' { out.push_str("$<$"); i += 1; continue; }
        if !in_math && bytes[i] == b'>' { out.push_str("$>$"); i += 1; continue; }
        out.push(bytes[i] as char);
        i += 1;
    }
    out
}

fn bank_meta(data: &Value) -> Value {
    let info = data.get("bank_info").and_then(|v| v.as_object()).map(|m| Value::Object(m.clone())).unwrap_or(json!({}));
    let qs = data.get("questions").and_then(|v| v.as_array()).cloned().unwrap_or_default();

    let mut type_counts: HashMap<String, i64> = HashMap::new();
    for q in &qs {
        if q.is_object() {
            let t = get_qtype(q);
            *type_counts.entry(t).or_insert(0) += 1;
        }
    }

    // first-question text snippet for card thumbnail
    let mut preview = String::new();
    if let Some(q0) = qs.first() {
        if q0.is_object() {
            let qtype = get_qtype(q0);
            let text = q0.get(&qtype)
                .and_then(|qd| qd.get("text"))
                .and_then(|t| t.as_str())
                .unwrap_or("")
                .to_string();
            let clean = strip_tags(&text);
            if clean.len() > 220 {
                let mut end = 220;
                while !clean.is_char_boundary(end) { end -= 1; }
                preview = format!("{}…", &clean[..end]);
            } else {
                preview = clean;
            }
        }
    }

    let type_counts_val: Value = type_counts.iter()
        .map(|(k, v)| (k.clone(), json!(v)))
        .collect::<serde_json::Map<_, _>>()
        .into();

    json!({
        "title": info.get("title").and_then(|v| v.as_str()).unwrap_or("Untitled Bank"),
        "bank_id": info.get("bank_id").and_then(|v| v.as_str()).unwrap_or(""),
        "description": info.get("description").and_then(|v| v.as_str()).unwrap_or(""),
        "authors": info.get("authors").cloned().unwrap_or(json!([])),
        "date_created": info.get("date created").or_else(|| info.get("date_created"))
            .and_then(|v| v.as_str()).unwrap_or(""),
        "lo": info.get("learning objectives").or_else(|| info.get("learning_objectives"))
            .cloned().unwrap_or(json!([])),
        "q_count": qs.len(),
        "q_types": type_counts_val,
        "preview": preview,
    })
}

fn is_bank(data: &Value) -> bool {
    data.get("questions").and_then(|v| v.as_array()).is_some()
}

fn load_yaml(path: &Path) -> Option<Value> {
    let content = std::fs::read_to_string(path).ok()?;
    serde_yaml::from_str(&content).ok()
}

fn extract_mc_answers(answers: &Value) -> Vec<(usize, String, bool)> {
    let mut result = Vec::new();
    if let Some(arr) = answers.as_array() {
        for (j, a) in arr.iter().enumerate() {
            if !a.is_object() {
                result.push((j, a.as_str().unwrap_or("").to_string(), false));
                continue;
            }
            let inner = a.get("answer");
            if let Some(inner_obj) = inner.and_then(|v| v.as_object()) {
                let text = inner_obj.get("text").and_then(|v| v.as_str()).unwrap_or("").to_string();
                let correct = inner_obj.get("correct").and_then(|v| v.as_bool()).unwrap_or(false);
                result.push((j, text, correct));
            } else if a.get("text").is_some() {
                let text = a.get("text").and_then(|v| v.as_str()).unwrap_or("").to_string();
                let correct = a.get("correct").and_then(|v| v.as_bool()).unwrap_or(false);
                result.push((j, text, correct));
            } else {
                result.push((j, a.to_string(), false));
            }
        }
    }
    result
}

fn version_label(v: i64) -> String {
    if v >= 1 && v <= 26 {
        ((b'A' + (v - 1) as u8) as char).to_string()
    } else {
        v.to_string()
    }
}

/// Simple seeded Fisher-Yates shuffle — deterministic per (version, question)
fn seeded_shuffle<T>(items: &mut Vec<T>, seed: u64) {
    let n = items.len();
    if n <= 1 { return; }
    let mut rng = seed;
    for i in (1..n).rev() {
        rng = rng.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let j = (rng >> 33) as usize % (i + 1);
        items.swap(i, j);
    }
}

/// Returns true if any answer choice has lock:true (meaning don't shuffle)
fn answers_have_lock(answers: &Value) -> bool {
    answers.as_array().map(|arr| arr.iter().any(|a| {
        a.get("answer").and_then(|inner| inner.get("lock")).and_then(|l| l.as_bool()).unwrap_or(false)
    })).unwrap_or(false)
}

fn strip_round_instruction(text: &str) -> String {
    // Strip trailing "Round your answer..." rounding instructions from numerical questions
    if let Some(pos) = text.rfind("Round") {
        let before_trimmed = text[..pos].trim_end();
        if pos == 0 || before_trimmed.ends_with(|c: char| matches!(c, '.' | '?' | '!')) {
            return before_trimmed.to_string();
        }
    }
    text.to_string()
}

fn tol_str(tol: &str, margin_type: &str) -> String {
    if tol.is_empty() {
        return String::new();
    }
    let pct = if margin_type == "percent" { r"\%" } else { "" };
    format!(r" \pm {}{}", tol, pct)
}

fn type_label(qtype: &str) -> &str {
    match qtype {
        "numerical" => "Numerical",
        "multiple_choice" => "Multiple Choice",
        "multiple_answers" => "Multiple Answer",
        "true_false" => "True / False",
        "essay" => "Essay",
        "formula" => "Formula",
        "categorization" => "Categorization",
        "fill_in_multiple_blanks" => "Fill-in-the-Blank",
        "ordering" => "Ordering",
        "hot_spot" => "Hot Spot",
        _ => qtype,
    }
}

fn resolve_figure(qdata: &Value, bank_dir: &Path) -> Option<PathBuf> {
    let fig = qdata.get("figure").and_then(|v| v.as_str())?;
    let basename = Path::new(fig).file_name()?;
    let candidates = [
        bank_dir.join(fig),
        bank_dir.join("Figures").join(basename),
        bank_dir.join("Figure").join(basename),
        bank_dir.join("figures").join(basename),
        bank_dir.join("figure").join(basename),
        bank_dir.join("Images").join(basename),
        bank_dir.join("images").join(basename),
    ];
    candidates.into_iter().find(|p| p.exists())
}

fn figure_to_base64(path: &Path) -> Option<String> {
    let bytes = std::fs::read(path).ok()?;
    let mime = match path.extension().and_then(|e| e.to_str()) {
        Some("png")        => "image/png",
        Some("jpg") | Some("jpeg") => "image/jpeg",
        Some("gif")        => "image/gif",
        Some("svg")        => "image/svg+xml",
        _                  => "image/png",
    };
    let b64 = base64::engine::general_purpose::STANDARD.encode(&bytes);
    Some(format!("data:{};base64,{}", mime, b64))
}

fn q_to_latex(q: &Value, num: usize, bank_dir: &Path, version: i64) -> String {
    let qtype = get_qtype(q);
    let qdata = q.get(&qtype).cloned().unwrap_or(json!({}));
    let raw_text = qdata.get("text").and_then(|v| v.as_str()).unwrap_or("");
    let mut body = html2tex(&latex_to_html(raw_text));
    if qtype == "numerical" {
        body = strip_round_instruction(&body);
        body.push_str("\n\nPlease show your work in the space below.");
    }
    let fig_latex = resolve_figure(&qdata, bank_dir)
        .map(|p| format!("\n\\begin{{center}}\\includegraphics[width=0.8\\linewidth,keepaspectratio]{{{}}}\\end{{center}}\n",
            p.to_string_lossy()))
        .unwrap_or_default();
    let mut out = vec![
        format!("\\question[3] % Q{}", num),
        body,
        fig_latex,
        String::new(),
    ];

    if qtype == "numerical" {
        out.push(r"\vspace{4mm}\underline{\hspace{4cm}} \textit{(Numerical)}".to_string());
        out.push(r"\vspace{6cm}".to_string());
        out.push(String::new());
    } else if qtype == "multiple_choice" || qtype == "multiple_answers" {
        out.push("\\begin{choices}".to_string());
        let answers_val = qdata.get("answers").cloned().unwrap_or(json!([]));
        let mut answer_list = extract_mc_answers(&answers_val);
        if !answers_have_lock(&answers_val) {
            seeded_shuffle(&mut answer_list, version as u64 * 10000 + num as u64);
        }
        for (_, atxt, correct) in &answer_list {
            let cmd = if *correct { "\\CorrectChoice" } else { "\\choice" };
            out.push(format!("  {} {}", cmd, html2tex(&atxt)));
        }
        out.push("\\end{choices}".to_string());
    } else if qtype == "true_false" {
        out.push("\\begin{choices}".to_string());
        out.push("  \\choice True".to_string());
        out.push("  \\choice False".to_string());
        out.push("\\end{choices}".to_string());
    } else if qtype == "essay" {
        out.push("\\vspace{4cm}".to_string());
    }
    out.push(String::new());
    out.join("\n")
}

fn pick_questions(cart: &Value, version: i64) -> Vec<Value> {
    let mut qs = Vec::new();
    if let Some(arr) = cart.as_array() {
        for item in arr {
            let raw = item.get("rawData").cloned().unwrap_or(json!({}));
            let questions = raw.get("questions").and_then(|v| v.as_array()).cloned().unwrap_or_default();
            if questions.is_empty() {
                continue;
            }
            let qn = item.get("qn").and_then(|v| v.as_i64()).unwrap_or(1).max(1) as usize;
            let n = questions.len();
            let start = (((version - 1) as usize * qn) % n) as usize;
            for i in 0..qn {
                qs.push(questions[(start + i) % n].clone());
            }
        }
    }
    qs
}

// ══════════════════════════════════════════════════════════════════════════════
// Tauri commands
// ══════════════════════════════════════════════════════════════════════════════

#[tauri::command]
fn scan_repo(path: String) -> Result<Value, String> {
    let root = Path::new(&path);
    if !root.is_dir() {
        return Err("Path not found".to_string());
    }

    let mut result: serde_json::Map<String, Value> = serde_json::Map::new();

    let mut course_entries: Vec<_> = std::fs::read_dir(root)
        .map_err(|e| e.to_string())?
        .filter_map(|e| e.ok())
        .collect();
    course_entries.sort_by_key(|e| e.file_name());

    for course_entry in course_entries {
        let course_name = course_entry.file_name().to_string_lossy().to_string();
        if !course_entry.path().is_dir() { continue; }
        if SKIP_COURSES.contains(&course_name.as_str()) { continue; }
        if course_name.starts_with('.') { continue; }

        let mut course_topics: serde_json::Map<String, Value> = serde_json::Map::new();

        let mut topic_entries: Vec<_> = std::fs::read_dir(course_entry.path())
            .map_err(|e| e.to_string())?
            .filter_map(|e| e.ok())
            .collect();
        topic_entries.sort_by_key(|e| e.file_name());

        for topic_entry in topic_entries {
            let topic_name = topic_entry.file_name().to_string_lossy().to_string();
            if !topic_entry.path().is_dir() { continue; }
            if topic_name.starts_with('.') { continue; }

            let mut banks: Vec<Value> = Vec::new();

            // Walk the topic directory recursively
            let mut walk_stack = vec![topic_entry.path()];
            while let Some(dir) = walk_stack.pop() {
                let mut dir_entries: Vec<_> = match std::fs::read_dir(&dir) {
                    Ok(rd) => rd.filter_map(|e| e.ok()).collect(),
                    Err(_) => continue,
                };
                dir_entries.sort_by_key(|e| e.file_name());

                let mut subdirs = Vec::new();
                let mut files = Vec::new();
                for entry in dir_entries {
                    if entry.path().is_dir() {
                        let name = entry.file_name().to_string_lossy().to_string();
                        if !SKIP_DIRS.contains(&name.as_str()) {
                            subdirs.push(entry.path());
                        }
                    } else {
                        files.push(entry.path());
                    }
                }

                for fp in &files {
                    let ext = fp.extension().and_then(|e| e.to_str()).unwrap_or("");
                    if ext != "yaml" && ext != "yml" { continue; }

                    // check if any component of the relative path is in SKIP_DIRS
                    let rel = fp.strip_prefix(&topic_entry.path()).unwrap_or(fp);
                    let skip = rel.components().any(|c| {
                        let s = c.as_os_str().to_string_lossy();
                        SKIP_DIRS.contains(&s.as_ref())
                    });
                    if skip { continue; }

                    if let Some(data) = load_yaml(fp) {
                        if is_bank(&data) {
                            let status = data.get("bank_info")
                                .and_then(|i| i.get("status"))
                                .and_then(|s| s.as_str())
                                .unwrap_or("");
                            if status == "draft" || status == "deprecated" {
                                continue;
                            }
                            let meta = bank_meta(&data);
                            banks.push(json!({
                                "path": fp.to_string_lossy(),
                                "meta": meta,
                            }));
                        }
                    }
                }

                // push subdirs for further traversal (sorted, reversed so pop gives sorted order)
                subdirs.reverse();
                walk_stack.extend(subdirs);
            }

            if !banks.is_empty() {
                course_topics.insert(topic_name, json!(banks));
            }
        }

        if !course_topics.is_empty() {
            result.insert(course_name, Value::Object(course_topics));
        }
    }

    Ok(json!({"data": result}))
}

#[tauri::command]
fn bank_data(path: String) -> Result<Value, String> {
    let fp = Path::new(&path);
    let data = load_yaml(fp).ok_or("Failed to load YAML")?;
    if !is_bank(&data) {
        return Err("Invalid bank".to_string());
    }

    let bank_dir = fp.parent().unwrap_or(Path::new("/"));
    let mut questions: Vec<Value> = Vec::new();

    for q in data.get("questions").and_then(|v| v.as_array()).cloned().unwrap_or_default() {
        let qtype = get_qtype(&q);
        let qdata = q.get(&qtype).cloned().unwrap_or(json!({}));
        let body = latex_to_html(qdata.get("text").and_then(|v| v.as_str()).unwrap_or(""));

        let mut answers: Vec<Value> = Vec::new();
        if qtype == "multiple_choice" || qtype == "multiple_answers" {
            let ans_val = qdata.get("answers").cloned().unwrap_or(json!([]));
            for (j, atxt, correct) in extract_mc_answers(&ans_val) {
                answers.push(json!({
                    "label": (b'A' + j as u8) as char,
                    "text": latex_to_html(&atxt),
                    "correct": correct,
                }));
            }
        } else if qtype == "numerical" {
            let ans = qdata.get("answer").cloned().unwrap_or(json!({}));
            let val = ans.get("value").map(|v| match v {
                Value::String(s) => s.clone(),
                other => other.to_string(),
            }).unwrap_or_default();
            let tol = ans.get("tolerance").and_then(|v| v.as_str()).unwrap_or("").to_string();
            let mt = ans.get("margin_type").and_then(|v| v.as_str()).unwrap_or("").to_string();
            let ts = if !tol.is_empty() {
                let pct = if mt == "percent" { "%" } else { "" };
                format!(" ± {}{}", tol, pct)
            } else {
                String::new()
            };
            if !val.is_empty() && val != "null" {
                answers.push(json!({
                    "label": "Answer",
                    "text": format!("{}{}", val, ts),
                    "correct": true,
                }));
            }
        } else if qtype == "true_false" {
            let av = qdata.get("answer").and_then(|v| v.as_bool()).unwrap_or(false);
            answers.push(json!({
                "label": "Answer",
                "text": if av { "True" } else { "False" },
                "correct": true,
            }));
        }

        let fb = qdata.get("feedback").cloned().unwrap_or(json!({}));
        let solution = latex_to_html(fb.get("general").and_then(|v| v.as_str()).unwrap_or(""));

        // figure resolution — use the same comprehensive resolver as the LaTeX export
        let fig_url = resolve_figure(&qdata, bank_dir)
            .and_then(|p| figure_to_base64(&p));

        let q_count = questions.len() + 1;
        questions.push(json!({
            "id": qdata.get("id").and_then(|v| v.as_str()).unwrap_or(&format!("q{}", q_count)),
            "title": qdata.get("title").and_then(|v| v.as_str()).unwrap_or(""),
            "type": qtype,
            "type_label": type_label(&qtype),
            "body": body,
            "answers": answers,
            "solution": solution,
            "fig_url": fig_url,
        }));
    }

    let meta = bank_meta(&data);
    Ok(json!({
        "questions": questions,
        "meta": meta,
        "rawData": data,
    }))
}

#[tauri::command]
fn export_tex(cart: Value, version: i64, title: String, kind: String) -> Result<String, String> {
    if kind == "key" {
        Ok(build_key_latex(&cart, version, &title))
    } else {
        Ok(build_exam_latex(&cart, version, &title))
    }
}

#[tauri::command]
fn export_html(cart: Value, version: i64, title: String, include_answers: bool) -> Result<String, String> {
    Ok(build_pdf_html(&cart, version, &title, include_answers))
}

// ══════════════════════════════════════════════════════════════════════════════
// Export builders
// ══════════════════════════════════════════════════════════════════════════════

fn build_exam_latex(cart: &Value, version: i64, title: &str) -> String {
    let mut qs_with_dir: Vec<(Value, PathBuf)> = Vec::new();
    let mut graphicspaths: Vec<String> = Vec::new();
    if let Some(arr) = cart.as_array() {
        for item in arr {
            let raw = item.get("rawData").cloned().unwrap_or(json!({}));
            let questions = raw.get("questions").and_then(|v| v.as_array()).cloned().unwrap_or_default();
            if questions.is_empty() { continue; }
            let bank_path = item.get("path").and_then(|v| v.as_str()).unwrap_or("");
            let bank_dir = Path::new(bank_path).parent().unwrap_or(Path::new(".")).to_path_buf();
            let dir_str = format!("{{{}/}}", bank_dir.to_string_lossy().replace('\\', "/"));
            if !graphicspaths.contains(&dir_str) { graphicspaths.push(dir_str); }
            let figs_dir = bank_dir.join("Figures");
            if figs_dir.is_dir() {
                let fd = format!("{{{}/}}", figs_dir.to_string_lossy().replace('\\', "/"));
                if !graphicspaths.contains(&fd) { graphicspaths.push(fd); }
            }
            let qn = item.get("qn").and_then(|v| v.as_i64()).unwrap_or(1).max(1) as usize;
            let n = questions.len();
            let start = (((version - 1) as usize * qn) % n) as usize;
            for i in 0..qn {
                qs_with_dir.push((questions[(start + i) % n].clone(), bank_dir.clone()));
            }
        }
    }
    let body: String = qs_with_dir.iter().enumerate()
        .map(|(i, (q, dir))| q_to_latex(q, i + 1, dir, version))
        .collect::<Vec<_>>()
        .join("\n\n");
    let graphicspath_line = if !graphicspaths.is_empty() {
        format!("\\graphicspath{{{}}}\n", graphicspaths.join(""))
    } else { String::new() };

    format!(
        r"\documentclass[12pt,addpoints]{{exam}}
\usepackage{{amsmath,amssymb,physics,geometry,microtype,graphicx}}
\geometry{{margin=1in}}
{}%\printanswers  % uncomment to show answers (e.g. for instructor copy)

\begin{{document}}
\begin{{center}}
  {{\Large\bfseries {}}}\\[4pt]
  Version {} \quad \today
\end{{center}}
\vspace{{2mm}}\hrule\vspace{{2mm}}
Name:\underline{{\hspace{{8cm}}}} \hfill Score: \underline{{\hspace{{2cm}}}} / \numpoints
\vspace{{6mm}}
\begin{{questions}}
{}
\end{{questions}}
\end{{document}}
",
        graphicspath_line, title, version_label(version), body
    )
}

fn build_key_latex(cart: &Value, version: i64, title: &str) -> String {
    let mut rows: Vec<String> = Vec::new();

    if let Some(arr) = cart.as_array() {
        for item in arr {
            let raw = item.get("rawData").cloned().unwrap_or(json!({}));
            let questions = raw.get("questions").and_then(|v| v.as_array()).cloned().unwrap_or_default();
            if questions.is_empty() { continue; }

            let qn = item.get("qn").and_then(|v| v.as_i64()).unwrap_or(1).max(1) as usize;
            let n = questions.len();
            let start = (((version - 1) as usize * qn) % n) as usize;

            for i in 0..qn {
                let q = &questions[(start + i) % n];
                let qtype = get_qtype(q);
                let qdata = q.get(&qtype).cloned().unwrap_or(json!({}));
                let q_num = rows.len() + 1;

                if qtype == "numerical" {
                    let ans = qdata.get("answer").cloned().unwrap_or(json!({}));
                    let val = ans.get("value").map(|v| match v {
                        Value::String(s) => s.clone(),
                        other => other.to_string(),
                    }).unwrap_or_else(|| "?".to_string());
                    let tol = ans.get("tolerance").and_then(|v| v.as_str()).unwrap_or("");
                    let margin_type = ans.get("margin_type").and_then(|v| v.as_str()).unwrap_or("");
                    let ts = tol_str(tol, margin_type);
                    rows.push(format!(r"  \item ${}{}$", val, ts));
                } else if qtype == "multiple_choice" || qtype == "multiple_answers" {
                    let ans_val = qdata.get("answers").cloned().unwrap_or(json!([]));
                    let mut answer_list = extract_mc_answers(&ans_val);
                    if !answers_have_lock(&ans_val) {
                        seeded_shuffle(&mut answer_list, version as u64 * 10000 + q_num as u64);
                    }
                    let correct_letters: Vec<String> = answer_list
                        .iter()
                        .enumerate()
                        .filter(|(_, (_, _, is_correct))| *is_correct)
                        .map(|(j, _)| ((b'A' + j as u8) as char).to_string())
                        .collect();
                    let ans_str = if correct_letters.is_empty() { "?".to_string() } else { correct_letters.join(", ") };
                    rows.push(format!(r"  \item {}", ans_str));
                } else if qtype == "true_false" {
                    let av = qdata.get("answer").and_then(|v| v.as_bool()).unwrap_or(false);
                    rows.push(format!(r"  \item {}", if av { "True" } else { "False" }));
                } else {
                    rows.push(r"  \item [See rubric]".to_string());
                }
            }
        }
    }

    let rows_str = rows.join("\n");
    format!(
        r"\documentclass{{article}}
\usepackage{{amsmath,geometry}}
\geometry{{margin=1in}}
\begin{{document}}
\section*{{{} --- Version {} --- Answer Key}}
\begin{{enumerate}}
{}
\end{{enumerate}}
\end{{document}}
",
        title, version_label(version), rows_str
    )
}

fn build_pdf_html(cart: &Value, version: i64, title: &str, include_answers: bool) -> String {
    let mut parts: Vec<String> = Vec::new();
    let mut q_num = 0usize;

    if let Some(arr) = cart.as_array() {
        for item in arr {
            let raw = item.get("rawData").cloned().unwrap_or(json!({}));
            let questions = raw.get("questions").and_then(|v| v.as_array()).cloned().unwrap_or_default();
            if questions.is_empty() { continue; }

            let qn = item.get("qn").and_then(|v| v.as_i64()).unwrap_or(1).max(1) as usize;
            let n = questions.len();
            let start = (((version - 1) as usize * qn) % n) as usize;

            let bank_path = item.get("path").and_then(|v| v.as_str()).unwrap_or("");
            let bank_dir = Path::new(bank_path).parent().unwrap_or(Path::new("."));

            for i in 0..qn {
                let q = &questions[(start + i) % n];
                let qtype = get_qtype(q);
                let qdata = q.get(&qtype).cloned().unwrap_or(json!({}));
                let body = latex_to_html(qdata.get("text").and_then(|v| v.as_str()).unwrap_or(""));
                let fig_html = resolve_figure(&qdata, bank_dir)
                    .and_then(|p| figure_to_base64(&p).map(|src| {
                        format!("<div class=\"q-fig\"><img src=\"{}\" style=\"max-width:100%;margin:.4cm 0;\"></div>", src)
                    }))
                    .unwrap_or_default();

                let mut ans_html = String::new();
                if qtype == "multiple_choice" || qtype == "multiple_answers" {
                    let ans_val = qdata.get("answers").cloned().unwrap_or(json!([]));
                    let mut answer_list = extract_mc_answers(&ans_val);
                    if !answers_have_lock(&ans_val) {
                        seeded_shuffle(&mut answer_list, version as u64 * 10000 + q_num as u64);
                    }
                    for (j, (_, atxt, correct)) in answer_list.iter().enumerate() {
                        let cls = if include_answers && *correct { "ans-ok" } else { "ans-opt" };
                        ans_html.push_str(&format!(
                            "<div class=\"{}\"><b>{}.</b> {}</div>",
                            cls,
                            (b'A' + j as u8) as char,
                            latex_to_html(atxt)
                        ));
                    }
                } else if qtype == "numerical" {
                    if include_answers {
                        let ans = qdata.get("answer").cloned().unwrap_or(json!({}));
                        let val = ans.get("value").map(|v| match v {
                            Value::String(s) => s.clone(),
                            other => other.to_string(),
                        }).unwrap_or_default();
                        let tol = ans.get("tolerance").and_then(|v| v.as_str()).unwrap_or("").to_string();
                        let mt = ans.get("margin_type").and_then(|v| v.as_str()).unwrap_or("").to_string();
                        let ts = if !tol.is_empty() {
                            let pct = if mt == "percent" { "%" } else { "" };
                            format!(" &plusmn; {}{}", tol, pct)
                        } else {
                            String::new()
                        };
                        if !val.is_empty() && val != "null" {
                            ans_html = format!("<div class=\"ans-ok\"><b>Answer:</b> {}{}</div>", val, ts);
                        }
                    } else {
                        ans_html = "<div class=\"ans-space\"></div>".to_string();
                    }
                } else if qtype == "true_false" {
                    if include_answers {
                        let av = qdata.get("answer").and_then(|v| v.as_bool()).unwrap_or(false);
                        ans_html = format!("<div class=\"ans-ok\"><b>Answer:</b> {}</div>", if av { "True" } else { "False" });
                    } else {
                        ans_html = "<div class=\"ans-opt\"><b>A.</b> True</div><div class=\"ans-opt\"><b>B.</b> False</div>".to_string();
                    }
                } else if !include_answers {
                    ans_html = "<div class=\"ans-space\" style=\"height:3cm\"></div>".to_string();
                }

                q_num += 1;
                let needs_work_area = !include_answers
                    && !matches!(qtype.as_str(), "multiple_choice" | "multiple_answers" | "true_false");
                let work = if needs_work_area {
                    "<div class=\"work-area\"><span class=\"work-lbl\">Work</span></div>".to_string()
                } else {
                    String::new()
                };

                parts.push(format!(
                    "<div class=\"sheet\"><div class=\"q-num\">Question {}</div><div class=\"q-body\">{}</div>{}<div class=\"ans-list\">{}</div>{}</div>",
                    q_num, body, fig_html, ans_html, work
                ));
            }
        }
    }

    let label = if include_answers { " \u{2014} Answer Key" } else { "" };
    let parts_html = parts.join("\n");

    format!(
        r#"<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} &#8212; Version {version}{label}</title>
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
.work-area{{border:1.5px dashed #d5d2c8;border-radius:7px;padding:.4cm .6cm;min-height:7cm;}}
.work-lbl{{font-size:7pt;color:#c5c2b8;text-transform:uppercase;letter-spacing:.1em;}}
.q-fig img{{max-width:100%;max-height:7cm;display:block;margin:.3cm auto;}}
.katex-display{{margin:.4cm 0;overflow-x:auto;}}
@page{{size:letter;margin:2cm 2.4cm;}}
@media print{{
  body{{background:#fff;}}
  .sheet{{box-shadow:none;margin:0 !important;max-width:none;padding:0;border-radius:0 !important;border-top:none !important;break-after:page;page-break-after:always;}}
  .sheet:last-child{{break-after:auto;page-break-after:auto;}}
  .work-area{{min-height:6cm;}}
  .q-fig img{{max-height:5cm;}}
}}
</style>
</head>
<body>
<div class="sheet">
<h1>{title} &#8212; Version {version}{label}</h1>
<div class="meta">ESTELA Exam Builder &middot; UCF / NSF-2421299</div>
<hr>
<div class="name-row">Name:&nbsp;<div class="line"></div>&nbsp;&nbsp;&nbsp;Score:&nbsp;<div class="score"></div></div>
</div>
{parts_html}
</body>
</html>"#,
        title = title,
        version = version_label(version),
        label = label,
        parts_html = parts_html,
    )
}

// ══════════════════════════════════════════════════════════════════════════════
// Bundle export
// ══════════════════════════════════════════════════════════════════════════════

#[tauri::command]
fn export_exam_bundle(cart: Value, versions: i64, title: String, dest_folder: String) -> Result<String, String> {
    let dest = PathBuf::from(&dest_folder);
    let exam_dir = dest.join("Exams");
    let key_dir  = dest.join("Keys");
    let img_dir  = dest.join("Images");
    std::fs::create_dir_all(&exam_dir).map_err(|e| e.to_string())?;
    std::fs::create_dir_all(&key_dir).map_err(|e| e.to_string())?;
    std::fs::create_dir_all(&img_dir).map_err(|e| e.to_string())?;

    // Copy all referenced images (deduplicated by filename)
    let mut images_copied = 0usize;
    if let Some(arr) = cart.as_array() {
        for item in arr {
            let bank_path = item.get("path").and_then(|v| v.as_str()).unwrap_or("");
            let bank_dir = Path::new(bank_path).parent().unwrap_or(Path::new("."));
            let raw = item.get("rawData").cloned().unwrap_or(json!({}));
            for q in raw.get("questions").and_then(|v| v.as_array()).cloned().unwrap_or_default() {
                let qtype = get_qtype(&q);
                let qdata = q.get(&qtype).cloned().unwrap_or(json!({}));
                if let Some(src) = resolve_figure(&qdata, bank_dir) {
                    let fname = src.file_name().unwrap_or_default();
                    let dst = img_dir.join(fname);
                    if !dst.exists() {
                        std::fs::copy(&src, &dst).map_err(|e| e.to_string())?;
                        images_copied += 1;
                    }
                }
            }
        }
    }

    // Generate all exam + key tex files; rewrite graphicspath to point at ../Images/
    let graphicspath_re = Regex::new(r"\\graphicspath\{[^}]*\}").unwrap();
    for v in 1..=versions {
        let exam_tex = build_exam_latex(&cart, v, &title);
        let exam_tex = graphicspath_re.replace(&exam_tex, r"\graphicspath{{../Images/}}").to_string();
        let key_tex  = build_key_latex(&cart, v, &title);
        std::fs::write(exam_dir.join(format!("exam_{}.tex", version_label(v))), &exam_tex).map_err(|e| e.to_string())?;
        std::fs::write(key_dir.join(format!("key_{}.tex",  version_label(v))), &key_tex).map_err(|e| e.to_string())?;
    }

    Ok(format!(
        "Exported {} version{} + {} image{} to {}",
        versions, if versions == 1 { "" } else { "s" },
        images_copied, if images_copied == 1 { "" } else { "s" },
        dest_folder
    ))
}

// ══════════════════════════════════════════════════════════════════════════════
// Remote download commands
// ══════════════════════════════════════════════════════════════════════════════

const UPSTREAM_REPO: &str = "Zhongzhou/ESTELA-physics-problem-bank";

#[tauri::command]
async fn fetch_remote_courses() -> Result<Vec<String>, String> {
    let client = reqwest::Client::builder()
        .user_agent("ESTELA-Exam-Builder")
        .build()
        .map_err(|e| e.to_string())?;

    let url = format!(
        "https://api.github.com/repos/{}/contents/",
        UPSTREAM_REPO
    );
    let resp: Vec<Value> = client
        .get(&url)
        .header("Accept", "application/vnd.github.v3+json")
        .send()
        .await
        .map_err(|e| format!("Network error: {}", e))?
        .json()
        .await
        .map_err(|e| format!("Parse error: {}", e))?;

    let skip = SKIP_COURSES;
    let courses: Vec<String> = resp
        .iter()
        .filter(|item| item.get("type").and_then(|t| t.as_str()) == Some("dir"))
        .filter_map(|item| item.get("name").and_then(|n| n.as_str()).map(String::from))
        .filter(|name| !skip.contains(&name.as_str()) && !name.starts_with('.'))
        .collect();

    Ok(courses)
}

#[tauri::command]
async fn download_courses(courses: Vec<String>, dest_folder: String) -> Result<String, String> {
    let client = reqwest::Client::builder()
        .user_agent("ESTELA-Exam-Builder")
        .build()
        .map_err(|e| e.to_string())?;

    let zip_url = format!(
        "https://github.com/{}/archive/refs/heads/main.zip",
        UPSTREAM_REPO
    );
    let bytes = client
        .get(&zip_url)
        .send()
        .await
        .map_err(|e| format!("Download error: {}", e))?
        .bytes()
        .await
        .map_err(|e| format!("Read error: {}", e))?;

    let cursor = std::io::Cursor::new(bytes);
    let mut archive = zip::ZipArchive::new(cursor).map_err(|e| e.to_string())?;

    // Detect the root prefix from the first ZIP entry (e.g. "ESTELA-physics-problem-bank-main/")
    let prefix = (0..archive.len())
        .find_map(|i| {
            let file = archive.by_index(i).ok()?;
            let name = file.name().to_string();
            name.find('/').map(|p| name[..=p].to_string())
        })
        .unwrap_or_default();

    let dest = PathBuf::from(&dest_folder);
    let mut extracted = 0usize;

    for i in 0..archive.len() {
        let mut file = archive.by_index(i).map_err(|e| e.to_string())?;
        let raw_name = file.name().to_string();

        let rel = match raw_name.strip_prefix(&prefix) {
            Some(r) if !r.is_empty() => r.to_string(),
            _ => continue,
        };

        // Only extract entries belonging to a selected course
        let first = rel.split('/').next().unwrap_or("");
        if !courses.contains(&first.to_string()) {
            continue;
        }

        let out_path = dest.join(&rel);

        if raw_name.ends_with('/') {
            std::fs::create_dir_all(&out_path).map_err(|e| e.to_string())?;
        } else {
            if let Some(parent) = out_path.parent() {
                std::fs::create_dir_all(parent).map_err(|e| e.to_string())?;
            }
            let mut content = Vec::new();
            file.read_to_end(&mut content).map_err(|e| e.to_string())?;
            std::fs::write(&out_path, content).map_err(|e| e.to_string())?;
            extracted += 1;
        }
    }

    Ok(format!("Extracted {} files to {}", extracted, dest_folder))
}

// ══════════════════════════════════════════════════════════════════════════════
// Main
// ══════════════════════════════════════════════════════════════════════════════

#[tauri::command]
fn save_tex(content: String, filename: String, folder: Option<String>) -> Result<String, String> {
    let dir = if let Some(f) = folder {
        PathBuf::from(f)
    } else {
        dirs::download_dir()
            .or_else(|| dirs::home_dir().map(|h| h.join("Downloads")))
            .unwrap_or_else(std::env::temp_dir)
    };
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let path = dir.join(&filename);
    std::fs::write(&path, content).map_err(|e| e.to_string())?;
    Ok(path.to_string_lossy().to_string())
}

#[tauri::command]
fn save_tex_batch(files: Vec<(String, String)>, folder: String) -> Result<Vec<String>, String> {
    let dir = PathBuf::from(&folder);
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let mut saved = Vec::new();
    for (filename, content) in files {
        let path = dir.join(&filename);
        std::fs::write(&path, &content).map_err(|e| e.to_string())?;
        saved.push(path.to_string_lossy().to_string());
    }
    Ok(saved)
}

#[tauri::command]
fn open_preview(html: String) -> Result<(), String> {
    let dir = std::env::temp_dir().join("estela");
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let path = dir.join("preview.html");
    std::fs::write(&path, html).map_err(|e| e.to_string())?;
    open::that(path).map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .register_uri_scheme_protocol("figure", |_app, request| {
            let path_str = request.uri().path();
            // On some platforms the path starts with //host or ///path
            // Normalize by stripping leading slashes beyond the first
            let path_str = path_str.trim_start_matches('/');
            let path = std::path::Path::new("/").join(path_str);
            match std::fs::read(&path) {
                Ok(bytes) => {
                    let mime = match path.extension().and_then(|e| e.to_str()) {
                        Some("png") => "image/png",
                        Some("jpg") | Some("jpeg") => "image/jpeg",
                        Some("gif") => "image/gif",
                        Some("svg") => "image/svg+xml",
                        _ => "application/octet-stream",
                    };
                    http::Response::builder()
                        .status(200)
                        .header("Content-Type", mime)
                        .header("Access-Control-Allow-Origin", "*")
                        .body(bytes)
                        .unwrap()
                }
                Err(_) => http::Response::builder()
                    .status(404)
                    .body(vec![])
                    .unwrap(),
            }
        })
        .invoke_handler(tauri::generate_handler![scan_repo, bank_data, export_tex, export_html, open_preview, save_tex, save_tex_batch, export_exam_bundle, fetch_remote_courses, download_courses])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
