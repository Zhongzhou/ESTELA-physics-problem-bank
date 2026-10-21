# Solution: Elevator Problem (Scenario 1a)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**, each with its own constant acceleration:

* **Segment 1:** The elevator starts from rest at the lobby and speeds up with constant acceleration until it reaches a cruising speed.
* **Segment 2:** Immediately after, it slows down uniformly with constant acceleration until it comes to rest at the target floor.

**Knowns (Segment 1):** acceleration, time interval, and initial velocity (implicitly rest).
**Knowns (Segment 2):** acceleration and time interval.
**Unknown (overall):** total displacement (the magnitude of the total upward position change).

---

### 2. Choose coordinate system

Let the **positive $\hat{j}$** direction be **upward** along the elevator shaft. All vertical quantities will be expressed relative to this axis.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Elevator speeds up from rest”

| Variable         | Symbol             | Value                           | Notes                               |
| ---------------- | ------------------ | ------------------------------- | ----------------------------------- |
| Displacement     | $\Delta \vec{r}_1$ | ? $\hat{j}$                     | To be determined                    |
| Initial velocity | $\vec{v}_{i1}$     | $0\, \text{m/s} \, \hat{j}$     | Given implicitly (starts from rest) |
| Final velocity   | $\vec{v}_{f1}$     | ? $ \hat{j}$                    | To be determined                    |
| Acceleration     | $\vec{a}_1$        | $1.2\, \text{m/s}^2 \, \hat{j}$ | Given                               |
| Time interval    | $\Delta t_1$       | $2.5\, \text{s}$                | Given                               |

---

#### Segment 2 — “Elevator slows to rest at target floor”

| Variable         | Symbol             | Value                              | Notes                             |
| ---------------- | ------------------ | ---------------------------------- | --------------------------------- |
| Displacement     | $\Delta \vec{r}_2$ | ? $ \hat{j}$                       | To be determined                  |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$            | Must be consistent with Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | $0\, \text{m/s} \, \hat{j}$        | Given implicitly (comes to rest)  |
| Acceleration     | $\vec{a}_2$        | $1.2\, \text{m/s}^2 \, (-\hat{j})$ | Given                             |
| Time interval    | $\Delta t_2$       | $2.5\, \text{s}$                   | Given                             |

---

### 4. Identify useful kinematic equations

For Segment 1, since we know $v_{i1}, a_1, t_1$, the displacement can be found using:

$$
\Delta \vec{r}_1 = \vec{v}_{i1}\,\Delta t_1 + \tfrac{1}{2}\,\vec{a}_1\,(\Delta t_1)^2
$$

For Segment 2, since we know $v_{f2}, a_2, t_2$, the displacement can be found using:

$$
\Delta \vec{r}_2 = \vec{v}_{i2}\,\Delta t_2 + \tfrac{1}{2}\,\vec{a}_2\,(\Delta t_2)^2
$$

Finally, the total displacement is:

$$
\Delta \vec{r}_{\text{tot}} = \Delta \vec{r}_1 + \Delta \vec{r}_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
\Delta \vec{r}_1 = (0)(2.5)\,\hat{j} + \tfrac{1}{2}(1.2)(2.5^2)\,\hat{j}
$$

$$
\Delta \vec{r}_1 = (0 + 3.75)\,\hat{j} = 3.75\,\text{m}\,\hat{j}
$$

$$
\vec{v}_{f1} = \vec{v}_{i1} + \vec{a}_1 \Delta t_1 = 0 + (1.2)(2.5)\,\hat{j} = 3.0\,\text{m/s}\,\hat{j}
$$

---

#### Segment 2

$$
\Delta \vec{r}_2 = (3.0)(2.5)\,\hat{j} + \tfrac{1}{2}(-1.2)(2.5^2)\,\hat{j}
$$

$$
\Delta \vec{r}_2 = (7.5 - 3.75)\,\hat{j} = 3.75\,\text{m}\,\hat{j}
$$

---

#### Total displacement

$$
\Delta \vec{r}_{\text{tot}} = 3.75\,\hat{j} + 3.75\,\hat{j} = 7.50\,\text{m}\,\hat{j}
$$

---

### Final Answer

The **magnitude of the elevator’s upward displacement** is

$$
\Delta r_{\text{tot}} = 7.50\, \text{m}
$$

---


# Solution: Elevator Problem (Scenario 1b)

---

### 1. Identify motion segments and knowns/unknowns

Again, we have **two segments of one-dimensional motion** with constant accelerations:

* **Segment 1:** The elevator starts from rest and accelerates upward until it has risen a certain distance.
* **Segment 2:** Immediately afterward, it decelerates uniformly until it comes to rest at the target floor.

**Knowns (Segment 1):** initial velocity (rest), acceleration, displacement.
**Knowns (Segment 2):** acceleration, final velocity (rest).
**Unknown (overall):** the total elapsed time of the trip.

---

### 2. Choose coordinate system

Let the **positive $\hat{j}$** direction be **upward** along the elevator shaft. All vertical quantities will be expressed relative to this axis.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Accelerating upward from rest”

| Variable         | Symbol             | Value                        | Notes                       |
| ---------------- | ------------------ | ---------------------------- | --------------------------- |
| Displacement     | $\Delta \vec{r}_1$ | $3.75\,\text{m}\,\hat{j}$    | Given                       |
| Initial velocity | $\vec{v}_{i1}$     | $0\,\text{m/s}\,\hat{j}$     | Implicit (starts from rest) |
| Final velocity   | $\vec{v}_{f1}$     | ?                            | To be determined            |
| Acceleration     | $\vec{a}_1$        | $1.2\,\text{m/s}^2\,\hat{j}$ | Given                       |
| Time interval    | $\Delta t_1$       | ?                            | To be determined            |

---

#### Segment 2 — “Slowing to a stop at the floor”

| Variable         | Symbol             | Value                          | Notes                |
| ---------------- | ------------------ | ------------------------------ | -------------------- |
| Displacement     | $\Delta \vec{r}_2$ | ?                              | To be determined     |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$        | Must match Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | $0\,\text{m/s}\,\hat{j}$       | Given                |
| Acceleration     | $\vec{a}_2$        | $1.2\,\text{m/s}^2 (-\hat{j})$ | Given                |
| Time interval    | $\Delta t_2$       | ?                              | To be determined     |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}=0$, displacement, and acceleration given, we use:

$$
v_{f1}^2 = v_{i1}^2 + 2a_1 \Delta r_1
$$

to find the final velocity, and then

$$
v_{f1} = v_{i1} + a_1 \Delta t_1
$$

to get $\Delta t_1$.

For Segment 2, with $v_{i2}=v_{f1}, v_{f2}=0,$ and acceleration known, we use:

$$
v_{f2} = v_{i2} + a_2 \Delta t_2
$$

to find $\Delta t_2$.

Finally,

$$
t_{\text{tot}} = \Delta t_1 + \Delta t_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
v_{f1}^2 = (0)^2 + 2(1.2)(3.75) = 9.0
$$

$$
v_{f1} = 3.0\,\text{m/s}\,\hat{j}
$$

Now,

$$
\Delta t_1 = \frac{v_{f1} - v_{i1}}{a_1} = \frac{3.0 - 0}{1.2} = 2.5\,\text{s}
$$

---

#### Segment 2

$$
v_{f2} = v_{i2} + a_2 \Delta t_2
$$

$$
0 = 3.0 + (-1.2)\Delta t_2
$$

$$
\Delta t_2 = \frac{3.0}{1.2} = 2.5\,\text{s}
$$

---

#### Total time

$$
t_{\text{tot}} = \Delta t_1 + \Delta t_2 = 2.5 + 2.5 = 5.0\,\text{s}
$$

---

### Final Answer

The **total travel time** for the elevator’s trip is

$$
t_{\text{tot}} = 5.0\,\text{s}
$$
---

# Solution: Train Problem (Scenario 2a)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The train accelerates uniformly from rest.
* **Segment 2:** The train continues at constant velocity (zero acceleration).

**Knowns (Segment 1):** initial velocity (rest), acceleration, and time interval.
**Knowns (Segment 2):** acceleration (zero), time interval.
**Unknown (overall):** the total displacement (magnitude of total forward distance traveled).

---

### 2. Choose coordinate system

Let the **positive $\hat{i}$** direction be **forward** along the straight track.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Accelerating forward from rest”

| Variable         | Symbol             | Value                         | Notes                               |
| ---------------- | ------------------ | ----------------------------- | ----------------------------------- |
| Displacement     | $\Delta \vec{r}_1$ | ? $ \hat{i}$                  | To be determined                    |
| Initial velocity | $\vec{v}_{i1}$     | $0\,\text{m/s}\,\hat{i}$      | Implicitly given (starts from rest) |
| Final velocity   | $\vec{v}_{f1}$     | ? $ \hat{i}$                  | To be determined                    |
| Acceleration     | $\vec{a}_1$        | $0.60\,\text{m/s}^2\,\hat{i}$ | Given                               |
| Time interval    | $\Delta t_1$       | $60\,\text{s}$                | Given                               |

---

#### Segment 2 — “Cruising at constant velocity”

| Variable         | Symbol             | Value                   | Notes                |
| ---------------- | ------------------ | ----------------------- | -------------------- |
| Displacement     | $\Delta \vec{r}_2$ | ? $ \hat{i}$            | To be determined     |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$ | Must match Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | equal to $\vec{v}_{i2}$ | Constant speed       |
| Acceleration     | $\vec{a}_2$        | $0\,\hat{i}$            | Given                |
| Time interval    | $\Delta t_2$       | $90\,\text{s}$          | Given                |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}=0, a_1, t_1$ known, we use the displacement equation:

$$
\Delta \vec{r}_1 = \vec{v}_{i1}\Delta t_1 + \tfrac{1}{2}\vec{a}_1(\Delta t_1)^2
$$

and final velocity:

$$
\vec{v}_{f1} = \vec{v}_{i1} + \vec{a}_1 \Delta t_1
$$

For Segment 2, with constant velocity, displacement is simply:

$$
\Delta \vec{r}_2 = \vec{v}_{i2}\,\Delta t_2
$$

Finally,

$$
\Delta \vec{r}_{\text{tot}} = \Delta \vec{r}_1 + \Delta \vec{r}_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
\Delta \vec{r}_1 = (0)(60)\hat{i} + \tfrac{1}{2}(0.60)(60^2)\hat{i}
$$

$$
\Delta \vec{r}_1 = (0 + 1080)\hat{i} = 1080\,\text{m}\,\hat{i}
$$

$$
\vec{v}_{f1} = 0 + (0.60)(60)\hat{i} = 36.0\,\text{m/s}\,\hat{i}
$$

---

#### Segment 2

$$
\Delta \vec{r}_2 = (36.0)(90)\hat{i} = 3240\,\text{m}\,\hat{i}
$$

---

#### Total displacement

$$
\Delta \vec{r}_{\text{tot}} = 1080\,\hat{i} + 3240\,\hat{i} = 4320\,\text{m}\,\hat{i}
$$

---

### Final Answer

The **magnitude of the train’s total forward displacement** is

$$
\Delta r_{\text{tot}} = 4320\,\text{m}
$$

---

# Solution: Train Problem (Scenario 2b)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The train accelerates uniformly from rest.
* **Segment 2:** The train moves at constant velocity after acceleration.

**Knowns (Segment 1):** displacement, initial velocity (rest), and acceleration.
**Knowns (Segment 2):** displacement and acceleration (zero).
**Unknown (overall):** the total elapsed time of travel.

---

### 2. Choose coordinate system

Let the **positive $\hat{i}$** direction be **forward** along the track.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Accelerating from rest”

| Variable         | Symbol             | Value                         | Notes                   |
| ---------------- | ------------------ | ----------------------------- | ----------------------- |
| Displacement     | $\Delta \vec{r}_1$ | $1080\,\text{m}\,\hat{i}$     | Given                   |
| Initial velocity | $\vec{v}_{i1}$     | $0\,\text{m/s}\,\hat{i}$      | Given implicitly (rest) |
| Final velocity   | $\vec{v}_{f1}$     | ?                             | To be determined        |
| Acceleration     | $\vec{a}_1$        | $0.60\,\text{m/s}^2\,\hat{i}$ | Given                   |
| Time interval    | $\Delta t_1$       | ?                             | To be determined        |

---

#### Segment 2 — “Cruising forward at constant speed”

| Variable         | Symbol             | Value                     | Notes                |
| ---------------- | ------------------ | ------------------------- | -------------------- |
| Displacement     | $\Delta \vec{r}_2$ | $3240\,\text{m}\,\hat{i}$ | Given                |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$   | Must match Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | equal to $\vec{v}_{i2}$   | Constant speed       |
| Acceleration     | $\vec{a}_2$        | $0\,\hat{i}$              | Given                |
| Time interval    | $\Delta t_2$       | ?                         | To be determined     |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}=0, a_1, \Delta r_1$ known, we use:

$$
v_{f1}^2 = v_{i1}^2 + 2a_1 \Delta r_1
$$

Then,

$$
\Delta t_1 = \frac{v_{f1} - v_{i1}}{a_1}
$$

For Segment 2, with constant velocity and displacement known:

$$
\Delta t_2 = \frac{\Delta r_2}{v_{i2}}
$$

Finally,

$$
t_{\text{tot}} = \Delta t_1 + \Delta t_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
v_{f1}^2 = 0^2 + 2(0.60)(1080) = 1296
$$

$$
v_{f1} = 36.0\,\text{m/s}\,\hat{i}
$$

Now,

$$
\Delta t_1 = \frac{36.0 - 0}{0.60} = 60.0\,\text{s}
$$

---

#### Segment 2

$$
\Delta t_2 = \frac{3240}{36.0} = 90.0\,\text{s}
$$

---

#### Total time

$$
t_{\text{tot}} = 60.0 + 90.0 = 150.0\,\text{s}
$$

---

### Final Answer

The **total travel time of the train** is

$$
t_{\text{tot}} = 150\,\text{s}
$$

---

# Solution: Rocket Sled Problem (Scenario 3b)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The sled accelerates under constant rocket thrust from rest.
* **Segment 2:** The sled decelerates uniformly under constant retro-thrust until it comes to rest.

**Knowns (Segment 1):** initial velocity (rest), acceleration, displacement.
**Knowns (Segment 2):** acceleration and final velocity (rest).
**Unknown (overall):** the total elapsed time of motion.

---

### 2. Choose coordinate system

Let the **positive $\hat{i}$** direction be **forward along the track**.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Boost forward from rest”

| Variable         | Symbol             | Value                         | Notes                   |
| ---------------- | ------------------ | ----------------------------- | ----------------------- |
| Displacement     | $\Delta \vec{r}_1$ | $150\,\text{m}\,\hat{i}$      | Given                   |
| Initial velocity | $\vec{v}_{i1}$     | $0\,\text{m/s}\,\hat{i}$      | Given implicitly (rest) |
| Final velocity   | $\vec{v}_{f1}$     | ?                             | To be determined        |
| Acceleration     | $\vec{a}_1$        | $12.0\,\text{m/s}^2\,\hat{i}$ | Given                   |
| Time interval    | $\Delta t_1$       | ?                             | To be determined        |

---

#### Segment 2 — “Retro-thrust braking”

| Variable         | Symbol             | Value                            | Notes                     |
| ---------------- | ------------------ | -------------------------------- | ------------------------- |
| Displacement     | $\Delta \vec{r}_2$ | ?                                | Not needed here           |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$          | Continuity with Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | $0\,\text{m/s}\,\hat{i}$         | Given (rest at end)       |
| Acceleration     | $\vec{a}_2$        | $15.0\,\text{m/s}^2\,(-\hat{i})$ | Given                     |
| Time interval    | $\Delta t_2$       | ?                                | To be determined          |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}=0, a_1, \Delta r_1$:

$$
v_{f1}^2 = v_{i1}^2 + 2a_1 \Delta r_1
$$

Then use

$$
\Delta t_1 = \frac{v_{f1} - v_{i1}}{a_1}
$$

For Segment 2, with $v_{i2}=v_{f1}, v_{f2}=0, a_2$:

$$
v_{f2} = v_{i2} + a_2 \Delta t_2
$$

Finally,

$$
t_{\text{tot}} = \Delta t_1 + \Delta t_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
v_{f1}^2 = 0^2 + 2(12.0)(150) = 3600
$$

$$
v_{f1} = 60.0\,\text{m/s}\,\hat{i}
$$

$$
\Delta t_1 = \frac{60.0 - 0}{12.0} = 5.0\,\text{s}
$$

---

#### Segment 2

$$
0 = 60.0 + (-15.0)\Delta t_2
$$

$$
\Delta t_2 = \frac{60.0}{15.0} = 4.0\,\text{s}
$$

---

#### Total time

$$
t_{\text{tot}} = 5.0 + 4.0 = 9.0\,\text{s}
$$

---

### Final Answer

The **total motion time of the rocket sled** is

$$
t_{\text{tot}} = 9.0\,\text{s}
$$

---

# Solution: Cyclist Problem (Scenario 4b)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The cyclist speeds up gently while coasting down a mild grade.
* **Segment 2:** The cyclist continues by applying a steady force on the pedals, giving stronger uniform acceleration.

**Knowns (Segment 1):** initial velocity, acceleration, displacement.
**Knowns (Segment 2):** acceleration and final velocity.
**Unknown (overall):** the total elapsed time of motion.

---

### 2. Choose coordinate system

Let the **positive $\hat{i}$** direction be **forward along the road**.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Mild speed-up down slope”

| Variable         | Symbol             | Value                         | Notes            |
| ---------------- | ------------------ | ----------------------------- | ---------------- |
| Displacement     | $\Delta \vec{r}_1$ | $75\,\text{m}\,\hat{i}$       | Given            |
| Initial velocity | $\vec{v}_{i1}$     | $5.0\,\text{m/s}\,\hat{i}$    | Given            |
| Final velocity   | $\vec{v}_{f1}$     | ?                             | To be determined |
| Acceleration     | $\vec{a}_1$        | $0.50\,\text{m/s}^2\,\hat{i}$ | Given            |
| Time interval    | $\Delta t_1$       | ?                             | To be determined |

---

#### Segment 2 — “Pushing harder”

| Variable         | Symbol             | Value                         | Notes                     |
| ---------------- | ------------------ | ----------------------------- | ------------------------- |
| Displacement     | $\Delta \vec{r}_2$ | ?                             | Not needed                |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$       | Continuity with Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | $0\,\text{m/s}\,\hat{i}$      | Given                     |
| Acceleration     | $\vec{a}_2$        | $-2.00\,\text{m/s}^2\,\hat{i}$ | Given                     |
| Time interval    | $\Delta t_2$       | ?                             | To be determined          |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}, a_1, \Delta r_1$ known:

$$
v_{f1}^2 = v_{i1}^2 + 2a_1 \Delta r_1
$$

and then

$$
\Delta t_1 = \frac{v_{f1} - v_{i1}}{a_1}
$$

For Segment 2, with $v_{i2}, v_{f2}, a_2$:

$$
\Delta t_2 = \frac{v_{f2} - v_{i2}}{a_2}
$$

Finally,

$$
t_{\text{tot}} = \Delta t_1 + \Delta t_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
v_{f1}^2 = (5.0)^2 + 2(0.50)(75) = 25 + 75 = 100
$$

$$
v_{f1} = 10.0\,\text{m/s}\,\hat{i}
$$

$$
\Delta t_1 = \frac{10.0 - 5.0}{0.50} = \frac{5.0}{0.50} = 10.0\,\text{s}
$$

---

#### Segment 2


$$
\Delta t_2 = \frac{0 - 10.0}{-2.00} = 5.0\,\text{s}
$$

---

#### Total time

$$
t_{\text{tot}} = 10.0 + 5.0 = 15.0\,\text{s}
$$

---

### Final Answer

The **total elapsed time of the cyclist’s motion** is

$$
t_{\text{tot}} = 15.0\,\text{s}
$$


---

# Solution: Cyclist Problem (Scenario 4c)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The cyclist accelerates moderately along a training stretch.
* **Segment 2:** The cyclist continues accelerating, but at a stronger rate, over a shorter distance.

**Knowns (Segment 1):** acceleration, time, displacement.
**Knowns (Segment 2):** acceleration and displacement.
**Unknown (overall):** the final velocity at the end of the second segment.

---

### 2. Choose coordinate system

Let the **positive $\hat{i}$** direction be **forward** along the road.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Moderate acceleration”

| Variable         | Symbol             | Value                         | Notes            |
| ---------------- | ------------------ | ----------------------------- | ---------------- |
| Displacement     | $\Delta \vec{r}_1$ | $75\,\text{m}\,\hat{i}$       | Given            |
| Initial velocity | $\vec{v}_{i1}$     | ?                             | To be determined |
| Final velocity   | $\vec{v}_{f1}$     | ?                             | To be determined |
| Acceleration     | $\vec{a}_1$        | $0.50\,\text{m/s}^2\,\hat{i}$ | Given            |
| Time interval    | $\Delta t_1$       | $10.0\,\text{s}$              | Given            |

---

#### Segment 2 — “Stronger acceleration”

| Variable         | Symbol             | Value                         | Notes                             |
| ---------------- | ------------------ | ----------------------------- | --------------------------------- |
| Displacement     | $\Delta \vec{r}_2$ | $25\,\text{m}\,\hat{i}$       | Given                             |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$       | Must match Segment 1              |
| Final velocity   | $\vec{v}_{f2}$     | ?                             | To be determined (overall target) |
| Acceleration     | $\vec{a}_2$        | $0.80\,\text{m/s}^2\,\hat{i}$ | Given                             |
| Time interval    | $\Delta t_2$       | ?                             | Not needed here                   |

---

### 4. Identify useful kinematic equations

For Segment 1, with $a_1, \Delta t_1$ known and initial velocity not stated, but displacement given, we can use:

$$
\Delta r_1 = v_{i1} \Delta t_1 + \tfrac{1}{2} a_1 (\Delta t_1)^2
$$

to solve for $v_{i1}$.
Then,

$$
v_{f1} = v_{i1} + a_1 \Delta t_1
$$

For Segment 2, with $v_{i2}, a_2, \Delta r_2$:

$$
v_{f2}^2 = v_{i2}^2 + 2a_2 \Delta r_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
75 = v_{i1}(10.0) + \tfrac{1}{2}(0.50)(10.0^2)
$$

$$
75 = 10v_{i1} + 25
$$

$$
10v_{i1} = 50 \quad \Rightarrow \quad v_{i1} = 5.0\,\text{m/s}\,\hat{i}
$$

Now,

$$
v_{f1} = 5.0 + (0.50)(10.0) = 10.0\,\text{m/s}\,\hat{i}
$$

Thus, $\vec{v}_{i2} = 10.0\,\text{m/s}\,\hat{i}$.

---

#### Segment 2

$$
v_{f2}^2 = (10.0)^2 + 2(0.80)(25)
$$

$$
v_{f2}^2 = 100 + 40 = 140
$$

$$
v_{f2} = \sqrt{140} \approx 11.8\,\text{m/s}\,\hat{i}
$$

---

### Final Answer

The **final speed of the cyclist** is

$$
v_{f2} \approx 11.8\,\text{m/s}
$$

---
Alright — let’s move on with **Scenario P1 (Package drop: total displacement).**

---

# Solution: Package Drop Problem (Scenario P1)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The package freefalls under gravity before the parachute deploys.
* **Segment 2:** Once the parachute deploys, the package decelerates uniformly until it comes to rest just as it touches the ground.

**Knowns (Segment 1):** initial velocity (rest), acceleration, and time interval.
**Knowns (Segment 2):** acceleration and final velocity (rest).
**Unknown (overall):** the total vertical displacement (magnitude of descent).

---

### 2. Choose coordinate system

Let the **positive $\hat{j}$** direction be **downward**, aligned with gravity and the package’s motion.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Freefall before chute deploys”

| Variable         | Symbol             | Value                        | Notes                   |
| ---------------- | ------------------ | ---------------------------- | ----------------------- |
| Displacement     | $\Delta \vec{r}_1$ | ? $ \hat{j}$                 | To be determined        |
| Initial velocity | $\vec{v}_{i1}$     | $0\,\text{m/s}\,\hat{j}$     | Given (rest at release) |
| Final velocity   | $\vec{v}_{f1}$     | ?                            | To be determined        |
| Acceleration     | $\vec{a}_1$        | $9.8\,\text{m/s}^2\,\hat{j}$ | Given                   |
| Time interval    | $\Delta t_1$       | $5.0\,\text{s}$              | Given                   |

---

#### Segment 2 — “Decelerating under parachute”

| Variable         | Symbol             | Value                           | Notes                     |
| ---------------- | ------------------ | ------------------------------- | ------------------------- |
| Displacement     | $\Delta \vec{r}_2$ | ? $ \hat{j}$                    | To be determined          |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$         | Continuity with Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | $0\,\text{m/s}\,\hat{j}$        | Given                     |
| Acceleration     | $\vec{a}_2$        | $4.0\,\text{m/s}^2\,(-\hat{j})$ | Given                     |
| Time interval    | $\Delta t_2$       | ?                               | To be determined          |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}, a_1, t_1$:

$$
\Delta r_1 = v_{i1} \Delta t_1 + \tfrac{1}{2} a_1 (\Delta t_1)^2
$$

$$
v_{f1} = v_{i1} + a_1 \Delta t_1
$$

For Segment 2, with $v_{i2}, v_{f2}, a_2$:

$$
\Delta r_2 = \frac{v_{f2}^2 - v_{i2}^2}{2a_2}
$$

Finally,

$$
\Delta r_{\text{tot}} = \Delta r_1 + \Delta r_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
\Delta r_1 = (0)(5.0) + \tfrac{1}{2}(9.8)(5.0^2)
$$

$$
\Delta r_1 = 122.5\,\text{m}\,\hat{j}
$$

$$
v_{f1} = 0 + (9.8)(5.0) = 49.0\,\text{m/s}\,\hat{j}
$$

---

#### Segment 2

$$
\Delta r_2 = \frac{(0)^2 - (49.0)^2}{2(-4.0)}
$$

$$
\Delta r_2 = \frac{-2401}{-8} = 300.1\,\text{m}\,\hat{j}
$$

---

#### Total displacement

$$
\Delta r_{\text{tot}} = 122.5 + 300.1 = 422.6\,\text{m}\,\hat{j}
$$

---

### Final Answer

The **magnitude of the package’s vertical displacement** is

$$
\Delta r_{\text{tot}} \approx 423\,\text{m}
$$

---
Alright — let’s continue with **Scenario P2 (Package drop: required parachute deceleration).**

---

# Solution: Package Drop Problem (Scenario P2)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The package freefalls under gravity before the parachute opens.
* **Segment 2:** Once the parachute deploys, it slows uniformly until the package comes to rest at ground level.

**Knowns (Segment 1):** initial velocity (rest), acceleration, and displacement.
**Knowns (Segment 2):** time interval and final velocity (rest).
**Unknown (overall):** the constant deceleration required from the parachute in order to stop the package in time.

---

### 2. Choose coordinate system

Let the **positive $\hat{j}$** direction be **downward**, aligned with the package’s motion.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Freefall before chute opens”

| Variable         | Symbol             | Value                        | Notes            |
| ---------------- | ------------------ | ---------------------------- | ---------------- |
| Displacement     | $\Delta \vec{r}_1$ | $245\,\text{m}\,\hat{j}$     | Given            |
| Initial velocity | $\vec{v}_{i1}$     | $0\,\text{m/s}\,\hat{j}$     | Given            |
| Final velocity   | $\vec{v}_{f1}$     | ?                            | To be determined |
| Acceleration     | $\vec{a}_1$        | $9.8\,\text{m/s}^2\,\hat{j}$ | Given            |
| Time interval    | $\Delta t_1$       | ?                            | Not needed here  |

---

#### Segment 2 — “Parachute braking”

| Variable         | Symbol             | Value                    | Notes                     |
| ---------------- | ------------------ | ------------------------ | ------------------------- |
| Displacement     | $\Delta \vec{r}_2$ | ?                        | Not needed                |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$  | Continuity with Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | $0\,\text{m/s}\,\hat{j}$ | Given                     |
| Acceleration     | $\vec{a}_2$        | ?                        | To be determined          |
| Time interval    | $\Delta t_2$       | $15.0\,\text{s}$         | Given                     |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}, a_1, \Delta r_1$:

$$
v_{f1}^2 = v_{i1}^2 + 2a_1 \Delta r_1
$$

This gives the velocity just before the parachute opens.

For Segment 2, with $v_{i2}, v_{f2}, \Delta t_2$:

$$
a_2 = \frac{v_{f2} - v_{i2}}{\Delta t_2}
$$

---

### 5. Algebraic solution

#### Segment 1

$$
v_{f1}^2 = (0)^2 + 2(9.8)(245) = 4802
$$

$$
v_{f1} = 69.3\,\text{m/s}\,\hat{j}
$$

Thus, $\vec{v}_{i2} = 69.3\,\text{m/s}\,\hat{j}$.

---

#### Segment 2

$$
a_2 = \frac{0 - 69.3}{15.0}
$$

$$
a_2 = -4.62\,\text{m/s}^2\,\hat{j}
$$

---

### Final Answer

The parachute must provide a **deceleration of magnitude**

$$
|\vec{a}_2| \approx 4.62\,\text{m/s}^2
$$

---
Alright — let’s work through **Scenario P3 (Package drop: total time).**

---

# Solution: Package Drop Problem (Scenario P3)

---

### 1. Identify motion segments and knowns/unknowns

We have **two segments of one-dimensional motion**:

* **Segment 1:** The package freefalls under gravity after being released from the drone.
* **Segment 2:** Once the parachute deploys, the package slows uniformly while descending further until reaching the ground.

**Knowns (Segment 1):** initial velocity (rest), acceleration, and displacement.
**Knowns (Segment 2):** acceleration and displacement.
**Unknown (overall):** the total elapsed time from release to landing.

---

### 2. Choose coordinate system

Let the **positive $\hat{j}$** direction be **downward**, aligned with gravity and the package’s motion.

---

### 3. Tables of kinematic variables

#### Segment 1 — “Freefall before chute deploys”

| Variable         | Symbol             | Value                        | Notes            |
| ---------------- | ------------------ | ---------------------------- | ---------------- |
| Displacement     | $\Delta \vec{r}_1$ | $490\,\text{m}\,\hat{j}$     | Given            |
| Initial velocity | $\vec{v}_{i1}$     | $0\,\text{m/s}\,\hat{j}$     | Given            |
| Final velocity   | $\vec{v}_{f1}$     | ?                            | To be determined |
| Acceleration     | $\vec{a}_1$        | $9.8\,\text{m/s}^2\,\hat{j}$ | Given            |
| Time interval    | $\Delta t_1$       | ?                            | To be determined |

---

#### Segment 2 — “Parachute braking”

| Variable         | Symbol             | Value                           | Notes                     |
| ---------------- | ------------------ | ------------------------------- | ------------------------- |
| Displacement     | $\Delta \vec{r}_2$ | $200\,\text{m}\,\hat{j}$        | Given                     |
| Initial velocity | $\vec{v}_{i2}$     | equal to $\vec{v}_{f1}$         | Continuity with Segment 1 |
| Final velocity   | $\vec{v}_{f2}$     | ?                               | To be determined          |
| Acceleration     | $\vec{a}_2$        | $2.5\,\text{m/s}^2\,(-\hat{j})$ | Given                     |
| Time interval    | $\Delta t_2$       | ?                               | To be determined          |

---

### 4. Identify useful kinematic equations

For Segment 1, with $v_{i1}, a_1, \Delta r_1$:

$$
v_{f1}^2 = v_{i1}^2 + 2a_1 \Delta r_1
$$

and

$$
\Delta t_1 = \frac{v_{f1} - v_{i1}}{a_1}
$$

For Segment 2, with $v_{i2}, a_2, \Delta r_2$:

$$
v_{f2}^2 = v_{i2}^2 + 2a_2 \Delta r_2
$$

and

$$
\Delta t_2 = \frac{v_{f2} - v_{i2}}{a_2}
$$

Finally,

$$
t_{\text{tot}} = \Delta t_1 + \Delta t_2
$$

---

### 5. Algebraic solution

#### Segment 1

$$
v_{f1}^2 = 0^2 + 2(9.8)(490) = 9604
$$

$$
v_{f1} = 98.0\,\text{m/s}\,\hat{j}
$$

$$
\Delta t_1 = \frac{98.0 - 0}{9.8} = 10.0\,\text{s}
$$

---

#### Segment 2

$$
v_{f2}^2 = (98.0)^2 + 2(-2.5)(200)
$$

$$
v_{f2}^2 = 9604 - 1000 = 8604
$$

$$
v_{f2} = 92.7\,\text{m/s}\,\hat{j}
$$

$$
\Delta t_2 = \frac{92.7 - 98.0}{-2.5} = \frac{-5.3}{-2.5} \approx 2.12\,\text{s}
$$

---

#### Total time

$$
t_{\text{tot}} = 10.0 + 2.12 = 12.1\,\text{s}
$$

---

### Final Answer

The **total time from release to landing** is

$$
t_{\text{tot}} \approx 12.1\,\text{s}
$$

---
