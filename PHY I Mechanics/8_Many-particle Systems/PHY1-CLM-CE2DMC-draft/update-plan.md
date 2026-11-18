# Update plan — PHY1-CLM-CE2DMC-11102026

Bank file: `PHY1-CLM-CE2DMC-11102026-draft.yaml`  
Inputs: `problem_inputs_temp.csv`  
Roles and solvers: `choice-set-adaptation.md`, `calc_split.py`, `calc_collision_forward.py`, `calc_collision_inverse.py`  
Follows the comments saved in `../../MC Bank Reviews/synthesis.md`.

Applied to the bank file. Before the inputs changed, the solvers reproduced every key and distractor then in the bank. After the inputs changed, the same solvers reproduced every new key below. Negative roles stay signed in `calculated_choices_temp.csv` and are printed as absolute values in the bank.

Choice order in the YAML is already known and is not part of this update. The six roles stay: drop the perpendicular component, treat kinetic energy as conserved, subtract the velocity vectors with no masses, replace a velocity with a speed, subtract the known speed from the initial speed, and the correct magnitude.

Two rules for every edited item:

- A choice that is a speed is the absolute value of its role. A negative result is the same mistake with the sign dropped.
- After that absolute value, the six printed numbers are distinct, any two differ by at least 0.10 m/s, and none of the five wrong choices sits within 5% of the key.

Re-run the matching script after each input change and publish those six numbers.

## 1. Replace the illegal distractors

These items keep their inputs. Only the negative printed choices change, to the absolute value of the same role.

| Item | Role that is negative | Print this instead |
|---|---|---:|
| q5 | known speed subtracted from the initial speed | 7.01 m/s |
| q13 | known speed subtracted from the initial speed | 11.62 m/s |
| q14 | known speed subtracted from the initial speed | 2.84 m/s |
| q18 | perpendicular component dropped | 10.00 m/s |
| q18 | velocities replaced by speeds | 5.13 m/s |
| q18 | known speed subtracted from the initial speed | 18.38 m/s |
| q23 | known speed subtracted from the initial speed | 20.99 m/s |
| q24 | known speed subtracted from the initial speed | 2.72 m/s |

q1, q6, q7, q9, q11, q20, and q22 also have a negative role today. Their inputs change in the sections below, so the absolute value is taken from the new calculation rather than from the old one.

## 2. Reword the combined mass

On q7, q8, q9, q10, q11, and q12 the first mass is already the combined system. The keys assume that. Each original opening sentence now names both objects and states that total. The later sentence that gives each mass after the separation is unchanged. q9 and q11 use the masses from section 3 in that later sentence.

- q7: A roller skater carrying a gym bag, with a total mass of 70.00 kg, is skating on a smooth surface at \(5.00\,\hat{i}\) m/s when they throw a heavy gym bag.
- q8: A small submarine carrying an exploration drone, with a total mass of 10000.00 kg, is cruising horizontally at \(10.00\,\hat{i}\) m/s when it launches an underwater exploration drone.
- q9: A small space-ship carrying an exploration pod, with a total mass of 5000.00 kg, is cruising in deep space at \(2000.00\,\hat{i}\) m/s when it launches an exploration pod.
- q10: A bumper car carrying its passenger, with a total mass of 180.00 kg, is coasting on a slick surface at \(3.00\,\hat{i}\) m/s when its passenger jumps out.
- q11: A hovercraft carrying a heavy supply crate, with a total mass of 1000.00 kg, is moving over a smooth surface at \(15.00\,\hat{i}\) m/s when it pushes a heavy supply crate.
- q12: A heavy sled carrying a dense satellite package, with a total mass of 250.00 kg, is sliding down a gentle, icy slope at \(8.00\,\hat{i}\) m/s when it launches a dense satellite package.

## 3. Suggested numbers where choices sit on top of each other

The sideways piece is too small next to the forward speed, so “drop the perpendicular component” and “use speeds instead of velocity” land on the key. Change only the fields below. Masses of the two pieces still add to the stated total.

| Item | Change | New key | Published choices, absolute values (m/s) |
|---|---|---:|---|
| q1 | known-piece \(v_y\): 50 → 150 | 303.61 | 303.61, 286.67, 258.33, 151.33, 264.39, 53.41 |
| q2 | known-piece \(v_y\): −50 → −600 | 5323.53 | 5323.53, 5009.99, 4901.01, 600.01, 4902.30, 32.57 |
| q3 | known-piece \(v_y\): 100 → 4500 | 8606.46 | 8606.46, 8066.67, 7180.53, 4501.11, 7272.16, 1091.75 |
| q4 | known-piece \(v_y\): −1.20 → −3.50 | 7.68 | 7.68, 5.00, 1.73, 3.55, 2.53, 0.88 |
| q7 | known-piece \(v_y\): 3 → 10 | 4.80 | 4.80, 4.50, 1.35, 10.44, 3.70, 7.81 |
| q8 | known-piece \(v_y\): −0.10 → −0.50 | 28.68 | 28.68, 14.90, 13.61, 0.51, 14.28, 0.09 |
| q9 | pod 500 kg at \((2500,\ 1000)\) → 1200 kg at \((4000,\ 2500)\); ship mass after launch is 3800 kg | 1579.82 | 1579.82, 1368.42, 1327.84, 3201.56, 1142.00, 2716.99 |
| q11 | crate 100 kg at \((20,\ 10)\) → 250 kg at \((22,\ 14)\); hovercraft mass after the push is 750 kg | 13.50 | 13.50, 12.67, 8.56, 15.65, 11.31, 11.08 |
| q15 | second incoming \(v_y\): 2 → 8.50 | 4.14 | 4.14, 0.86, 9.55, 17.24, 9.43, 3.01 |
| q16 | combined \(v_y\): 1 → 2 | 6.00 | 6.00, 4.80, 5.37, 2.24, 5.65, 1.47 |
| q17 | lighter craft \(v_y\): 800 → 1500 | 948.68 | 948.68, 900.00, 1140.18, 1581.14, 1116.23, 581.14 |
| q20 | combined velocity \((0.60,\ -0.60)\) → \((0.90,\ -1.20)\) | 3.09 | 3.09, 0.75, 2.03, 1.20, 2.25, 0.50 |
| q21 | second incoming \(v_y\): 4 → 8.50 | 5.60 | 5.60, 4.33, 7.26, 9.39, 7.14, 2.73 |
| q22 | combined \(v_y\): −1 → −4 | 9.60 | 9.60, 1.64, 6.11, 4.12, 6.36, 1.00 |

Order of the six numbers in each row: correct magnitude, perpendicular component dropped, kinetic energy treated as conserved, velocity difference with no masses, speeds used in place of velocity, initial speed minus known speed.

q10, q12, q13, q14, q18, q23, and q24 already meet the 5% and 0.10 m/s rules. Their inputs are unchanged. Section 1 is applied where a choice was negative.

The existing-number check passed for all 24 items: each solver, using the inputs then on file, reproduced the key and the five distractors already in the bank. The same solvers then reproduced every new row in the table above, so those numbers were written into the bank. No formula change was required. After absolute values, every item has six distinct choices, every pair differs by at least 0.10 m/s, and no wrong choice is within 5% of its key. The alpha in q6 has a kinetic energy of about 4.52 MeV.

## 4. New numbers for the alpha decay (q6)

The present alpha speed, about 5004 m/s, is a kinetic energy of about 0.52 eV for a 4 u particle. Keep the decay and the masses. Multiply the velocity scale so the alpha carries a few MeV.

- Parent: 240 u, velocity \(6.00\times 10^{5}\,\hat{i}\) m/s.
- Known fragment: 236 u, velocity \((6.00\times 10^{5}\,\hat{i} - 2.50\times 10^{5}\,\hat{j})\) m/s.
- Alpha: 4 u. Asked speed: \(1.476\times 10^{7}\) m/s (14762198.35 m/s at two decimals).
- Kinetic energy of that alpha: about 4.5 MeV.

Published choices, with the two negative roles made positive: 14762198.35, 600000.00, 1824143.63, 250000.00, 2350000.00, and 50000.00 m/s.

## 5. New context for q19

Replace the train cars on merging rails with two hockey players on ice who collide and hold on. The ice supports their weight and does not supply the sideways impulse a rail would.

- Player A: 90 kg, velocity \(5.00\,\hat{i}\) m/s.
- Player B: 70 kg, velocity \((2.00\,\hat{i} + 8.00\,\hat{j})\) m/s.
- Asked value: speed of the pair just after they hold on.
- Key: 5.08 m/s.
- Published choices: 5.08, 3.69, 6.62, 8.54, 6.42, and 3.25 m/s.

The last of those is the absolute value of player A’s speed minus player B’s speed.

## 6. One wording fix on q1

In q1, change “two decimal places after zero” to “two decimal places.” Use the new \(v_y = 150\) m/s from section 3 in that same stem.
