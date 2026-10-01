# Agent 1: input checker

You are the parent agent. Read this file and edit the user's input YAML yourself. Do not spawn a subagent for this step.

## Required fields

These must be present and non-empty:

- `name`
- `context.scenario`
- `context.scenario_specifications`
- `context.n_scenarios` (a positive integer)
- `structure.formulas`
- `structure.variable_specifications`
- `structure.possible_unknowns`

The key `other (optional)` and every field under it may be empty. Leave those fields alone unless the user supplied text there that is relevant to a clarification.

## What to do

1. Run `scripts/validate_input.py` on the input file.
2. Rewrite every formula string into standard LaTeX. Edit the input file directly. Keep branching groups such as a key `One of:` whose value is a list of formulas. Rewrite the strings inside those lists too.
   - `F_net = m v^2 / r` becomes `F_{\mathrm{net}} = \frac{m v^{2}}{r}`
   - A bare `pi` becomes `\pi`
3. If the validator lists missing fields, or a required value is ambiguous, ask the user. One ambiguity to catch: a symbol in `possible_unknowns` that does not match the symbols in the formulas. Do not invent physics requirements the user did not state.
4. If `warnings` is non-empty, show each warning. A warning that `n_scenarios` is greater than 10 does not block confirmation.
5. Show the edited YAML. Then stop.

The scenario sidecar and Agents 2 and 3 start only after the user explicitly confirms this input in a later message.
