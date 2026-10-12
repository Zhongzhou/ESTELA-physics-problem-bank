"""Build equation combinations, calculation functions, and scenario rows.

Python writes the calculation sidecar and the function module. A classifier
subagent is used only when the input omits parameters.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import keyword
import math
import re
import sys
from pathlib import Path

try:
    import sympy
    from decimal import Decimal, ROUND_HALF_UP
    from sympy import Eq
    from sympy.parsing.sympy_parser import (
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )
    from sympy.printing.pycode import pycode
except ImportError:
    sys.stderr.write(
        "SymPy and PyYAML are required. Run this skill with the repo venv:\n"
        ".venv/Scripts/python.exe -m pip install -r "
        ".cursor/skills/problem-creation/requirements.txt\n"
    )
    sys.exit(1)

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required. Run this skill with the repo venv:\n"
        ".venv/Scripts/python.exe -m pip install -r "
        ".cursor/skills/problem-creation/requirements.txt\n"
    )
    sys.exit(1)


MAX_CLASSIFY_ATTEMPTS = 5
PARSE_TRANSFORMS = standard_transformations + (implicit_multiplication_application,)

# Symbols treated as constants unless the user lists them under parameters.
# pi is detected from the parsed formula, where SymPy reads it as the constant Pi.
SAFE_CONSTANTS = {
    "g": "9.80",
    "G": "6.67430e-11",
    "epsilon_0": "8.8541878128e-12",
    "mu_0": "1.25663706212e-6",
    "k_B": "1.380649e-23",
    "N_A": "6.02214076e23",
    "hbar": "1.054571817e-34",
    "sigma": "5.670374419e-8",
}

COMMANDS = {
    "pi": "pi",
    "cdot": "*",
    "times": "*",
    "alpha": "alpha",
    "beta": "beta",
    "gamma": "gamma",
    "delta": "delta",
    "epsilon": "epsilon",
    "varepsilon": "epsilon",
    "theta": "theta",
    "vartheta": "theta",
    "mu": "mu",
    "nu": "nu",
    "xi": "xi",
    "rho": "rho",
    "sigma": "sigma",
    "tau": "tau",
    "phi": "phi",
    "varphi": "phi",
    "psi": "psi",
    "omega": "omega",
    "kappa": "kappa",
    "eta": "eta",
    "ell": "ell",
    "lambda": "lambda",
    "Delta": "Delta_",
    "Omega": "Omega_",
}

FUNCTIONS = {"sin", "cos", "tan", "ln", "log", "exp", "asin", "acos", "atan", "sqrt"}

HEADER = (
    "# Calculation table for the problem-creation workflow.\n"
    "# Python writes this file.\n"
    "# equation_sets are the Agent 4 rows.\n"
    "# rows pair each accepted scenario with every equation set.\n"
)

MODULE_HEADER = (
    '"""Generated calculation functions. Python writes this file."""\n\n'
    "import math\n"
    "from decimal import Decimal, ROUND_HALF_UP\n"
)


class FormulaError(Exception):
    pass


class ClassificationError(Exception):
    pass


def configure_stdio() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def fail(message: str, code: int = 1) -> None:
    sys.stderr.write(message.rstrip() + "\n")
    raise SystemExit(code)


def emit(payload: dict, code: int = 0) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    raise SystemExit(code)


def load_yaml(path: Path):
    if not path.is_file():
        fail(f"File not found: {path}")
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def save(path: Path, data: dict) -> None:
    body = yaml.dump(
        data,
        Dumper=NoAliasDumper,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
    )
    path.write_text(HEADER + body, encoding="utf-8")


def default_calc_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.calculations.yaml")


def module_path_for(calc_path: Path) -> Path:
    return calc_path.with_suffix(".py")


def optional_block(data: dict) -> dict:
    for key in ("other (optional)", "other"):
        block = data.get(key)
        if isinstance(block, dict):
            return block
    return {}


def is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def rounding_places(block: dict) -> int:
    value = block.get("rounding_decimal", 2)
    if is_blank(value):
        return 2
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        fail("rounding_decimal must be a non-negative integer.")
    return value


def tolerance_value(block: dict):
    value = block.get("tolerance")
    if is_blank(value):
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail("tolerance must be a number when it is present.")
    return value


def find_brace(text: str, start: int) -> int:
    if start >= len(text) or text[start] != "{":
        raise FormulaError(f"Expected '{{' in formula near: {text[start:start + 20]!r}")
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    raise FormulaError(f"Unclosed '{{' in formula: {text}")


def read_command(text: str, start: int) -> tuple[str, int]:
    index = start + 1
    if index < len(text) and text[index] == "\\":
        return "\\", index + 1
    while index < len(text) and text[index].isalpha():
        index += 1
    if index == start + 1:
        raise FormulaError(f"Unknown LaTeX near: {text[start:start + 20]!r}")
    return text[start + 1 : index], index


def convert_latex(text: str) -> str:
    converted = walk_latex(text.strip(), 0, len(text.strip()))
    converted = replace_scripts(converted)
    return insert_multiplication(converted)


def walk_latex(text: str, start: int, end: int) -> str:
    pieces: list[str] = []
    index = start
    while index < end:
        if text[index] == "\\":
            name, index = read_command(text, index)
            if name in {"left", "right"}:
                continue
            if name == "mathrm":
                while index < end and text[index].isspace():
                    index += 1
                close = find_brace(text, index)
                pieces.append(walk_latex(text, index + 1, close))
                index = close + 1
                continue
            if name == "frac":
                piece, index = consume_frac(text, index, end)
                pieces.append(piece)
                continue
            if name == "sqrt":
                piece, index = consume_sqrt(text, index, end)
                pieces.append(piece)
                continue
            if name in FUNCTIONS:
                piece, index = consume_function(text, name, index, end)
                pieces.append(piece)
                continue
            if name not in COMMANDS:
                raise FormulaError(f"Unsupported LaTeX command: \\{name}")
            pieces.append(COMMANDS[name])
            continue
        pieces.append(text[index])
        index += 1
    return "".join(pieces)


def consume_frac(text: str, index: int, end: int) -> tuple[str, int]:
    while index < end and text[index].isspace():
        index += 1
    close_num = find_brace(text, index)
    numerator = walk_latex(text, index + 1, close_num)
    index = close_num + 1
    while index < end and text[index].isspace():
        index += 1
    close_den = find_brace(text, index)
    denominator = walk_latex(text, index + 1, close_den)
    return f"(({numerator})/({denominator}))", close_den + 1


def consume_sqrt(text: str, index: int, end: int) -> tuple[str, int]:
    while index < end and text[index].isspace():
        index += 1
    close = find_brace(text, index)
    inner = walk_latex(text, index + 1, close)
    return f"sqrt({inner})", close + 1


def consume_function(text: str, name: str, index: int, end: int) -> tuple[str, int]:
    while index < end and text[index].isspace():
        index += 1
    if index < end and text[index] == "(":
        return name, index
    if index < end and text[index] == "{":
        close = find_brace(text, index)
        inner = walk_latex(text, index + 1, close)
        return f"{name}({inner})", close + 1
    atom, index = consume_atom(text, index, end)
    return f"{name}({atom})", index


def consume_atom(text: str, index: int, end: int) -> tuple[str, int]:
    if index >= end:
        raise FormulaError("A function is missing its argument.")
    if text[index] == "\\":
        name, next_index = read_command(text, index)
        if name in COMMANDS:
            return COMMANDS[name], next_index
        if name in FUNCTIONS or name in {"frac", "sqrt", "mathrm"}:
            piece = walk_latex(text, index, end)
            return piece, end
        raise FormulaError(f"Unsupported LaTeX command: \\{name}")
    if text[index] == "(":
        depth = 0
        close = index
        for cursor in range(index, end):
            if text[cursor] == "(":
                depth += 1
            elif text[cursor] == ")":
                depth -= 1
                if depth == 0:
                    close = cursor
                    break
        else:
            raise FormulaError(f"Unclosed '(' in formula: {text}")
        return walk_latex(text, index, close + 1), close + 1
    match = re.match(r"[A-Za-z0-9_.]+", text[index:end])
    if not match:
        raise FormulaError(f"Expected a symbol near: {text[index:index + 20]!r}")
    return match.group(0), index + len(match.group(0))


def replace_scripts(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(
            r"([A-Za-z0-9_]+)_\{([^{}]+)\}",
            lambda match: match.group(1) + "_" + re.sub(r"\s+", "", match.group(2)),
            text,
        )
        text = re.sub(r"\^\{([^{}]+)\}", r"**(\1)", text)
        text = re.sub(r"\^([0-9]+)", r"**(\1)", text)
    return text


def insert_multiplication(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"(\d)\s*([A-Za-z(])", r"\1*\2", text)
    text = re.sub(r"\)\s*([A-Za-z0-9_(])", r")*\1", text)
    text = re.sub(r"([A-Za-z0-9_])\s+([A-Za-z(])", r"\1*\2", text)
    text = re.sub(
        r"([A-Za-z_][A-Za-z0-9_]*)\*\(",
        lambda match: match.group(1) + "("
        if match.group(1) in FUNCTIONS
        else match.group(0),
        text,
    )
    return text


def parse_side(latex_side: str):
    converted = convert_latex(latex_side)
    if not converted:
        raise FormulaError("A formula side is empty.")
    try:
        return parse_expr(converted, transformations=PARSE_TRANSFORMS, evaluate=True)
    except Exception as exc:
        raise FormulaError(f"Could not parse '{latex_side}' as '{converted}': {exc}") from exc


def parse_formula(latex: str):
    if latex.count("=") != 1:
        raise FormulaError(f"Each formula needs one equals sign: {latex}")
    left, right = latex.split("=", 1)
    equation = Eq(parse_side(left), parse_side(right))
    return equation


def ordered_names(latex: str, equation) -> list[str]:
    converted = convert_latex(latex.split("=", 1)[0]) + " " + convert_latex(latex.split("=", 1)[1])
    known = {symbol.name for symbol in equation.free_symbols}
    if equation.has(sympy.pi):
        known.add("pi")
    names: list[str] = []
    for match in re.finditer(r"[A-Za-z_][A-Za-z0-9_]*", converted):
        name = match.group(0)
        if name in FUNCTIONS or name not in known or name in names:
            continue
        names.append(name)
    for name in sorted(known):
        if name not in names:
            names.append(name)
    return names


def expand_formulas(items) -> list[list[str]]:
    if isinstance(items, str):
        text = items.strip()
        if not text:
            raise FormulaError("structure.formulas is empty.")
        return [[text]]
    if not isinstance(items, list) or not items:
        raise FormulaError("structure.formulas must be a list of formulas.")
    combinations: list[list[str]] = [[]]
    for item in items:
        choices = choices_for(item)
        combinations = [combo + choice for combo in combinations for choice in choices]
    return combinations


def choices_for(item) -> list[list[str]]:
    if isinstance(item, str):
        text = item.strip()
        if not text:
            raise FormulaError("A formula string is empty.")
        return [[text]]
    if isinstance(item, dict) and list(item) == ["One of"]:
        options = item["One of"]
        if not isinstance(options, list) or len(options) < 2:
            raise FormulaError("One of: needs two or more formulas.")
        choices: list[list[str]] = []
        for option in options:
            if isinstance(option, str):
                choices.extend(choices_for(option))
            elif isinstance(option, list):
                choices.extend(expand_formulas(option))
            else:
                choices.extend(choices_for(option))
        return choices
    raise FormulaError(f"A formula entry must be a string or a One of: group, not {item!r}.")


def normalize_symbol(token: str) -> str:
    text = token.strip().strip("$")
    if not text:
        raise FormulaError("A variable name is empty.")
    if "\\" in text or "{" in text or "^" in text:
        text = insert_multiplication(replace_scripts(convert_latex(text)))
    text = text.replace(" ", "")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text):
        raise FormulaError(f"Not a variable name: {token}")
    return text


def parse_parameter_spec(value) -> list[dict]:
    if is_blank(value):
        return []
    if isinstance(value, list):
        items = []
        for entry in value:
            if not isinstance(entry, str):
                raise FormulaError("parameters entries must be strings.")
            items.extend(parse_parameter_spec(entry))
        return items
    if not isinstance(value, str):
        raise FormulaError("parameters must be a string or a list of names.")
    items = []
    for part in value.split(","):
        piece = " ".join(part.split())
        if not piece:
            continue
        if " or " in piece:
            options = [normalize_symbol(option) for option in piece.split(" or ")]
            if len(options) < 2 or any(not option for option in options):
                raise FormulaError(f"A parameter choice is incomplete: {piece}")
            items.append({"choice": options})
        else:
            items.append({"symbol": normalize_symbol(piece)})
    return items


def resolve_parameters(items: list[dict], symbols: set[str]) -> list[str]:
    chosen: list[str] = []
    for item in items:
        if "symbol" in item:
            name = item["symbol"]
            if name not in symbols:
                raise ClassificationError(
                    f"Parameter {name} is not in this equation set. "
                    "Symbols here: " + ", ".join(sorted(symbols))
                )
            chosen.append(name)
            continue
        present = [name for name in item["choice"] if name in symbols]
        if len(present) != 1:
            rendered = " or ".join(item["choice"])
            raise ClassificationError(
                f"Choice '{rendered}' must match exactly one symbol in this equation set."
            )
        chosen.append(present[0])
    if len(chosen) != len(set(chosen)):
        raise ClassificationError("parameters repeats a variable in one equation set.")
    return chosen


def constant_names_for(symbols: list[str], user_parameters: set[str] | None) -> list[str]:
    names = []
    for name in symbols:
        if name == "pi":
            names.append(name)
            continue
        if name not in SAFE_CONSTANTS:
            continue
        if user_parameters is not None and name in user_parameters:
            continue
        names.append(name)
    return names


def constant_record(name: str) -> dict:
    if name == "pi":
        return {"symbol": "pi", "python": "math.pi", "value": float(math.pi)}
    literal = SAFE_CONSTANTS[name]
    return {"symbol": name, "python": literal, "value": float(literal)}


def variable_symbols(names: list[str], constants: list[str]) -> list[str]:
    skip = set(constants)
    return [name for name in names if name not in skip]


def classify_specified(sets: list[dict], items: list[dict]) -> None:
    user_names = set()
    for item in items:
        if "symbol" in item:
            user_names.add(item["symbol"])
        else:
            user_names.update(item["choice"])
    errors = []
    for entry in sets:
        try:
            constants = constant_names_for(entry["symbols"], user_names)
            pool = set(variable_symbols(entry["symbols"], constants))
            parameters = resolve_parameters(items, set(entry["symbols"]))
            held_constants = [name for name in parameters if name not in pool]
            if held_constants:
                raise ClassificationError(
                    f"{', '.join(held_constants)} is a constant in {entry['id']}. "
                    "Remove it from parameters."
                )
            computed = [name for name in entry["symbols"] if name in pool and name not in parameters]
            if len(computed) != len(entry["formulas"]):
                raise ClassificationError(
                    f"`parameters` leaves computed variables {computed or '[]'} in {entry['id']}, "
                    f"which has {len(entry['formulas'])} equations. "
                    "The number of computed variables must equal the number of equations. "
                    "Adjust parameters."
                )
        except ClassificationError as exc:
            errors.append(str(exc))
            continue
        entry["constants"] = [constant_record(name) for name in constants]
        entry["parameters"] = parameters
        entry["computed"] = computed
    if errors:
        raise ClassificationError(" ".join(errors))


def py_name(name: str) -> str:
    if keyword.iskeyword(name):
        return name + "_"
    return name


def pick_solution(expression, solutions: list):
    if not solutions:
        raise FormulaError(f"No solution for {expression}.")
    ranked = []
    for solution in solutions:
        if getattr(solution, "free_symbols", None) and expression in solution.free_symbols:
            continue
        try:
            value = complex(solution.subs({symbol: 1 for symbol in solution.free_symbols}).evalf())
        except Exception:
            continue
        if abs(value.imag) > 1e-8:
            continue
        ranked.append((value.real, solution))
    if not ranked:
        raise FormulaError(f"Solutions for {expression} are not usable real expressions.")
    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked[0][1]


def elimination_steps(equations: list, computed: list[str]):
    remaining = set(computed)
    known_started = set()
    for equation in equations:
        known_started.update(symbol.name for symbol in equation.free_symbols)
    known_started -= remaining
    known = set(known_started)
    unused = list(equations)
    steps: list[tuple[str, sympy.Expr]] = []
    while remaining:
        progressed = False
        for equation in list(unused):
            names = {symbol.name for symbol in equation.free_symbols}
            pending = names & remaining
            if len(pending) != 1:
                continue
            if not (names - pending) <= known:
                continue
            name = next(iter(pending))
            symbol = sympy.Symbol(name)
            solution = pick_solution(symbol, list(sympy.solve(equation, symbol, dict=False)))
            steps.append((name, solution))
            known.add(name)
            remaining.remove(name)
            unused.remove(equation)
            progressed = True
            break
        if progressed:
            continue
        if not unused:
            break
        subset_names = set()
        for equation in unused:
            subset_names.update(symbol.name for symbol in equation.free_symbols)
        subset_names &= remaining
        if len(subset_names) != len(unused):
            break
        symbols = [sympy.Symbol(name) for name in computed if name in subset_names]
        solved = sympy.solve(unused, symbols, dict=True)
        if not solved:
            break
        choice = None
        best_score = None
        for candidate in solved:
            score = 0.0
            usable = True
            for symbol in symbols:
                expression = candidate[symbol]
                try:
                    value = complex(
                        expression.subs({item: 1 for item in expression.free_symbols}).evalf()
                    )
                except Exception:
                    usable = False
                    break
                if abs(value.imag) > 1e-8:
                    usable = False
                    break
                score += value.real
            if usable and (best_score is None or score > best_score):
                best_score = score
                choice = candidate
        if choice is None:
            break
        for symbol in symbols:
            steps.append((symbol.name, choice[symbol]))
            remaining.remove(symbol.name)
        unused = []
    if remaining:
        missing = ", ".join(sorted(remaining))
        raise FormulaError(f"Could not solve for computed variables: {missing}")
    return steps


def round_step(value, places: int) -> float:
    quantum = Decimal(1).scaleb(-places)
    return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP))


def evaluate_step(expression, env: dict) -> float:
    code = pycode(expression)
    local = {"math": math, **env}
    for name, literal in SAFE_CONSTANTS.items():
        local.setdefault(name, float(literal))
    value = eval(code, {"math": math}, local)
    return float(value)


def render_steps(steps, places: int) -> str:
    lines = []
    for name, expression in steps:
        code = pycode(expression)
        for symbol in sorted(expression.free_symbols, key=lambda item: item.name):
            safe = py_name(symbol.name)
            if safe != symbol.name:
                code = re.sub(rf"\b{re.escape(symbol.name)}\b", safe, code)
        lines.append(f"    {py_name(name)} = round_step({code}, {places})")
    return "\n".join(lines)


def function_source(entry: dict, places: int, steps) -> str:
    arguments = ", ".join(py_name(name) for name in entry["parameters"])
    constants = [
        record
        for record in entry["constants"]
        if record["symbol"] != "pi"
    ]
    assignments = "\n".join(
        f"    {py_name(record['symbol'])} = {record['python']}" for record in constants
    )
    body = render_steps(steps, places)
    returns = ", ".join(f"{name!r}: {py_name(name)}" for name, _expression in steps)
    formula_comments = "\n".join(f"    # {formula}" for formula in entry["formulas"])
    parts = [f"def {entry['function']}({arguments}):", formula_comments]
    if assignments:
        parts.append(assignments)
    parts.append(body)
    parts.append(f"    return {{{returns}}}")
    return "\n".join(parts) + "\n"


def module_source(entries: list[dict], places: int, steps_by_id: dict) -> str:
    functions = "\n\n".join(
        function_source(entry, places, steps_by_id[entry["id"]]) for entry in entries
    )
    helper = (
        "def round_step(value, places):\n"
        "    quantum = Decimal(1).scaleb(-places)\n"
        "    return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP))\n"
    )
    return MODULE_HEADER + f"\nROUNDING_DECIMAL = {places}\n\n" + helper + "\n\n" + functions


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(f"calculations_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise FormulaError(f"Could not load generated functions: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_parameters(names: list[str], count: int = 4) -> list[dict]:
    base = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 8.0, 9.5]
    rows = []
    for row_index in range(count):
        values = {}
        for column, name in enumerate(names):
            values[name] = base[(row_index * 3 + column) % len(base)]
        rows.append(values)
    return rows


def substitute_knowns(expression, env: dict):
    mapping = {}
    for symbol in expression.free_symbols:
        if symbol.name in env:
            mapping[symbol] = env[symbol.name]
        elif symbol.name in SAFE_CONSTANTS:
            mapping[symbol] = float(SAFE_CONSTANTS[symbol.name])
    return expression.subs(mapping)


def validate_entry(entry: dict, steps, module, places: int) -> None:
    equations = [parse_formula(formula) for formula in entry["formulas"]]
    for sample in sample_parameters(entry["parameters"]):
        rounded = dict(sample)
        exact = dict(sample)
        python_exact = dict(sample)
        for name, expression in steps:
            exact_value = substitute_knowns(expression, exact).evalf()
            if exact_value.free_symbols or not exact_value.is_real:
                raise FormulaError(f"{entry['id']} did not evaluate {name} from {sample}.")
            python_value = evaluate_step(expression, python_exact)
            if abs(python_value - float(exact_value)) > 1e-6 * max(1.0, abs(float(exact_value))):
                raise FormulaError(f"{entry['id']} Python code for {name} does not match the solved formula.")
            exact[name] = exact_value
            python_exact[name] = python_value
            rounded[name] = round_step(evaluate_step(expression, rounded), places)
        mapping = {sympy.Symbol(name): value for name, value in exact.items()}
        for equation in equations:
            residual = (equation.lhs - equation.rhs).subs(mapping).evalf()
            scale = abs(complex(equation.lhs.subs(mapping).evalf())) + 1.0
            if abs(complex(residual)) / scale > 1e-6:
                raise FormulaError(
                    f"{entry['id']} does not satisfy its formulas for parameters {sample}."
                )
        produced = getattr(module, entry["function"])(**sample)
        for name, _expression in steps:
            if abs(produced[name] - rounded[name]) > 1e-9:
                raise FormulaError(
                    f"{entry['function']} returned {name}={produced[name]}, expected {rounded[name]}."
                )


def build_functions(data: dict, calc_path: Path) -> dict:
    places = int(data["rounding_decimal"])
    steps_by_id = {}
    for entry in data["equation_sets"]:
        if not entry.get("parameters") and entry.get("parameters") != []:
            fail(f"{entry['id']} has no parameters yet. Classify that set first.")
        if "computed" not in entry:
            fail(f"{entry['id']} has no computed variables yet. Classify that set first.")
        equations = [parse_formula(formula) for formula in entry["formulas"]]
        steps = elimination_steps(equations, list(entry["computed"]))
        entry["computed"] = [name for name, _expression in steps]
        entry["steps"] = [
            {"symbol": name, "expression": pycode(expression)}
            for name, expression in steps
        ]
        entry["function"] = entry.get("function") or f"solve_{entry['id']}"
        steps_by_id[entry["id"]] = steps
        entry["validated"] = False
    source = module_source(data["equation_sets"], places, steps_by_id)
    destination = module_path_for(calc_path)
    destination.write_text(source, encoding="utf-8")
    data["functions_module"] = str(destination)
    module = load_module(destination)
    for entry in data["equation_sets"]:
        validate_entry(entry, steps_by_id[entry["id"]], module, places)
        entry["validated"] = True
    return data


def accepted_scenarios(path: Path) -> tuple[dict, list[str]]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        fail(f"Scenario file must be a mapping: {path}")
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list):
        fail("Scenario file is missing scenarios.")
    if any(item.get("status") == "pending" for item in scenarios):
        fail("Resolve pending scenarios before building calculations.")
    accepted = [item["text"] for item in scenarios if item.get("status") == "accepted" and item.get("text")]
    target = data.get("target")
    if not isinstance(target, int) or isinstance(target, bool):
        fail("Scenario file target must be an integer.")
    if len(accepted) < target:
        fail(
            f"Scenario list has {len(accepted)} accepted scenarios and target {target}. "
            "Finish Agents 2 and 3 first."
        )
    return data, accepted


def blank_set(index: int, formulas: list[str]) -> dict:
    parsed = []
    symbols: list[str] = []
    for formula in formulas:
        equation = parse_formula(formula)
        parsed.append(str(equation))
        for name in ordered_names(formula, equation):
            if name not in symbols:
                symbols.append(name)
    return {
        "id": f"eqset_{index:02d}",
        "formulas": formulas,
        "parsed": parsed,
        "symbols": symbols,
        "function": f"solve_eqset_{index:02d}",
    }


def read_input(path: Path) -> tuple[dict, dict]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        fail(f"Input YAML must be a mapping: {path}")
    structure = data.get("structure")
    if not isinstance(structure, dict) or "formulas" not in structure:
        fail("structure.formulas is missing from the input file.")
    return data, optional_block(data)


def public_set(entry: dict) -> dict:
    payload = {
        "id": entry["id"],
        "formulas": entry["formulas"],
        "symbols": entry["symbols"],
        "equation_count": len(entry["formulas"]),
        "constants": [record["symbol"] for record in entry.get("constants", [])],
    }
    if entry.get("parameters") is not None and "computed" in entry:
        payload["parameters"] = entry["parameters"]
        payload["computed"] = entry["computed"]
    return payload


def snapshot(data: dict, path: Path) -> dict:
    sets = data.get("equation_sets", [])
    rows = data.get("rows", [])
    validated = bool(sets) and all(item.get("validated") for item in sets)
    return {
        "file": str(path),
        "functions_module": data.get("functions_module"),
        "needs_classifier": bool(data.get("needs_classifier")),
        "classify_attempts": int(data.get("classify_attempts", 0)),
        "validated": validated,
        "equation_sets": [public_set(item) for item in sets],
        "rows": len(rows),
        "complete": validated and len(rows) == len(sets) * max(len({row.get("scenario_index") for row in rows}), 0)
        if rows
        else False,
        "error": data.get("error"),
    }


def cmd_prepare(args: argparse.Namespace) -> None:
    out = args.out or default_calc_path(args.input)
    if out.exists() and not args.force:
        fail(f"Calculation file already exists: {out}. Pass --force to replace it.")
    _scenario_data, _accepted = accepted_scenarios(args.scenarios)
    try:
        source, block = read_input(args.input)
        combinations = expand_formulas(source["structure"]["formulas"])
        sets = [blank_set(index, formulas) for index, formulas in enumerate(combinations, start=1)]
        items = parse_parameter_spec(block.get("parameters"))
    except FormulaError as exc:
        fail(str(exc))
    specifications = source["structure"].get("variable_specifications") or []
    if isinstance(specifications, str):
        specifications = [specifications]
    data = {
        "source_input": str(args.input),
        "source_scenarios": str(args.scenarios),
        "rounding_decimal": rounding_places(block),
        "needs_classifier": not items,
        "classify_attempts": 0,
        "parameters_source": "input" if items else None,
        "variable_specifications": specifications,
        "equation_sets": sets,
        "rows": [],
    }
    tolerance = tolerance_value(block)
    if tolerance is not None:
        data["tolerance"] = tolerance
    if items:
        try:
            classify_specified(sets, items)
        except ClassificationError as exc:
            emit(
                {
                    "file": str(out),
                    "stop": True,
                    "needs_classifier": False,
                    "error": str(exc),
                    "equation_sets": [
                        {
                            "id": entry["id"],
                            "formulas": entry["formulas"],
                            "symbols": entry["symbols"],
                            "equation_count": len(entry["formulas"]),
                        }
                        for entry in sets
                    ],
                },
                2,
            )
        data["needs_classifier"] = False
    else:
        for entry in sets:
            constants = constant_names_for(entry["symbols"], None)
            entry["constants"] = [constant_record(name) for name in constants]
    save(out, data)
    emit(snapshot(data, out))


def classification_errors(data: dict, proposed: list[dict]) -> list[str]:
    if not isinstance(proposed, list):
        return ["Classifier JSON must contain a list under sets."]
    by_id = {}
    errors = []
    for item in proposed:
        if not isinstance(item, dict) or "id" not in item:
            errors.append("Each set needs an id, parameters, and computed.")
            continue
        by_id[item["id"]] = item
    expected = [entry["id"] for entry in data["equation_sets"]]
    if set(by_id) != set(expected):
        errors.append(
            "Classifier sets must be exactly: " + ", ".join(expected) + "."
        )
        return errors
    roles: dict[str, set[str]] = {}
    for entry in data["equation_sets"]:
        item = by_id[entry["id"]]
        parameters = item.get("parameters")
        computed = item.get("computed")
        if not isinstance(parameters, list) or not isinstance(computed, list):
            errors.append(f"{entry['id']} needs list fields parameters and computed.")
            continue
        try:
            parameters = [normalize_symbol(str(name)) for name in parameters]
            computed = [normalize_symbol(str(name)) for name in computed]
        except FormulaError as exc:
            errors.append(str(exc))
            continue
        constants = {record["symbol"] for record in entry.get("constants", [])}
        pool = [name for name in entry["symbols"] if name not in constants]
        if len(computed) != len(entry["formulas"]):
            errors.append(
                f"{entry['id']} has {len(entry['formulas'])} equations and computed variables {computed}."
            )
        if len(parameters) != len(set(parameters)) or len(computed) != len(set(computed)):
            errors.append(f"{entry['id']} repeats a variable.")
        if set(parameters) & set(computed):
            errors.append(f"{entry['id']} lists a variable as both a parameter and a computed variable.")
        if set(parameters) | set(computed) != set(pool):
            errors.append(
                f"{entry['id']} must use each non-constant symbol once. "
                f"Symbols: {pool}. Constants already removed: {sorted(constants) or '[]'}."
            )
        for name in pool:
            role = "parameters" if name in parameters else "computed"
            if name in parameters or name in computed:
                roles.setdefault(name, set()).add(role)
        item["_parameters"] = parameters
        item["_computed"] = computed
    for name, used in roles.items():
        if len(used) != 1:
            errors.append(
                f"{name} must have the same role in every equation set where it appears."
            )
    return errors


def cmd_classify_receive(args: argparse.Namespace) -> None:
    data = load_calc(args.file)
    if not data.get("needs_classifier"):
        fail("parameters are already classified. Continue with build.")
    data["classify_attempts"] = int(data.get("classify_attempts", 0)) + 1
    save(args.file, data)
    payload = snapshot(data, args.file)
    payload["stop"] = data["classify_attempts"] > MAX_CLASSIFY_ATTEMPTS
    payload["variable_specifications"] = data.get("variable_specifications", [])
    emit(payload, 2 if payload["stop"] else 0)


def cmd_apply(args: argparse.Namespace) -> None:
    data = load_calc(args.file)
    if not data.get("needs_classifier"):
        fail("parameters are already classified. Continue with build.")
    try:
        proposed = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Classifier JSON is invalid: {exc}")
    sets = proposed.get("sets") if isinstance(proposed, dict) else None
    errors = classification_errors(data, sets)
    if errors:
        payload = snapshot(data, args.file)
        payload["ok"] = False
        payload["stop"] = int(data.get("classify_attempts", 0)) > MAX_CLASSIFY_ATTEMPTS
        payload["errors"] = errors
        emit(payload, 2 if payload["stop"] else 1)
    for entry in data["equation_sets"]:
        match = next(item for item in sets if item["id"] == entry["id"])
        entry["parameters"] = match["_parameters"]
        entry["computed"] = match["_computed"]
    data["needs_classifier"] = False
    data["parameters_source"] = "classifier"
    data.pop("error", None)
    save(args.file, data)
    payload = snapshot(data, args.file)
    payload["ok"] = True
    emit(payload)


def cmd_build(args: argparse.Namespace) -> None:
    data = load_calc(args.file)
    if data.get("needs_classifier"):
        fail("Choose parameters and computed variables before build.")
    try:
        data = build_functions(data, args.file)
    except Exception as exc:
        data["error"] = str(exc)
        save(args.file, data)
        payload = snapshot(data, args.file)
        payload["stop"] = True
        emit(payload, 2)
    data.pop("error", None)
    save(args.file, data)
    emit(snapshot(data, args.file))


def cmd_associate(args: argparse.Namespace) -> None:
    data = load_calc(args.file)
    if not data.get("equation_sets") or not all(item.get("validated") for item in data["equation_sets"]):
        fail("Build and validate the calculation functions before associate.")
    scenario_path = Path(data["source_scenarios"])
    _scenario_data, accepted = accepted_scenarios(scenario_path)
    rows = []
    number = 1
    for scenario_index, text in enumerate(accepted):
        for entry in data["equation_sets"]:
            rows.append(
                {
                    "id": f"row_{number:03d}",
                    "scenario_index": scenario_index,
                    "scenario": text,
                    "equation_set": entry["id"],
                    "formulas": entry["formulas"],
                    "constants": entry["constants"],
                    "parameters": entry["parameters"],
                    "computed": entry["computed"],
                    "function": entry["function"],
                }
            )
            number += 1
    data["rows"] = rows
    save(args.file, data)
    payload = snapshot(data, args.file)
    payload["complete"] = True
    payload["accepted_scenarios"] = len(accepted)
    payload["equation_set_count"] = len(data["equation_sets"])
    emit(payload)


def cmd_status(args: argparse.Namespace) -> None:
    data = load_calc(args.file)
    emit(snapshot(data, args.file))


def load_calc(path: Path) -> dict:
    data = load_yaml(path)
    if not isinstance(data, dict) or "equation_sets" not in data:
        fail(f"Calculation file is missing equation_sets: {path}")
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    prepare = commands.add_parser("prepare", help="Expand formula combinations into the calculation file")
    prepare.add_argument("--input", required=True, type=Path)
    prepare.add_argument("--scenarios", required=True, type=Path)
    prepare.add_argument("--out", type=Path)
    prepare.add_argument("--force", action="store_true")
    prepare.set_defaults(func=cmd_prepare)

    receive = commands.add_parser(
        "classify-receive",
        help="Increment classify_attempts because a classifier pass is starting",
    )
    receive.add_argument("--file", required=True, type=Path)
    receive.set_defaults(func=cmd_classify_receive)

    apply = commands.add_parser("apply", help="Store a classifier JSON if it satisfies the checks")
    apply.add_argument("--file", required=True, type=Path)
    apply.add_argument("--json-file", required=True, type=Path)
    apply.set_defaults(func=cmd_apply)

    build = commands.add_parser("build", help="Write and validate calculation functions")
    build.add_argument("--file", required=True, type=Path)
    build.set_defaults(func=cmd_build)

    associate = commands.add_parser(
        "associate",
        help="Pair every accepted scenario with every equation set",
    )
    associate.add_argument("--file", required=True, type=Path)
    associate.set_defaults(func=cmd_associate)

    status = commands.add_parser("status", help="Show calculation progress without changing the file")
    status.add_argument("--file", required=True, type=Path)
    status.set_defaults(func=cmd_status)
    return parser


def main() -> None:
    configure_stdio()
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
