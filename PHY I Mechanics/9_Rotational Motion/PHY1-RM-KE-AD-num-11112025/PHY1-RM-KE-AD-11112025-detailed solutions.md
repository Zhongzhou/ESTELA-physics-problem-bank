### Problem 1A

A ceiling fan blade starts from rest and speeds up with a constant angular acceleration of 1.6 rad/s² for 15.0 s.

1. **Type of motion**

   The blade **starts from rest and speeds up with constant angular acceleration**, so this is **rotational motion with constant angular acceleration** and we can use rotational kinematics.

2. **Objective**

   We want the **angular displacement** of the blade during this speeding-up period, expressed in **revolutions**.

3. **Rotational kinematic variables (for this time interval)**

   * (\omega_i = 0~\text{rad/s})

     * *Given explicitly* (“starts from rest”).
   * (\alpha = 1.6~\text{rad/s}^2)

     * *Given explicitly*.
   * (t = 15.0~\text{s})

     * *Given explicitly*.
   * (\theta = ?) (angular displacement)

     * *Unknown; what we’re solving for*.
   * (\omega_f)

     * *Not needed for this solution*.

4. **Relevant kinematic equation & why**

   For constant angular acceleration, the angular displacement is related to initial angular velocity, angular acceleration, and time by
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]
   This equation is relevant because we know (\omega_i), (\alpha), and (t), and we want (\theta).

5. **Algebraic steps (symbolic solution)**

   Start from:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]
   Since (\omega_i = 0),
   [
   \theta = 0 \cdot t + \tfrac{1}{2}\alpha t^2 = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \tfrac{1}{2}(1.6~\text{rad/s}^2)(15.0~\text{s})^2
     = 0.8 \times 225~\text{rad}
     = 180~\text{rad}.
     ]

   * Convert to revolutions using (1~\text{rev} = 2\pi~\text{rad}):
     [
     \theta_{\text{rev}} = \frac{180~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 28.6~\text{rev}.
     ]

**Answer (1A):** (\boxed{28.6~\text{revolutions}})

---

### Problem 1B

A ceiling fan accelerates uniformly from rest to a final angular velocity of 26 rad/s over 12.0 s.

1. **Type of motion**

   The fan **starts from rest and speeds up uniformly** to a higher angular speed, so it undergoes **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **total angular displacement** while it is speeding up, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})

     * *Given explicitly* (“from rest”).
   * (\omega_f = 26~\text{rad/s})

     * *Given explicitly*.
   * (t = 12.0~\text{s})

     * *Given explicitly*.
   * (\theta = ?)

     * *Unknown; what we’re solving for*.
   * (\alpha)

     * *Implicitly defined (constant), but we don’t need to compute it directly.*

4. **Relevant kinematic equation & why**

   For constant angular acceleration, the angular displacement can be written in terms of the average angular velocity:
   [
   \theta = \bar{\omega} t
   \quad \text{with} \quad
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]
   This is useful because we know (\omega_i), (\omega_f), and (t).

5. **Algebraic steps (symbolic solution)**

   First write average angular velocity:
   [
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]
   Then angular displacement:
   [
   \theta = \bar{\omega} t = \tfrac{1}{2}(\omega_i + \omega_f)t.
   ]
   With (\omega_i = 0),
   [
   \theta = \tfrac{1}{2}(0 + \omega_f)t = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \tfrac{1}{2}(26~\text{rad/s})(12.0~\text{s})
     = 13 \times 12~\text{rad}
     = 156~\text{rad}.
     ]

   * Convert to revolutions:
     [
     \theta_{\text{rev}} = \frac{156~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 24.8~\text{rev}.
     ]

**Answer (1B):** (\boxed{24.8~\text{revolutions}})

---

### Problem 1C

A ceiling fan blade starts from rest and speeds up at 2.9 rad/s² until its angular speed reaches 7.4 rad/s.

1. **Type of motion**

   The blade **starts from rest and speeds up at a constant angular acceleration** to a specified angular speed, so it is undergoing **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this speeding-up interval, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})

     * *Given explicitly* (“starts from rest”).
   * (\omega_f = 7.4~\text{rad/s})

     * *Given explicitly*.
   * (\alpha = 2.9~\text{rad/s}^2)

     * *Given explicitly*.
   * (\theta = ?)

     * *Unknown; what we’re solving for*.
   * (t)

     * *Not given and not required if we choose the right equation.*

4. **Relevant kinematic equation & why**

   For constant angular acceleration, the angular velocities and angular displacement are related by:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   This equation is relevant because it directly relates (\omega_i), (\omega_f), (\alpha), and (\theta), and we don’t need the time.

5. **Algebraic steps (symbolic solution)**

   Start from:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   Solve for (\theta):
   [
   \omega_f^2 - \omega_i^2 = 2\alpha\theta
   ]
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}.
   ]
   Since (\omega_i = 0),
   [
   \theta = \frac{\omega_f^2}{2\alpha}.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \frac{(7.4~\text{rad/s})^2}{2(2.9~\text{rad/s}^2)}
     = \frac{54.76~\text{rad}^2/\text{s}^2}{5.8~\text{rad/s}^2}
     \approx 9.44~\text{rad}.
     ]

   * Convert to revolutions:
     [
     \theta_{\text{rev}} = \frac{9.44~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 1.5~\text{rev}.
     ]

**Answer (1C):** (\boxed{1.5~\text{revolutions}})

---

### Problem 2A

A cyclist begins pedaling from rest, and the bicycle wheel accelerates uniformly at 8.3 rad/s² for 9.8 s.

1. **Type of motion**

   The wheel **starts from rest and speeds up with a constant angular acceleration**, so this is **rotational motion with constant angular acceleration**, and rotational kinematic equations apply.

2. **Objective**

   We want the **angular displacement** of the wheel during this acceleration phase, expressed in **revolutions**.

3. **Rotational kinematic variables (for this interval)**

   * (\omega_i = 0~\text{rad/s})

     * *Given explicitly* (“from rest”).
   * (\alpha = 8.3~\text{rad/s}^2)

     * *Given explicitly*.
   * (t = 9.8~\text{s})

     * *Given explicitly*.
   * (\theta = ?) (angular displacement)

     * *Unknown; what we’re solving for*.
   * (\omega_f)

     * *Not needed for this solution*.

4. **Relevant kinematic equation & why**

   For constant angular acceleration:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]
   This is relevant because we know (\omega_i), (\alpha), and (t), and we want (\theta).

5. **Algebraic steps (symbolic solution)**

   Start from:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]
   With (\omega_i = 0):
   [
   \theta = 0 \cdot t + \tfrac{1}{2}\alpha t^2 = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \tfrac{1}{2}(8.3~\text{rad/s}^2)(9.8~\text{s})^2
     = 4.15 \times 96.04~\text{rad}
     \approx 398.6~\text{rad}.
     ]

   * Convert to revolutions, using (1~\text{rev} = 2\pi~\text{rad}):
     [
     \theta_{\text{rev}} = \frac{398.6~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 63.4~\text{rev}.
     ]

**Answer (2A):** (\boxed{63.4~\text{revolutions}})

---

### Problem 2B

A bicycle wheel increases its angular speed uniformly from rest to 30 rad/s in 5.4 s.

1. **Type of motion**

   The wheel **speeds up uniformly from rest to a higher angular speed**, so it undergoes **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **total angular displacement** during this speeding-up interval, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})

     * *Given explicitly* (“from rest”).
   * (\omega_f = 30~\text{rad/s})

     * *Given explicitly*.
   * (t = 5.4~\text{s})

     * *Given explicitly*.
   * (\theta = ?)

     * *Unknown; what we’re solving for*.
   * (\alpha)

     * *Implicitly defined (constant), but not needed directly.*

4. **Relevant kinematic equation & why**

   With constant angular acceleration, the angular displacement can be written in terms of the **average angular velocity**:
   [
   \theta = \bar{\omega} t, \quad \text{where} \quad \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]
   This is useful because we know (\omega_i), (\omega_f), and (t).

5. **Algebraic steps (symbolic solution)**

   Average angular velocity:
   [
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]
   Angular displacement:
   [
   \theta = \bar{\omega} t = \tfrac{1}{2}(\omega_i + \omega_f)t.
   ]
   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}(0 + \omega_f)t = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \tfrac{1}{2}(30~\text{rad/s})(5.4~\text{s})
     = 15 \times 5.4~\text{rad}
     = 81.0~\text{rad}.
     ]

   * Convert to revolutions:
     [
     \theta_{\text{rev}} = \frac{81.0~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 12.9~\text{rev}.
     ]

**Answer (2B):** (\boxed{12.9~\text{revolutions}})

---

### Problem 2C

Starting from rest, a cyclist’s wheel spins up to 50 rad/s under a constant angular acceleration of 9.4 rad/s².

1. **Type of motion**

   The wheel **starts from rest and speeds up with a constant angular acceleration** to a given angular speed, so it is in **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** while the wheel speeds up, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})

     * *Given explicitly* (“starting from rest”).
   * (\omega_f = 50~\text{rad/s})

     * *Given explicitly*.
   * (\alpha = 9.4~\text{rad/s}^2)

     * *Given explicitly*.
   * (\theta = ?)

     * *Unknown; what we’re solving for*.
   * (t)

     * *Not given, and not required with the right equation.*

4. **Relevant kinematic equation & why**

   For constant angular acceleration:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   This is relevant because it directly connects (\omega_i), (\omega_f), (\alpha), and (\theta), and does **not** require time.

5. **Algebraic steps (symbolic solution)**

   Start from:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   Solve for (\theta):
   [
   \omega_f^2 - \omega_i^2 = 2\alpha\theta
   ]
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}.
   ]
   With (\omega_i = 0):
   [
   \theta = \frac{\omega_f^2}{2\alpha}.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \frac{(50~\text{rad/s})^2}{2(9.4~\text{rad/s}^2)}
     = \frac{2500~\text{rad}^2/\text{s}^2}{18.8~\text{rad/s}^2}
     \approx 133.0~\text{rad}.
     ]

   * Convert to revolutions:
     [
     \theta_{\text{rev}} = \frac{133.0~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 21.2~\text{rev}.
     ]

**Answer (2C):** (\boxed{21.2~\text{revolutions}})

---

## **Problem 3A**

A car starts from rest and its tires experience an angular acceleration of 17 rad/s² for 6.6 s.

1. **Type of motion**

   The tire **starts from rest and speeds up with a constant angular acceleration**, meaning this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this acceleration phase, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
     *Given explicitly (“from rest”).*
   * (\alpha = 17~\text{rad/s}^2)
     *Given explicitly.*
   * (t = 6.6~\text{s})
     *Given explicitly.*
   * (\theta = ?)
     *Unknown; what we are solving for.*
   * (\omega_f)
     *Not needed.*

4. **Relevant kinematic equation & why**

   We know (\omega_i), (\alpha), and (t), so:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2
   ]
   directly gives angular displacement for constant angular acceleration.

5. **Algebraic steps (symbolic solution)**

   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(17~\text{rad/s}^2)(6.6~\text{s})^2
     = 8.5 \times 43.56
     \approx 370.3~\text{rad}.
     ]

   * Revolutions:
     [
     \theta_{\text{rev}} = \frac{370.3}{2\pi} \approx 58.9~\text{rev}.
     ]

**Answer (3A):** (\boxed{58.9~\text{revolutions}})

---

## **Problem 3B**

A car tire spins up from rest to 100 rad/s in 12.0 s.

1. **Type of motion**

   The tire **speeds up uniformly from rest**, indicating **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this speeding-up interval, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 100~\text{rad/s})
   * (t = 12.0~\text{s})
   * (\theta = ?)
   * (\alpha) (not needed directly)

4. **Relevant kinematic equation & why**

   Angular displacement with constant acceleration can be expressed using **average angular velocity**:
   [
   \theta = \bar{\omega} t, \quad \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]
   We know both angular speeds and time, so this is the most direct approach.

5. **Algebraic steps (symbolic solution)**

   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(100~\text{rad/s})(12.0~\text{s})
     = 50 \times 12
     = 600~\text{rad}.
     ]

   * Revolutions:
     [
     \theta_{\text{rev}} = \frac{600}{2\pi} \approx 95.5~\text{rev}.
     ]

**Answer (3B):** (\boxed{95.5~\text{revolutions}})

---

## **Problem 3C**

A car tire starts from rest and accelerates at 6.0 rad/s² until its angular speed reaches 110 rad/s.

1. **Type of motion**

   The tire **starts from rest and reaches a higher angular speed under constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this acceleration, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 110~\text{rad/s})
   * (\alpha = 6.0~\text{rad/s}^2)
   * (\theta = ?)
   * (t) (not needed)

4. **Relevant kinematic equation & why**

   This equation links angular velocities, acceleration, and displacement without requiring time:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   All quantities except (\theta) are known.

5. **Algebraic steps (symbolic solution)**

   Solve for (\theta):
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}.
   ]
   With (\omega_i = 0):
   [
   \theta = \frac{\omega_f^2}{2\alpha}.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \frac{(110~\text{rad/s})^2}{2(6.0~\text{rad/s}^2)}
     = \frac{12100}{12}
     \approx 1008.3~\text{rad}.
     ]

   * Revolutions:
     [
     \theta_{\text{rev}} = \frac{1008.3}{2\pi} \approx 160.5~\text{rev}.
     ]

**Answer (3C):** (\boxed{160.5~\text{revolutions}})

---

## **Problem 4A**

An electric drill starts from rest and its chuck speeds up with a uniform angular acceleration of 330 rad/s² for 7.7 s.

1. **Type of motion**

   The chuck **starts from rest and speeds up with a uniform angular acceleration**, so this is **rotational motion with constant angular acceleration**, and rotational kinematics apply.

2. **Objective**

   We want the **angular displacement** of the chuck during this spin-up, expressed in **revolutions**.

3. **Rotational kinematic variables (for this interval)**

   * (\omega_i = 0~\text{rad/s})
       • *Given explicitly* (“starts from rest”).
   * (\alpha = 330~\text{rad/s}^2)
       • *Given explicitly*.
   * (t = 7.7~\text{s})
       • *Given explicitly*.
   * (\theta = ?)
       • *Unknown; what we are solving for*.
   * (\omega_f)
       • *Not needed for this solution*.

4. **Relevant kinematic equation & why**

   For constant angular acceleration, angular displacement is:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]
   This is relevant because we know (\omega_i), (\alpha), and (t), and we want (\theta).

5. **Algebraic steps (symbolic solution)**

   Start from:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]
   With (\omega_i = 0):
   [
   \theta = 0 \cdot t + \tfrac{1}{2}\alpha t^2 = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \tfrac{1}{2}(330~\text{rad/s}^2)(7.7~\text{s})^2
     = 165 \times 59.29~\text{rad}
     \approx 9782.9~\text{rad}.
     ]

   * Convert to revolutions ((1~\text{rev} = 2\pi~\text{rad})):
     [
     \theta_{\text{rev}} = \frac{9782.9~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 1557.0~\text{rev}.
     ]

**Answer (4A):** (\boxed{1557.0~\text{revolutions}})

---

## **Problem 4B**

A power drill accelerates from rest to 2600 rad/s in 7.7 s.

1. **Type of motion**

   The drill chuck **speeds up uniformly from rest to a higher angular speed**, so it is undergoing **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **total angular displacement** during the spin-up, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
       • *Given explicitly* (“from rest”).
   * (\omega_f = 2600~\text{rad/s})
       • *Given explicitly*.
   * (t = 7.7~\text{s})
       • *Given explicitly*.
   * (\theta = ?)
       • *Unknown; what we are solving for*.
   * (\alpha)
       • *Implicitly defined as constant, but we don’t need to compute it directly*.

4. **Relevant kinematic equation & why**

   With constant angular acceleration, angular displacement can be written using the **average angular velocity**:
   [
   \theta = \bar{\omega} t, \quad \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]
   This is useful because we know (\omega_i), (\omega_f), and (t).

5. **Algebraic steps (symbolic solution)**

   Average angular velocity:
   [
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]
   Angular displacement:
   [
   \theta = \bar{\omega} t = \tfrac{1}{2}(\omega_i + \omega_f)t.
   ]
   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \tfrac{1}{2}(2600~\text{rad/s})(7.7~\text{s})
     = 1300 \times 7.7~\text{rad}
     = 10010.0~\text{rad}.
     ]

   * In revolutions:
     [
     \theta_{\text{rev}} = \frac{10010.0~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 1593.1~\text{rev}.
     ]

**Answer (4B):** (\boxed{1593.1~\text{revolutions}})

---

## **Problem 4C**

A drill motor brings its chuck from rest to 2600 rad/s while accelerating steadily at 330 rad/s².

1. **Type of motion**

   The chuck **starts from rest and reaches a high angular speed under steady (constant) angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this interval, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
       • *Given explicitly* (“from rest”).
   * (\omega_f = 2600~\text{rad/s})
       • *Given explicitly*.
   * (\alpha = 330~\text{rad/s}^2)
       • *Given explicitly*.
   * (\theta = ?)
       • *Unknown; what we are solving for*.
   * (t)
       • *Not given and not required if we use the right equation*.

4. **Relevant kinematic equation & why**

   The relation that connects angular velocities, acceleration, and displacement (without time) is:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   This is relevant because (\omega_i), (\omega_f), and (\alpha) are known, and we want (\theta).

5. **Algebraic steps (symbolic solution)**

   Start from:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   Solve for (\theta):
   [
   \omega_f^2 - \omega_i^2 = 2\alpha\theta
   ]
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}.
   ]
   With (\omega_i = 0):
   [
   \theta = \frac{\omega_f^2}{2\alpha}.
   ]

6. **Substitute, solve in radians, then convert to revolutions**

   * In radians:
     [
     \theta = \frac{(2600~\text{rad/s})^2}{2(330~\text{rad/s}^2)}
     = \frac{6760000~\text{rad}^2/\text{s}^2}{660~\text{rad/s}^2}
     \approx 10242.4~\text{rad}.
     ]

   * In revolutions:
     [
     \theta_{\text{rev}} = \frac{10242.4~\text{rad}}{2\pi~\text{rad/rev}}
     \approx 1630.1~\text{rev}.
     ]

**Answer (4C):** (\boxed{1630.1~\text{revolutions}})

---

## **Problem 5A**

A turntable platter starts from rest and accelerates at 0.23 rad/s² for 25.0 s.

1. **Type of motion**

   The platter **starts from rest and speeds up with a constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this acceleration, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\alpha = 0.23~\text{rad/s}^2)
   * (t = 25.0~\text{s})
   * (\theta = ?)
   * (\omega_f) (not required)

4. **Relevant kinematic equation & why**

   With known (\omega_i), (\alpha), and (t), angular displacement is:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]

5. **Algebraic steps (symbolic solution)**

   Since (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(0.23)(25.0)^2
     = 0.115 \times 625
     = 71.875~\text{rad}.
     ]

   * Revolutions:
     [
     \theta_{\text{rev}} = \frac{71.875}{2\pi} \approx 11.4~\text{rev}.
     ]

**Answer (5A):** (\boxed{11.4~\text{revolutions}})

---

## **Problem 5B**

A vinyl record accelerates uniformly from rest to 7.5 rad/s in 20.0 s.

1. **Type of motion**

   The record **speeds up uniformly from rest**, meaning it is in **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this acceleration, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 7.5~\text{rad/s})
   * (t = 20.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   With constant acceleration, angular displacement equals the average angular velocity times time:
   [
   \theta = \bar{\omega}t, \qquad \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]

5. **Algebraic steps (symbolic solution)**

   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(7.5)(20.0)
     = 3.75 \times 20.0
     = 75.0~\text{rad}.
     ]

   * Revolutions:
     [
     \theta_{\text{rev}} = \frac{75.0}{2\pi} \approx 11.9~\text{rev}.
     ]

**Answer (5B):** (\boxed{11.9~\text{revolutions}})

---

## **Problem 5C**

A record player spins up from rest to 7.4 rad/s with constant angular acceleration of 0.22 rad/s².

1. **Type of motion**

   The record **starts from rest and speeds up with a constant angular acceleration**, so it is in **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this spin-up, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 7.4~\text{rad/s})
   * (\alpha = 0.22~\text{rad/s}^2)
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   The equation that avoids needing time is:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   We know (\omega_i), (\omega_f), and (\alpha), so this directly gives (\theta).

5. **Algebraic steps (symbolic solution)**

   Solve for (\theta):
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}.
   ]
   With (\omega_i = 0):
   [
   \theta = \frac{\omega_f^2}{2\alpha}.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \frac{(7.4)^2}{2(0.22)}
     = \frac{54.76}{0.44}
     \approx 124.5~\text{rad}.
     ]

   * Revolutions:
     [
     \theta_{\text{rev}} = \frac{124.5}{2\pi} \approx 19.8~\text{rev}.
     ]

**Answer (5C):** (\boxed{19.8~\text{revolutions}})

---

## **Problem 6A**

A helicopter’s rotor begins spinning from rest and accelerates uniformly at 2.8 rad/s² for 14.0 s.

1. **Type of motion**

   The rotor **starts from rest and speeds up at a constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\alpha = 2.8~\text{rad/s}^2)
   * (t = 14.0~\text{s})
   * (\theta = ?)
   * (\omega_f) (not required)

4. **Relevant kinematic equation & why**

   With known (\omega_i), (\alpha), and (t), angular displacement is:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]

5. **Algebraic steps (symbolic solution)**

   Since (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(2.8)(14.0)^2
     = 1.4 \times 196
     = 274.4~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{274.4}{2\pi} \approx 43.7~\text{rev}.
     ]

**Answer (6A):** (\boxed{43.7~\text{revolutions}})

---

## **Problem 6B**

A helicopter rotor speeds up from rest to 45 rad/s in 16.0 s.

1. **Type of motion**

   The rotor **speeds up uniformly from rest**, meaning **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 45~\text{rad/s})
   * (t = 16.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   Displacement with constant angular acceleration can be written using average angular velocity:
   [
   \theta = \bar{\omega} t,
   \qquad
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]

5. **Algebraic steps (symbolic solution)**

   Because (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(45)(16.0)
     = 22.5 \times 16.0
     = 360.0~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{360.0}{2\pi} \approx 57.3~\text{rev}.
     ]

**Answer (6B):** (\boxed{57.3~\text{revolutions}})

---

## **Problem 6C**

The main rotor starts from rest and accelerates at 1.2 rad/s² until it reaches 39 rad/s.

1. **Type of motion**

   The rotor **starts from rest and increases angular speed under constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 39~\text{rad/s})
   * (\alpha = 1.2~\text{rad/s}^2)
   * (\theta = ?)
   * (t) (not needed)

4. **Relevant kinematic equation & why**

   Use the relation that avoids time:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   We know (\omega_i), (\omega_f), and (\alpha), so we can solve directly for (\theta).

5. **Algebraic steps (symbolic solution)**

   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}
   = \frac{\omega_f^2}{2\alpha}
   \quad (\text{since } \omega_i = 0).
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \frac{(39)^2}{2(1.2)}
     = \frac{1521}{2.4}
     \approx 633.8~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{633.8}{2\pi} \approx 100.9~\text{rev}.
     ]

**Answer (6C):** (\boxed{100.9~\text{revolutions}})

---

## **Problem 7A**

A washing machine begins its spin cycle from rest, accelerating at 6.2 rad/s² for 9.5 s.

1. **Type of motion**

   The drum **starts from rest and speeds up under constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\alpha = 6.2~\text{rad/s}^2)
   * (t = 9.5~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   With known (\omega_i), (\alpha), and (t), angular displacement is:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]

5. **Algebraic steps (symbolic solution)**

   Because (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(6.2)(9.5)^2
     = 3.1 \times 90.25
     = 279.8~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{279.8}{2\pi} \approx 44.5~\text{rev}.
     ]

**Answer (7A):** (\boxed{44.5~\text{revolutions}})

---

## **Problem 7B**

A washer drum accelerates uniformly from rest to 130 rad/s in 11.0 s.

1. **Type of motion**

   The drum **speeds up uniformly from rest**, so it undergoes **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 130~\text{rad/s})
   * (t = 11.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   For constant acceleration, angular displacement can be found using average angular velocity:
   [
   \theta = \bar{\omega} t,
   \qquad
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]

5. **Algebraic steps (symbolic solution)**

   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(130)(11.0)
     = 65 \times 11.0
     = 715.0~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{715.0}{2\pi} \approx 113.8~\text{rev}.
     ]

**Answer (7B):** (\boxed{113.8~\text{revolutions}})

---

## **Problem 7C**

During a fast spin cycle, the drum starts from rest and speeds up at 12 rad/s² until it reaches 150 rad/s.

1. **Type of motion**

   The drum **starts from rest and increases angular speed under constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 150~\text{rad/s})
   * (\alpha = 12~\text{rad/s}^2)
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   Use the relation that avoids needing time:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]
   All quantities except (\theta) are known.

5. **Algebraic steps (symbolic solution)**

   Solve for (\theta):
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}
   = \frac{\omega_f^2}{2\alpha}
   \quad (\text{because } \omega_i = 0).
   ]

6. **Substitute, solve in radians, convert to revolutions**

   * Radians:
     [
     \theta = \frac{(150)^2}{2(12)}
     = \frac{22500}{24}
     = 937.5~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{937.5}{2\pi} \approx 149.2~\text{rev}.
     ]

**Answer (7C):** (\boxed{149.2~\text{revolutions}})

---

## **Problem 8A**

A figure skater starts a spin from rest and accelerates uniformly at 8.2 rad/s² for 2.8 s.

1. **Type of motion**

   The skater **starts from rest and speeds up under constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\alpha = 8.2~\text{rad/s}^2)
   * (t = 2.8~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   With known (\omega_i), (\alpha), and (t), angular displacement follows:
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]

5. **Algebraic steps (symbolic solution)**

   Since (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(8.2)(2.8)^2
     = 4.1 \times 7.84
     = 32.144~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{32.144}{2\pi} \approx 5.1~\text{rev}.
     ]

**Answer (8A):** (\boxed{5.1~\text{revolutions}})

---

## **Problem 8B**

A skater spins up from rest to 14 rad/s in 4.0 s.

1. **Type of motion**

   The skater **speeds up uniformly from rest**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 14~\text{rad/s})
   * (t = 4.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   With constant acceleration, displacement is:
   [
   \theta = \bar{\omega} t, \qquad
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]

5. **Algebraic steps (symbolic solution)**

   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(14)(4.0)
     = 7 \times 4
     = 28~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{28}{2\pi} \approx 4.5~\text{rev}.
     ]

**Answer (8B):** (\boxed{4.5~\text{revolutions}})

---

## **Problem 8C**

A skater pulls her arms in and accelerates at 1.6 rad/s² until her angular speed reaches 8.2 rad/s.

1. **Type of motion**

   She **starts from rest and increases her angular speed with constant angular acceleration**, which is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this acceleration, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 8.2~\text{rad/s})
   * (\alpha = 1.6~\text{rad/s}^2)
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   The equation linking angular speeds, acceleration, and displacement (without time) is:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]

5. **Algebraic steps (symbolic solution)**

   Solve for (\theta):
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}
   = \frac{\omega_f^2}{2\alpha}
   \quad (\text{since } \omega_i=0).
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \frac{(8.2)^2}{2(1.6)}
     = \frac{67.24}{3.2}
     \approx 21.0~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{21.0}{2\pi} \approx 3.3~\text{rev}.
     ]

**Answer (8C):** (\boxed{3.3~\text{revolutions}})

---

## **Problem 9A**

A CD starts from rest and accelerates at 25 rad/s² for 20.0 s.

1. **Type of motion**

   The disc **starts from rest and speeds up with a constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\alpha = 25~\text{rad/s}^2)
   * (t = 20.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   With known (\omega_i), (\alpha), and (t):
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]

5. **Algebraic steps (symbolic solution)**

   Since (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(25)(20.0)^2
     = 12.5 \times 400
     = 5000~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{5000}{2\pi} \approx 795.8~\text{rev}.
     ]

**Answer (9A):** (\boxed{795.8~\text{revolutions}})

---

## **Problem 9B**

A DVD spins up from rest to 500 rad/s in 15.0 s.

1. **Type of motion**

   The disc **speeds up uniformly from rest**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 500~\text{rad/s})
   * (t = 15.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   For constant angular acceleration:
   [
   \theta = \bar{\omega} t,
   \qquad \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]

5. **Algebraic steps (symbolic solution)**

   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(500)(15.0)
     = 250 \times 15
     = 3750~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{3750}{2\pi} \approx 596.8~\text{rev}.
     ]

**Answer (9B):** (\boxed{596.8~\text{revolutions}})

---

## **Problem 9C**

A CD starts from rest and accelerates uniformly at 45 rad/s² until it reaches 450 rad/s.

1. **Type of motion**

   The disc **starts from rest and increases angular speed under constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement** during this acceleration, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 450~\text{rad/s})
   * (\alpha = 45~\text{rad/s}^2)
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   Use the relation that avoids time:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]

5. **Algebraic steps (symbolic solution)**

   Solve for (\theta):
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}
   = \frac{\omega_f^2}{2\alpha}
   \quad (\text{since } \omega_i=0).
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \frac{(450)^2}{2(45)}
     = \frac{202500}{90}
     = 2250~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{2250}{2\pi} \approx 358.1~\text{rev}.
     ]

**Answer (9C):** (\boxed{358.1~\text{revolutions}})

---

## **Problem 10A**

A turbine starts from rest and accelerates at 0.32 rad/s² for 18.0 s.

1. **Type of motion**

   The blades **start from rest and speed up with constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\alpha = 0.32~\text{rad/s}^2)
   * (t = 18.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   With known (\omega_i), (\alpha), and (t):
   [
   \theta = \omega_i t + \tfrac{1}{2}\alpha t^2.
   ]

5. **Algebraic steps (symbolic solution)**

   Because (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\alpha t^2.
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(0.32)(18.0)^2
     = 0.16 \times 324
     = 51.84~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{51.84}{2\pi} \approx 8.2~\text{rev}.
     ]

**Answer (10A):** (\boxed{8.2~\text{revolutions}})

---

## **Problem 10B**

A turbine speeds up from rest to 8.0 rad/s in 10.0 s.

1. **Type of motion**

   The turbine **speeds up uniformly from rest**, so it is undergoing **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 8.0~\text{rad/s})
   * (t = 10.0~\text{s})
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   Angular displacement under constant acceleration can be found using the average angular velocity:
   [
   \theta = \bar{\omega} t,
   \qquad
   \bar{\omega} = \tfrac{1}{2}(\omega_i + \omega_f).
   ]

5. **Algebraic steps (symbolic solution)**

   With (\omega_i = 0):
   [
   \theta = \tfrac{1}{2}\omega_f t.
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \tfrac{1}{2}(8.0)(10.0)
     = 4.0 \times 10.0
     = 40.0~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{40.0}{2\pi} \approx 6.4~\text{rev}.
     ]

**Answer (10B):** (\boxed{6.4~\text{revolutions}})

---

## **Problem 10C**

A turbine starts from rest and accelerates at 0.90 rad/s² until its angular speed reaches 10 rad/s.

1. **Type of motion**

   The blades **start from rest and increase angular speed with constant angular acceleration**, so this is **rotational motion with constant angular acceleration**.

2. **Objective**

   We want the **angular displacement**, expressed in **revolutions**.

3. **Rotational kinematic variables**

   * (\omega_i = 0~\text{rad/s})
   * (\omega_f = 10~\text{rad/s})
   * (\alpha = 0.90~\text{rad/s}^2)
   * (\theta = ?)

4. **Relevant kinematic equation & why**

   The equation that connects angular speeds, acceleration, and displacement (without time) is:
   [
   \omega_f^2 = \omega_i^2 + 2\alpha\theta.
   ]

5. **Algebraic steps (symbolic solution)**

   Solve for (\theta):
   [
   \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}
   = \frac{\omega_f^2}{2\alpha}
   \quad (\text{because } \omega_i = 0).
   ]

6. **Substitute, compute radians, convert to revolutions**

   * Radians:
     [
     \theta = \frac{(10)^2}{2(0.90)}
     = \frac{100}{1.8}
     \approx 55.6~\text{rad}.
     ]

   * Revolutions:
     [
     \frac{55.6}{2\pi} \approx 8.8~\text{rev}.
     ]

**Answer (10C):** (\boxed{8.8~\text{revolutions}})

---
