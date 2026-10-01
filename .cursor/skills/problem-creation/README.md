# Problem-creation agents

This skill turns an input YAML into a reviewed list of physics scenarios. In Cursor, ask to run the problem-creation workflow and name the input file. The skill instructions are in [SKILL.md](SKILL.md). An example input is [problem-creation agents/input-scheme.yaml](<../../../problem-creation agents/input-scheme.yaml>).

Problem statements, numbers, and solutions are not generated yet. A later agent should read the confirmed input and the accepted scenarios.

## Usage

1. Create the repo virtual environment once, from the repository root:

```bash
py -3 -m venv .venv
.venv/Scripts/python.exe -m pip install -r .cursor/skills/problem-creation/requirements.txt
```

On macOS or Linux the interpreter is `.venv/bin/python`. The `.venv` directory is git-ignored.

2. Copy the example input, or start a new YAML with the same fields. Informal math is fine. The checker rewrites formulas into LaTeX.
3. In chat, ask to run the problem-creation workflow on that file.
4. Read the edited input. Answer any clarification questions. Confirm the input when it looks right. Scenario generation does not start before that confirmation.
5. When the run finishes, open the sidecar next to the input. For `input-scheme.yaml` the sidecar is `input-scheme.scenarios.yaml`.

If a sidecar already exists, the workflow asks before replacing it.

## Workflow

```text
Input YAML
  -> Agent 1 checks and edits the input
  -> you confirm
  -> Python creates the sidecar and copies context.n_scenarios into target
  -> repeat:
       Python increments update_count
       Agent 2 writes the scenarios still needed
       Agent 3 keeps or rejects that batch
  -> sidecar file with the accepted list
```

Python is the only writer of `target` and `update_count`. The target is always copied from `context.n_scenarios` in the input file. Agent prompts do not contain a fixed scenario count.

`update_count` starts at 0. It increases by 1 each time a generation pass starts. Passes 1 through 5 are allowed. If the count goes past 5 and the accepted list is still short of `target`, the run stops. You can lower `context.n_scenarios` or change `context.scenario_specifications`, confirm another attempt, and continue. Lowering the target writes the new number back to the input, copies it into the sidecar, and resets `update_count` to 0. Scenarios already accepted or rejected stay in the file. If the accepted list already meets the new target, the run finishes.

A value of `n_scenarios` greater than 10 produces a warning during the input check. The warning does not block confirmation.

## Agents

### Agent 1: input checker

Instructions: [agents/input-checker.md](agents/input-checker.md).

The chat agent does this step itself and edits the input file in place. It rewrites every formula string into standard LaTeX, including formulas nested under a branch such as `One of:`. It asks you when a required field is missing or ambiguous, for example when a symbol in `possible_unknowns` does not match the formulas. It then shows the edited YAML and waits.

Required fields:

- `name`
- `context.scenario`
- `context.scenario_specifications`
- `context.n_scenarios` (a positive integer)
- `structure.formulas`
- `structure.variable_specifications`
- `structure.possible_unknowns`

`other (optional)` and every field under it may be empty.

### Agent 2: scenario generator

Instructions: [agents/scenario-generator.md](agents/scenario-generator.md).

A separate subagent writes only the number of scenarios still needed. Each scenario is one or two short sentences describing a situation, not a full problem, not given numbers, and not a solution. It must follow the scenario specifications and must not repeat an accepted scenario, a rejected scenario, or a close paraphrase of either.

### Agent 3: scenario critic

Instructions: [agents/scenario-critic.md](agents/scenario-critic.md).

A separate subagent judges only the new batch. It rejects a scenario that breaks a specification or that is unsuitable as the setting of an introductory physics calculation problem. Each rejection includes a short reason. Survivors are marked accepted. The parent agent applies those decisions with the Python script, then asks Agent 2 to fill whatever gap remains.

## Result file

The sidecar stays on disk after a finished run and after an early stop. Accepted scenarios are the `scenarios` entries with `status: accepted`. Removed ones are under `rejected` with the reason.

```yaml
source_input: path/to/input.yaml
target: 10          # copied from context.n_scenarios
update_count: 2
scenarios:
  - text: A puck slides at constant speed in a horizontal circle on a frictionless air table.
    status: accepted
rejected:
  - text: In the Bohr model, an electron moves in a circular orbit about a proton.
    reason: A Bohr-model electron is a quantum mechanical particle, which the specifications exclude.
```

`target` in a real file is whatever `context.n_scenarios` was when the sidecar was created or last updated.

## Scripts

Run these from the repository root with `.venv/Scripts/python.exe`. Replace `INPUT.yaml` with the input path. The sidecar path is the input path with `.scenarios.yaml` added before the extension, beside the input file.

| Script | Role |
| --- | --- |
| `scripts/validate_input.py INPUT.yaml` | Report missing required fields, the formula strings, and a warning when `n_scenarios` is greater than 10. |
| `scripts/scenario_list.py init --input INPUT.yaml` | Create the sidecar and copy `context.n_scenarios` into `target`. |
| `scripts/scenario_list.py receive --file SIDECAR.yaml` | Start a generation pass and increment `update_count`. Exit code 2 means the round cap was hit and the target is still unmet. |
| `scripts/scenario_list.py add --file SIDECAR.yaml --text "..."` | Append pending scenarios. Repeat `--text` for each one. |
| `scripts/scenario_list.py remove --file SIDECAR.yaml --index 0 --reason "..."` | Reject pending items by their index in the new batch and accept the rest. Omit `--index` to accept the whole batch. |
| `scripts/scenario_list.py status --file SIDECAR.yaml` | Print the current counts without changing the file. |
| `scripts/scenario_list.py set-target --file SIDECAR.yaml --input INPUT.yaml` | Copy `context.n_scenarios` again and reset `update_count` to 0. |

Quote paths that contain spaces.
