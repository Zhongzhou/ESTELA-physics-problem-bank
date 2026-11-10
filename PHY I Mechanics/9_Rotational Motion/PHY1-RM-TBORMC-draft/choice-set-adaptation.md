# Adapting the q1 choice set

Source bank: `PHY1-RM-TBOR-11112025`
Choice set: `q1-mc-draft.md`

All thirty problems are the same horizontal rod. The length is $L = 1.0\text{ m}$, the rod is uniform, and it is in static equilibrium. An external force points upward at $60^\circ$ from the vertical. Distances in the problem text are measured from the right end. The answer is rounded to the nearest integer.

Only the vertical component produces a torque about the pivot. That component is $F\cos 60^\circ = F/2$. The rod’s weight acts at its center, $L/2$. With positions measured from the right end, the signed lever arms are

$a_b = x_b - x_p,\quad a_r = \tfrac{1}{2}L - x_p,\quad a_f = x_f - x_p.$

Equilibrium is $W_b a_b + W_r a_r - (F/2)\, a_f = 0$.

The q1 choice set has six distractors:

| Role | Mistake |
| --- | --- |
| No angle | The $60^\circ$ angle is ignored, so the whole force is treated as perpendicular to the rod. |
| Sine and cosine swapped | $F\sin 60^\circ$ is used as the perpendicular component. |
| Opposite directions | The block and the rod are given opposite torque directions. On q1 they are on the same side of the pivot, so the torques should add. |
| Rod ignored | The rod’s weight is left out. Only the block is balanced against the force. |
| Full length | The rod’s lever arm is $L$, not the distance from the pivot to the center. |
| Weights added | The two weights are added and that sum is reported as the force. Lever arms and the angle never enter. |

Two of those roles name the unknown. “Rod ignored” cannot be used when the question asks for the rod weight. “Weights added” cannot be used when the question asks for a weight, because one of the weights is the unknown. The sections below keep the same six roles and rewrite those two for the other unknowns. A further substitute is used only where the rewritten role rounds to the same integer as another choice, or rounds to 0 N.

Where a signed mistake comes out negative, the choice is the absolute value, as in the q1 opposite-direction choice $\lvert 16 - 0.5\rvert$.

## Where the pivot, the block, and the force are

The rod’s center is always at $L/2$.

- Pivot at either end (`q1`–`q10`, `q21`–`q30`): the center and the block are on the same side of the pivot.
- Pivot at $L/4$ (`q11`–`q15`): the center is to the left of the pivot. The block is on the opposite side only in `q11` and `q12`, where the block is at the right end.
- Pivot at $3L/4$ (`q16`–`q20`): the center is to the right of the pivot. The block is on the opposite side only in `q19` and `q20`, where the block is at the left end.

| q | Pivot | Block | Force | Asked | Block and center |
| --- | --- | --- | --- | --- | --- |
| 1 | right end | $L/8$ | $3L/4$ | $F$ | same side |
| 2 | right end | $L/8$ | left end | $W_r$ | same side |
| 3 | right end | $L/4$ | $3L/4$ | $W_b$ | same side |
| 4 | right end | $L/4$ | left end | $F$ | same side |
| 5 | right end | $3L/4$ | $L/4$ | $W_r$ | same side |
| 6 | right end | $3L/4$ | left end | $W_b$ | same side |
| 7 | right end | $7L/8$ | $L/4$ | $F$ | same side |
| 8 | right end | $7L/8$ | left end | $W_r$ | same side |
| 9 | right end | left end | $L/4$ | $W_b$ | same side |
| 10 | right end | left end | $3L/4$ | $F$ | same side |
| 11 | $L/4$ | right end | $3L/4$ | $W_r$ | opposite sides |
| 12 | $L/4$ | right end | left end | $W_b$ | opposite sides |
| 13 | $L/4$ | $3L/4$ | left end | $F$ | same side |
| 14 | $L/4$ | $7L/8$ | left end | $W_r$ | same side |
| 15 | $L/4$ | left end | $3L/4$ | $W_b$ | same side |
| 16 | $3L/4$ | right end | $L/4$ | $F$ | same side |
| 17 | $3L/4$ | $L/8$ | right end | $W_r$ | same side |
| 18 | $3L/4$ | $L/4$ | right end | $W_b$ | same side |
| 19 | $3L/4$ | left end | right end | $F$ | opposite sides |
| 20 | $3L/4$ | left end | $L/4$ | $W_r$ | opposite sides |
| 21 | left end | right end | $L/4$ | $W_b$ | same side |
| 22 | left end | right end | $3L/4$ | $F$ | same side |
| 23 | left end | $L/8$ | right end | $W_r$ | same side |
| 24 | left end | $L/8$ | $3L/4$ | $W_b$ | same side |
| 25 | left end | $L/4$ | right end | $F$ | same side |
| 26 | left end | $L/4$ | $3L/4$ | $W_r$ | same side |
| 27 | left end | $3L/4$ | right end | $W_b$ | same side |
| 28 | left end | $3L/4$ | $L/4$ | $F$ | same side |
| 29 | left end | $7L/8$ | right end | $W_r$ | same side |
| 30 | left end | $7L/8$ | $L/4$ | $W_b$ | same side |

On an interior pivot the rote lever arm $L$ reaches past the end of the rod. The largest real distance from a pivot at $L/4$ or $3L/4$ to either end is $3L/4$, and the center is only $L/4$ from that pivot. The full-length choice is still the q1 mistake $\tau_r = W_r L$. It is kept wherever that integer is distinct. Where it is not, the substitute is the on-rod mistake $\lvert a_r\rvert = L/2$.

## Updates that are not the q1 wording

- **`q1` (bank values):** The bank has a rod of 8 N and a block of 4 N, so the correct force is 12 N. The weights-added choice is $4 + 8 = 12\text{ N}$, the same integer. The draft already separates them by raising the rod weight to 32 N and leaving the block at 4 N. The correct force becomes 44 N, and the six q1 distractors are 22 N, 25 N, 41 N, 1 N, 87 N, and 36 N. No distractor is replaced.
- **`q13`:** The bank’s block of 4 N makes the correct force 11 N and the weights-added choice 12 N. The block is raised to 16 N. The correct force is 27 N, and the weights-added choice is 24 N. The weight torques are no longer equal, so the same-side force table applies and the two q13 substitutes are dropped.
- **`q21`:** With a rod of 8 N and a force of 21.33 N, $W_b = F/2 - W_r$ rounds to 3 N, one newton from the correct 4 N. The rod is raised to 32 N and the force to 53.33 N. The correct block weight stays 4 N. The weight torques are no longer equal, so the standard block-weight table applies.
- **`q29`:** With a block of 4 N, ignoring the block returns the force, 9 N, which is one newton from the correct rod weight, 8 N. The block is raised to 8 N and the force to 18 N. The correct rod weight is 16 N, and ignoring the block gives 18 N.
- **Every rod-weight item:** “Ignore the rod” is replaced by “ignore the block,” $W_r = (F/2)\, a_f / a_r$. “Add the weights” is replaced by the force balance $W_r = \lvert F - W_b\rvert$.
- **Every block-weight item:** “Add the weights” is replaced by $W_b = \lvert F - W_r\rvert$. “Ignore the rod” stays.
- **Opposite sides:** The correct weight torques already have opposite signs. The q1 “opposite directions” mistake would repeat the correct solution. The error that belongs in that slot is the reverse: the two weights are given the same direction.
- **Equal weight torques** (`q9`, `q10`, `q18`, `q22`): $\lvert\tau_b\rvert = \lvert\tau_r\rvert$. The difference used by the direction mistake is 0 N. Forgetting the angle then gives the same integer as dropping one of the two equal torques. Those two slots need substitutes. `q13` and `q21` were in this group until their weights were changed.
- **Negative signed results,** kept as magnitudes: the full-length block weight on `q3` (48 N), `q6` (3 N), `q27` (48 N), and `q30` (56 N); and the no-angle, sine/cosine, rod-ignored, and force-balance choices on `q12`.

## Items that need a new distractor

| q | Slot that fails | Why | Substitute | Rounds to |
| --- | --- | --- | --- | --- |
| 4 | Opposite directions | Rounds to 12 N, the same as sine/cosine swapped | Ignore the block | 4 N |
| 9 | Opposite directions | Rounds to 12 N, the same as no angle | $W_b = F/2 - W_r$ | 24 N |
| 9 | Full length | Rod torque at lever arm $L$ equals the force torque, so the block weight is 0 N | Rod lever arm set to the force’s lever arm, $L/4$ | 6 N |
| 10 | Opposite directions | The two weight torques are equal, so the difference is 0 N | $F\cos 60^\circ = W_b + W_r$ | 48 N |
| 10 | Rod ignored | Matches the no-angle choice, 21 N | Block placed at the center; both weights use $L/2$ | 32 N |
| 11 | Same direction | Block torque equals the force torque, so the rod weight is 0 N | Lever arms read as the distances from the right end | 12 N |
| 11 | $W_r = \lvert F - W_b\rvert$ | $F = W_b$, so the difference is 0 N | $W_r = F/2 + W_b$ | 24 N |
| 12 | Same direction | Magnitude equals the correct block weight, 4 N | Rod lever arm taken as $L/2$ instead of $L/4$ | 36 N |
| 14 | $W_r = \lvert F - W_b\rvert$ | Equals the correct rod weight, 16 N. The version with the angle, $\lvert F/2 - W_b\rvert$, equals the full-length choice, 4 N | $W_r = F/2 + W_b$ | 20 N |
| 15 | Full length | Magnitude equals the correct block weight, 16 N | Rod lever arm taken as $L/2$ instead of $L/4$ | 5 N |
| 17 | $W_r = \lvert F - W_b\rvert$ | Equals the correct rod weight, 8 N. The version with the angle equals the full-length choice, 2 N | $W_r = F/2 + W_b$ | 10 N |
| 18 | Opposite directions | Rounds to 24 N, the same as no angle | Lever arms read from the right end. The force is at the right end, so it contributes no torque | 32 N |
| 18 | Full length | Magnitude equals “rod ignored,” 16 N | $W_b = F/2 + W_r$ | 27 N |
| 19 | Rod ignored | Magnitude equals the correct force, 11 N, because the block torque equals the net weight torque | Ignore the block instead | 21 N |
| 20 | $W_r = \lvert F - W_b\rvert$ | Equals the same-direction choice, 24 N | $W_r = \lvert F/2 - W_b\rvert$ | 10 N |
| 22 | Opposite directions | Equal weight torques, so the difference is 0 N | $F\cos 60^\circ = W_b + W_r$ | 48 N |
| 22 | Rod ignored | Matches the no-angle choice, 64 N | Block placed at the center; both weights use $L/2$ | 96 N |
| 30 | $W_b = \lvert F - W_r\rvert$ | Equals the correct block weight, 8 N | $W_b = \lvert F/2 - W_r\rvert$ | 4 N |

`q7`, `q13`, `q16`, `q25`, and `q28` take the q1 force set with no substitute. `q2`, `q5`, `q8`, `q23`, `q26`, and `q29` take the rod-weight set with no substitute. `q3`, `q6`, `q21`, `q24`, and `q27` take the block-weight set with no substitute. `q1` does too, after the rod weight is changed to 32 N.

## Force unknown, same side of an end pivot

Problems that use this table unchanged: `q1` (draft weights), `q7`, `q13`, `q25`, `q28`. `q13` has an interior pivot, and both weights are still on the same side of it.

$F_\perp$ stands for the perpendicular component used in that row.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $F = (W_b a_b + W_r a_r) / (\tfrac{1}{2} a_f)$ | Both weights produce torque in the same direction. The rod’s weight acts at $L/2$. The upward force contributes $F\cos 60^\circ$. |
| Distractor | $F = (W_b a_b + W_r a_r) / a_f$ | The $60^\circ$ angle is ignored and the full force is treated as perpendicular to the rod. |
| Distractor | $F = (W_b a_b + W_r a_r) / (\tfrac{\sqrt{3}}{2} a_f)$ | Sine and cosine are swapped. |
| Distractor | $F = \lvert \lvert W_b a_b\rvert - \lvert W_r a_r\rvert \rvert / (\tfrac{1}{2}\lvert a_f\rvert)$ | The block and the rod are given opposite torque directions. |
| Distractor | $F = W_b a_b / (\tfrac{1}{2} a_f)$ | The rod’s weight is ignored. |
| Distractor | $a_r$ is replaced by $\pm L$, with the sign of the true arm | The rod’s torque is calculated with the full length $L$, not the center. |
| Distractor | $F = W_b + W_r$ | The two weights are added and reported as the force. |

### q1 — Right-end pivot, block at $L/8$, force at $3L/4$

The draft uses a rod weight of 32 N and a block weight of 4 N. The bank’s pair, 8 N and 4 N, makes the weights-added choice equal the correct force.

Uses the table above. Rounded choices: 44 N, 22 N, 25 N, 41 N, 1 N, 87 N, 36 N.

### q7 — Right-end pivot, block at $7L/8$, force at $L/4$

The rod weighs 32 N and the block weighs 16 N. The force is the unknown.

Uses the table above.

### q25 — Left-end pivot, block at $L/4$, force at the right end

The rod weighs 8 N and the block weighs 4 N. The force is the unknown. Both weights are on the same side of the left-end pivot, so the q1 direction mistake still applies.

Uses the table above.

### q28 — Left-end pivot, block at $3L/4$, force at $L/4$

The rod weighs 4 N and the block weighs 32 N. The force is the unknown.

Uses the table above.

### q4 — Right-end pivot, block at $L/4$, force at the left end

The rod weighs 4 N and the block weighs 32 N. Sine/cosine swapped and the opposite-direction mistake both round to 12 N. The opposite-direction slot is replaced by ignoring the block. The rod is the lighter object, so dropping the block is a different mistake from dropping the rod.

| Role | Value | Formula | Misconception |
| --- | --- | --- | --- |
| Correct | 20 N | $F = (W_b a_b + W_r a_r) / (\tfrac{1}{2} a_f)$ | Same-side torques, rod at $L/2$, perpendicular component $F\cos 60^\circ$. |
| Distractor | 10 N | denominator uses $1$ instead of $\tfrac{1}{2}$ | The angle is ignored. |
| Distractor | 12 N | denominator uses $\tfrac{\sqrt{3}}{2}$ | Sine and cosine are swapped. |
| Distractor | 4 N | $F = W_r a_r / (\tfrac{1}{2} a_f)$ | The block is ignored. Only the rod is balanced against the force. |
| Distractor | 16 N | $F = W_b a_b / (\tfrac{1}{2} a_f)$ | The rod is ignored. |
| Distractor | 24 N | $a_r \to L$ | The rod’s lever arm is the full length. |
| Distractor | 36 N | $F = W_b + W_r$ | The weights are added. |

### q10 and q22 — Equal weight torques, end pivot

On both items $\lvert\tau_b\rvert = \lvert\tau_r\rvert = 8\text{ N}\cdot\text{m}$. The opposite-direction force is 0 N. Dropping either weight then matches the no-angle choice, because doubling the force (forgetting $\cos 60^\circ$) has the same effect as deleting one of two equal torques.

The zero slot becomes a force balance that keeps the angle and drops the lever arms, $F\cos 60^\circ = W_b + W_r$. The duplicate “rod ignored” slot becomes “the block is placed at the center.”

`q10`: pivot at the right end, block of 8 N at the left end, rod of 16 N, force at $3L/4$. The block’s true lever arm is $L$. Placing it at the center gives both weights the lever arm $L/2$.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 43 N | Same-side torques, rod at $L/2$, component $F\cos 60^\circ$. |
| Distractor | 21 N | The angle is ignored. |
| Distractor | 25 N | Sine and cosine are swapped. |
| Distractor | 48 N | Lever arms are ignored and the angle is kept: $F = 2(W_b + W_r)$. |
| Distractor | 32 N | The block is placed at the center. Both weights use lever arm $L/2$. |
| Distractor | 64 N | The rod’s lever arm is $L$. |
| Distractor | 24 N | The weights are added and reported as the force. |

`q22`: pivot at the left end, block of 8 N at the right end, rod of 16 N, force at $3L/4$. Same two substitutes. The center is $L/2$ from the left-end pivot, and the block’s true lever arm is $L$.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 128 N | Same-side torques, rod at $L/2$, component $F\cos 60^\circ$. |
| Distractor | 64 N | The angle is ignored. |
| Distractor | 74 N | Sine and cosine are swapped. |
| Distractor | 48 N | $F\cos 60^\circ = W_b + W_r$. |
| Distractor | 96 N | The block is placed at the center. Both weights use lever arm $L/2$. |
| Distractor | 192 N | The rod’s lever arm is $L$. |
| Distractor | 24 N | The weights are added and reported as the force. |

## Force unknown, interior pivot

### q16 — Pivot at $3L/4$, block at the right end, force at $L/4$

The rod weighs 4 N and the block weighs 32 N. The block and the center are both to the right of the pivot, so the q1 direction mistake applies. The full-length choice uses lever arm $L$ even though the rod extends only $3L/4$ from this pivot. That integer, 112 N, is still distinct from the correct 100 N.

Uses the end-pivot force table above.

### q13 — Pivot at $L/4$, block at $3L/4$, force at the left end

The rod weighs 8 N and the block weighs 16 N. The bank’s block was 4 N, which put the weights-added choice one newton from the correct force. Both weights are on the left of the pivot, so the same-side force table applies.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 27 N | Same-side torques. The center is $L/4$ from this pivot. The component is $F\cos 60^\circ$. |
| Distractor | 13 N | The angle is ignored. |
| Distractor | 15 N | Sine and cosine are swapped. |
| Distractor | 16 N | The block and the rod are given opposite torque directions. |
| Distractor | 21 N | The rod’s weight is ignored. |
| Distractor | 43 N | The rod’s lever arm is the full length $L$. |
| Distractor | 24 N | The weights are added and reported as the force. |

### q19 — Pivot at $3L/4$, block at the left end, force at the right end

The rod weighs 32 N and the block weighs 16 N. The center is to the right of the pivot and the block is to the left, so the correct weight torques have opposite signs. The direction mistake adds them.

Dropping the rod reproduces the correct force. The block torque and the net weight torque are both $4\text{ N}\cdot\text{m}$, so deleting the rod and taking the magnitude leaves the same force. That slot drops the block instead.

| Role | Value | Formula | Misconception |
| --- | --- | --- | --- |
| Correct | 11 N | $F = (W_b a_b + W_r a_r) / (\tfrac{1}{2} a_f)$ | The block and the center are on opposite sides, so the weight torques subtract. |
| Distractor | 5 N | perpendicular factor $1$ | The angle is ignored. |
| Distractor | 6 N | perpendicular factor $\tfrac{\sqrt{3}}{2}$ | Sine and cosine are swapped. |
| Distractor | 32 N | $F = (\lvert W_b a_b\rvert + \lvert W_r a_r\rvert) / (\tfrac{1}{2}\lvert a_f\rvert)$ | The two weights are given the same direction. |
| Distractor | 21 N | $F = W_r a_r / (\tfrac{1}{2} a_f)$ | The block is ignored. Dropping the rod repeats the correct magnitude. |
| Distractor | 75 N | $a_r \to -L$ | The rod’s lever arm is the full length $L$. |
| Distractor | 48 N | $F = W_b + W_r$ | The weights are added and reported as the force. |

## Rod weight unknown

The block and the force are given. The rod weight is

$W_r = \big((F/2)\, a_f - W_b a_b\big) / a_r.$

On the same side of the pivot, the direction mistake puts the block on the force’s side of the equation:

$W_r = \big(\lvert (F/2)\, a_f\rvert + \lvert W_b a_b\rvert\big) / \lvert a_r\rvert.$

The rod is the unknown, so the dropped-weight role drops the block. The no-lever-arm role is $W_r = \lvert F - W_b\rvert$.

Problems that use this table unchanged: `q2`, `q5`, `q8`, `q23`, `q26`, `q29`. All six have the block and the center on the same side. `q23`, `q26`, and `q29` have the pivot at the left end; the signed arms take care of that.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $W_r = \big((F/2)\, a_f - W_b a_b\big) / a_r$ | Same-side torques, rod at its center, component $F\cos 60^\circ$. |
| Distractor | $(F/2)$ replaced by $F$ | The angle is ignored. |
| Distractor | $(F/2)$ replaced by $F\sin 60^\circ$ | Sine and cosine are swapped. |
| Distractor | $W_r = \big(\lvert (F/2)\, a_f\rvert + \lvert W_b a_b\rvert\big) / \lvert a_r\rvert$ | The weights are given opposite directions, so the rod has to balance the force and the block together. |
| Distractor | $W_r = (F/2)\, a_f / a_r$ | The block is ignored. |
| Distractor | $a_r \to \pm L$ | The rod’s lever arm is the full length $L$. |
| Distractor | $W_r = \lvert F - W_b\rvert$ | Lever arms and the angle never enter. The rod weight is the force minus the block weight. |

### q2 — Right-end pivot, block at $L/8$, force at the left end

Block 8 N, force 18 N. Uses the table above.

### q5 — Right-end pivot, block at $3L/4$, force at $L/4$

Block 4 N, force 56 N. Uses the table above.

### q8 — Right-end pivot, block at $7L/8$, force at the left end

Block 32 N, force 60 N. Uses the table above.

### q23 — Left-end pivot, block at $L/8$, force at the right end

Block 16 N, force 60 N. Uses the table above.

### q26 — Left-end pivot, block at $L/4$, force at $3L/4$

Block 8 N, force 112 N. Uses the table above.

### q29 — Left-end pivot, block at $7L/8$, force at the right end

Block 8 N, force 18 N. The correct rod weight is 16 N. The bank’s block was 4 N and its force was 9 N, so ignoring the block gave 9 N, one newton from the correct 8 N. Ignoring the block now gives the force, 18 N. Uses the table above.

### q14 — Pivot at $L/4$, block at $7L/8$, force at the left end

Block 8 N, force 24 N. The center is $L/4$ to the left of the pivot, on the same side as the block. The first six rows of the rod-weight table apply, and the full-length choice is 4 N.

$W_r = \lvert F - W_b\rvert$ equals the correct answer, 16 N. Keeping the angle, $\lvert F/2 - W_b\rvert$, equals the full-length choice, 4 N. The slot that remains is to add the vertical component to the block:

$W_r = F/2 + W_b = 20\text{ N}.$

The student adds the block weight to $F\cos 60^\circ$ and never uses a lever arm.

### q17 — Pivot at $3L/4$, block at $L/8$, force at the right end

Block 4 N, force 12 N. Same side of the pivot. The first six rows apply, and the full-length choice is 2 N.

$W_r = \lvert F - W_b\rvert$ equals the correct answer, 8 N, and $\lvert F/2 - W_b\rvert$ equals the full-length choice. The substitute is

$W_r = F/2 + W_b = 10\text{ N}.$

### q11 — Pivot at $L/4$, block at the right end, force at $3L/4$

Block 16 N, force 16 N. The center is to the left of the pivot and the block is to the right.

The same-direction mistake asks the block torque and the rod torque to add up to the force torque. Those first two are already equal, both $4\text{ N}\cdot\text{m}$, so the rod weight comes out 0 N. $F - W_b$ is also 0 N.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 32 N | Opposite sides of the pivot. The center is $L/4$ to the left. The component is $F\cos 60^\circ$. |
| Distractor | 48 N | The angle is ignored. |
| Distractor | 44 N | Sine and cosine are swapped. |
| Distractor | 12 N | Every lever arm is the distance from the right end. The block is at the right end, so its arm is taken to be zero, and the rod is given arm $L/2$. |
| Distractor | 16 N | The block is ignored. |
| Distractor | 8 N | The rod’s lever arm is $L$. |
| Distractor | 24 N | The rod weight is $F\cos 60^\circ$ plus the block weight. Lever arms never enter. |

### q20 — Pivot at $3L/4$, block at the left end, force at $L/4$

Block 4 N, force 28 N. The center is to the right of the pivot and the block is to the left. Giving the weights the same direction produces a distinct rod weight, 24 N. The no-angle force balance $F - W_b$ lands on that same 24 N, so the force-balance slot keeps the angle:

$W_r = \lvert F/2 - W_b\rvert = 10\text{ N}.$

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 32 N | Opposite sides. The center is $L/4$ to the right of the pivot. |
| Distractor | 60 N | The angle is ignored. |
| Distractor | 52 N | Sine and cosine are swapped. |
| Distractor | 24 N | The weights are given the same direction, so $W_r = (\lvert\tau_F\rvert - \lvert\tau_b\rvert) / \lvert a_r\rvert$. |
| Distractor | 28 N | The block is ignored. |
| Distractor | 8 N | The rod’s lever arm is $L$. |
| Distractor | 10 N | Lever arms are ignored and the angle is kept: the rod weight is $F\cos 60^\circ$ minus the block weight. |

## Block weight unknown

The rod and the force are given. The block weight is

$W_b = \big((F/2)\, a_f - W_r a_r\big) / a_b.$

On the same side of the pivot, the direction mistake gives the unknown block the force torque plus the rod torque:

$W_b = \big(\lvert (F/2)\, a_f\rvert + \lvert W_r a_r\rvert\big) / \lvert a_b\rvert.$

“Ignore the rod” stays. The no-lever-arm role is $W_b = \lvert F - W_r\rvert$.

Problems that use this table unchanged: `q3`, `q6`, `q21`, `q24`, `q27`. The full-length result is negative on `q3`, `q6`, and `q27`, because a lever arm of $L$ makes the rod torque larger than the force torque. The choice is the magnitude: 48 N, 3 N, and 48 N. On `q21` the full-length magnitude is 12 N.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $W_b = \big((F/2)\, a_f - W_r a_r\big) / a_b$ | Same-side torques, rod at its center, component $F\cos 60^\circ$. |
| Distractor | $(F/2)$ replaced by $F$ | The angle is ignored. |
| Distractor | $(F/2)$ replaced by $F\sin 60^\circ$ | Sine and cosine are swapped. |
| Distractor | $W_b = \big(\lvert (F/2)\, a_f\rvert + \lvert W_r a_r\rvert\big) / \lvert a_b\rvert$ | The weights are given opposite directions, so the block balances the force and the rod together. |
| Distractor | $W_b = (F/2)\, a_f / a_b$ | The rod is ignored. |
| Distractor | $a_r \to \pm L$, then the absolute value | The rod’s lever arm is the full length $L$. |
| Distractor | $W_b = \lvert F - W_r\rvert$ | Lever arms and the angle never enter. The block weight is the force minus the rod weight. |

### q3 — Right-end pivot, block at $L/4$, force at $3L/4$

Rod 32 N, force 53.33 N. Uses the table above. The full-length choice is 48 N.

### q6 — Right-end pivot, block at $3L/4$, force at the left end

Rod 16 N, force 28 N. Uses the table above. The full-length choice is 3 N.

### q24 — Left-end pivot, block at $L/8$, force at $3L/4$

Rod 4 N, force 240 N. Uses the table above.

### q27 — Left-end pivot, block at $3L/4$, force at the right end

Rod 32 N, force 40 N. Uses the table above. The full-length choice is 48 N.

### q30 — Left-end pivot, block at $7L/8$, force at $L/4$

Rod 16 N, force 24 N. The first six rows apply. The full-length magnitude is 56 N.

$W_b = \lvert F - W_r\rvert$ equals the correct answer, 8 N. Keeping the angle separates it:

$W_b = \lvert F/2 - W_r\rvert = 4\text{ N}.$

The signed result of that force balance is $-4\text{ N}$. The choice is the magnitude.

### q21 — Left-end pivot, block at the right end, force at $L/4$

Rod 32 N, force 53.33 N. The bank’s rod was 8 N and its force was 21.33 N. That pair made $W_b = F/2 - W_r$ round to 3 N, one newton from the correct block weight, 4 N. The correct block weight is still 4 N. The center and the block are on the same side of the left-end pivot, so the block-weight table applies.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 4 N | Same-side torques about the left end, rod at $L/2$ from that end. |
| Distractor | 24 N | The angle is ignored. |
| Distractor | 19 N | Sine and cosine are swapped. |
| Distractor | 36 N | The block and the rod are given opposite torque directions. |
| Distractor | 20 N | The rod is ignored. |
| Distractor | 12 N | The rod’s lever arm is the full length $L$. |
| Distractor | 21 N | The block weight is the force minus the rod weight. |

### q9 — Equal weight torques, block at an end

The block and rod torques are $4\text{ N}\cdot\text{m}$ each, and the force torque is $8\text{ N}\cdot\text{m}$. The opposite-direction block weight matches the no-angle choice, 12 N. The full-length rod torque exactly cancels the force torque, so the block weight is 0 N.

The direction slot becomes a force balance that keeps the angle, $W_b = F/2 - W_r$. The full-length slot puts the rod’s weight at the force’s position.

`q9`: pivot at the right end, rod 8 N, force 64 N at $L/4$, block at the left end. The force’s lever arm is $L/4$.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 4 N | Same-side torques, rod at $L/2$, component $F\cos 60^\circ$. |
| Distractor | 12 N | The angle is ignored. |
| Distractor | 10 N | Sine and cosine are swapped. |
| Distractor | 24 N | Lever arms are ignored and the angle is kept: $W_b = F/2 - W_r$. |
| Distractor | 8 N | The rod is ignored. |
| Distractor | 6 N | The rod is given the force’s lever arm, $L/4$, instead of $L/2$. |
| Distractor | 56 N | The block weight is the force minus the rod weight. |

### q15 — Pivot at $L/4$, block at the left end, force at $3L/4$

Rod 32 N, force 80 N. The block and the center are both to the left of the pivot. The true rod arm is $L/4$. Replacing it with $L$ gives $-16\text{ N}$, whose magnitude is the correct block weight. The substitute uses the memorized end-pivot arm $L/2$, which is still on the rod.

The no-angle choice is 43 N and the sine/cosine choice is 36 N. They differ by more than a rounding step from each other and from the correct 16 N. The direction choice is 37 N, one newton from the sine/cosine choice, and the two remain different integers.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 16 N | Same side of the interior pivot. The center is $L/4$ from the pivot. |
| Distractor | 43 N | The angle is ignored. |
| Distractor | 36 N | Sine and cosine are swapped. |
| Distractor | 37 N | The weights are given opposite directions, so the block balances the force and the rod together. |
| Distractor | 27 N | The rod is ignored. |
| Distractor | 5 N | The rod’s lever arm is taken as $L/2$ even though the center is $L/4$ from the pivot. |
| Distractor | 48 N | The block weight is the force minus the rod weight. |

### q12 — Pivot at $L/4$, block at the right end, force at the left end

Rod 32 N, force 18.67 N. The block and the center are on opposite sides. Several signed mistakes come out negative; the choices are the magnitudes.

The same-direction equation gives $-4\text{ N}$, whose magnitude is the correct answer. The substitute is the interior-pivot arm students import from the end-pivot problems: the rod’s lever arm is $L/2$ rather than the true $L/4$. The full-length choice, 100 N, stays.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 4 N | Opposite sides. The center is $L/4$ to the left of the pivot, and the block is at the right end. |
| Distractor | 24 N | The angle is ignored. The signed result is $-24\text{ N}$. |
| Distractor | 16 N | Sine and cosine are swapped. The signed result is about $-16.5\text{ N}$. |
| Distractor | 36 N | The rod’s lever arm is taken as $L/2$ instead of $L/4$. |
| Distractor | 28 N | The rod is ignored. The signed result is $-28\text{ N}$. |
| Distractor | 100 N | The rod’s lever arm is $L$. |
| Distractor | 13 N | The block weight is the force minus the rod weight. The signed result is $-13.3\text{ N}$. |

### q18 — Pivot at $3L/4$, block at $L/4$, force at the right end

Rod 16 N, force 21.33 N. The block and the center are both to the right of the pivot, and the two weight torques are equal.

The opposite-direction choice matches the no-angle choice, 24 N. The full-length magnitude matches “rod ignored,” 16 N. The force sits at the right end, which is the origin of the distances printed in the problem, so reading those distances as lever arms gives the force no torque.

| Role | Value | Misconception |
| --- | --- | --- |
| Correct | 8 N | Same side of the pivot at $3L/4$. The center is $L/4$ to the right. |
| Distractor | 24 N | The angle is ignored. |
| Distractor | 20 N | Sine and cosine are swapped. |
| Distractor | 32 N | Lever arms are the distances from the right end. The force is at the right end, so its torque is dropped, and the rod is given arm $L/2$. The signed result is $-32\text{ N}$. |
| Distractor | 16 N | The rod is ignored. |
| Distractor | 27 N | The block weight is $F\cos 60^\circ$ plus the rod weight. Lever arms never enter. |
| Distractor | 5 N | The block weight is the force minus the rod weight. |
