# Quality
Source: PHY1-RM-TBORMC-11102026.yaml
Target physics: inferred — static torque balance on one horizontal rod about a pivot, with the rod weight, one hanging weight, and one force at 60° to the vertical

## Mathematical correctness
- Result: weak
- Relation: Στ = 0 about the pivot, with the force’s perpendicular component taken as F/2 and the rod weight at the rod center
- Checked: 30 items
- Finding: Every marked key matches that relation after nearest-integer rounding, including mid-rod and left-end pivots. The stem states the force is 60° with respect to the vertical, so the component perpendicular to the horizontal rod is F sin 60°, but every feedback line writes F cos 60° = F/2. The integers stay consistent with the labeled factor of 1/2; the axis and angle wording do not.
- Mismatches:
  - q1–q30: stated keys match recomputation with F/2; stem says 60° from vertical, feedback names F cos 60° = F/2 (complementary trig / reference-direction mislabel)

## Contextual numbers
- Result: fail
- Finding: Every stem uses L = 1.0 m and 60°. Weights and many keys are drawn from 4, 8, 16, and 32 N. A few forces are written as 18.67 or 53.33, but the bank is clean textbook values.

## Problem body
- Result: fail
- Finding: Items stand alone and name the target, but every stem is the same paragraph with the pivot, the unknown, and the positions swapped.

## Variation across the bank
- Result: fail
- Finding: The object, length, and angle never change. Moving the pivot and cycling the unknown among force, rod weight, and block weight is not a new setting. Many keys are again 4, 8, 16, or 32 N.

## Same physics
- Result: pass
- Finding: Every item is the same torque balance. Changing which quantity is unknown and which side of the pivot a weight hangs on still maps onto that solution.

## Distractors
- Result: pass
- Finding: Six parallel integer-newton choices come from one shared list of moves: drop the 60° factor, swap sine and cosine, reverse one torque, omit one weight, put the rod’s weight at full length, or add the two weights. On q1 those are 22, 25, 41, 1, 87, and 36 N beside the key 44 N.

---

# Quality
Source: PHY1-CLM-CE2DMC-11102026.yaml
Target physics: inferred — conserve linear momentum on each axis, then take the magnitude, for a split/launch or a perfectly inelastic collision

## Mathematical correctness
- Result: pass
- Relation: Σp_x and Σp_y conserved; asked value is the magnitude of the unknown velocity (leftover piece, combined velocity, or other incoming velocity)
- Checked: 24 items
- Finding: Every marked key matches the recomputed magnitude to the two-decimal rounding the stems state. Feedback names that same two-axis conservation. No stem-to-working axis or sign mislabel was found in the solution text.
- Mismatches: none

## Contextual numbers
- Result: weak
- Finding: Many speeds are round values written to two decimals, such as 300, 5000.00, and 8.00. A few components are uneven, such as 1.73, 84.75, and 3.40, and the magnitudes fit the named objects.

## Problem body
- Result: weak
- Finding: Objects and events differ and each stem asks for a magnitude, but q1–q12 share one closing template and q13–q24 share another. q1 says to round “to two decimal places after zero.”

## Variation across the bank
- Result: pass
- Finding: Settings run from a shell and a rocket to ice, a tackle, trains, and rafts. Keys run from 1.28 m/s to 8066.94 m/s.

## Same physics
- Result: pass
- Finding: Every item conserves momentum on each axis and then takes a magnitude. Asking for the leftover piece, the combined speed, or the other incoming speed does not change that principle.

## Distractors
- Result: weak
- Finding: Wrong choices are a shared set of component mistakes. On q1, 286.67 m/s is the x component alone, 284.08 m/s treats the fragment velocity as a scalar, and 53.85 m/s is the known fragment’s kick. The same method stops separating the choices when the kick is small next to a large speed: on q2 and q3, three choices sit within a few meters per second of a multi-thousand m/s key. Thirteen items also offer a negative number for a magnitude.
