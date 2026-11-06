# Branch Circuit Sizing — Exercises

Practice problems for branch circuit sizing under CEC 2022 / NEC 2020. Concepts grounded in [[branch-circuit-sizing]].

---

## Problem 1: Easy

A single-phase 120.0 V non-continuous branch circuit supplies a lighting array with a steady draw of 12.0 A. What is the minimum required branch-circuit conductor ampacity and OCPD rating?

- **Answer:** 12.0 A conductor ampacity (standard 15.0 A OCPD)
- **Worked Solution:**
  1. Determine continuous load status: Non-continuous operation evaluates at 100.0% multiplier.
  2. Calculation: $12.0\text{ A} \times 1.0 = 12.0\text{ A}$.
  3. Code Citation: NEC 210.19(A)(1) requires conductor ampacity not less than non-continuous load.
  4. OCPD Selection: Standard OCPD per NEC 240.6(A) is 15.0 A using #14 AWG copper.

---

## Problem 2: Medium

A continuous commercial office lighting load operates for 8.0 h continuously at 277.0 V single-phase with a total connected load of 4432.0 VA. Calculate the continuous operating current, the required minimum circuit ampacity, and the minimum standard overcurrent protective device rating.

- **Answer:** 16.0 A operating current; 20.0 A minimum circuit ampacity; 20.0 A OCPD
- **Worked Solution:**
  1. Compute operating current: $I = \frac{4432.0\text{ VA}}{277.0\text{ V}} = 16.0\text{ A}$.
  2. Apply continuous load factor: Operating time of 8.0 h qualifies as continuous (> 3.0 h). Per NEC 210.19(A)(1) and NEC 210.20(A), multiply by 125.0%.
  3. Minimum ampacity calculation: $16.0\text{ A} \times 1.25 = 20.0\text{ A}$.
  4. OCPD Selection: Per NEC 240.6(A), minimum standard fuse or inverse time circuit breaker is 20.0 A.
  5. Conductor Selection: Minimum conductor is #12 AWG copper rated 20.0 A per NEC Table 310.16 and NEC 240.4(D)(5).

---

## Problem 3: Trap

A raceway contains 4.0 current-carrying #10 AWG THHN copper conductors installed in an ambient temperature of 40.0 °C. The termination lugs on the 30.0 A circuit breaker are listed for 75.0 °C only. What is the allowable ampacity of each conductor after derating, and what is the maximum permissible continuous load in amperes that can be connected to this circuit?

- **Answer:** 29.92 A allowable ampacity; 24.0 A maximum continuous load
- **Worked Solution:**
  1. Base ampacity lookup: From NEC Table 310.16, #10 AWG THHN in 90.0 °C column is 40.0 A. (Per NEC 110.14(C) and Article 310, 90.0 °C ampacity may be used as the starting point for derating adjustments).
  2. Ambient temperature correction: From NEC Table 310.15(B)(1), 40.0 °C in 90.0 °C rating column has a correction factor of 0.91.
  3. Conductor bundling adjustment: For 4.0 current-carrying conductors, NEC Table 310.15(C)(1) specifies an adjustment factor of 0.82 (or 80.0% / 0.82 depending on table cycle; NEC 2020 Table 310.15(C)(1) is 0.80). Derating factor: 0.80.
  4. Adjusted ampacity calculation: $40.0\text{ A} \times 0.91 \times 0.80 = 29.12\text{ A}$.
  5. Terminal limitation verification: Per NEC 110.14(C)(1)(a)(3), terminal is rated 75.0 °C. Table 310.16 75.0 °C ampacity for #10 AWG is 35.0 A. Since $29.12\text{ A} \le 35.0\text{ A}$, the allowable ampacity remains 29.12 A.
  6. Trap check — Continuous load on 30.0 A breaker: The breaker rating is 30.0 A, but conductor allowable ampacity is 29.12 A. Per NEC 210.20(A), continuous load must not exceed 80.0% of the rating. For a 30.0 A breaker with 29.12 A conductor limit, maximum continuous load is $29.12\text{ A} \div 1.25 = 23.30\text{ A}$ (or $30.0\text{ A} \times 0.80 = 24.0\text{ A}$ constrained by conductor to 23.30 A).
