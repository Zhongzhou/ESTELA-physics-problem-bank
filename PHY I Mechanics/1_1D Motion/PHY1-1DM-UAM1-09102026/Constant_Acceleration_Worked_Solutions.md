# Straight-Line Motion with Constant Acceleration: Worked Solutions

These 17 solutions follow the five-part format: identify the motion segment and requested quantity, organize the five kinematic variables, select an equation, solve algebraically, and substitute numerical values with units.

Each problem defines its own positive axis. Displacement, velocity, and acceleration are vectors; elapsed time and vector magnitudes are scalars. Unit vectors have magnitude one. Distance equals displacement magnitude here because none of the selected segments includes a reversal. For Earth free fall, the solutions use \(g=9.81\,\mathrm{m/s^2}\). Numerical values are carried through with guard digits and rounded at the end as requested in each problem.

Equations involving squared velocities are written for signed components, such as \(v_{fx}^{\,2}=v_{ix}^{\,2}+2a_x\Delta x\); the corresponding vector is then reconstructed with its unit vector. No equation divides by a vector.

---

## Problem 1: Pulling away from a traffic light

**Problem statement**

A driver is waiting at a red light on a straight, level road beside a public library. When the light turns green, the car pulls away from rest and travels 36.0 m during the next 6.0 s. Its speed increases at a constant rate throughout this stretch. How fast is the car moving at the end of those 6.0 s? Report the speed in meters per second to **two significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The car begins moving from rest after the light turns green.
- **Final event:** The car completes the next 6.0 s of motion, having traveled 36.0 m.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The car starts from rest and travels 36.0 m in 6.0 s.

Choose the positive \(x\)-axis along the car's forward motion, with unit vector \(\hat{\mathbf{i}}\).

The requested ending speed is the magnitude of the final instantaneous velocity vector, \(|\vec{v}_f|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((36.0\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((0\,\mathrm{m/s})\hat{\mathbf{i}}=\vec{0}\) | Implicit: the car starts from rest. |
| Final instantaneous velocity | \(\vec{v}_f\) | **?** | To be solved for. The question requests its magnitude. |
| Acceleration | \(\vec{a}\) | Not given | Constant; numerical value not given or needed. |
| Time interval | \(\Delta t\) | \(6.0\,\mathrm{s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know \(\Delta\vec{r}\), \(\vec{v}_i\), and \(\Delta t\), and need \(\vec{v}_f\). The average-velocity equation avoids the unknown acceleration:

\[
\Delta\vec{r}=\frac{\vec{v}_i+\vec{v}_f}{2}\,\Delta t.
\]

**4. Solve algebraically for the unknown**

Multiply by 2, divide by the scalar \(\Delta t\), and subtract \(\vec{v}_i\):

\[
\begin{aligned}
\Delta\vec{r}&=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t\\[3pt]
2\Delta\vec{r}&=(\vec{v}_i+\vec{v}_f)\Delta t\\[3pt]
\frac{2\Delta\vec{r}}{\Delta t}&=\vec{v}_i+\vec{v}_f\\[3pt]
\vec{v}_f&=\frac{2\Delta\vec{r}}{\Delta t}-\vec{v}_i.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\vec{v}_f&=\frac{2(36.0\,\mathrm{m})\hat{\mathbf{i}}}{6.0\,\mathrm{s}}-(0\,\mathrm{m/s})\hat{\mathbf{i}}\\[3pt]
&=(12\,\mathrm{m/s})\hat{\mathbf{i}}.
\end{aligned}
\]

The velocity points forward. Taking its magnitude removes the direction from the requested speed.

\[
|\vec{v}_f|=\boxed{12\,\mathrm{m/s}}
\]

**Rounding:** Two significant figures.

---

## Problem 2: A smooth stop for a city bus

**Problem statement**

A city bus is approaching a stop on a straight, level street, where passengers are waiting to board. The bus is traveling at 10.0 m/s when the driver begins braking. To make the stop comfortable for the standing passengers, the driver reduces the bus's speed at a constant rate until it comes to rest, traveling 35.0 m after braking begins. What is the magnitude of the bus's acceleration during braking? Report your answer in \(\mathrm{m/s^2}\) to **three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The driver begins braking while the bus is moving at 10.0 m/s.
- **Final event:** The bus first comes to rest, 35.0 m farther along the street.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The bus enters the braking segment at 10.0 m/s, travels 35.0 m, and stops.

Choose the positive \(x\)-axis along the bus's forward motion, with unit vector \(\hat{\mathbf{i}}\).

The requested quantity is the magnitude of the acceleration vector, \(|\vec{a}|\). We will determine the vector and then take its magnitude.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((35.0\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((10.0\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((0\,\mathrm{m/s})\hat{\mathbf{i}}=\vec{0}\) | Implicit: the bus comes to rest. |
| Acceleration | \(\vec{a}\) | **?** | To be solved for. The question requests its magnitude. |
| Time interval | \(\Delta t\) | Not given | Not required for this calculation. |

**3. Select a kinematic equation**

We know the displacement and both endpoint velocities, but not the time. Use the time-independent kinematic equation for the signed \(x\)-components. Here \(\vec{v}_i=v_{ix}\hat{\mathbf{i}}\), \(\vec{v}_f=v_{fx}\hat{\mathbf{i}}\), and \(\Delta\vec{r}=\Delta x\hat{\mathbf{i}}\):

\[
v_{fx}^{\,2}=v_{ix}^{\,2}+2a_x\Delta x.
\]

**4. Solve algebraically for the unknown**

Subtract \(v_{ix}^{\,2}\), divide by \(2\Delta x\), and reconstruct the acceleration vector:

\[
\begin{aligned}
v_{fx}^{\,2}&=v_{ix}^{\,2}+2a_x\Delta x\\[3pt]
v_{fx}^{\,2}-v_{ix}^{\,2}&=2a_x\Delta x\\[3pt]
a_x&=\frac{v_{fx}^{\,2}-v_{ix}^{\,2}}{2\Delta x}\\[3pt]
\vec{a}&=\left(\frac{v_{fx}^{\,2}-v_{ix}^{\,2}}{2\Delta x}\right)\hat{\mathbf{i}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
a_x&=\frac{(0\,\mathrm{m/s})^2-(10.0\,\mathrm{m/s})^2}{2(35.0\,\mathrm{m})}\\[3pt]
&=-1.42857\ldots\,\mathrm{m/s^2}\\[3pt]
\vec{a}&=(-1.42857\ldots\,\mathrm{m/s^2})\hat{\mathbf{i}}.
\end{aligned}
\]

The negative component places the acceleration opposite the bus's motion, as expected while braking.

\[
|\vec{a}|=\boxed{1.43\,\mathrm{m/s^2}}
\]

**Rounding:** Three significant figures.

---

## Problem 3: A commuter train leaving the station area

**Problem statement**

A commuter train has already left a downtown station and is entering a straight section of track. A technician reviewing the train's motion records a speed of 8.0 m/s at the beginning of a 20.0 s interval and 16.0 m/s at its end. Throughout this interval, the train's speed increases at a constant rate. How far does the train travel during those 20.0 s? Report the distance in **meters, rounded to the nearest meter**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The recorded 20.0 s interval begins, with the train already moving at 8.0 m/s.
- **Final event:** That interval ends, with the train moving at 16.0 m/s.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The two endpoint speeds are 8.0 m/s and 16.0 m/s, and the interval lasts 20.0 s.

Choose the positive \(x\)-axis along the train's forward motion, with unit vector \(\hat{\mathbf{i}}\).

The motion does not reverse within this segment, so the requested distance is the magnitude of the displacement vector, \(|\Delta\vec{r}|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | **?** | To be solved for. The question requests its magnitude. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((8.0\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((16.0\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Acceleration | \(\vec{a}\) | Not given | Constant; numerical value not given or needed. |
| Time interval | \(\Delta t\) | \(20.0\,\mathrm{s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know both endpoint velocity vectors and the elapsed time. For constant acceleration, the average velocity is the arithmetic mean of the endpoint velocities:

\[
\frac{\Delta\vec{r}}{\Delta t}=\frac{\vec{v}_i+\vec{v}_f}{2}.
\]

**4. Solve algebraically for the unknown**

Multiply both sides by \(\Delta t\) to isolate the displacement vector:

\[
\begin{aligned}
\frac{\Delta\vec{r}}{\Delta t}&=\frac{\vec{v}_i+\vec{v}_f}{2}\\[3pt]
\Delta\vec{r}&=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\Delta\vec{r}&=\frac{(8.0\,\mathrm{m/s})\hat{\mathbf{i}}+(16.0\,\mathrm{m/s})\hat{\mathbf{i}}}{2}(20.0\,\mathrm{s})\\[3pt]
&=(240\,\mathrm{m})\hat{\mathbf{i}}.
\end{aligned}
\]

The train travels forward throughout the interval, so distance equals displacement magnitude.

\[
|\Delta\vec{r}|=\boxed{240\,\mathrm{m}}
\]

**Rounding:** The nearest meter.

---

## Problem 4: An airplane between runway markers

**Problem statement**

During a takeoff roll, an airplane passes a painted runway marker while traveling at 45.0 m/s. It continues along the straight runway and passes another marker 250 m farther ahead 5.0 s later. For this short portion of the takeoff roll, assume that its speed increases at a constant rate and that the airplane remains on the runway. How fast is the airplane moving as it passes the second marker? Report the speed in **meters per second, rounded to the nearest whole number**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The airplane passes the first runway marker at 45.0 m/s.
- **Final event:** It passes the second marker, 250 m farther along the runway, 5.0 s later.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The airplane enters the measured segment at 45.0 m/s and covers 250 m in 5.0 s.

Choose the positive \(x\)-axis forward along the runway, with unit vector \(\hat{\mathbf{i}}\).

The requested ending speed is the magnitude of the final instantaneous velocity vector, \(|\vec{v}_f|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((250\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((45.0\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | **?** | To be solved for. The question requests its magnitude. |
| Acceleration | \(\vec{a}\) | Not given | Constant; numerical value not given or needed. |
| Time interval | \(\Delta t\) | \(5.0\,\mathrm{s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know \(\Delta\vec{r}\), \(\vec{v}_i\), and \(\Delta t\), and need \(\vec{v}_f\). The average-velocity equation avoids the unknown acceleration:

\[
\Delta\vec{r}=\frac{\vec{v}_i+\vec{v}_f}{2}\,\Delta t.
\]

**4. Solve algebraically for the unknown**

Multiply by 2, divide by the scalar \(\Delta t\), and subtract \(\vec{v}_i\):

\[
\begin{aligned}
\Delta\vec{r}&=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t\\[3pt]
2\Delta\vec{r}&=(\vec{v}_i+\vec{v}_f)\Delta t\\[3pt]
\frac{2\Delta\vec{r}}{\Delta t}&=\vec{v}_i+\vec{v}_f\\[3pt]
\vec{v}_f&=\frac{2\Delta\vec{r}}{\Delta t}-\vec{v}_i.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\vec{v}_f&=\frac{2(250\,\mathrm{m})\hat{\mathbf{i}}}{5.0\,\mathrm{s}}-(45.0\,\mathrm{m/s})\hat{\mathbf{i}}\\[3pt]
&=(100-45.0)\,\mathrm{m/s}\;\hat{\mathbf{i}}\\[3pt]
&=(55\,\mathrm{m/s})\hat{\mathbf{i}}.
\end{aligned}
\]

This is the velocity at the second marker. The question requests its magnitude.

\[
|\vec{v}_f|=\boxed{55\,\mathrm{m/s}}
\]

**Rounding:** The nearest whole meter per second.

---

## Problem 5: A glass elevator rising through an atrium

**Problem statement**

A maintenance technician is checking the gentle startup of a glass passenger elevator in a museum atrium. The elevator leaves a lower landing from rest and rises vertically, increasing its speed at a constant rate. After rising 6.0 m, it is moving upward at 1.50 m/s. How much time passes between leaving the landing and reaching that height? Report the time in seconds to **two significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The elevator leaves the lower landing from rest.
- **Final event:** The elevator has risen 6.0 m and is moving upward at 1.50 m/s.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The elevator starts from rest, rises 6.0 m, and reaches an upward speed of 1.50 m/s.

Choose the positive \(y\)-axis vertically upward, with unit vector \(\hat{\mathbf{j}}\).

The requested quantity is the elapsed time \(\Delta t\), which is a positive scalar.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((6.0\,\mathrm{m})\hat{\mathbf{j}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((0\,\mathrm{m/s})\hat{\mathbf{j}}=\vec{0}\) | Implicit: the elevator leaves from rest. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((1.50\,\mathrm{m/s})\hat{\mathbf{j}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Acceleration | \(\vec{a}\) | Not given | Constant; numerical value not given or needed. |
| Time interval | \(\Delta t\) | **?** | To be solved for. |

**3. Select a kinematic equation**

We know the displacement and both endpoint velocities. The average-velocity equation contains the unknown time and does not require acceleration:

\[
\Delta\vec{r}=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t.
\]

**4. Solve algebraically for the unknown**

Equate the \(y\)-components, then isolate \(\Delta t\). This divides scalar components, not vectors:

\[
\begin{aligned}
\Delta\vec{r}&=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t\\[3pt]
\Delta y&=\frac{v_{iy}+v_{fy}}{2}\Delta t\\[3pt]
2\Delta y&=(v_{iy}+v_{fy})\Delta t\\[3pt]
\Delta t&=\frac{2\Delta y}{v_{iy}+v_{fy}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\Delta t&=\frac{2(6.0\,\mathrm{m})}{0\,\mathrm{m/s}+1.50\,\mathrm{m/s}}\\[3pt]
&=8.0\,\mathrm{s}.
\end{aligned}
\]

The elapsed time is a scalar and has no unit vector.

\[
\Delta t=\boxed{8.0\,\mathrm{s}}
\]

**Rounding:** Two significant figures.

---

## Problem 6: Backing a fragile load into position

**Problem statement**

A warehouse operator is backing a forklift carrying a crated laboratory instrument along a straight, level aisle. The forklift is moving backward at 1.5 m/s when the operator begins braking. To avoid jarring the load, the operator reduces its speed at a constant rate and brings it to rest after it travels another 4.0 m backward. What is the magnitude of the forklift's acceleration while it is braking? Report your answer in \(\mathrm{m/s^2}\) to **two significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The operator begins braking while the forklift is backing at 1.5 m/s.
- **Final event:** The forklift first comes to rest after traveling another 4.0 m backward.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The forklift enters the braking segment at 1.5 m/s, moves 4.0 m backward, and stops.

Choose the positive \(x\)-axis along the forklift's backward travel down the aisle, with unit vector \(\hat{\mathbf{i}}\).

The requested quantity is the magnitude of the acceleration vector, \(|\vec{a}|\). We will determine the vector and then take its magnitude.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((4.0\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((1.5\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((0\,\mathrm{m/s})\hat{\mathbf{i}}=\vec{0}\) | Implicit: the forklift comes to rest. |
| Acceleration | \(\vec{a}\) | **?** | To be solved for. The question requests its magnitude. |
| Time interval | \(\Delta t\) | Not given | Not required for this calculation. |

**3. Select a kinematic equation**

We know the displacement and both endpoint velocities, but not the time. Use the time-independent kinematic equation for the signed \(x\)-components. Here \(\vec{v}_i=v_{ix}\hat{\mathbf{i}}\), \(\vec{v}_f=v_{fx}\hat{\mathbf{i}}\), and \(\Delta\vec{r}=\Delta x\hat{\mathbf{i}}\):

\[
v_{fx}^{\,2}=v_{ix}^{\,2}+2a_x\Delta x.
\]

**4. Solve algebraically for the unknown**

Subtract \(v_{ix}^{\,2}\), divide by \(2\Delta x\), and reconstruct the acceleration vector:

\[
\begin{aligned}
v_{fx}^{\,2}&=v_{ix}^{\,2}+2a_x\Delta x\\[3pt]
v_{fx}^{\,2}-v_{ix}^{\,2}&=2a_x\Delta x\\[3pt]
a_x&=\frac{v_{fx}^{\,2}-v_{ix}^{\,2}}{2\Delta x}\\[3pt]
\vec{a}&=\left(\frac{v_{fx}^{\,2}-v_{ix}^{\,2}}{2\Delta x}\right)\hat{\mathbf{i}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
a_x&=\frac{(0\,\mathrm{m/s})^2-(1.5\,\mathrm{m/s})^2}{2(4.0\,\mathrm{m})}\\[3pt]
&=-0.28125\,\mathrm{m/s^2}\\[3pt]
\vec{a}&=(-0.28125\,\mathrm{m/s^2})\hat{\mathbf{i}}.
\end{aligned}
\]

Here the positive axis points backward along the forklift's travel. The negative acceleration therefore points forward, opposite its backward motion.

\[
|\vec{a}|=\boxed{0.28\,\mathrm{m/s^2}}
\]

**Rounding:** Two significant figures.

---

## Problem 7: Coasting up a skateboard ramp

**Problem statement**

A skateboarder rolls onto the bottom of a straight uphill ramp at a skatepark and continues upward without pushing. The ramp has a uniform slope, and the skateboarder's speed decreases at a constant rate. Starting from the moment the skateboarder enters the ramp, the skateboard travels 3.00 m along the incline and reaches a momentary stop 2.0 s later. What is the magnitude of the skateboarder's acceleration during this uphill climb? Report your answer in \(\mathrm{m/s^2}\) to **two significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The moving skateboarder enters the bottom of the uphill ramp.
- **Final event:** The skateboarder reaches the first momentary stop, after traveling 3.00 m along the ramp in 2.0 s.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The uphill travel is 3.00 m, the elapsed time is 2.0 s, and the ending velocity is zero.

Choose the positive \(x\)-axis uphill along the straight ramp, with unit vector \(\hat{\mathbf{i}}\).

The requested quantity is the magnitude of the acceleration vector, \(|\vec{a}|\). We will determine the vector and then take its magnitude.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((3.00\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | Not given | Not required for this calculation. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((0\,\mathrm{m/s})\hat{\mathbf{i}}=\vec{0}\) | Implicit: the skateboarder reaches a momentary stop. |
| Acceleration | \(\vec{a}\) | **?** | To be solved for. The question requests its magnitude. |
| Time interval | \(\Delta t\) | \(2.0\,\mathrm{s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know displacement, final velocity, and elapsed time. The final-velocity form avoids the unknown entering velocity:

\[
\Delta\vec{r}=\vec{v}_f\Delta t-\frac12\vec{a}(\Delta t)^2.
\]

**4. Solve algebraically for the unknown**

This form follows from the usual displacement equation by substituting \(\vec{v}_i=\vec{v}_f-\vec{a}\Delta t\). Then isolate \(\vec{a}\):

\[
\begin{aligned}
\Delta\vec{r}&=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2\\[3pt]
&=(\vec{v}_f-\vec{a}\Delta t)\Delta t+\frac12\vec{a}(\Delta t)^2\\[3pt]
&=\vec{v}_f\Delta t-\frac12\vec{a}(\Delta t)^2\\[3pt]
\frac12\vec{a}(\Delta t)^2&=\vec{v}_f\Delta t-\Delta\vec{r}\\[3pt]
\vec{a}&=\frac{2(\vec{v}_f\Delta t-\Delta\vec{r})}{(\Delta t)^2}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\vec{a}&=\frac{2\left[(0\,\mathrm{m/s})\hat{\mathbf{i}}(2.0\,\mathrm{s})-(3.00\,\mathrm{m})\hat{\mathbf{i}}\right]}{(2.0\,\mathrm{s})^2}\\[3pt]
&=(-1.5\,\mathrm{m/s^2})\hat{\mathbf{i}}.
\end{aligned}
\]

Because the positive axis points uphill, the negative acceleration points downhill. The segment ends at the first stop, before any downhill return.

\[
|\vec{a}|=\boxed{1.5\,\mathrm{m/s^2}}
\]

**Rounding:** Two significant figures.

---

## Problem 8: Testing a downhill ski trail

**Problem statement**

A skier testing a freshly groomed trail enters a straight, evenly sloping downhill section at 4.0 m/s. During the next 5.0 s, the skier neither pushes nor brakes. The motion over this stretch has a constant acceleration of \(1.2\,\mathrm{m/s^2}\), directed down the slope. How fast is the skier moving at the end of those 5.0 s? Report the speed in **meters per second to one decimal place**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The skier enters the selected downhill section at 4.0 m/s.
- **Final event:** The skier has traveled down that straight section for 5.0 s.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The skier enters at 4.0 m/s and has a downhill acceleration of \(1.2\,\mathrm{m/s^2}\) for 5.0 s.

Choose the positive \(x\)-axis downhill along the straight ski trail, with unit vector \(\hat{\mathbf{i}}\).

The requested ending speed is the magnitude of the final instantaneous velocity vector, \(|\vec{v}_f|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | Not given | Not required for this calculation. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((4.0\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | **?** | To be solved for. The question requests its magnitude. |
| Acceleration | \(\vec{a}\) | \((1.2\,\mathrm{m/s^2})\hat{\mathbf{i}}\) | Explicitly given in magnitude and direction. |
| Time interval | \(\Delta t\) | \(5.0\,\mathrm{s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know the entering velocity, acceleration, and elapsed time. Use the constant-acceleration relation between velocity change and time:

\[
\vec{a}=\frac{\vec{v}_f-\vec{v}_i}{\Delta t}.
\]

**4. Solve algebraically for the unknown**

Multiply by \(\Delta t\), then add \(\vec{v}_i\):

\[
\begin{aligned}
\vec{a}&=\frac{\vec{v}_f-\vec{v}_i}{\Delta t}\\[3pt]
\vec{a}\Delta t&=\vec{v}_f-\vec{v}_i\\[3pt]
\vec{v}_f&=\vec{v}_i+\vec{a}\Delta t.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\vec{v}_f&=(4.0\,\mathrm{m/s})\hat{\mathbf{i}}+(1.2\,\mathrm{m/s^2})\hat{\mathbf{i}}(5.0\,\mathrm{s})\\[3pt]
&=(4.0+6.0)\,\mathrm{m/s}\;\hat{\mathbf{i}}\\[3pt]
&=(10.0\,\mathrm{m/s})\hat{\mathbf{i}}.
\end{aligned}
\]

The velocity points downhill, along the chosen positive axis. Its magnitude is the requested speed.

\[
|\vec{v}_f|=\boxed{10.0\,\mathrm{m/s}}
\]

**Rounding:** One decimal place.

---

## Problem 9: A parcel on a sorting chute

**Problem statement**

At a parcel-sorting station, a worker holds a small box motionless at the upper end of a straight, inclined delivery chute. The worker releases the box without pushing it, and it slides 1.80 m along the chute to the lower end in 1.20 s. Assume that its speed increases at a constant rate throughout the slide. What is the magnitude of the box's acceleration as it moves down the chute? Report your answer in \(\mathrm{m/s^2}\) to **three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The worker releases the stationary box without pushing it.
- **Final event:** The box reaches the lower end of the chute, having slid 1.80 m in 1.20 s.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The box starts from rest and slides 1.80 m along the chute in 1.20 s.

Choose the positive \(x\)-axis downward along the inclined chute, with unit vector \(\hat{\mathbf{i}}\).

The requested quantity is the magnitude of the acceleration vector, \(|\vec{a}|\). We will determine the vector and then take its magnitude.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((1.80\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((0\,\mathrm{m/s})\hat{\mathbf{i}}=\vec{0}\) | Implicit: the box is motionless and released without a push. |
| Final instantaneous velocity | \(\vec{v}_f\) | Not given | Not required for this calculation. |
| Acceleration | \(\vec{a}\) | **?** | To be solved for. The question requests its magnitude. |
| Time interval | \(\Delta t\) | \(1.20\,\mathrm{s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know the displacement, entering velocity, and elapsed time. Use the displacement-time equation, which does not require the ending velocity:

\[
\Delta\vec{r}=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2.
\]

**4. Solve algebraically for the unknown**

Subtract \(\vec{v}_i\Delta t\), multiply by 2, and divide by \((\Delta t)^2\):

\[
\begin{aligned}
\Delta\vec{r}&=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2\\[3pt]
\Delta\vec{r}-\vec{v}_i\Delta t&=\frac12\vec{a}(\Delta t)^2\\[3pt]
\vec{a}&=\frac{2(\Delta\vec{r}-\vec{v}_i\Delta t)}{(\Delta t)^2}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\vec{a}&=\frac{2\left[(1.80\,\mathrm{m})\hat{\mathbf{i}}-(0\,\mathrm{m/s})\hat{\mathbf{i}}(1.20\,\mathrm{s})\right]}{(1.20\,\mathrm{s})^2}\\[3pt]
&=(2.50\,\mathrm{m/s^2})\hat{\mathbf{i}}.
\end{aligned}
\]

The acceleration points down the chute, in the same direction as the motion.

\[
|\vec{a}|=\boxed{2.50\,\mathrm{m/s^2}}
\]

**Rounding:** Three significant figures.

---

## Problem 10: A hockey puck crossing rough ice

**Problem statement**

A hockey coach reviews a practice video filmed on a rough, snow-dusted section of level ice. After leaving the stick, a puck slides in a straight line across two marks that are 3.0 m apart. The video shows that the puck is moving at 6.0 m/s as it passes the first mark and 4.0 m/s as it passes the second. Assume that its speed decreases at a constant rate between the marks. How much time does the puck take to travel from the first mark to the second? Report the time in seconds to **two significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The puck crosses the first mark at 6.0 m/s, after contact with the stick has ended.
- **Final event:** The puck crosses the second mark, 3.0 m away, at 4.0 m/s.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The puck covers 3.0 m between marks, with endpoint speeds of 6.0 m/s and 4.0 m/s.

Choose the positive \(x\)-axis along the puck's motion from the first mark toward the second, with unit vector \(\hat{\mathbf{i}}\).

The requested quantity is the elapsed time \(\Delta t\), which is a positive scalar.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((3.0\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((6.0\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((4.0\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Acceleration | \(\vec{a}\) | Not given | Constant; numerical value not given or needed. |
| Time interval | \(\Delta t\) | **?** | To be solved for. |

**3. Select a kinematic equation**

We know the displacement and both endpoint velocities. The average-velocity equation contains the unknown time and does not require acceleration:

\[
\Delta\vec{r}=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t.
\]

**4. Solve algebraically for the unknown**

Equate the \(x\)-components, then isolate \(\Delta t\). This divides scalar components, not vectors:

\[
\begin{aligned}
\Delta\vec{r}&=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t\\[3pt]
\Delta x&=\frac{v_{ix}+v_{fx}}{2}\Delta t\\[3pt]
2\Delta x&=(v_{ix}+v_{fx})\Delta t\\[3pt]
\Delta t&=\frac{2\Delta x}{v_{ix}+v_{fx}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\Delta t&=\frac{2(3.0\,\mathrm{m})}{6.0\,\mathrm{m/s}+4.0\,\mathrm{m/s}}\\[3pt]
&=0.60\,\mathrm{s}.
\end{aligned}
\]

This is the time between the two marks. The puck is still moving at the final event.

\[
\Delta t=\boxed{0.60\,\mathrm{s}}
\]

**Rounding:** Two significant figures.

---

## Problem 11: Keys dropped from a balcony

**Problem statement**

A resident holds a set of keys motionless over an apartment balcony, directly above an empty patch of ground 12.0 m below the release point. The keys slip from the resident's fingers without being thrown and fall straight down. Neglect air resistance. How much time passes from the instant the keys are released until they reach the ground? Report the time in seconds to **three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The keys leave the resident's fingers from rest.
- **Final event:** The keys reach the ground 12.0 m below the release point, just before impact.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The keys are released from rest and fall 12.0 m. Neglecting air resistance, their acceleration is supplied implicitly by free fall near Earth's surface.

Choose the positive \(y\)-axis vertically upward, with unit vector \(\hat{\mathbf{j}}\).

The requested quantity is the elapsed time \(\Delta t\), which is a positive scalar.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((-12.0\,\mathrm{m})\hat{\mathbf{j}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((0\,\mathrm{m/s})\hat{\mathbf{j}}=\vec{0}\) | Implicit: the keys are released from rest without being thrown. |
| Final instantaneous velocity | \(\vec{v}_f\) | Not given | Not required for this calculation. |
| Acceleration | \(\vec{a}\) | \((-9.81\,\mathrm{m/s^2})\hat{\mathbf{j}}\) | Implicit: Earth free fall; use \(g=9.81\,\mathrm{m/s^2}\), directed downward. |
| Time interval | \(\Delta t\) | **?** | To be solved for. |

**3. Select a kinematic equation**

We know the displacement, the zero entering velocity, and the downward acceleration. The displacement-time equation contains the unknown time and avoids the impact velocity:

\[
\Delta\vec{r}=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2.
\]

**4. Solve algebraically for the unknown**

Equate the vertical components and use \(v_{iy}=0\). The ratio \(2\Delta y/a_y\) is positive because both \(\Delta y\) and \(a_y\) are negative. Choose the positive square root because elapsed time is positive:

\[
\begin{aligned}
\Delta\vec{r}&=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2\\[3pt]
\Delta y&=v_{iy}\Delta t+\frac12a_y(\Delta t)^2\\[3pt]
\Delta y&=\frac12a_y(\Delta t)^2\\[3pt]
(\Delta t)^2&=\frac{2\Delta y}{a_y}\\[3pt]
\Delta t&=\sqrt{\frac{2\Delta y}{a_y}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\Delta t&=\sqrt{\frac{2(-12.0\,\mathrm{m})}{-9.81\,\mathrm{m/s^2}}}\\[3pt]
&=1.56412\ldots\,\mathrm{s}.
\end{aligned}
\]

Both the displacement and acceleration point downward, giving a positive quantity under the square root. The impact itself is outside this constant-acceleration segment.

\[
\Delta t=\boxed{1.56\,\mathrm{s}}
\]

**Rounding:** Three significant figures.

---

## Problem 12: Practicing a tennis-ball toss

**Problem statement**

A tennis player is practicing a vertical ball toss before a serve. A video shows that the ball rises 2.00 m above the point where it leaves the player's hand before reaching its highest point and beginning to fall. Consider the ball's motion after it has left the hand, and neglect air resistance. How fast was the ball moving upward just as it left the player's hand? Report the speed in meters per second to **three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The ball leaves the player's hand while moving upward.
- **Final event:** The ball first reaches its highest point, 2.00 m above the release point.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The ball rises 2.00 m and is momentarily at rest at the top. Its downward acceleration follows from free fall near Earth's surface.

Choose the positive \(y\)-axis vertically upward, with unit vector \(\hat{\mathbf{j}}\).

The requested starting speed is the magnitude of the initial instantaneous velocity vector, \(|\vec{v}_i|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((2.00\,\mathrm{m})\hat{\mathbf{j}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | **?** | To be solved for. The question requests its magnitude. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((0\,\mathrm{m/s})\hat{\mathbf{j}}=\vec{0}\) | Implicit: the ball is momentarily at rest at its highest point. |
| Acceleration | \(\vec{a}\) | \((-9.81\,\mathrm{m/s^2})\hat{\mathbf{j}}\) | Implicit: Earth free fall; use \(g=9.81\,\mathrm{m/s^2}\), directed downward. |
| Time interval | \(\Delta t\) | Not given | Not required for this calculation. |

**3. Select a kinematic equation**

We know the vertical rise, the zero velocity at the top, and the downward acceleration. Use the time-independent equation for the signed vertical components:

\[
v_{fy}^{\,2}=v_{iy}^{\,2}+2a_y\Delta y.
\]

**4. Solve algebraically for the unknown**

Isolate \(v_{iy}^{\,2}\), take the square root, and reconstruct the vector. Choose the positive root because the ball leaves the hand moving upward:

\[
\begin{aligned}
v_{fy}^{\,2}&=v_{iy}^{\,2}+2a_y\Delta y\\[3pt]
v_{iy}^{\,2}&=v_{fy}^{\,2}-2a_y\Delta y\\[3pt]
v_{iy}&=\sqrt{v_{fy}^{\,2}-2a_y\Delta y}\\[3pt]
\vec{v}_i&=\sqrt{v_{fy}^{\,2}-2a_y\Delta y}\;\hat{\mathbf{j}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
v_{iy}&=\sqrt{(0\,\mathrm{m/s})^2-2(-9.81\,\mathrm{m/s^2})(2.00\,\mathrm{m})}\\[3pt]
&=6.26418\ldots\,\mathrm{m/s}\\[3pt]
\vec{v}_i&=(6.26418\ldots\,\mathrm{m/s})\hat{\mathbf{j}}.
\end{aligned}
\]

The initial velocity points upward. At the highest point the velocity is zero, but the acceleration remains downward.

\[
|\vec{v}_i|=\boxed{6.26\,\mathrm{m/s}}
\]

**Rounding:** Three significant figures.

---

## Problem 13: An ion traveling through a mass spectrometer

**Problem statement**

An analytical chemist uses a mass spectrometer to examine ions from a water sample. Inside the instrument, a positively charged ion enters a straight electric-field region that is 2.00 cm long, moving toward a detector at \(5.00\times10^3\,\mathrm{m/s}\). The region is evacuated, and a uniform electric field pointing toward the detector makes the ion's speed increase at a constant rate. Electronic measurements show that the ion spends 2.00 microseconds in this region. How fast is the ion moving as it leaves the region? Report the speed in meters per second to **three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The ion enters the electric-field region at \(5.00\times10^3\,\mathrm{m/s}\).
- **Final event:** The ion reaches the exit of that region, after traveling 2.00 cm in 2.00 microseconds.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The entering speed is \(5.00\times10^3\,\mathrm{m/s}\); the region is 2.00 cm long and the transit time is 2.00 microseconds.

Choose the positive \(x\)-axis along the electric-field region toward the detector, with unit vector \(\hat{\mathbf{i}}\).

The requested ending speed is the magnitude of the final instantaneous velocity vector, \(|\vec{v}_f|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((2.00\,\mathrm{cm})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((5.00\times10^3\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | **?** | To be solved for. The question requests its magnitude. |
| Acceleration | \(\vec{a}\) | Not given | Constant; numerical value not given or needed. |
| Time interval | \(\Delta t\) | \(2.00\,\mathrm{\mu s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know \(\Delta\vec{r}\), \(\vec{v}_i\), and \(\Delta t\), and need \(\vec{v}_f\). The average-velocity equation avoids the unknown acceleration:

\[
\Delta\vec{r}=\frac{\vec{v}_i+\vec{v}_f}{2}\,\Delta t.
\]

**4. Solve algebraically for the unknown**

Multiply by 2, divide by the scalar \(\Delta t\), and subtract \(\vec{v}_i\):

\[
\begin{aligned}
\Delta\vec{r}&=\frac{\vec{v}_i+\vec{v}_f}{2}\Delta t\\[3pt]
2\Delta\vec{r}&=(\vec{v}_i+\vec{v}_f)\Delta t\\[3pt]
\frac{2\Delta\vec{r}}{\Delta t}&=\vec{v}_i+\vec{v}_f\\[3pt]
\vec{v}_f&=\frac{2\Delta\vec{r}}{\Delta t}-\vec{v}_i.
\end{aligned}
\]

**5. Substitute values with units and calculate**

Convert the given length and time to SI units before substituting:

\[
2.00\,\mathrm{cm}=2.00\times10^{-2}\,\mathrm{m},\qquad
2.00\,\mu\mathrm{s}=2.00\times10^{-6}\,\mathrm{s}.
\]

\[
\begin{aligned}
\vec{v}_f&=\frac{2(2.00\times10^{-2}\,\mathrm{m})\hat{\mathbf{i}}}{2.00\times10^{-6}\,\mathrm{s}}-(5.00\times10^3\,\mathrm{m/s})\hat{\mathbf{i}}\\[3pt]
&=(2.00\times10^4-5.00\times10^3)\,\mathrm{m/s}\;\hat{\mathbf{i}}\\[3pt]
&=(1.50\times10^4\,\mathrm{m/s})\hat{\mathbf{i}}.
\end{aligned}
\]

The ion exits moving toward the detector. The requested speed is the magnitude of that velocity.

\[
|\vec{v}_f|=\boxed{1.50\times10^4\,\mathrm{m/s}}
\]

**Rounding:** Three significant figures.

---

## Problem 14: Launching a cold atom in a gravity experiment

**Problem statement**

In a laboratory on Earth, a researcher uses lasers to launch a cooled atom vertically upward inside a vacuum chamber. At the instant the laser forces are switched off, the atom is moving upward at 4.00 m/s. From that instant onward, it moves under gravity alone. How far does the atom rise from the point where the laser forces end before reaching its highest point? Report the distance in meters to **two significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The laser forces are switched off while the atom is moving upward at 4.00 m/s.
- **Final event:** The atom first reaches its highest point in the vacuum chamber.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The atom begins this free-flight segment at 4.00 m/s upward and ends momentarily at rest; Earth's gravity supplies its constant downward acceleration.

Choose the positive \(y\)-axis vertically upward, with unit vector \(\hat{\mathbf{j}}\).

The motion does not reverse within this segment, so the requested distance is the magnitude of the displacement vector, \(|\Delta\vec{r}|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | **?** | To be solved for. The question requests its magnitude. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((4.00\,\mathrm{m/s})\hat{\mathbf{j}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((0\,\mathrm{m/s})\hat{\mathbf{j}}=\vec{0}\) | Implicit: the atom is momentarily at rest at its highest point. |
| Acceleration | \(\vec{a}\) | \((-9.81\,\mathrm{m/s^2})\hat{\mathbf{j}}\) | Implicit: Earth free fall after the lasers are switched off; use \(g=9.81\,\mathrm{m/s^2}\), downward. |
| Time interval | \(\Delta t\) | Not given | Not required for this calculation. |

**3. Select a kinematic equation**

We know both endpoint velocities and the constant downward acceleration, but not the time. Use the time-independent equation for the signed vertical components:

\[
v_{fy}^{\,2}=v_{iy}^{\,2}+2a_y\Delta y.
\]

**4. Solve algebraically for the unknown**

Subtract \(v_{iy}^{\,2}\), divide by \(2a_y\), and reconstruct the displacement vector:

\[
\begin{aligned}
v_{fy}^{\,2}&=v_{iy}^{\,2}+2a_y\Delta y\\[3pt]
v_{fy}^{\,2}-v_{iy}^{\,2}&=2a_y\Delta y\\[3pt]
\Delta y&=\frac{v_{fy}^{\,2}-v_{iy}^{\,2}}{2a_y}\\[3pt]
\Delta\vec{r}&=\left(\frac{v_{fy}^{\,2}-v_{iy}^{\,2}}{2a_y}\right)\hat{\mathbf{j}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\Delta y&=\frac{(0\,\mathrm{m/s})^2-(4.00\,\mathrm{m/s})^2}{2(-9.81\,\mathrm{m/s^2})}\\[3pt]
&=0.815494\ldots\,\mathrm{m}\\[3pt]
\Delta\vec{r}&=(0.815494\ldots\,\mathrm{m})\hat{\mathbf{j}}.
\end{aligned}
\]

The displacement is upward. There is no reversal before the final event, so the rise is its magnitude. Gravity still acts downward at the highest point.

\[
|\Delta\vec{r}|=\boxed{0.82\,\mathrm{m}}
\]

**Rounding:** Two significant figures.

---

## Problem 15: Collecting a rock sample on the Moon

**Problem statement**

On the Moon, a rover's robotic arm holds a rock sample motionless 0.600 m above a collection tray. The gripper opens, allowing the sample to drop straight down into the tray. During the fall, the sample has a constant downward acceleration of \(1.62\,\mathrm{m/s^2}\). How much time passes between the gripper releasing the sample and the sample reaching the tray? Report the time in seconds to **three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The gripper releases the stationary rock sample.
- **Final event:** The sample reaches the tray 0.600 m below the release point, just before contact.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The sample starts from rest, falls 0.600 m, and has a stated downward acceleration of \(1.62\,\mathrm{m/s^2}\).

Choose the positive \(y\)-axis vertically upward, with unit vector \(\hat{\mathbf{j}}\).

The requested quantity is the elapsed time \(\Delta t\), which is a positive scalar.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((-0.600\,\mathrm{m})\hat{\mathbf{j}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((0\,\mathrm{m/s})\hat{\mathbf{j}}=\vec{0}\) | Implicit: the sample is held motionless before release. |
| Final instantaneous velocity | \(\vec{v}_f\) | Not given | Not required for this calculation. |
| Acceleration | \(\vec{a}\) | \((-1.62\,\mathrm{m/s^2})\hat{\mathbf{j}}\) | Explicitly given in magnitude and downward direction; the component is negative because upward is positive. |
| Time interval | \(\Delta t\) | **?** | To be solved for. |

**3. Select a kinematic equation**

We know the displacement, the zero entering velocity, and the downward acceleration. The displacement-time equation contains the unknown time and avoids the impact velocity:

\[
\Delta\vec{r}=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2.
\]

**4. Solve algebraically for the unknown**

Equate the vertical components and use \(v_{iy}=0\). The ratio \(2\Delta y/a_y\) is positive because both \(\Delta y\) and \(a_y\) are negative. Choose the positive square root because elapsed time is positive:

\[
\begin{aligned}
\Delta\vec{r}&=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2\\[3pt]
\Delta y&=v_{iy}\Delta t+\frac12a_y(\Delta t)^2\\[3pt]
\Delta y&=\frac12a_y(\Delta t)^2\\[3pt]
(\Delta t)^2&=\frac{2\Delta y}{a_y}\\[3pt]
\Delta t&=\sqrt{\frac{2\Delta y}{a_y}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
\Delta t&=\sqrt{\frac{2(-0.600\,\mathrm{m})}{-1.62\,\mathrm{m/s^2}}}\\[3pt]
&=0.860663\ldots\,\mathrm{s}.
\end{aligned}
\]

The two negative vertical components give a positive elapsed time. The segment ends just before contact with the tray.

\[
\Delta t=\boxed{0.861\,\mathrm{s}}
\]

**Rounding:** Three significant figures.

---

## Problem 16: A space probe testing its main engine

**Problem statement**

A space probe is traveling through the outer solar system, far from planets, at 12.00 km/s relative to the Sun. During a planned test, it fires its main chemical engine for 60.0 s in the direction it is already moving. Throughout the burn, the probe has a constant acceleration of \(0.500\,\mathrm{m/s^2}\) in that direction. For this short interval, treat the path as straight and neglect gravity and changes in the probe's mass. How far does the probe travel relative to the Sun during the burn? Report the distance in **kilometers to three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The engine burn begins, with the probe already traveling at 12.00 km/s relative to the Sun.
- **Final event:** The 60.0 s engine burn ends.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The probe enters the burn at 12.00 km/s and accelerates along its motion at \(0.500\,\mathrm{m/s^2}\) for 60.0 s. The straight-path model neglects gravity and mass changes over the burn.

Choose the positive \(x\)-axis along the probe's motion in the Sun-centered reference frame, with unit vector \(\hat{\mathbf{i}}\).

The motion does not reverse within this segment, so the requested distance is the magnitude of the displacement vector, \(|\Delta\vec{r}|\).

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | **?** | To be solved for. The question requests its magnitude. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((12.00\,\mathrm{km/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | Not given | Not required for this calculation. |
| Acceleration | \(\vec{a}\) | \((0.500\,\mathrm{m/s^2})\hat{\mathbf{i}}\) | Explicitly given in magnitude and direction. |
| Time interval | \(\Delta t\) | \(60.0\,\mathrm{s}\) | Explicitly given; time is a scalar. |

**3. Select a kinematic equation**

We know the entering velocity, acceleration, and elapsed time. Use the displacement-time equation; the ending velocity is not needed:

\[
\Delta\vec{r}=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2.
\]

**4. Solve algebraically for the unknown**

The common form already isolates \(\Delta\vec{r}\). Factoring out \(\Delta t\) gives an equivalent form; the requested distance is the magnitude of this vector:

\[
\begin{aligned}
\Delta\vec{r}&=\vec{v}_i\Delta t+\frac12\vec{a}(\Delta t)^2\\[3pt]
&=\left(\vec{v}_i+\frac12\vec{a}\Delta t\right)\Delta t\\[3pt]
\text{distance}&=|\Delta\vec{r}|.
\end{aligned}
\]

**5. Substitute values with units and calculate**

Use kilometers consistently because the requested answer is in kilometers:

\[
0.500\,\mathrm{m/s^2}
\left(\frac{1\,\mathrm{km}}{1000\,\mathrm{m}}\right)
=0.000500\,\mathrm{km/s^2}.
\]

\[
\begin{aligned}
\Delta\vec{r}&=(12.00\,\mathrm{km/s})\hat{\mathbf{i}}(60.0\,\mathrm{s})
+\frac12(0.000500\,\mathrm{km/s^2})\hat{\mathbf{i}}(60.0\,\mathrm{s})^2\\[3pt]
&=(720\,\mathrm{km}+0.900\,\mathrm{km})\hat{\mathbf{i}}\\[3pt]
&=(720.9\,\mathrm{km})\hat{\mathbf{i}}.
\end{aligned}
\]

The probe continues along the same direction, so distance equals displacement magnitude. Retain the unrounded terms until after adding them.

\[
|\Delta\vec{r}|=720.9\,\mathrm{km}\approx\boxed{721\,\mathrm{km}}
\]

**Rounding:** Three significant figures.

---

## Problem 17: Studying friction between rock surfaces

**Problem statement**

Geophysics students are studying how rock surfaces resist sliding. They use a launcher to send a small rock block along a straight, horizontal track lined with another type of rock. Just after the launcher loses contact with the block, the block is moving at 1.50 m/s. It then slows at a constant rate and comes to rest after sliding 0.250 m along the track. What is the magnitude of the block's acceleration during this slide? Report your answer in \(\mathrm{m/s^2}\) to **three significant figures**.

**1. Identify the motion segment, physics, and requested quantity**

- **Initial event:** The launcher loses contact with the rock block, which is moving at 1.50 m/s.
- **Final event:** The block first comes to rest after sliding 0.250 m along the track.

This is motion with **constant acceleration along a straight segment**, so the kinematic equations apply. The block enters the unpowered slide at 1.50 m/s, travels 0.250 m, and stops.

Choose the positive \(x\)-axis along the block's motion after the launcher releases it, with unit vector \(\hat{\mathbf{i}}\).

The requested quantity is the magnitude of the acceleration vector, \(|\vec{a}|\). We will determine the vector and then take its magnitude.

**2. Organize the kinematic variables**

| Kinematic variable | Symbol | Value | Given or unknown? |
|---|---|---|---|
| Displacement | \(\Delta\vec{r}\) | \((0.250\,\mathrm{m})\hat{\mathbf{i}}\) | Distance explicitly given; the vector direction follows from the chosen axis and motion. |
| Initial instantaneous velocity | \(\vec{v}_i\) | \((1.50\,\mathrm{m/s})\hat{\mathbf{i}}\) | Speed explicitly given; the vector direction follows from the stated motion and chosen axis. |
| Final instantaneous velocity | \(\vec{v}_f\) | \((0\,\mathrm{m/s})\hat{\mathbf{i}}=\vec{0}\) | Implicit: the block comes to rest. |
| Acceleration | \(\vec{a}\) | **?** | To be solved for. The question requests its magnitude. |
| Time interval | \(\Delta t\) | Not given | Not required for this calculation. |

**3. Select a kinematic equation**

We know the displacement and both endpoint velocities, but not the time. Use the time-independent kinematic equation for the signed \(x\)-components. Here \(\vec{v}_i=v_{ix}\hat{\mathbf{i}}\), \(\vec{v}_f=v_{fx}\hat{\mathbf{i}}\), and \(\Delta\vec{r}=\Delta x\hat{\mathbf{i}}\):

\[
v_{fx}^{\,2}=v_{ix}^{\,2}+2a_x\Delta x.
\]

**4. Solve algebraically for the unknown**

Subtract \(v_{ix}^{\,2}\), divide by \(2\Delta x\), and reconstruct the acceleration vector:

\[
\begin{aligned}
v_{fx}^{\,2}&=v_{ix}^{\,2}+2a_x\Delta x\\[3pt]
v_{fx}^{\,2}-v_{ix}^{\,2}&=2a_x\Delta x\\[3pt]
a_x&=\frac{v_{fx}^{\,2}-v_{ix}^{\,2}}{2\Delta x}\\[3pt]
\vec{a}&=\left(\frac{v_{fx}^{\,2}-v_{ix}^{\,2}}{2\Delta x}\right)\hat{\mathbf{i}}.
\end{aligned}
\]

**5. Substitute values with units and calculate**

\[
\begin{aligned}
a_x&=\frac{(0\,\mathrm{m/s})^2-(1.50\,\mathrm{m/s})^2}{2(0.250\,\mathrm{m})}\\[3pt]
&=-4.50\,\mathrm{m/s^2}\\[3pt]
\vec{a}&=(-4.50\,\mathrm{m/s^2})\hat{\mathbf{i}}.
\end{aligned}
\]

The acceleration points opposite the block's motion during the slide. The launcher's earlier push is outside the selected segment.

\[
|\vec{a}|=\boxed{4.50\,\mathrm{m/s^2}}
\]

**Rounding:** Three significant figures.

---

## Answer Key

| Problem | Requested quantity | Reported answer |
|---|---|---|
| 1 | Final speed | \(12\,\mathrm{m/s}\) |
| 2 | Acceleration magnitude | \(1.43\,\mathrm{m/s^2}\) |
| 3 | Distance | \(240\,\mathrm{m}\) |
| 4 | Final speed | \(55\,\mathrm{m/s}\) |
| 5 | Time interval | \(8.0\,\mathrm{s}\) |
| 6 | Acceleration magnitude | \(0.28\,\mathrm{m/s^2}\) |
| 7 | Acceleration magnitude | \(1.5\,\mathrm{m/s^2}\) |
| 8 | Final speed | \(10.0\,\mathrm{m/s}\) |
| 9 | Acceleration magnitude | \(2.50\,\mathrm{m/s^2}\) |
| 10 | Time interval | \(0.60\,\mathrm{s}\) |
| 11 | Time interval | \(1.56\,\mathrm{s}\) |
| 12 | Initial speed | \(6.26\,\mathrm{m/s}\) |
| 13 | Final speed | \(1.50\times10^4\,\mathrm{m/s}\) |
| 14 | Rise | \(0.82\,\mathrm{m}\) |
| 15 | Time interval | \(0.861\,\mathrm{s}\) |
| 16 | Distance | \(721\,\mathrm{km}\) |
| 17 | Acceleration magnitude | \(4.50\,\mathrm{m/s^2}\) |
