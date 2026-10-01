---
name: problem-creation
description: >-
  Runs the physics problem-creation workflow: check an input-scheme YAML,
  normalize formulas to LaTeX, confirm with the user, then generate and
  critique scenarios into a sidecar file. Use when the user asks to run the
  problem-creation workflow, check an input scheme, or generate physics
  problem scenarios from an input-scheme YAML.
---

# Problem creation

Orchestrate three stages. You talk to the user yourself for Agent 1 and for the confirmation gate. Spawn Agent 2 and Agent 3 with the Task tool (`subagent_type: generalPurpose`). Python is the only writer of `update_count` and of the scenario target.

Scripts, run from the repo root with the project virtual environment. On Windows that interpreter is `.venv/Scripts/python.exe`. On macOS or Linux it is `.venv/bin/python`. Do not use a system `python` or `py -3`.

```bash
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/validate_input.py "INPUT.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py init --input "INPUT.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py receive --file "INPUT.scenarios.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py status --file "INPUT.scenarios.yaml"
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py add --file "INPUT.scenarios.yaml" --text "..."
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py remove --file "INPUT.scenarios.yaml" --index 0 --reason "..."
.venv/Scripts/python.exe .cursor/skills/problem-creation/scripts/scenario_list.py set-target --file "INPUT.scenarios.yaml" --input "INPUT.yaml"
```

The environment is the repo-root `.venv` directory, which git ignores. Recreate it with `py -3 -m venv .venv`, then install [requirements.txt](requirements.txt) using that interpreter.

`init` writes `INPUT.scenarios.yaml` beside the input. `target` in that file is copied from `context.n_scenarios`. Never type a scenario count into a prompt or a script call except by passing values printed in the script JSON (`target`, `needed`).

Quote paths that contain spaces. If a sidecar already exists, ask the user before `init --force`.

## 1. Check the input

Read [agents/input-checker.md](agents/input-checker.md) and follow it. If the user did not name a file, ask which input YAML to use.

After editing, show the YAML and any validator warnings, then stop. Do not run `init`, `receive`, or Agents 2 and 3 in this turn.

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
   - `complete: true`: go to the finish step.
   - Otherwise spawn Agent 2.
3. Agent 2 prompt is the full text of [agents/scenario-generator.md](agents/scenario-generator.md) plus the scenario, the specifications, `accepted_texts`, `rejected`, and `needed` from the receive JSON. Append each returned string with `add --text`. One `add` call may take several `--text` flags.
4. Agent 3 prompt is the full text of [agents/scenario-critic.md](agents/scenario-critic.md) plus the specifications and `pending_texts` from the add JSON, numbered from 0. Apply the reviews with one `remove` call. Pass `--index` and `--reason` only for `keep: false`. If every pending scenario is kept, run `remove` with no index. If the review count does not match the pending list, run Agent 3 once more. If it still does not match, stop and tell the user. The sidecar is unchanged until `remove` succeeds.
5. When `remove` or `status` reports `complete: true`, finish. Otherwise go back to `receive`.

Subagents return JSON only. They do not edit the sidecar and they do not call each other.

### After a stop

Edit the input file with the user's new `n_scenarios` and/or specifications. Wait until they confirm another attempt. Then run `set-target --input` so the sidecar copies `context.n_scenarios` and `update_count` returns to 0. Accepted and rejected scenarios stay in the file.

If that status is `complete: true`, finish. If not, go back to `receive`.

## Finish

Tell the user the scenarios are complete. Print the accepted texts and the sidecar path.

The sidecar remains on disk, including after an early stop. Open it to review the result: `scenarios` entries with `status: accepted` are the kept list, and `rejected` keeps the removed text plus the reason. The chat message points at that file.

## Downstream agents

Problem writing, numbers, and solution generation are not part of this skill yet. A later agent should read the confirmed input YAML and the accepted scenarios in the sidecar.
