# Pre-exam AI quality audit — Physics I multiple-choice banks

**Date:** 2026-11-11  
**Inputs:** `PHY1-CLM-CE2DMC-11102026.yaml` (24 momentum questions) and `PHY1-RM-TBORMC-11102026.yaml` (30 torque questions).  
**Scope:** Independent computational re-solving from values parsed from problem statements; multiple-choice uniqueness, spacing, plausibility, and text-based physics feasibility. The separately referenced figures, source numerical banks, and `choice-set-adaptation.md` were not uploaded and were **not** visually or historically verified.

## Executive verdict

**Both banks' answer keys pass numerical verification: 54/54.** All key values agree with solutions calculated independently from the problem bodies at the requested rounding precision; 54/54 questions have exactly one keyed choice; no repeated numerical choice occurs within a question. In the torque bank all 30 text-derived location triplets match the location metadata embedded in their referenced image filenames, **but this does not verify the pictures themselves**.

**Not yet exam-ready without review of distractors, mass wording, and diagram assets.** All 54 correct choices occupy answer position 1 in the YAML; actual exposure depends on whether the testing platform shuffles.

## Quantitative metrics

| Check | Momentum bank (24) | Torque bank (30) |
|---|---:|---:|
| Independently correct keys | 24/24 | 30/30 |
| Exactly one keyed answer | 24/24 | 30/30 |
| Unique numerical choices per question | 24/24 | 30/30 |
| Key at first position | 24/24 | 30/30 |
| Questions with a distractor <1% from key | 7 | 0 |
| Questions with a distractor <5% from key | 9 | 1 |
| Questions with any pair of options <1% apart relative to key | 12 | 0 |
| Questions with two choices ≤0.05 m/s or ≤1 N apart | 7 | 7 |
| Negative numeric distractors for nonnegative requested magnitudes | 16 | 0 |
| Figures embedded in YAML as references | 0 | 30 (images not provided) |

*All relative distance percentages are calculated as `abs(choice1-choice2)/abs(correct_key)×100` and are **screening flags, not proven psychometric acceptance thresholds**. Pairwise closeness considers wrong–wrong pairs too; distance from the correct key is a different metric.*

## Highest-priority issues

### 1. Check answer shuffling (both banks)

**All 54 YAML answer arrays put the keyed correct choice first.** This is an immediate test-security issue only if the exam platform preserves the original order. Run a full student-preview test and confirm randomization per delivered question, not just per bank.

### 2. Invalid negative-speed distractors (momentum)

The momentum bank includes **16 negative candidate magnitudes** even though every question asks for a speed or magnitude of velocity. In particular: q1, q5, q6, q7, q9, q11, q13, q14, q18, q20, q22, q23, q24. Negative vector *components* can make sense; negative *speed* does not. Replace negative numeric choices with positive values tied to a traceable, plausible calculation error. Do not simply take the absolute value without checking whether it duplicates an existing option.

### 3. Near-indistinguishable options (both banks)

- **Within 1% of the correct momentum key:** q1, q2, q3, q7, q9, q11, q19.
- **Within 5% of the correct momentum key:** q1, q2, q3, q7, q9, q11, q16, q17, q19.
- **Any pair of momentum choices within 0.05 m/s:** q2, q7, q8, q11, q15, q16, q19.
- **Torque wrong–wrong options 1 N apart:** q10, q13, q15, q19, q21, q25, q28. No torque distractor lies only 1 N away from its correct answer; the 1 N pairs occur among distractors.

**Examples:** Momentum q2 lists `5009.23` and `5009.24 m/s` as *different distractors* (0.01 m/s apart); q3 lists correct `8066.94` and distractor `8066.67 m/s` (0.27 m/s, ≈0.0033% apart); q7 lists `4.53` correct and `4.50 m/s` (only three reported 0.01-m/s increments); torque q10 includes wrong alternatives `24 N` and `25 N`.

Recommendation: set an agreed numerical separation rule for **every pair**, not just correct-vs-distractor. A pilot threshold worth reviewing is 5% of correct magnitude *plus a minimum number of output precision increments*, with instructor overrides for deliberately subtle misconception checks. Avoid blindly widening useful diagnostic distractors if doing so breaks their connection to a student mistake; instead adjust the given scenario values.

### 4. Feasibility and clarity of the physical story

- **Momentum q7:** It begins with a `70 kg roller skater` but says the skater is `60 kg` immediately after throwing a `10 kg` bag. Reword the first mass as the **combined skater-and-bag system**. Without this, the stated skater appears to lose 10 kg merely by throwing another object.
- **Momentum q10:** A `180 kg bumper car` becomes a `110 kg bumper car` after a `70 kg passenger` jumps. State that `180 kg` is the **car-and-passenger total** before the jump.
- **Momentum q8, q9, q11, q12:** Similar, weaker ambiguities about whether the original submarine, spaceship, hovercraft, or sled mass includes the released/pushed object. Make each initial mass explicitly a *combined system mass*. This is a wording fix; the keyed values are correct under the combined-mass interpretation.
- **Momentum q19:** Two train cars on merging railway tracks are a questionable example of an isolated **two-dimensional** inelastic collision. The rails can exert external transverse impulses; 2D momentum for the two-car system alone need not be conserved. Prefer freely moving carts/vehicles on an approximately frictionless 2D surface, or explicitly idealize the system and address rail impulse limitations.
- **Momentum q6:** The alpha particle's calculated speed is ≈5004 m/s, corresponding to kinetic energy ≈0.52 eV for a 4-u particle. This is an unusually weak energy scale for an ordinary alpha-decay story; consider revising the nuclear context or values if physical realism is important.
- **Momentum q1:** Revise `Round your answer to two decimal places after zero` to `Round your answer to two decimal places`.
- **Torque bank:** All 30 unknown weights/forces are positive and are uniquely determined by the text-derived lever arms; no torque-sign contradiction was found in the *text*. Final approval still requires inspecting all diagrams for positions, upward direction and 60° angle measured from the vertical.

### 5. Distractor-origin verification remains incomplete

The YAML metadata refers to `choice-set-adaptation.md`, source banks, scripts, and torque images. These were not among the two attachments. We can assess the **actual answer choices**, but cannot yet verify that each incorrect choice faithfully maps to its *intended* student error or that conversion preserved the original conditions. Provide the adaptation plan and images for a final cross-check.

## Reproducible independent physics checks

**Momentum separation/launch:**

`v_unknown = (M V_initial − m_known v_known)/(M−m_known)`, evaluated separately in x and y; then take vector magnitude. For forward sticking collisions: `v_final=(m1 v1+m2 v2)/(m1+m2)`. For inverse sticking: `v2=((m1+m2)v_final−m1 v1)/m2`.

**Torque balance:** Let `x` measure distance from right end of the horizontal 1-m rod. For pivot `x_p`, block `x_b`, and applied force `x_F`, use signed equilibrium:

`(x_F − x_p) F cos(60°) − (0.5 − x_p) W_rod − (x_b − x_p) W_block = 0`.

Solve for the one missing quantity; require a nonzero lever arm and nonnegative physical magnitude. The horizontal component of F is balanced by pivot reaction (not a torque about the pivot).

## Suggested reusable AI quality-control workflow

1. **Structural validator:** Load every YAML question, check unique IDs, answer count, exactly one correct flag, valid units/types, duplicate choice values, markup, and resolvable figure assets.
2. **Blind independent solver:** Pass the *problem body only*, with no answer choices or bank feedback, to a separate AI. Require a structured derivation, assumptions, and result, then check its calculation programmatically.
3. **Deterministic physics verifier:** For supported templates, solve by scripted vector conservation and signed torque balance; compare the computed result at the bank's requested precision with exactly one answer option.
4. **Feasibility checker:** Independently ask whether the numerical parameters and **story** can coexist: mass bookkeeping, positive weights, geometry, force directions, conservation assumptions, and units. Report `pass / needs clarification / infeasible` rather than relying on one binary judgment.
5. **Distractor evaluator:** Compute minimum distances **to key and among every pair**; flag invalid physical quantities, close duplicates, overly easy outliers, and distractors that do not correspond to a specific plausible misconception. The quality reviewer should be blind to the intended distractor labels initially.
6. **Visual and exam-delivery validator:** Compare each figure against the text (locations, directions, angles) and preview the exam in the actual LMS to confirm option shuffling, math rendering, asset visibility, and rounding instructions.
7. **Instructor signoff and revision loop:** Treat incorrect/absent keys, multiple numerically valid choices, unsolvable/problematic physics, mismatched figures, and unshuffled visible answer keys as **blocking**; treat weak distractors, suspiciously close options, and ambiguous but repairable stories as **revision** items. Re-run all checks after edits. A later student pilot can measure distractor selection frequencies; numerical separation alone does not establish educational quality.

## Question-by-question results

The columns below give the independently computed unrounded result, the YAML key, the closest distractor, and percentage difference from the key. `Neg` counts impossible negative options. `Pair` is the *smallest pairwise separation across all choices*. See CSV for explicit flag codes and parsed quantities.

### Momentum — 24 questions

| ID | Calculated (unrounded) | Key | Nearest distractor | Gap to key | Closest pair | Neg |
|---|---:|---:|---:|---:|---:|---:|
| q1 | 288.59814 | 288.60 | 286.67 | 0.669% | 1.12 | 1 |
| q2 | 5012.23501 | 5,012.24 | 5,009.99 | 0.045% | 0.01 | 0 |
| q3 | 8066.94214 | 8,066.94 | 8,066.67 | 0.003% | 0.27 | 0 |
| q4 | 5.38516 | 5.39 | 5.00 | 7.236% | 0.08 | 0 |
| q5 | 81.98916 | 81.99 | 73.33 | 10.562% | 0.61 | 1 |
| q6 | 5004.43906 | 5,004.44 | 617.97 | 87.652% | 101.89 | 2 |
| q7 | 4.52769 | 4.53 | 4.50 | 0.662% | 0.03 | 1 |
| q8 | 15.68502 | 15.69 | 14.90 | 5.035% | 0.02 | 0 |
| q9 | 1947.61646 | 1,947.62 | 1,944.44 | 0.163% | 3.18 | 1 |
| q10 | 5.5857 | 5.59 | 5.00 | 10.555% | 0.22 | 0 |
| q11 | 14.48712 | 14.49 | 14.44 | 0.345% | 0.05 | 1 |
| q12 | 13.45219 | 13.45 | 12.03 | 10.558% | 0.33 | 0 |
| q13 | 14.14214 | 14.14 | 10.00 | 29.279% | 0.62 | 1 |
| q14 | 4.47214 | 4.47 | 5.48 | 22.595% | 0.42 | 1 |
| q15 | 1.2813 | 1.28 | 0.86 | 32.812% | 0.01 | 0 |
| q16 | 5.1264 | 5.13 | 5.02 | 2.144% | 0.04 | 0 |
| q17 | 914.11159 | 914.11 | 900.00 | 1.544% | 0.26 | 0 |
| q18 | 31.62278 | 31.62 | 22.36 | 29.285% | 4.87 | 3 |
| q19 | 3.73893 | 3.74 | 3.71 | 0.802% | 0.03 | 0 |
| q20 | 1.5 | 1.50 | 0.72 | 52.000% | 0.07 | 1 |
| q21 | 4.6428 | 4.64 | 4.33 | 6.681% | 0.06 | 0 |
| q22 | 2.8748 | 2.87 | 2.02 | 29.617% | 0.06 | 1 |
| q23 | 27.85678 | 27.86 | 26.00 | 6.676% | 1.01 | 1 |
| q24 | 5.5509 | 5.55 | 3.88 | 30.090% | 0.27 | 1 |

### Torque — 30 questions

| ID | Calculated (unrounded) | Key | Nearest distractor | Gap to key | Closest pair | Neg |
|---|---:|---:|---:|---:|---:|---:|
| q1 | 44 | 44 | 41 | 6.818% | 3 | 0 |
| q2 | 16 | 16 | 18 | 12.500% | 2 | 0 |
| q3 | 15.995 | 16 | 21 | 31.250% | 5 | 0 |
| q4 | 20 | 20 | 16 | 20.000% | 2 | 0 |
| q5 | 8 | 8 | 4 | 50.000% | 2 | 0 |
| q6 | 8 | 8 | 12 | 50.000% | 2 | 0 |
| q7 | 240 | 240 | 139 | 42.083% | 8 | 0 |
| q8 | 4 | 4 | 2 | 50.000% | 2 | 0 |
| q9 | 4 | 4 | 6 | 50.000% | 2 | 0 |
| q10 | 42.66667 | 43 | 48 | 11.628% | 1 | 0 |
| q11 | 32 | 32 | 24 | 25.000% | 4 | 0 |
| q12 | 3.995 | 4 | 13 | 225.000% | 4 | 0 |
| q13 | 26.66667 | 27 | 24 | 11.111% | 1 | 0 |
| q14 | 16 | 16 | 20 | 25.000% | 4 | 0 |
| q15 | 16 | 16 | 27 | 68.750% | 1 | 0 |
| q16 | 100 | 100 | 96 | 4.000% | 4 | 0 |
| q17 | 8 | 8 | 10 | 25.000% | 2 | 0 |
| q18 | 7.9975 | 8 | 5 | 37.500% | 3 | 0 |
| q19 | 10.66667 | 11 | 6 | 45.455% | 1 | 0 |
| q20 | 32 | 32 | 28 | 12.500% | 2 | 0 |
| q21 | 3.99875 | 4 | 12 | 200.000% | 1 | 0 |
| q22 | 128 | 128 | 96 | 25.000% | 10 | 0 |
| q23 | 32 | 32 | 44 | 37.500% | 4 | 0 |
| q24 | 32 | 32 | 34 | 6.250% | 2 | 0 |
| q25 | 14 | 14 | 12 | 14.286% | 1 | 0 |
| q26 | 16 | 16 | 8 | 50.000% | 4 | 0 |
| q27 | 16 | 16 | 8 | 50.000% | 5 | 0 |
| q28 | 26.66667 | 27 | 32 | 18.519% | 1 | 0 |
| q29 | 16 | 16 | 18 | 12.500% | 2 | 0 |
| q30 | 8 | 8 | 4 | 50.000% | 4 | 0 |

## A concise meeting statement

> I tested all 54 questions using a deterministic independent physics solver rather than trusting the marked answers. All answer keys are numerically correct. The largest outstanding issues are answer-order randomization, negative speed distractors, closely spaced choices (including pairs of distractors), and a handful of scenarios where the stated original mass is unclear. I would propose a multi-stage AI evaluation workflow combining independent solving, programmatic choice checks, an adversarial physical-feasibility review, and figure-to-text verification before an instructor signs off.

## Interpretation limits

This is a **pre-exam numerical and textual QA audit**, not experimental validation of distractors. Correctness was checked against the equations represented in the bodies, not against the original bank or the missing images. No claim is made that the distractors' intended cognitive mechanisms were confirmed. The separation heuristics and recommended priorities should be confirmed with the advisor/instructor before revising source assets.
