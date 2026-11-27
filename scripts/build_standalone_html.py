#!/usr/bin/env python3
"""Build a single-file ESTELA Exam Builder with embedded problem banks (zip + base64).

Bank YAMLs, figure images, and Canvas QTI packages (zips containing an
imsmanifest.xml next to each bank YAML) are bundled so the standalone page can
offer per-bank "Download Canvas QTI" without any backend.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import re
import sys
import zipfile
from pathlib import Path

SKIP_DIRS = {
    "Old", "old", "Archive", "archive", "Older versions", "Older Versions",
    "Drafts", "drafts", "Temporary", "temporary", "venv", "__pycache__",
    ".git", "Scripts", "scripts", "Figure Creation", "figure_creation",
}

SKIP_COURSES = {
    "venv", "Templates", "Bank Statistics", ".git",
    "frontend", "src-tauri", "src", "node_modules", ".github",
    "target", "dist", "build", "scripts", "docs",
}

BANK_EXT = {".yaml", ".yml"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def should_skip_path(parts: tuple[str, ...]) -> bool:
    return any(p in SKIP_DIRS for p in parts)


def is_qti_zip(path: Path) -> bool:
    """Canvas QTI packages are zips with an imsmanifest.xml at the root."""
    try:
        with zipfile.ZipFile(path) as zf:
            return "imsmanifest.xml" in zf.namelist()
    except Exception:
        return False


def should_include_file(path: Path) -> bool:
    ext = path.suffix.lower()
    if ext in BANK_EXT or ext in IMAGE_EXT:
        return True
    if ext == ".zip" and is_qti_zip(path):
        return True
    return False


def find_courses(repo_root: Path) -> list[str]:
    """Every top-level folder that holds at least one bank YAML: a new course folder
    (PHY II EM, 2026-11) is bundled without anyone editing this script or the workflow."""
    found = []
    for path in sorted(repo_root.iterdir()):
        if not path.is_dir() or path.name in SKIP_COURSES or path.name.startswith("."):
            continue
        if any(f.suffix.lower() in BANK_EXT and not should_skip_path(f.relative_to(path).parts)
               for f in path.rglob("*") if f.is_file()):
            found.append(path.name)
    return found


def build_zip_bytes(repo_root: Path, courses: list[str]) -> bytes:
    buf = io.BytesIO()
    qti_count = 0
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for course in courses:
            course_path = repo_root / course
            if not course_path.is_dir():
                print(f"warning: course not found: {course_path}", file=sys.stderr)
                continue
            for fpath in sorted(course_path.rglob("*")):
                if not fpath.is_file():
                    continue
                rel = fpath.relative_to(repo_root)
                parts = rel.parts
                if not parts or parts[0] in SKIP_COURSES or parts[0].startswith("."):
                    continue
                if should_skip_path(parts[1:]):
                    continue
                if not should_include_file(fpath):
                    continue
                # nested zips (QTI packages) are already compressed — store as-is
                if fpath.suffix.lower() == ".zip":
                    qti_count += 1
                    zf.write(fpath, rel.as_posix(), compress_type=zipfile.ZIP_STORED)
                else:
                    zf.write(fpath, rel.as_posix())
    print(f"Embedded Canvas QTI packages: {qti_count}", file=sys.stderr)
    return buf.getvalue()


def inline_script(html: str, src_name: str, content: str) -> str:
    tag = f'<script src="{src_name}"></script>'
    if tag not in html:
        raise ValueError(f"Template missing {tag}")
    return html.replace(tag, f"<script>\n{content}\n</script>", 1)


def build_standalone_html(
    template_path: Path,
    frontend_dir: Path,
    repo_root: Path,
    courses: list[str],
    label: str,
) -> str:
    html = template_path.read_text(encoding="utf-8")

    jszip_tag = '<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>'
    if jszip_tag not in html:
        html = html.replace(
            '<script src="https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js"></script>\n'
            + jszip_tag,
        )

    html = inline_script(html, "bank-source.js", (frontend_dir / "bank-source.js").read_text(encoding="utf-8"))
    html = inline_script(html, "exam-export.js", (frontend_dir / "exam-export.js").read_text(encoding="utf-8"))

    # Enhanced template (frontend/enhanced.html) adds the desktop-parity exporters.
    # Only inline it when the template actually references it, so the default
    # index.html build is unchanged.
    plus_tag = '<script src="exam-export-plus.js"></script>'
    if plus_tag in html:
        html = inline_script(
            html, "exam-export-plus.js",
            (frontend_dir / "exam-export-plus.js").read_text(encoding="utf-8"),
        )

    zip_bytes = build_zip_bytes(repo_root, courses)
    b64 = base64.b64encode(zip_bytes).decode("ascii")
    mb = len(zip_bytes) / (1024 * 1024)
    print(f"Bundle zip: {mb:.1f} MB ({len(b64):,} base64 chars)", file=sys.stderr)

    bundle_script = (
        "<script>\n"
        f"window.__ESTELA_BUNDLE__ = {{ label: {json.dumps(label)}, zipBase64: {json.dumps(b64)} }};\n"
        "</script>\n"
    )
    marker = '<script src="https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js"></script>'
    html = html.replace(marker, bundle_script + marker)

    html = html.replace(
        "<title>ESTELA Exam Builder · Problem Bank</title>",
        "<title>ESTELA Exam Builder · Standalone</title>",
    )
    return html


def main() -> int:
    parser = argparse.ArgumentParser(description="Build standalone ESTELA Exam Builder HTML")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--courses",
        nargs="+",
        default=None,
        help="Course folder names to embed (default: every top-level folder with a bank)",
    )
    parser.add_argument(
        "--label",
        default="",
        help="Display label for bundled banks (default: course names joined)",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=None,
        help="HTML template (default: frontend/index.html)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file (default: docs/standalone.html, published via GitHub Pages)",
    )
    args = parser.parse_args()

    repo_root = args.repo.resolve()
    frontend_dir = repo_root / "frontend"
    template_path = (args.template or frontend_dir / "index.html").resolve()
    output_path = (args.output or repo_root / "docs" / "standalone.html").resolve()
    courses = args.courses or find_courses(repo_root)
    print(f"Courses: {', '.join(courses)}", file=sys.stderr)
    label = args.label or ", ".join(courses)

    if not template_path.is_file():
        print(f"error: template not found: {template_path}", file=sys.stderr)
        return 1

    html = build_standalone_html(template_path, frontend_dir, repo_root, courses, label)
    output_path.write_text(html, encoding="utf-8")
    out_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"Wrote {output_path} ({out_mb:.1f} MB)", file=sys.stderr)
    print("Open via double-click (file://). KaTeX/js-yaml/JSZip load from CDN — internet required for math.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
