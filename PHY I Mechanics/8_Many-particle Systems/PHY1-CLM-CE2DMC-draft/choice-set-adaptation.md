# Adapting the q1 choice set

Source bank: `PHY1-CLM-CE2D-10232025`
Choice set: `q1-mc-draft.md`

The twenty-four problems fall into three calculation patterns, handled by three scripts and one input table:

- `calc_split.py` handles the twelve split and launch problems (`q1`–`q12`).
- `calc_collision_forward.py` handles the six sticking collisions where both incoming velocities are known and the combined speed is asked (`q13`, `q15`, `q17`, `q19`, `q21`, `q23`).
- `calc_collision_inverse.py` handles the six sticking collisions where the combined velocity and one incoming velocity are known and the other incoming speed is asked (`q14`, `q16`, `q18`, `q20`, `q22`, `q24`).

All known values and the script assignment for each problem are stored in `problem_inputs_temp.csv`. `run_all_calculations.py` reads that table and calls the matching script for each row.

Numerical values are omitted from the tables below.

## Updates applied to `q2`, `q5`, `q6`, and the inverse collisions

- **`q2` (Rocket separation):** Give the main body a vertical velocity component of $-50.00\hat{j}\text{ m/s}$, so $\vec{v}_2=(4996.67\hat{i}-50.00\hat{j})\text{ m/s}$. The payload then has $v_{1y}=+150.00\text{ m/s}$ and all six choices are well separated.
- **`q5` (Exploding firework):** Use $\hat{j}$ as vertically upward, so the initial velocity in the problem text is $\vec{V}=(50.00\hat{j})\text{ m/s}$, matching the solution. The parallel component is $y$ and the perpendicular component is $x$.
- **`q6` (Alpha decay) and inverse collisions `q14`, `q18`, `q24`:** When the kinetic-energy formula gives a negative value inside the square root, take the absolute value before the square root: $\sqrt{\lvert MV^2-m_{\text{known}}\lvert\vec{v}_{\text{known}}\rvert^2\rvert/m_{\text{unknown}}}$ for splits, and $\sqrt{\lvert M_f\lvert\vec{V}_f\rvert^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ for inverse collisions. This reflects a student assuming they made a sign slip and dropping the minus sign.

## Split and launch problems (`calc_split.py`)

### q1 — Exploding shell

Known piece is $\vec{v}_1$. Unknown piece is $m_2$.

A $10.0 \text{ kg}$ cannon shell is traveling with an initial velocity of $\vec{V} = (300 \hat{i}) \text{ m/s}$ when it suddenly explodes into two fragments.

Immediately after the explosion, one fragment has a mass of $4.0 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_1 = (320 \hat{i} + 50 \hat{j}) \text{ m/s}$.

Assuming the linear momentum of the shell system is conserved immediately before and after the explosion, what is the magnitude of the velocity of the second fragment? Round your answer to two decimal places after zero.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_2\rvert=\sqrt{v_{2x}^2+v_{2y}^2}$, with $v_{2x}=(MV_x-m_1 v_{1x})/m_2$ and $v_{2y}=-m_1 v_{1y}/m_2$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_2=(MV_x-m_1 v_{1x})/m_2$ | The perpendicular component is dropped. |
| Distractor | $v_2=\sqrt{\lvert MV^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_2\rvert=\lvert\vec{V}-\vec{v}_1\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_2=(MV-m_1\lvert\vec{v}_1\rvert)/m_2$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_2=V-\lvert\vec{v}_1\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q2 — Rocket separation (updated with vertical component)

Known piece is $\vec{v}_2$. Unknown piece is $m_1$. The main body's velocity is updated to include $-50.00\hat{j}\text{ m/s}$.

A $200.00 \text{ kg}$ small sounding rocket is traveling in deep space with an initial velocity of $\vec{V} = (5000.00 \hat{i}) \text{ m/s}$ when it separates its payload section from the main body.

Immediately after the separation, the main body, which has a mass of $150.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_2 = (4996.67 \hat{i} - 50.00 \hat{j}) \text{ m/s}$. The separated payload section has the remaining mass of $50.00 \text{ kg}$.

Assuming the linear momentum of the rocket system is conserved immediately before and after the separation, what is the magnitude of the velocity of the payload section? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_1\rvert=\sqrt{v_{1x}^2+v_{1y}^2}$, with $v_{1x}=(MV_x-m_2 v_{2x})/m_1$ and $v_{1y}=-m_2 v_{2y}/m_1$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_1=(MV_x-m_2 v_{2x})/m_1$ | The perpendicular component is dropped. |
| Distractor | $v_1=\sqrt{\lvert MV^2-m_2\lvert\vec{v}_2\rvert^2\rvert/m_1}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_1\rvert=\lvert\vec{V}-\vec{v}_2\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_1=(MV-m_2\lvert\vec{v}_2\rvert)/m_1$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_1=V-\lvert\vec{v}_2\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q3 — Space debris fracture

Known piece is $\vec{v}_1$. Unknown piece is $m_2$.

A $50.00 \text{ kg}$ fragment of space debris traveling in a straight line with an initial velocity of $\vec{V} = (8000.00 \hat{i}) \text{ m/s}$ fractures internally into two pieces.

Immediately after fracturing, one piece has a mass of $20.00 \text{ kg}$ and is observed to be moving with a velocity of $\vec{v}_1 = (7900.00 \hat{i} + 100.00 \hat{j}) \text{ m/s}$. The second piece has the remaining mass of $30.00 \text{ kg}$.

Assuming the linear momentum of the system is conserved immediately before and after the fracture, what is the magnitude of the velocity of the second piece? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_2\rvert=\sqrt{v_{2x}^2+v_{2y}^2}$, with $v_{2x}=(MV_x-m_1 v_{1x})/m_2$ and $v_{2y}=-m_1 v_{1y}/m_2$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_2=(MV_x-m_1 v_{1x})/m_2$ | The perpendicular component is dropped. |
| Distractor | $v_2=\sqrt{\lvert MV^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_2\rvert=\lvert\vec{V}-\vec{v}_1\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_2=(MV-m_1\lvert\vec{v}_1\rvert)/m_2$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_2=V-\lvert\vec{v}_1\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q4 — Exploding ice block

Known piece is $\vec{v}_2$. Unknown piece is $m_1$.

A $80.00 \text{ kg}$ large block of ice sliding frictionlessly across a frozen lake with an initial velocity of $\vec{V} = (4.00 \hat{i}) \text{ m/s}$ explodes into two pieces.

Immediately after the explosion, one piece, which has a mass of $50.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_2 = (3.40 \hat{i} - 1.20 \hat{j}) \text{ m/s}$. The other piece has the remaining mass of $30.00 \text{ kg}$.

Assuming the linear momentum of the system is conserved immediately before and after the explosion, what is the magnitude of the velocity of the other piece? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_1\rvert=\sqrt{v_{1x}^2+v_{1y}^2}$, with $v_{1x}=(MV_x-m_2 v_{2x})/m_1$ and $v_{1y}=-m_2 v_{2y}/m_1$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_1=(MV_x-m_2 v_{2x})/m_1$ | The perpendicular component is dropped. |
| Distractor | $v_1=\sqrt{\lvert MV^2-m_2\lvert\vec{v}_2\rvert^2\rvert/m_1}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_1\rvert=\lvert\vec{V}-\vec{v}_2\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_1=(MV-m_2\lvert\vec{v}_2\rvert)/m_1$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_1=V-\lvert\vec{v}_2\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q5 — Exploding firework (updated with $\hat{j}$ as upward)

Known piece is $\vec{v}_1$. Unknown piece is $m_2$. The initial velocity is along $\hat{j}$.

A $0.50 \text{ kg}$ piece of firework traveling directly upwards with an initial velocity of $\vec{V} = (50.00 \hat{j}) \text{ m/s}$ explodes into two non-identical pieces. (Assuming that the $\hat{j}$ direction is defined vertically upwards.)

Immediately after the explosion, one piece has a mass of $0.20 \text{ kg}$ and is observed to be moving with a velocity of $\vec{v}_1 = (55.00 \hat{i} + 15.00 \hat{j}) \text{ m/s}$. The second piece has the remaining mass of $0.30 \text{ kg}$.

Assuming the linear momentum of the system is conserved immediately before and after the explosion, what is the magnitude of the velocity of the second piece? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_2\rvert=\sqrt{v_{2x}^2+v_{2y}^2}$, with $v_{2x}=-m_1 v_{1x}/m_2$ and $v_{2y}=(MV_y-m_1 v_{1y})/m_2$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_2=(MV_y-m_1 v_{1y})/m_2$ | The perpendicular component ($x$) is dropped. |
| Distractor | $v_2=\sqrt{\lvert MV^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_2\rvert=\lvert\vec{V}-\vec{v}_1\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_2=(MV-m_1\lvert\vec{v}_1\rvert)/m_2$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_2=V-\lvert\vec{v}_1\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q6 — Alpha decay

Known piece is $\vec{v}_2$. Unknown piece is $m_1$. The energy choice uses the absolute value inside the square root.

A $240.00 \text{ u}$ heavy nucleus (parent) moving in a straight line with an initial velocity of $\vec{V} = (200.00 \hat{i}) \text{ m/s}$ undergoes alpha decay.

Immediately after the decay, the resulting daughter nucleus, which has a mass of $236.00 \text{ u}$, is observed to be moving with a velocity of $\vec{v}_2 = (199.92 \hat{i} - 84.75 \hat{j}) \text{ m/s}$. The emitted alpha particle has the remaining mass of $4.00 \text{ u}$.

Assuming the linear momentum of the system is conserved immediately before and after the decay, what is the magnitude of the velocity of the alpha particle? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_1\rvert=\sqrt{v_{1x}^2+v_{1y}^2}$, with $v_{1x}=(MV_x-m_2 v_{2x})/m_1$ and $v_{1y}=-m_2 v_{2y}/m_1$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_1=(MV_x-m_2 v_{2x})/m_1$ | The perpendicular component is dropped. |
| Distractor | $v_1=\sqrt{\lvert MV^2-m_2\lvert\vec{v}_2\rvert^2\rvert/m_1}$ | Kinetic energy is treated as conserved, with the sign inside the square root ignored. |
| Distractor | $\lvert\vec{v}_1\rvert=\lvert\vec{V}-\vec{v}_2\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_1=(MV-m_2\lvert\vec{v}_2\rvert)/m_1$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_1=V-\lvert\vec{v}_2\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q7 — Skater throws bag

Known piece is $\vec{v}_1$. Unknown piece is $m_2$.

A $70.00 \text{ kg}$ roller skater is skating on a smooth surface with an initial velocity of $\vec{V} = (5.00 \hat{i}) \text{ m/s}$ when they throw a heavy gym bag.

Immediately after throwing the bag, the gym bag, which has a mass of $10.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_1 = (8.00 \hat{i} + 3.00 \hat{j}) \text{ m/s}$. The skater has the remaining mass of $60.00 \text{ kg}$.

Assuming the linear momentum of the skater-bag system is conserved immediately before and after the throw, what is the magnitude of the velocity of the skater? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_2\rvert=\sqrt{v_{2x}^2+v_{2y}^2}$, with $v_{2x}=(MV_x-m_1 v_{1x})/m_2$ and $v_{2y}=-m_1 v_{1y}/m_2$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_2=(MV_x-m_1 v_{1x})/m_2$ | The perpendicular component is dropped. |
| Distractor | $v_2=\sqrt{\lvert MV^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_2\rvert=\lvert\vec{V}-\vec{v}_1\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_2=(MV-m_1\lvert\vec{v}_1\rvert)/m_2$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_2=V-\lvert\vec{v}_1\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q8 — Submarine launches drone

Known piece is $\vec{v}_2$. Unknown piece is $m_1$.

A $10000.00 \text{ kg}$ small submarine is cruising horizontally with an initial velocity of $\vec{V} = (10.00 \hat{i}) \text{ m/s}$ when it launches an underwater exploration drone.

Immediately after the launch, the submarine, which has a new mass of $9800.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_2 = (9.90 \hat{i} - 0.10 \hat{j}) \text{ m/s}$. The exploration drone has a mass of $200.00 \text{ kg}$.

Assuming the linear momentum of the submarine-drone system is conserved immediately before and after the launch, what is the magnitude of the velocity of the exploration drone? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_1\rvert=\sqrt{v_{1x}^2+v_{1y}^2}$, with $v_{1x}=(MV_x-m_2 v_{2x})/m_1$ and $v_{1y}=-m_2 v_{2y}/m_1$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_1=(MV_x-m_2 v_{2x})/m_1$ | The perpendicular component is dropped. |
| Distractor | $v_1=\sqrt{\lvert MV^2-m_2\lvert\vec{v}_2\rvert^2\rvert/m_1}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_1\rvert=\lvert\vec{V}-\vec{v}_2\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_1=(MV-m_2\lvert\vec{v}_2\rvert)/m_1$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_1=V-\lvert\vec{v}_2\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q9 — Space-ship launches pod

Known piece is $\vec{v}_1$. Unknown piece is $m_2$.

A $5000.00 \text{ kg}$ small space-ship is cruising in deep space with an initial velocity of $\vec{V} = (2000.00 \hat{i}) \text{ m/s}$ when it launches an exploration pod.

Immediately after the launch, the exploration pod, which has a mass of $500.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_1 = (2500.00 \hat{i} + 1000.00 \hat{j}) \text{ m/s}$. The space-ship has the remaining mass of $4500.00 \text{ kg}$.

Assuming the linear momentum of the system is conserved immediately before and after the launch, what is the magnitude of the velocity of the space-ship? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_2\rvert=\sqrt{v_{2x}^2+v_{2y}^2}$, with $v_{2x}=(MV_x-m_1 v_{1x})/m_2$ and $v_{2y}=-m_1 v_{1y}/m_2$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_2=(MV_x-m_1 v_{1x})/m_2$ | The perpendicular component is dropped. |
| Distractor | $v_2=\sqrt{\lvert MV^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_2\rvert=\lvert\vec{V}-\vec{v}_1\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_2=(MV-m_1\lvert\vec{v}_1\rvert)/m_2$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_2=V-\lvert\vec{v}_1\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q10 — Passenger jumps from bumper car

Known piece is $\vec{v}_2$. Unknown piece is $m_1$.

A $180.00 \text{ kg}$ bumper car is coasting on a slick surface with an initial velocity of $\vec{V} = (3.00 \hat{i}) \text{ m/s}$ when its passenger jumps out.

Immediately after the jump, the bumper car, which has a new mass of $110.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_2 = (1.73 \hat{i} - 1.59 \hat{j}) \text{ m/s}$. The passenger has a mass of $70.00 \text{ kg}$.

Assuming the linear momentum of the car-passenger system is conserved immediately before and after the jump, what is the magnitude of the velocity of the passenger? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_1\rvert=\sqrt{v_{1x}^2+v_{1y}^2}$, with $v_{1x}=(MV_x-m_2 v_{2x})/m_1$ and $v_{1y}=-m_2 v_{2y}/m_1$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_1=(MV_x-m_2 v_{2x})/m_1$ | The perpendicular component is dropped. |
| Distractor | $v_1=\sqrt{\lvert MV^2-m_2\lvert\vec{v}_2\rvert^2\rvert/m_1}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_1\rvert=\lvert\vec{V}-\vec{v}_2\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_1=(MV-m_2\lvert\vec{v}_2\rvert)/m_1$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_1=V-\lvert\vec{v}_2\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q11 — Hovercraft pushes crate

Known piece is $\vec{v}_1$. Unknown piece is $m_2$.

A $1000.00 \text{ kg}$ hovercraft is moving over a smooth surface with an initial velocity of $\vec{V} = (15.00 \hat{i}) \text{ m/s}$ when it pushes a heavy supply crate.

Immediately after being pushed, the supply crate, which has a mass of $100.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_1 = (20.00 \hat{i} + 10.00 \hat{j}) \text{ m/s}$. The hovercraft has the remaining mass of $900.00 \text{ kg}$.

Assuming the linear momentum of the system is conserved immediately before and after the push, what is the magnitude of the velocity of the hovercraft? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_2\rvert=\sqrt{v_{2x}^2+v_{2y}^2}$, with $v_{2x}=(MV_x-m_1 v_{1x})/m_2$ and $v_{2y}=-m_1 v_{1y}/m_2$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_2=(MV_x-m_1 v_{1x})/m_2$ | The perpendicular component is dropped. |
| Distractor | $v_2=\sqrt{\lvert MV^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_2\rvert=\lvert\vec{V}-\vec{v}_1\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_2=(MV-m_1\lvert\vec{v}_1\rvert)/m_2$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_2=V-\lvert\vec{v}_1\rvert$ | The known piece's speed is subtracted from the initial speed. |

### q12 — Sled launches package

Known piece is $\vec{v}_2$. Unknown piece is $m_1$.

A $250.00 \text{ kg}$ heavy sled is sliding down a gentle, icy slope with an initial velocity of $\vec{V} = (8.00 \hat{i}) \text{ m/s}$ when it launches a dense satellite package.

Immediately after the launch, the sled, which has a new mass of $220.00 \text{ kg}$, is observed to be moving with a velocity of $\vec{v}_2 = (7.45 \hat{i} - 0.82 \hat{j}) \text{ m/s}$. The satellite package has a mass of $30.00 \text{ kg}$.

Assuming the linear momentum of the sled-package system is conserved immediately before and after the launch, what is the magnitude of the velocity of the satellite package? Round your answer to two decimal places.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_1\rvert=\sqrt{v_{1x}^2+v_{1y}^2}$, with $v_{1x}=(MV_x-m_2 v_{2x})/m_1$ and $v_{1y}=-m_2 v_{2y}/m_1$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_1=(MV_x-m_2 v_{2x})/m_1$ | The perpendicular component is dropped. |
| Distractor | $v_1=\sqrt{\lvert MV^2-m_2\lvert\vec{v}_2\rvert^2\rvert/m_1}$ | Kinetic energy is treated as conserved. |
| Distractor | $\lvert\vec{v}_1\rvert=\lvert\vec{V}-\vec{v}_2\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_1=(MV-m_2\lvert\vec{v}_2\rvert)/m_1$ | The known piece's speed replaces its velocity components. |
| Distractor | $v_1=V-\lvert\vec{v}_2\rvert$ | The known piece's speed is subtracted from the initial speed. |

## Sticking collisions, combined speed unknown (`calc_collision_forward.py`)

Problems: `q13` colliding asteroids, `q15` football tackle, `q17` space probe docking, `q19` train car coupling, `q21` ice skaters, `q23` cargo drone catch.

$M_f=m_1+m_2$, and $\vec{v}_1$ lies along $\hat{i}$.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{V}_f\rvert=\sqrt{V_{fx}^2+V_{fy}^2}$, with $V_{fx}=(m_1 v_{1x}+m_2 v_{2x})/M_f$ and $V_{fy}=(m_1 v_{1y}+m_2 v_{2y})/M_f$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $V_f=(m_1 v_{1x}+m_2 v_{2x})/M_f$ | The perpendicular component is dropped. |
| Distractor | $V_f=\sqrt{(m_1\lvert\vec{v}_1\rvert^2+m_2\lvert\vec{v}_2\rvert^2)/M_f}$ | Kinetic energy is treated as conserved through the sticking collision. |
| Distractor | $\lvert\vec{V}_f\rvert=\lvert\vec{v}_1-\vec{v}_2\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $V_f=(m_1\lvert\vec{v}_1\rvert+m_2\lvert\vec{v}_2\rvert)/M_f$ | The speeds are added as if the collision were one-dimensional. |
| Distractor | $V_f=\lvert\vec{v}_1\rvert-\lvert\vec{v}_2\rvert$ | One speed is subtracted from the other. |

### q13 — Colliding asteroids

An asteroid of mass $m_1 = 1000.00 \text{ kg}$ is traveling through space with a velocity of $\vec{v}_1 = (20.00 \hat{i}) \text{ m/s}$. It collides with a second asteroid of mass $m_2 = 500.00 \text{ kg}$ traveling at $\vec{v}_2 = (-10.00 \hat{i} + 30.00 \hat{j}) \text{ m/s}$. The two asteroids stick together.

Assuming the linear momentum of the two-asteroid system is conserved, what is the magnitude of the velocity of the combined mass immediately after the collision? Round your answer to two decimal places.

### q15 — Football tackle

A $110.00 \text{ kg}$ linebacker running at $\vec{v}_1 = (8.00 \hat{i}) \text{ m/s}$ tackles a $100.00 \text{ kg}$ running back who is moving at $\vec{v}_2 = (-7.00 \hat{i} + 2.00 \hat{j}) \text{ m/s}$. The linebacker holds on, and the two players move together.

Assuming the linear momentum of the two-player system is conserved, what is the magnitude of their combined velocity immediately after the tackle? Round your answer to two decimal places.

### q17 — Space probe docking

A $4000.00 \text{ kg}$ space probe traveling at $\vec{v}_1 = (1000.00 \hat{i}) \text{ m/s}$ docks with a $1000.00 \text{ kg}$ supply module moving at $\vec{v}_2 = (500.00 \hat{i} + 800.00 \hat{j}) \text{ m/s}$. The two craft lock together.

Assuming the linear momentum of the system is conserved, what is the magnitude of the velocity of the combined craft immediately after docking? Round your answer to two decimal places.

### q19 — Train car coupling

A $20000.00 \text{ kg}$ train car moving at $\vec{v}_1 = (5.00 \hat{i}) \text{ m/s}$ on a straight track couples with a $15000.00 \text{ kg}$ car that is moving at $\vec{v}_2 = (2.00 \hat{i} + 1.00 \hat{j}) \text{ m/s}$ on an adjacent track (the tracks merge).

Assuming the linear momentum of the system is conserved, what is the magnitude of the velocity of the two coupled cars immediately after they link? Round your answer to two decimal places.

### q21 — Ice skaters

A $70.00 \text{ kg}$ ice skater moving at $\vec{v}_1 = (6.00 \hat{i}) \text{ m/s}$ grabs onto a $50.00 \text{ kg}$ skater who is moving at $\vec{v}_2 = (2.00 \hat{i} + 4.00 \hat{j}) \text{ m/s}$. The two skaters then glide off together.

Assuming the linear momentum of the system is conserved, what is the magnitude of their combined velocity immediately after they join? Round your answer to two decimal places.

### q23 — Cargo drone catch

A $80.00 \text{ kg}$ cargo drone is flying horizontally at $\vec{v}_1 = (30.00 \hat{i}) \text{ m/s}$. It moves to catch a $20.00 \text{ kg}$ package that is moving at $\vec{v}_2 = (10.00 \hat{i} + 50.00 \hat{j}) \text{ m/s}$. The drone catches the package and holds onto it.

Assuming the linear momentum of the system is conserved, what is the magnitude of the velocity of the drone and its package immediately after the catch? Round your answer to two decimal places.

## Sticking collisions, second incoming speed unknown (`calc_collision_inverse.py`)

Problems: `q14` colliding mud balls, `q16` shopping carts, `q18` clay projectiles, `q20` rafts linking, `q22` bumper cars, `q24` colliding sleds.

$\vec{v}_2$ is the unknown. $\vec{v}_1$ lies along $\hat{i}$. The energy choice uses the absolute value inside the square root so that `q14`, `q18`, and `q24` use the same formula as `q16`, `q20`, and `q22`.

| Role | Formula | Misconception |
| --- | --- | --- |
| Correct | $\lvert\vec{v}_2\rvert=\sqrt{v_{2x}^2+v_{2y}^2}$, with $v_{2x}=(M_f V_{fx}-m_1 v_{1x})/m_2$ and $v_{2y}=(M_f V_{fy}-m_1 v_{1y})/m_2$ | Momentum is conserved on each axis, then the components are combined. |
| Distractor | $v_2=(M_f V_{fx}-m_1 v_{1x})/m_2$ | The perpendicular component is dropped. |
| Distractor | $v_2=\sqrt{\lvert M_f\lvert\vec{V}_f\rvert^2-m_1\lvert\vec{v}_1\rvert^2\rvert/m_2}$ | Kinetic energy is treated as conserved, with the sign inside the square root ignored when negative. |
| Distractor | $\lvert\vec{v}_2\rvert=\lvert\vec{V}_f-\vec{v}_1\rvert$ | Velocities are subtracted with no masses. |
| Distractor | $v_2=(M_f\lvert\vec{V}_f\rvert-m_1\lvert\vec{v}_1\rvert)/m_2$ | Speeds are used in place of the velocity components. |
| Distractor | $v_2=\lvert\vec{V}_f\rvert-\lvert\vec{v}_1\rvert$ | The known speed is subtracted from the final speed. |

### q14 — Colliding mud balls

A $0.50 \text{ kg}$ ball of mud is thrown with a velocity of $\vec{v}_1 = (10.00 \hat{i}) \text{ m/s}$. It strikes and sticks to a second ball of mud. The combined mass of $0.80 \text{ kg}$ is observed moving with a final velocity of $\vec{V}_{f} = (7.00 \hat{i} + 1.50 \hat{j}) \text{ m/s}$.

Assuming the linear momentum of the system is conserved, what was the magnitude of the initial velocity of the second mud ball (which had a mass of $0.30 \text{ kg}$)? Round your answer to two decimal places.

### q16 — Shopping carts

A $20.00 \text{ kg}$ shopping cart moving at $\vec{v}_1 = (3.00 \hat{i}) \text{ m/s}$ collides with another shopping cart. The carts lock together and move off with a combined mass of $45.00 \text{ kg}$ and a final velocity of $\vec{V}_{f} = (4.00 \hat{i} + 1.00 \hat{j}) \text{ m/s}$.

Assuming the linear momentum of the system is conserved, what was the magnitude of the initial velocity of the second shopping cart (which had a mass of $25.00 \text{ kg}$)? Round your answer to two decimal places.

### q18 — Clay projectiles

A $2.00 \text{ kg}$ clay projectile is fired with a velocity of $\vec{v}_1 = (50.00 \hat{i}) \text{ m/s}$. It strikes and sticks to a $1.00 \text{ kg}$ clay target. The combined $3.00 \text{ kg}$ mass moves with a final velocity of $\vec{V}_{f} = (30.00 \hat{i} - 10.00 \hat{j}) \text{ m/s}$.

Assuming the linear momentum of the system is conserved, what was the magnitude of the initial velocity of the $1.00 \text{ kg}$ target? Round your answer to two decimal places.

### q20 — Rafts linking

A $300.00 \text{ kg}$ raft moving at $\vec{v}_1 = (1.00 \hat{i}) \text{ m/s}$ collides and links with a second raft. The combined mass of $500.00 \text{ kg}$ is observed moving with a final velocity of $\vec{V}_{f} = (0.60 \hat{i} - 0.60 \hat{j}) \text{ m/s}$.

Assuming the linear momentum of the system is conserved, what was the magnitude of the initial velocity of the second raft (which had a mass of $200.00 \text{ kg}$)? Round your answer to two decimal places.

### q22 — Bumper cars

A $150.00 \text{ kg}$ bumper car (car 1) moving at $\vec{v}_1 = (4.00 \hat{i}) \text{ m/s}$ crashes into a second bumper car (car 2). The cars stick together and move off with a combined mass of $260.00 \text{ kg}$ and a final velocity of $\vec{V}_{f} = (3.00 \hat{i} - 1.00 \hat{j}) \text{ m/s}$.

Assuming the linear momentum of the system is conserved, what was the magnitude of the initial velocity of car 2 (which had a mass of $110.00 \text{ kg}$)? Round your answer to two decimal places.

### q24 — Colliding sleds

A $100.00 \text{ kg}$ sled is moving at $\vec{v}_1 = (10.00 \hat{i}) \text{ m/s}$ on a frozen lake. It collides with another sled, and they stick together. The combined mass of $180.00 \text{ kg}$ is observed moving with a final velocity of $\vec{V}_{f} = (7.00 \hat{i} + 2.00 \hat{j}) \text{ m/s}$.

Assuming the linear momentum of the system is conserved, what was the magnitude of the initial velocity of the second sled (which had a mass of $80.00 \text{ kg}$)? Round your answer to two decimal places.
