# Update plan — PHY1-RM-TBORMC-11102026

Bank file: `PHY1-RM-TBORMC-11102026-draft.yaml`  
Choice roles: `choice-set-adaptation.md`  
Figures stay in `../PHY1-RM-TBOR-11112025/Figures/`  
Follows the comments saved in `../../MC Bank Reviews/synthesis.md`.

## Leave as it is

- The keys and the figures are already right. The force is \(60^\circ\) from the vertical, so the component perpendicular to the rod is the vertical component, \(F\cos 60^\circ = F/2\). The feedback that says so is the correct identity. The sine reading came from one evaluator. Do not edit stems, feedback, or figures for the angle.
- Pairs of wrong answers that sit 1 N apart can stay. That includes q10, q13, q15, q19, q21, q25, and q28, and the 96 N choice beside the 100 N key on q16.
- Positions, \(L = 1.0\,\mathrm{m}\), the \(60^\circ\) angle, and the six distractor roles stay. Number changes do not need new figures.
- Choice order in the YAML is already known and is not part of this update.

## Change the newton values

Weights and many keys are 4, 8, 16, or 32 N. Replace the givens below, re-solve the unknown from

\[
(x_F - x_p)\frac{F}{2} = (0.5 - x_p)W_r + (x_b - x_p)W_b,
\]


and round that unknown to the nearest integer. Then rebuild the six distractors from the roles in `choice-set-adaptation.md` with these givens. Positions in the table are the ones already in the bank, measured from the right end in units of \(L\).

Author input: First, check if the above equation always gives the correct answer in each problem using existing numbers. It might be that you will need different equation for different situation since the location of the pivot, force and hanging object changes. If the check passes, then update all the numbers.

| Item | Unknown | New givens | Exact unknown | Nearest integer |
|---|---|---|---:|---:|
| q1 | \(F\) | rod 42 N, block 5 N | 57.67 N | 58 N |
| q2 | rod | block 14 N, \(F = 31\) N | 27.50 N | 28 N |
| q3 | block | rod 70 N, \(F = 117\) N | 35.50 N | 36 N |
| q4 | \(F\) | rod 6 N, block 48 N | 30.00 N | 30 N |
| q5 | rod | block 10 N, \(F = 146\) N | 21.50 N | 22 N |
| q6 | block | rod 18 N, \(F = 35\) N | 11.33 N | 11 N |
| q7 | \(F\) | rod 42 N, block 21 N | 315.00 N | 315 N |
| q8 | rod | block 54 N, \(F = 120\) N | 25.50 N | 26 N |
| q9 | block | rod 18 N, \(F = 141\) N | 8.62 N | 9 N |
| q10 | \(F\) | rod 24 N, block 12 N | 64.00 N | 64 N |
| q11 | rod | block 42 N, \(F = 42\) N | 84.00 N | 84 N |
| q12 | block | rod 37 N, \(F = 21\) N | 5.50 N | 6 N |
| q13 | \(F\) | rod 10 N, block 21 N | 34.67 N | 35 N |
| q14 | rod | block 14 N, \(F = 41\) N | 26.50 N | 26 N |
| q15 | block | rod 70 N, \(F = 176\) N | 35.33 N | 35 N |
| q16 | \(F\) | rod 6 N, block 48 N | 150.00 N | 150 N |
| q17 | rod | block 10 N, \(F = 31\) N | 21.50 N | 22 N |
| q18 | block | rod 18 N, \(F = 25\) N | 9.75 N | 10 N |
| q19 | \(F\) | rod 42 N, block 21 N | 14.00 N | 14 N |
| q20 | rod | block 7 N, \(F = 48\) N | 55.00 N | 55 N |
| q21 | block | rod 70 N, \(F = 117\) N | 8.88 N | 9 N |
| q22 | \(F\) | rod 24 N, block 12 N | 192.00 N | 192 N |
| q23 | rod | block 42 N, \(F = 156\) N | 82.50 N | 82 N |
| q24 | block | rod 5 N, \(F = 276\) N | 36.57 N | 37 N |
| q25 | \(F\) | rod 10 N, block 5 N | 17.50 N | 18 N |
| q26 | rod | block 14 N, \(F = 190\) N | 26.50 N | 26 N |
| q27 | block | rod 70 N, \(F = 88\) N | 36.00 N | 36 N |
| q28 | \(F\) | rod 6 N, block 48 N | 40.00 N | 40 N |
| q29 | rod | block 21 N, \(F = 47\) N | 41.75 N | 42 N |
| q30 | block | rod 18 N, \(F = 28\) N | 12.00 N | 12 N |

q8 is the one place a uniform scale landed back on 8 N. The row above uses \(F = 120\,\mathrm{N}\) instead, which gives 25.50 N and a key of 26 N.

Each new weight is outside \(\{4, 8, 16, 32\}\). The solved key is outside that set as well. Lever arms are unchanged, and every solved unknown is positive, so the upward-force direction in the existing figures still holds.


