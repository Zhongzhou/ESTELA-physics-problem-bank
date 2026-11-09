"""Build a table of bank name, id, model, version, and date created."""

import csv
import re
from pathlib import Path

TEMPLATE_BANK_ID = "EXP-PB1-EXMPLPB-01012026"
SKIP_DIR_NAMES = {
    "old",
    "old files",
    "drafts",
    "archive",
    "sources",
    "supporting files",
    "older versions",
    "version with alternate numbers",
    "files",
    "templates",
}


def bank_info_block(content):
    """Return the bank_info section, stopping at the next top-level key."""
    match = re.search(r"(?m)^bank_info:.*$", content)
    if not match:
        return ""
    lines = []
    for line in content[match.end():].splitlines():
        if line and not line.startswith((" ", "\t", "#")):
            break
        lines.append(line)
    return "\n".join(lines)


def clean_value(value):
    if value is None:
        return ""
    value = value.strip().strip("\"'")
    if "#" in value:
        value = value.split("#", 1)[0].strip().strip("\"'")
    return value


def field_value(block, field_name):
    pattern = rf"(?m)^\s+{re.escape(field_name)}:\s*(.*)$"
    match = re.search(pattern, block)
    if not match:
        return ""
    return clean_value(match.group(1))


def first_field(block, field_names):
    for name in field_names:
        value = field_value(block, name)
        if value:
            return value
    return ""


def extract_row(file_path):
    content = file_path.read_text(encoding="utf-8")
    block = bank_info_block(content)
    if not block:
        return None

    bank_id = field_value(block, "bank_id")
    if not bank_id or bank_id == TEMPLATE_BANK_ID:
        return None

    model = first_field(block, ["model"])
    if not model:
        model = field_value(block, "LLM")

    return {
        "Bank Name": field_value(block, "title"),
        "Bank Id": bank_id,
        "Model": model,
        "Version": first_field(block, ["version", "bank version", "generator version"]),
        "Date Created": first_field(block, ["date created", "date_created"]),
    }


def is_primary_bank_file(yaml_file, course_dir):
    """Keep the current bank file that sits directly in its bank folder."""
    try:
        parts = yaml_file.relative_to(course_dir).parts
    except ValueError:
        return False
    if any(part.lower() in SKIP_DIR_NAMES for part in parts[:-1]):
        return False
    if len(parts) < 2 or not parts[-2].startswith("PHY"):
        return False
    # File must live directly in the bank folder, not in a nested draft or source folder.
    return len(parts) == 3 or (len(parts) == 2 and parts[0].startswith("PHY"))


def select_bank_files(course_dir):
    candidates = list(course_dir.glob("**/*.yaml")) + list(course_dir.glob("**/*.yml"))
    by_folder = {}
    for path in candidates:
        if not is_primary_bank_file(path, course_dir):
            continue
        by_folder.setdefault(path.parent, []).append(path)

    selected = []
    for folder, files in by_folder.items():
        prefixed = [path for path in files if path.name.startswith("PHY")]
        if prefixed:
            selected.extend(prefixed)
            continue
        # Some banks keep the questions in a file that does not start with PHY.
        for path in files:
            if path.name.lower() == "meta.yaml":
                continue
            selected.append(path)
    return selected


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    course_dirs = [
        path
        for path in repo_root.iterdir()
        if path.is_dir() and path.name.startswith("PHY")
    ]

    rows = []
    for course_dir in sorted(course_dirs):
        for yaml_file in select_bank_files(course_dir):
            try:
                row = extract_row(yaml_file)
            except OSError as exc:
                print(f"Error reading {yaml_file}: {exc}")
                continue
            if row:
                rows.append(row)

    rows.sort(key=lambda row: row["Bank Id"])

    output_file = script_dir / "bank_model_version.csv"
    fieldnames = ["Bank Name", "Bank Id", "Model", "Version", "Date Created"]
    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    missing_model = sum(1 for row in rows if not row["Model"])
    missing_version = sum(1 for row in rows if not row["Version"])
    missing_date = sum(1 for row in rows if not row["Date Created"])
    print(f"Wrote {len(rows)} banks to {output_file}")
    print(
        f"Missing model: {missing_model}; "
        f"missing version: {missing_version}; "
        f"missing date: {missing_date}"
    )


if __name__ == "__main__":
    main()
