---
source: "CEC 2022 / NEC 2020 Article 210.19(A)(1), Article 210.20, Table 310.16"
last-verified: "2026-11-06"
prereqs:
  - "[[grounding-vs-bonding]]"
---

# Branch Circuit Conductor Sizing

Branch circuit sizing under the California Electrical Code balances ampacity, continuous loads, and conductor temperature ratings.

---

## 1. Continuous Load Multiplier

- **Continuous Load Rule:** Loads operating for 3.0 h or more must be calculated at 125.0% of nominal rating per NEC 210.19(A)(1) and NEC 210.20(A).
- **Non-Continuous Load:** Evaluated at 100.0% of nominal rating.
- **Formula:**
  $$\text{Minimum Circuit Rating} = (\text{Non-Continuous Amperes} \times 1.0) + (\text{Continuous Amperes} \times 1.25)$$

---

## 2. Conductor Ampacity & Terminal Ratings

- **Reference Table:** Conductor ampacities are governed by NEC Table 310.16.
- **Terminal Temperature Provisions:** NEC 110.14(C) dictates termination ratings:
  - Equipment rated 100.0 A or less, or marked for #14 AWG through #1 AWG conductors: 60.0 °C rating unless listed and marked for 75.0 °C.
  - Equipment rated over 100.0 A or marked for conductors larger than #1 AWG: 75.0 °C rating.
- **Derating Adjustments:** Ampacity adjustment factors for more than 3.0 current-carrying conductors in a raceway follow NEC Table 310.15(C)(1). Ambient temperature correction factors follow NEC Table 310.15(B)(1) or Table 310.15(B)(2).

---

## 3. Related Safety Provisions

Proper bonding and ground-fault current paths must accompany all branch circuit raceways as established in [[grounding-vs-bonding]].
