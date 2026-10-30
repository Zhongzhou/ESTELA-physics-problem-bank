---
name: problem-creation
description: >-
  Runs the physics problem-creation workflow: check an input-scheme YAML,
  normalize formulas to LaTeX, confirm with the user, generate and critique
  scenarios, then build calculation functions and associate each accepted
  scenario with every equation set. Use when the user asks to run the
  problem-creation workflow, check an input scheme, or generate physics
  problem scenarios from an input-scheme YAML.
---

# Problem creation

Orchestrate the workflow below. You talk to the user yourself for Agent 1 and for the confirmation gate. Spawn Agent 2, Agent 3, and the Agent 4 classifier with the Task tool (`subagent_type: generalPurpose`). Python is the only writer of `update_count`, the scenario target, the calculation sidecar, and the calculation functions.

Scripts, run from the repo root with the project virtual environment. On Windows that interpreter is `.venv/Scripts/python.exe`. On macOS or Linux it is `.venv/bin/python`. Do not use a system `python` or `py -3`.

```bash
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/validate_input.py "INPUT.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py init --input "INPUT.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py receive --file "INPUT.scenarios.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py status --file "INPUT.scenarios.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py add --file "INPUT.scenarios.yaml" --text "..."
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py remove --file "INPUT.scenarios.yaml" --index 0 --reason "..."
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py set-target --file "INPUT.scenarios.yaml" --input "INPUT.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/calculation_table.py prepare --input "INPUT.yaml" --scenarios "INPUT.scenarios.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/calculation_table.py classify-receive --file "INPUT.calculations.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/calculation_table.py apply --file "INPUT.calculations.yaml" --json-file "classify.json"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/calculation_table.py build --file "INPUT.calculations.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/calculation_table.py associate --file "INPUT.calculations.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/calculation_table.py status --file "INPUT.calculations.yaml"
```

The environment is the repo-root `.venv` directory, which git ignores. Recreate it with `py -3 -m venv .venv`, then install [requirements.txt](requirements.txt) using that interpreter.

`init` writes `INPUT.scenarios.yaml` beside the input. `target` in that file is copied from `context.n_scenarios`. Never type a scenario count into a prompt or a script call except by passing values printed in the script JSON (`target`, `needed`).

`prepare` writes `INPUT.calculations.yaml` beside the input, and `build` writes `INPUT.calculations.py` beside that file. Do not type a computed-variable count into a prompt. Use `equation_count` from the script JSON.

Quote paths that contain spaces. If a sidecar already exists, ask the user before `init --force` or `prepare --force`.

## 1. Check the input

Read [agents/input-checker.md](agents/input-checker.md) and follow it. If the user did not name a file, ask which input YAML to use.

After editing, show the YAML and any validator warnings, then stop. Do not run `init`, `receive`, Agents 2 and 3, or the calculation scripts in this turn.

## 2. Generate and critique

Start this section only after the user explicitly confirms the input.

```text
- [ ] init the sidecar
- [ ] receive
- [ ] stop, finish, or generate
- [ ] add the new scenarios
- [ ] critique and remove
- [ ] repeat until complete or stopped
```

1. `init --input` the confirmed file.
2. `receive`. This increments `update_count`.
   - Exit code 2 (`stop: true`): `update_count` is greater than 5 and accepted scenarios are still below `target`. Tell the user the model could not find enough scenarios. Give them the sidecar path. Ask whether to lower `context.n_scenarios` or to adjust `context.scenario_specifications`.
   - `complete: true`: go to the calculation stage.
   - Otherwise spawn Agent 2.
3. Agent 2 prompt is the full text of [agents/scenario-generator.md](agents/scenario-generator.md) plus the scenario, the specifications, `accepted_texts`, `rejected`, and `needed` from the receive JSON. Append each returned string with `add --text`. One `add` call may take several `--text` flags.
4. Agent 3 prompt is the full text of [agents/scenario-critic.md](agents/scenario-critic.md) plus the specifications and `pending_texts` from the add JSON, numbered from 0. Apply the reviews with one `remove` call. Pass `--index` and `--reason` only for `keep: false`. If every pending scenario is kept, run `remove` with no index. If the review count does not match the pending list, run Agent 3 once more. If it still does not match, stop and tell the user. The sidecar is unchanged until `remove` succeeds.
5. When `remove` or `status` reports `complete: true`, go to the calculation stage. Otherwise go back to `receive`.

Subagents return JSON only. They do not edit the sidecar and they do not call each other.

### After a stop

Edit the input file with the user's new `n_scenarios` and/or specifications. Wait until they confirm another attempt. Then run `set-target --input` so the sidecar copies `context.n_scenarios` and `update_count` returns to 0. Accepted and rejected scenarios stay in the file.

If that status is `complete: true`, go to the calculation stage. If not, go back to `receive`.

The scenario sidecar remains on disk, including after an early stop. `scenarios` entries with `status: accepted` are the kept list, and `rejected` keeps the removed text plus the reason.

## 3. Equations, functions, and scenario rows

Start this section only after the scenario status is `complete: true`.

`question_unknowns` and `unknown_rotation` stay unused. Do not send them to a subagent.

```text
- [ ] prepare
- [ ] classify, when parameters is omitted
- [ ] build the functions
- [ ] associate accepted scenarios
```

1. `prepare --input` the confirmed file and `--scenarios` its sidecar.
   - Exit code 2 (`stop: true`): the supplied `parameters` list does not leave one computed variable per equation. Tell the user the `error` text. The calculation file is not written. Wait until they change `parameters` and confirm another attempt, then run `prepare` again.
   - `needs_classifier: false`: `parameters` was present. Go to `build`.
   - `needs_classifier: true`: `parameters` was omitted. Go to `classify-receive`.
2. `classify-receive`. This increments `classify_attempts`.
   - Exit code 2 (`stop: true`): more than 5 classifier passes have failed. Tell the user the model could not split the symbols. Give them the calculation-file path.
   - Otherwise spawn the classifier. Its prompt is the full text of [agents/equation-classifier.md](agents/equation-classifier.md) plus the `classify-receive` JSON. On a retry, also include `errors` from the last `apply`.
3. Write the classifier JSON to `classify.json` beside the calculation file. `apply --json-file` that path.
   - `ok: true`: go to `build`.
   - `ok: false` and `stop: false`: go back to `classify-receive`.
   - `stop: true`: tell the user the `errors`, then stop.
4. `build`. This writes the Python module and checks each function against its formulas.
   - Exit code 2 (`stop: true`): the formulas could not be solved or the check failed. Tell the user the `error` text and both file paths, then stop.
5. `associate`. This pairs every accepted scenario with every equation set. Constants stay at the fixed values stored on the row. Parameters stay function arguments. Computed variables stay function outputs. This step does not choose random numbers.

`prepare` reads `other (optional).parameters`. A choice such as `T or f` is resolved from the symbols in each equation set. When that field is omitted, the classifier chooses the split: parameters are easier to estimate, and computed variables are harder to estimate. Safe constants that appear in the formulas, including `pi` and `g`, are fixed inside the functions unless the user listed that symbol under `parameters`. `g` uses `9.80`. Each computed value is rounded to `rounding_decimal` (default 2) at that step. Constants keep full precision.

## Finish

Tell the user the calculation table is complete. Give the scenario sidecar path, the calculation sidecar path, and the function-module path. For each equation set, give its id, parameters, computed variables, and function name. Give the row count from `associate`.

Open the calculation sidecar to review the result. `equation_sets` are the Agent 4 rows. `rows` are the Agent 5 pairs. Random numbers, question wording, and `unknown_rotation` versions are not part of this skill yet.
