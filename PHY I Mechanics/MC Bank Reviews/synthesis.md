# Physics I multiple-choice bank synthesis

Torque bank `PHY1-RM-TBORMC-11102026` (30 items) and momentum bank `PHY1-CLM-CE2DMC-11102026` (24 items).

Sources: the qualitative rubric in `quality.md`, and the 11 Nov 2026 computational audit in `physics_bank_quality_report.md`, with item flags from `problem_bank_audit.csv`.

Both banks have correct keys. Neither is exam-ready. All 54 keys match an independent solve, each question has one keyed choice, and in every case that choice is listed first.

## How the two reviews line up

Ratings below are from `quality.md`. The audit agrees that every key is numerically right. It is the source for the slot-1, spacing, and negative-choice counts.

| Dimension | Momentum (24) | Torque (30) |
|---|---|---|
| Mathematical correctness | Pass. Two-axis momentum, then magnitude. | Weak. Keys match F/2; feedback names cos where the stem requires sin. |
| Contextual numbers | Weak. Mostly round speeds written to two decimals. | Fail. Weights and many keys are 4, 8, 16, or 32 N. |
| Problem body | Weak. Two shared closings, plus one bad rounding sentence. | Fail. Same paragraph; pivot, unknown, and positions swap. |
| Variation across the bank | Pass. Shell, rocket, ice, tackle, trains, rafts. Keys 1.28–8066.94 m/s. | Fail. Length 1.0 m, angle 60°, and the rod never change. |
| Same physics | Pass. Leftover piece, combined speed, or other incoming speed. | Pass. Unknown cycles among force, rod weight, and block weight. |
| Distractors | Weak. Shared component mistakes; they collapse when the kick is small. | Pass. One shared list of torque mistakes, as integer newtons. |

Share of items flagged by the computational screen (percent of each bank). Relative gap is abs(choice − key) / abs(key). These percents are screening flags, not a psychometric cutoff.

| Screen | Momentum | Torque |
|---|---:|---:|
| Correct choice listed first | 24/24 (100%) | 30/30 (100%) |
| A negative speed among the choices | 13/24 (54%) | 0/30 |
| A distractor within 1% of the key | 7/24 (29%) | 0/30 |
| A distractor within 5% of the key | 9/24 (38%) | 1/30 (3%) |
| Some pair of choices within 1% of the key | 12/24 (50%) | 0/30 |
| Two wrong answers 1 N apart | — | 7/30 |

## Key issues

Three defects apply to both banks. The keyed choice is the first entry in all 54 YAML answer arrays, so a platform that keeps file order exposes the key. The 30 torque figures were referenced and not inspected. `choice-set-adaptation.md` and the source banks were not in the audit, so each wrong choice’s intended mistake is inferred from the numbers that shipped.

### Torque bank

The angle label and the feedback disagree on every item. The stem says the force is 60° from the vertical, so the component perpendicular to the horizontal rod is F sin 60°. Every feedback line writes F cos 60° = F/2. All 30 keys match that factor of 1/2 after nearest-integer rounding, including mid-rod and left-end pivots. The integers agree with each other. The named function and the stated reference axis do not. The audit’s solver used F cos 60° and therefore confirmed the keys under the feedback’s formula; it did not clear the stem.

The bank does not change the situation. Length stays 1.0 m, the angle stays 60°, and the object stays one rod. Moving the pivot and cycling the unknown among force, rod weight, and block weight is the same solution in a new blank. Many keys are again 4, 8, 16, or 32 N. A few forces appear as 18.67 or 53.33.

### Momentum bank

Sixteen negative choices sit on 13 items that ask for a speed or a velocity magnitude: q1, q5, q6, q7, q9, q11, q13, q14, q18, q20, q22, q23, and q24. q6 contributes two of those choices and q18 contributes three. A negative component can be a real mistake. A negative magnitude cannot.

When the kicked piece is slow next to a large speed, the component-error choices land on top of each other. A distractor is within 1% of the key on q1, q2, q3, q7, q9, q11, and q19, and within 5% on those plus q16 and q17. Twelve items have some pair of choices within 1% of the key. q2 lists 5009.23 and 5009.24 m/s as different distractors. q3’s key, 8066.94 m/s, is 0.27 m/s from 8066.67 m/s.

Several stories do not state the mass the key assumes.

- q7 opens on a 70 kg skater and then a 60 kg skater after a 10 kg bag is thrown. 
- q10’s 180 kg bumper car becomes 110 kg after a 70 kg passenger jumps.
- q8, q9, q11, and q12 leave the same point softer for a submarine, spaceship, hovercraft, and sled. The keys hold if the first mass is the combined system.  
[c](In all of the above situations, the first object is the combined weight of the system. This just requires re-wording)
- q19 treats two train cars on merging rails as an isolated two-dimensional collision. The rails can supply a sideways impulse. [c](Change into a new context)
- q6’s alpha particle leaves near 5004 m/s, about 0.52 eV for a 4 u particle. [c](need to suggest new numbers)

## Minor issues

These are real edits, and they sit behind the key issues. Torque distractors already trace to recognizable mistakes. Momentum variation and the underlying principle already hold.

| Issue | Bank | Where it shows up |
|---|---|---|
| Two wrong answers 1 N apart | Torque | q10, q13, q15, q19, q21, q25, q28. None of these pairs includes the key. |
| Nearest distractor 4% from the key | Torque | q16 only (96 N beside 100 N). Every other torque key is at least 6% from its nearest distractor. |
| Clean textbook magnitudes | Torque | 4, 8, 16, 32 N dominate. A handful of forces are already uneven (18.67, 53.33). |
| Round speeds written to two decimals | Momentum | Values such as 300, 5000.00, and 8.00. A few components are uneven (1.73, 84.75, 3.40) and fit the objects. |
| Two closing templates | Momentum | q1–q12 share one ending and q13–q24 share another. q1 says “two decimal places after zero.” |
| Pairs within 0.05 m/s | Momentum | q2, q7, q8, q11, q15, q16, q19. q8 and q15 are tight pairs that are not within 1% of the key. |

Torque distractors can stay. Six parallel integer-newton choices come from one list: drop the 60° factor, swap sine and cosine, reverse one torque, omit one weight, put the rod’s weight at full length, or add the two weights. On q1 those are 22, 25, 41, 1, 87, and 36 N beside the key 44 N. No torque item offers a negative weight. Widening a 1 N distractor pair is worth doing only when that pair is still tied to one of these mistakes.

Momentum distractors have a sound origin. Wrong choices are component mistakes. On q1, 286.67 m/s is the x component alone, 284.08 m/s treats the fragment velocity as a scalar, and 53.85 m/s is the known fragment’s kick. That menu is worth keeping. It stops separating the choices on the large-speed items listed under key issues. Settings and the conservation principle already vary enough to pass.

## Improvement strategy

Fix delivery and the stories that can mark a correct student wrong, then retune numbers so the existing mistake-based choices spread out. Re-solve the whole bank after each physics edit.

1. **Confirm how choices are shown.** Run a student preview and check randomization on each delivered question. If the platform keeps YAML order, shuffle inside the files so slot 1 is not the key on all 54 items. [c](ignore this one, I already know)
2. **Align the torque stem, figure, and feedback.** Decide the angle’s reference axis and make the stem, the diagram, and the feedback name the same component. For 60° from the vertical on a horizontal rod, the perpendicular factor is sin 60°, which is not 1/2. If the figure measures 60° from the horizontal, the stem should say so and cos 60° = 1/2 is the right factor. Then re-solve all 30 items and open every image for pivot, block, force position, upward direction, and the angle. [c](The answer is correct, and the figures are correct. Vertical component according to the figure should be cos 60 degree, not sin. One AI evaluator made a mistake)
3. **Repair momentum stories and illegal choices.** Replace all 16 negative magnitudes with positive values that each come from one traceable mistake, and check the replacement is not already on the list. State the opening mass as the combined system on q7 and q10, and do the same for q8, q9, q11, and q12. Replace q19 with freely moving objects on a surface that can be treated as isolated, or state the rail idealization in the stem. Revise q6’s speeds or drop the alpha-decay framing. Change q1 to “round to two decimal places.” [c](We need to divise a plan to replace illeagal distractors)
4. **Separate every pair by changing the givens.** Adopt a pilot rule worth instructor sign-off: every pair of choices, including two wrong answers, at least 5% of the correct magnitude and at least a few steps of the reported precision. Keep the mistake each distractor encodes. Change masses, speeds, lengths, and angles so those mistakes land far enough apart. First momentum retunes: q2, q3, q7, q9, q11, and q19. On torque, separate the 1 N distractor pairs on q10, q13, q15, q19, q21, q25, and q28 the same way. [c](divise a plan for momentum bank, ignor the torque bank because 1N apart should be ok)
5. **Break the torque clone and the momentum closings.** Vary rod length, angle, and object, and leave the 4 / 8 / 16 / 32 N family. The misconception menu can stay; it is the part of this bank that already works. Give the momentum items more than two shared endings so q1–q12 and q13–q24 are not recognizable as two templates. [c](Yes, suggest new numbers)
6. **Re-run one checklist, then sign off.** After edits: unique IDs and exactly one correct flag; a solve from the stem alone, with no choices in view; a scripted check of two-axis momentum and signed torque balance at the requested precision; a feasibility mark of pass, needs clarification, or infeasible; distractor distances scored before anyone reads the intended-error labels; figure-to-text comparison and an LMS preview. Block release for a bad key, two numerically valid choices, infeasible physics, a figure that contradicts the text, or an unshuffled key. Treat close options and ambiguous wording as required revisions. A later student pilot can show which distractors are actually chosen; spacing alone does not establish that. [c](Ignore this for now)

## Still missing from both reviews

`choice-set-adaptation.md`, the source numerical banks, and the 30 torque images. The choices can be judged as they stand. Whether each wrong answer survived conversion as the intended mistake, and whether each diagram matches its filename’s location triplet, still needs those files. 
