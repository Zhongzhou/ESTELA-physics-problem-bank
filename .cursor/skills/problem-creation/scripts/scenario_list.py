"""Keep the scenario sidecar: target comes from the input, and the round count is enforced here."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required. Run this skill with the repo venv:\n"
        ".venv/Scripts/python.exe -m pip install -r "
        ".cursor/skills/problem-creation/requirements.txt\n"
    )
    sys.exit(1)

# Generation passes allowed after init. The 6th receive stops if the target is still unmet.
MAX_UPDATES = 5

HEADER = (
    "# Review file for the problem-creation workflow.\n"
    "# scenarios with status accepted are the kept list.\n"
    "# target is copied from context.n_scenarios in the input file.\n"
)


def configure_stdio() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def fail(message: str, code: int = 1) -> None:
    sys.stderr.write(message.rstrip() + "\n")
    raise SystemExit(code)


def load_yaml(path: Path):
    if not path.is_file():
        fail(f"File not found: {path}")
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_target(input_path: Path) -> int:
    data = load_yaml(input_path)
    if not isinstance(data, dict):
        fail(f"Input YAML must be a mapping: {input_path}")
    context = data.get("context")
    if not isinstance(context, dict) or "n_scenarios" not in context:
        fail("context.n_scenarios is missing from the input file.")
    value = context["n_scenarios"]
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        fail("context.n_scenarios must be a positive integer in the input file.")
    return value


def default_sidecar(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.scenarios.yaml")


def save(path: Path, data: dict) -> None:
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)
    path.write_text(HEADER + body, encoding="utf-8")


def load_sidecar(path: Path) -> dict:
    data = load_yaml(path)
    if not isinstance(data, dict):
        fail(f"Scenario file must be a mapping: {path}")
    for key in ("target", "update_count", "scenarios", "rejected"):
        if key not in data:
            fail(f"Scenario file is missing {key}: {path}")
    if isinstance(data["target"], bool) or not isinstance(data["target"], int):
        fail("Scenario file target must be an integer copied from the input.")
    if not isinstance(data["scenarios"], list) or not isinstance(data["rejected"], list):
        fail("Scenario file scenarios and rejected must be lists.")
    return data


def norm(text: str) -> str:
    return " ".join(text.split()).casefold()


def snapshot(data: dict, path: Path) -> dict:
    accepted = [item["text"] for item in data["scenarios"] if item.get("status") == "accepted"]
    pending = [item["text"] for item in data["scenarios"] if item.get("status") == "pending"]
    needed = max(0, int(data["target"]) - len(accepted))
    complete = len(accepted) >= int(data["target"])
    rounds_exceeded = int(data["update_count"]) > MAX_UPDATES
    return {
        "file": str(path),
        "target": int(data["target"]),
        "update_count": int(data["update_count"]),
        "accepted": len(accepted),
        "pending": len(pending),
        "needed": needed,
        "complete": complete,
        "rounds_exceeded": rounds_exceeded,
        "stop": rounds_exceeded and not complete,
        "accepted_texts": accepted,
        "pending_texts": pending,
        "rejected": data["rejected"],
    }


def emit(payload: dict, code: int = 0) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    raise SystemExit(code)


def known_texts(data: dict) -> set[str]:
    texts = {norm(item["text"]) for item in data["scenarios"] if item.get("text")}
    texts.update(norm(item["text"]) for item in data["rejected"] if item.get("text"))
    return texts


def cmd_init(args: argparse.Namespace) -> None:
    target = read_target(args.input)
    out = args.out or default_sidecar(args.input)
    if out.exists() and not args.force:
        fail(f"Scenario file already exists: {out}. Pass --force to replace it.")
    data = {
        "source_input": str(args.input),
        "target": target,
        "update_count": 0,
        "scenarios": [],
        "rejected": [],
    }
    save(out, data)
    emit(snapshot(data, out))


def cmd_status(args: argparse.Namespace) -> None:
    data = load_sidecar(args.file)
    emit(snapshot(data, args.file))


def cmd_receive(args: argparse.Namespace) -> None:
    data = load_sidecar(args.file)
    data["update_count"] = int(data["update_count"]) + 1
    save(args.file, data)
    payload = snapshot(data, args.file)
    emit(payload, 2 if payload["stop"] else 0)


def cmd_add(args: argparse.Namespace) -> None:
    data = load_sidecar(args.file)
    texts = args.text or []
    if not texts:
        fail("Pass at least one --text.")
    cleaned: list[str] = []
    seen = known_texts(data)
    for text in texts:
        item = " ".join(text.split())
        if not item:
            fail("Scenario text is empty.")
        key = norm(item)
        if key in seen:
            fail(f"Scenario repeats an existing or rejected scenario: {item}")
        seen.add(key)
        cleaned.append(item)
    accepted = sum(1 for item in data["scenarios"] if item.get("status") == "accepted")
    pending = sum(1 for item in data["scenarios"] if item.get("status") == "pending")
    if accepted + pending + len(cleaned) > int(data["target"]):
        room = int(data["target"]) - accepted - pending
        fail(f"Refusing to add {len(cleaned)} scenarios; only {room} slots remain under target.")
    for item in cleaned:
        data["scenarios"].append({"text": item, "status": "pending"})
    save(args.file, data)
    emit(snapshot(data, args.file))


def cmd_remove(args: argparse.Namespace) -> None:
    data = load_sidecar(args.file)
    indexes = args.index or []
    reasons = args.reason or []
    if len(indexes) != len(reasons):
        fail("Each --index needs one --reason, in the same order.")
    pending_positions = [
        pos for pos, item in enumerate(data["scenarios"]) if item.get("status") == "pending"
    ]
    if len(set(indexes)) != len(indexes):
        fail("Repeated --index.")
    for index in indexes:
        if index < 0 or index >= len(pending_positions):
            fail(f"Pending index out of range: {index}")
    drop = set(indexes)
    for index, reason in sorted(zip(indexes, reasons), reverse=True):
        why = " ".join(reason.split())
        if not why:
            fail("A removal reason is empty.")
        pos = pending_positions[index]
        item = data["scenarios"].pop(pos)
        data["rejected"].append({"text": item["text"], "reason": why})
    for item in data["scenarios"]:
        if item.get("status") == "pending":
            item["status"] = "accepted"
    save(args.file, data)
    payload = snapshot(data, args.file)
    if drop and not payload["rejected"]:
        fail("Removals were not recorded.")
    emit(payload)


def cmd_set_target(args: argparse.Namespace) -> None:
    data = load_sidecar(args.file)
    if any(item.get("status") == "pending" for item in data["scenarios"]):
        fail("Resolve pending scenarios with remove before set-target.")
    data["target"] = read_target(args.input)
    data["source_input"] = str(args.input)
    data["update_count"] = 0
    save(args.file, data)
    emit(snapshot(data, args.file))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Create a sidecar from context.n_scenarios")
    init.add_argument("--input", required=True, type=Path)
    init.add_argument("--out", type=Path)
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    for name, func, help_text in (
        ("status", cmd_status, "Show counts without changing the file"),
        ("receive", cmd_receive, "Increment update_count because a generator pass is starting"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--file", required=True, type=Path)
        command.set_defaults(func=func)

    add = commands.add_parser("add", help="Append pending scenarios")
    add.add_argument("--file", required=True, type=Path)
    add.add_argument("--text", action="append", required=True)
    add.set_defaults(func=cmd_add)

    remove = commands.add_parser(
        "remove",
        help="Drop pending scenarios by pending-list index and accept the rest",
    )
    remove.add_argument("--file", required=True, type=Path)
    remove.add_argument("--index", action="append", type=int)
    remove.add_argument("--reason", action="append")
    remove.set_defaults(func=cmd_remove)

    set_target = commands.add_parser(
        "set-target",
        help="Copy context.n_scenarios into the sidecar and reset update_count",
    )
    set_target.add_argument("--file", required=True, type=Path)
    set_target.add_argument("--input", required=True, type=Path)
    set_target.set_defaults(func=cmd_set_target)
    return parser


def main() -> None:
    configure_stdio()
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
