"""
viewer.py — YAML Problem Bank Viewer
Single-file tkinter viewer for ESTELA physics problem bank YAML files.
"""
import re
import tkinter as tk
from tkinter import filedialog, font as tkfont
from html.parser import HTMLParser
import zipfile
import tempfile
import os

try:
    import yaml
except ImportError:
    yaml = None

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ---------------------------------------------------------------------------
# Content parsing
# ---------------------------------------------------------------------------

class TableParser(HTMLParser):
    """Parse an HTML <table> into a list-of-rows (each row is a list of str)."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self._current_row = None
        self._current_cell = None
        self._in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._current_row = []
        elif tag in ("td", "th"):
            self._current_cell = []
            self._in_cell = True

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self._in_cell = False
            if self._current_row is not None and self._current_cell is not None:
                self._current_row.append("".join(self._current_cell).strip())
            self._current_cell = None
        elif tag == "tr":
            if self._current_row is not None:
                self.rows.append(self._current_row)
            self._current_row = None

    def handle_data(self, data):
        if self._in_cell and self._current_cell is not None:
            self._current_cell.append(data)


def parse_content(text):
    """
    Parse mixed content into a list of tagged segments:
      ('text',  str)
      ('latex', str)
      ('table', list[list[str]])
    """
    segments = []
    pattern = re.compile(
        r'<latex>(.*?)</latex>|<table>(.*?)</table>',
        re.DOTALL | re.IGNORECASE,
    )
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            segments.append(('text', text[pos:m.start()]))
        if m.group(1) is not None:
            segments.append(('latex', m.group(1)))
        else:
            tp = TableParser()
            tp.feed(m.group(2))
            segments.append(('table', tp.rows))
        pos = m.end()
    if pos < len(text):
        segments.append(('text', text[pos:]))
    return segments


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class BankViewerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Problem Bank Viewer")
        self.geometry("860x700")
        self.minsize(600, 400)

        self._questions = []
        self._bank_info = {}
        self._current_index = 0
        self._yaml_dir = None
        self._figure_cache = {}   # filename → PhotoImage (keeps references alive)
        self._tmp_dirs = []       # temp dirs to clean up on exit

        self._build_ui()
        self.bind("<Left>",  lambda e: self._prev_question())
        self.bind("<Right>", lambda e: self._next_question())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        # ---- header bar ----
        self._header_var = tk.StringVar(value="No file loaded")
        header = tk.Label(
            self,
            textvariable=self._header_var,
            anchor="w",
            padx=8,
            pady=4,
            relief="groove",
            bg="#dce8f5",
            font=("Helvetica", 11, "bold"),
        )
        header.pack(side="top", fill="x")

        # ---- toolbar ----
        toolbar = tk.Frame(self, relief="raised", bd=1, bg="#f0f0f0")
        toolbar.pack(side="top", fill="x")

        open_btn = tk.Button(toolbar, text="Open File", command=self.open_file, padx=6)
        open_btn.pack(side="left", padx=4, pady=3)

        tk.Label(toolbar, bg="#f0f0f0", width=2).pack(side="left")

        self._prev_btn = tk.Button(toolbar, text="◀", command=self._prev_question, width=3)
        self._prev_btn.pack(side="left", padx=2, pady=3)

        self._nav_var = tk.StringVar(value="")
        nav_label = tk.Label(toolbar, textvariable=self._nav_var, bg="#f0f0f0", width=16)
        nav_label.pack(side="left")

        self._next_btn = tk.Button(toolbar, text="▶", command=self._next_question, width=3)
        self._next_btn.pack(side="left", padx=2, pady=3)

        # ---- main text area ----
        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)

        self._text = tk.Text(
            frame,
            wrap="word",
            state="disabled",
            padx=12,
            pady=8,
            spacing1=2,
            spacing3=2,
            cursor="arrow",
        )
        scrollbar = tk.Scrollbar(frame, command=self._text.yview)
        self._text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._text.pack(side="left", fill="both", expand=True)

        self._configure_tags()
        self._show_placeholder("Open a YAML file to begin.  (Ctrl+O)")

    def _configure_tags(self):
        tw = self._text
        base_size = 11
        tw.tag_configure("title",   font=("Helvetica", base_size + 2, "bold"))
        tw.tag_configure("type_badge",
                         font=("Helvetica", base_size - 1),
                         foreground="#555555")
        tw.tag_configure("meta",    font=("Helvetica", base_size - 1), foreground="#777777")
        tw.tag_configure("label",   font=("Helvetica", base_size, "bold"))
        tw.tag_configure("body",    font=("Helvetica", base_size))
        tw.tag_configure("latex",
                         font=("Courier", base_size),
                         background="#f5f5dc",
                         relief="flat")
        tw.tag_configure("answer_val",
                         font=("Helvetica", base_size, "bold"),
                         foreground="#1a6e1a")
        tw.tag_configure("answer_tol",
                         font=("Helvetica", base_size),
                         foreground="#555555")
        tw.tag_configure("divider", font=("Helvetica", 4))
        tw.tag_configure("section", font=("Helvetica", base_size, "bold"),
                         foreground="#333399")
        tw.tag_configure("placeholder", font=("Helvetica", 12), foreground="#aaaaaa")

    # ------------------------------------------------------------------
    # File loading
    # ------------------------------------------------------------------

    def open_file(self):
        if yaml is None:
            self._show_placeholder("PyYAML is not installed.\nRun:  pip install pyyaml")
            return
        path = filedialog.askopenfilename(
            title="Open Problem Bank",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")],
        )
        if path:
            self.load_bank(path)

    def load_bank(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as exc:
            self._show_placeholder(f"Failed to load file:\n{exc}")
            return

        self._yaml_dir = os.path.dirname(path)
        self._bank_info = data.get("bank_info", {})
        raw_questions = data.get("questions", [])

        # Each question entry is a dict like {type_key: {fields...}}
        self._questions = []
        for item in raw_questions:
            for qtype, qdata in item.items():
                self._questions.append({"_type": qtype, **qdata})

        # Update header
        title = self._bank_info.get("title", "")
        bank_id = self._bank_info.get("bank_id", "")
        authors = self._bank_info.get("authors", "")
        parts = [p for p in [title, bank_id, authors] if p]
        self._header_var.set("  ·  ".join(parts) if parts else os.path.basename(path))

        if self._questions:
            self._current_index = 0
            self.show_question(0)
        else:
            self._show_placeholder("No questions found in this file.")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _prev_question(self):
        if self._questions and self._current_index > 0:
            self._current_index -= 1
            self.show_question(self._current_index)

    def _next_question(self):
        if self._questions and self._current_index < len(self._questions) - 1:
            self._current_index += 1
            self.show_question(self._current_index)

    def _update_nav(self):
        n = len(self._questions)
        if n:
            self._nav_var.set(f"Question {self._current_index + 1} of {n}")
        else:
            self._nav_var.set("")
        self._prev_btn.config(state="normal" if self._current_index > 0 else "disabled")
        self._next_btn.config(state="normal" if self._current_index < n - 1 else "disabled")

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _show_placeholder(self, msg):
        tw = self._text
        tw.config(state="normal")
        tw.delete("1.0", "end")
        tw.insert("end", "\n\n" + msg, "placeholder")
        tw.config(state="disabled")

    def show_question(self, index):
        self._update_nav()
        q = self._questions[index]
        tw = self._text
        tw.config(state="normal")
        tw.delete("1.0", "end")

        # Clear figure cache for previous question (keep memory tidy)
        self._figure_cache.clear()

        qtype = q.get("_type", "unknown")
        title = q.get("title", q.get("id", ""))
        points = q.get("points", "")
        badge = f"  [{qtype.upper()}  ·  {points}pt]" if points else f"  [{qtype.upper()}]"

        # --- Title line ---
        tw.insert("end", title, "title")
        tw.insert("end", badge + "\n", "type_badge")
        tw.insert("end", "\n", "divider")

        # --- Figure (if present) ---
        figure = q.get("figure")
        if figure:
            self._insert_figure(tw, figure)
            tw.insert("end", "\n", "body")

        # --- Question text ---
        text = q.get("text", "")
        if text:
            self.render_content(tw, text)
            tw.insert("end", "\n", "body")

        # --- Answer ---
        self._insert_answer(tw, q)
        tw.insert("end", "\n", "body")

        # --- Feedback ---
        feedback = q.get("feedback", {})
        if feedback:
            tw.insert("end", "─" * 60 + "\n", "meta")
            tw.insert("end", "Feedback\n", "section")
            general = feedback.get("general", "")
            if general:
                self.render_content(tw, general)
            on_correct = feedback.get("on_correct", "")
            on_incorrect = feedback.get("on_incorrect", "")
            if on_correct or on_incorrect:
                tw.insert("end", "\n", "body")
                if on_correct:
                    tw.insert("end", "✓ Correct: ", "label")
                    tw.insert("end", on_correct + "\n", "body")
                if on_incorrect:
                    tw.insert("end", "✗ Incorrect: ", "label")
                    tw.insert("end", on_incorrect + "\n", "body")

        tw.config(state="disabled")
        tw.yview_moveto(0)

    def _insert_answer(self, tw, q):
        qtype = q.get("_type", "")
        answer = q.get("answer", {})

        if qtype == "numerical" and isinstance(answer, dict):
            value = answer.get("value", "")
            tolerance = answer.get("tolerance", "")
            margin_type = answer.get("margin_type", "")
            tw.insert("end", "Answer: ", "label")
            tw.insert("end", str(value), "answer_val")
            if tolerance and margin_type:
                unit_str = "%" if margin_type == "percent" else margin_type
                tw.insert("end", f"  (±{tolerance} {unit_str})", "answer_tol")
            tw.insert("end", "\n", "body")

        elif qtype in ("multiple_choice", "multiple_answers"):
            choices = answer if isinstance(answer, list) else []
            partial = q.get("partial", False)
            if qtype == "multiple_answers" and partial:
                tw.insert("end", "[Partial credit enabled]\n", "meta")
            for choice in choices:
                if isinstance(choice, dict):
                    text = choice.get("text", "")
                    correct = choice.get("correct", False)
                    marker = "✓ " if correct else "  • "
                    tag = "answer_val" if correct else "body"
                    tw.insert("end", marker, tag)
                    self.render_content(tw, str(text))
                    tw.insert("end", "\n", "body")
        else:
            if answer:
                tw.insert("end", "Answer: ", "label")
                tw.insert("end", str(answer) + "\n", "body")

    def render_content(self, tw, text):
        """Parse mixed content and insert into the Text widget."""
        for seg_type, seg_val in parse_content(text):
            if seg_type == "text":
                tw.insert("end", seg_val, "body")
            elif seg_type == "latex":
                tw.insert("end", seg_val, "latex")
            elif seg_type == "table":
                self.insert_table(tw, seg_val)

    def insert_table(self, tw, rows):
        """Embed a grid Frame into the Text widget."""
        if not rows:
            return

        container = tk.Frame(tw, bd=1, relief="solid", bg="white")

        # Determine if first row is a header (heuristic: came from <thead>/<th>)
        # Since TableParser doesn't distinguish, treat first row as header always.
        for r_idx, row in enumerate(rows):
            for c_idx, cell in enumerate(row):
                bg = "#dce8f5" if r_idx == 0 else ("white" if r_idx % 2 == 0 else "#f7f7f7")
                weight = "bold" if r_idx == 0 else "normal"
                lbl = tk.Label(
                    container,
                    text=cell,
                    font=("Helvetica", 10, weight),
                    bg=bg,
                    fg="#222222",
                    relief="flat",
                    bd=0,
                    padx=6,
                    pady=3,
                    anchor="w",
                )
                lbl.grid(row=r_idx, column=c_idx, sticky="nsew",
                         padx=1, pady=1)
                container.columnconfigure(c_idx, weight=1)

        tw.insert("end", "\n", "body")
        tw.window_create("end", window=container)
        tw.insert("end", "\n", "body")

    def _insert_figure(self, tw, figure_filename):
        """Try to load a figure image and embed it, or show a placeholder."""
        img_path = self._resolve_figure(figure_filename)
        if img_path and PIL_AVAILABLE:
            try:
                img = Image.open(img_path)
                img.thumbnail((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self._figure_cache[figure_filename] = photo
                tw.image_create("end", image=photo)
                tw.insert("end", "\n", "body")
                return
            except Exception:
                pass
        # Placeholder
        tw.insert("end", f"[Figure: {figure_filename}]\n", "meta")

    def _resolve_figure(self, filename):
        """Resolve figure filename relative to yaml dir; try zip if not found."""
        if not self._yaml_dir:
            return None
        direct = os.path.join(self._yaml_dir, filename)
        if os.path.isfile(direct):
            return direct

        # Try zip files in the same directory
        for entry in os.listdir(self._yaml_dir):
            if entry.lower().endswith(".zip"):
                zip_path = os.path.join(self._yaml_dir, entry)
                try:
                    with zipfile.ZipFile(zip_path) as zf:
                        names = zf.namelist()
                        for name in names:
                            if os.path.basename(name) == filename:
                                tmp = tempfile.mkdtemp()
                                self._tmp_dirs.append(tmp)
                                zf.extract(name, tmp)
                                return os.path.join(tmp, name)
                except Exception:
                    continue
        return None

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def _on_close(self):
        import shutil
        for d in self._tmp_dirs:
            shutil.rmtree(d, ignore_errors=True)
        self.destroy()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if yaml is None:
        import sys
        print("ERROR: PyYAML is not installed. Run:  pip install pyyaml", file=sys.stderr)
        sys.exit(1)
    app = BankViewerApp()
    app.mainloop()
