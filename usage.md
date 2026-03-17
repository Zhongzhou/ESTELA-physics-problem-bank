# ESTELA Problem Bank Visualizer

A Flask web app for browsing, previewing, and building exams from the ESTELA isomorphic physics problem banks.

## Features

- **Browse** all problem banks organized by course and topic
- **Search** across bank titles, IDs, descriptions, and learning objectives
- **Filter** by course and topic via sidebar dropdowns
- **Preview** every question in a bank with full LaTeX rendering (KaTeX)
- **Answer display** — correct answers highlighted, solutions shown
- **Cart** — add/remove banks, grouped by topic
- **LaTeX export** — generate N exam versions + answer keys as `.tex` files
  - Each version draws a different isomorphic problem from each bank (round-robin)
- **PDF export** — direct PDF output (requires weasyprint, see below)

## Setup

### 1. Install Python (3.12+)

Download from https://www.python.org/downloads/ — check "Add to PATH" during install.

### 2. Install dependencies

Using uv (recommended):
```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
uv run python app.py
```

Your browser will open automatically at http://localhost:5174

### 4. Load your repository

In the sidebar, enter the path to your local clone of the ESTELA problem bank, e.g.:

- **Windows:** `C:\Users\yourname\Documents\ucf-physics-automation-tool`
- **Mac/Linux:** `/Users/yourname/Documents/ucf-physics-automation-tool`

Then click **Load**.

## Building an Exam

1. Browse or search the problem banks and click **+ Add** on the ones you want
2. In the sidebar, set the exam title and number of versions (capped to the max available per your cart)
3. The export panel appears automatically — click a version button to download `.tex` or PDF
4. Compile `.tex` files with `pdflatex` (requires the `exam` LaTeX class: `tlmgr install exam`)

## Notes on LaTeX Output

- The generated exams use the `exam` document class
- Each version picks a different problem from each bank (version 1 = problem 1, version 2 = problem 2, etc.)
- `\printanswers` is commented out by default — uncomment in the `.tex` file to produce an instructor copy with answers shown
- You'll need a LaTeX distribution: [MiKTeX](https://miktex.org/) (Windows) or [MacTeX](https://www.tug.org/mactex/) (Mac)

## PDF Export (optional)

PDF export requires weasyprint:

```bash
uv add weasyprint
```

## Project Structure

```
ucf-physics-automation-tool/
├── app.py              ← Main Flask application (backend + frontend)
├── requirements.txt    ← Python dependencies
├── pyproject.toml      ← Project metadata (uv)
├── usage.md            ← This file
├── PHY I Mechanics/    ← Problem bank YAML files organized by unit
└── Templates/          ← YAML templates and AI prompts for new banks
```
