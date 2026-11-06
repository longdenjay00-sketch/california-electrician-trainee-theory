---
source: "CEC 2022 / NEC 2020 Article 314.16, Table 314.16(A), Table 314.16(B)"
last-verified: "2026-11-06"
prereqs:
  - "[[branch-circuit-sizing]]"
---

# Outlet and Device Box Fill Calculations

California Electrical Code Article 314 dictates minimum interior volume requirements for metallic and nonmetallic junction, device, and pull boxes.

---

## 1. Conductor Volume Allowances (Table 314.16(B))

- **#18 AWG:** 1.50 cu in (24.6 cm³)
- **#16 AWG:** 1.75 cu in (28.7 cm³)
- **#14 AWG:** 2.00 cu in (32.8 cm³)
- **#12 AWG:** 2.25 cu in (36.9 cm³)
- **#10 AWG:** 2.50 cu in (41.0 cm³)
- **#8 AWG:** 3.00 cu in (49.2 cm³)
- **#6 AWG:** 5.00 cu in (81.9 cm³)

---

## 2. Counting Rules (NEC 314.16(B)(1)-(5))

1. **Conductor Fill (314.16(B)(1)):**
   - Conductors entering from outside and terminating or spliced: count = 1.0 each.
   - Uncut conductors passing through: count = 1.0 each.
   - Pigtails originating and terminating entirely within the box: count = 0.0.
2. **Clamp Fill (314.16(B)(2)):**
   - Internal factory or field-installed clamps: count = 1.0 allowance total, evaluated at the volume of the largest conductor present in the box.
3. **Support Fittings (314.16(B)(3)):**
   - Fixture studs or hickeys: count = 1.0 allowance for each type present, evaluated at the volume of the largest conductor.
4. **Device or Equipment Yokes (314.16(B)(4)):**
   - Each single or multi-device yoke/strap (switches, duplex receptacles): count = 2.0 allowances, evaluated at the volume of the largest conductor connected to that device.
5. **Equipment Grounding Conductors (314.16(B)(5)):**
   - Up to 4.0 EGCs: count = 1.0 allowance total, evaluated at the largest EGC present.
   - Each additional EGC beyond 4.0: add 0.25 allowance per EGC based on the largest EGC.

---

## 3. Related Modules

- Box calculations build upon conductor sizing established in [[branch-circuit-sizing]].
- Automated web evaluation tool located at `tools/web/box-fill.html`.
