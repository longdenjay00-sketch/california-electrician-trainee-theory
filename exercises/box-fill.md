# Box Fill Calculations — Exercises

Practice calculations for box volume requirements under CEC 2022 / NEC 2020 Article 314.16. Theoretical basis defined in [[box-fill]].

---

## Problem 1: Easy

A single-gang device box contains two 14/2 with ground Nonmetallic-Sheathed (NM) cables, one single-pole toggle switch, two internal cable clamps, and an equipment grounding conductor splice. What is the total minimum volume required for the enclosure in cubic inches?

- **Answer:** 16.0 cu in
- **Worked Solution:**
  1. Conductor count per NEC 314.16(B)(1): 4.0 insulated #14 AWG conductors entering box. $4.0 \times 2.00\text{ cu in} = 8.00\text{ cu in}$.
  2. Clamp allowance per NEC 314.16(B)(2): Internal clamps present count as 1.0 allowance based on largest conductor (#14 AWG). $1.0 \times 2.00\text{ cu in} = 2.00\text{ cu in}$.
  3. Device allowance per NEC 314.16(B)(4): One switch yoke counts as 2.0 allowances based on #14 AWG. $2.0 \times 2.00\text{ cu in} = 4.00\text{ cu in}$.
  4. Grounding allowance per NEC 314.16(B)(5): Two #14 AWG EGCs count as 1.0 allowance based on largest EGC (#14 AWG). $1.0 \times 2.00\text{ cu in} = 2.00\text{ cu in}$.
  5. Total calculation: $8.00\text{ cu in} + 2.00\text{ cu in} + 4.00\text{ cu in} + 2.00\text{ cu in} = 16.00\text{ cu in}$.

---

## Problem 2: Medium

A two-gang metal device box with internal clamps houses three 14/2 NM cables and two 12/2 NM cables. The box contains one duplex receptacle wired to #12 AWG and one single-pole switch wired to #14 AWG. All grounding conductors are spliced together. Calculate the total required box volume in cubic inches.

- **Answer:** 34.56 cu in
- **Worked Solution:**
  1. Conductor fill per NEC 314.16(B)(1): Six #14 AWG conductors ($6.0 \times 2.00\text{ cu in} = 12.00\text{ cu in}$) plus four #12 AWG conductors ($4.0 \times 2.25\text{ cu in} = 9.00\text{ cu in}$). Conductor subtotal: 21.00 cu in.
  2. Clamp fill per NEC 314.16(B)(2): Internal clamps present count as 1.0 allowance based on largest conductor present in the box (#12 AWG: 2.25 cu in). Subtotal: 2.25 cu in.
  3. Device fill per NEC 314.16(B)(4): Switch yoke on #14 AWG counts as $2.0 \times 2.00\text{ cu in} = 4.00\text{ cu in}$. Receptacle yoke on #12 AWG counts as $2.0 \times 2.25\text{ cu in} = 4.50\text{ cu in}$. Device subtotal: 8.50 cu in.
  4. Grounding fill per NEC 314.16(B)(5): Total 5.0 EGCs (three #14 AWG and two #12 AWG). Largest EGC is #12 AWG (2.25 cu in). Base allowance for first 4.0 EGCs is 1.0; fifth EGC adds 0.25 allowance. Total multiplier: $1.25 \times 2.25\text{ cu in} = 2.81\text{ cu in}$ (rounded to two decimal places).
  5. Total calculation: $21.00\text{ cu in} + 2.25\text{ cu in} + 8.50\text{ cu in} + 2.81\text{ cu in} = 34.56\text{ cu in}$.

---

## Problem 3: Trap

An electrician is roughing in a four-square junction box containing eight #12 AWG THHN conductors entering via EMT (no internal clamps). Four conductors pass straight through without splice; four conductors are spliced together. Two 6.0 in #12 AWG equipment grounding pigtails connect from the box ground screw to the splice. Six #12 AWG equipment grounding conductors enter the box. What is the total box volume required, and what is the trap regarding the pigtails and extra grounds?

- **Answer:** 21.38 cu in
- **Worked Solution:**
  1. Conductor fill per NEC 314.16(B)(1): 4.0 spliced conductors + 4.0 through conductors = 8.0 conductors total. $8.0 \times 2.25\text{ cu in} = 18.00\text{ cu in}$.
  2. Pigtail trap per NEC 314.16(B)(1): Pigtails originating and terminating entirely within the box count as 0.0 volume allowance. Do not add conductor volume for either ground pigtail or circuit pigtail.
  3. Clamp fill per NEC 314.16(B)(2): External EMT connectors contain no internal clamps; count is 0.0 cu in.
  4. Device fill per NEC 314.16(B)(4): Junction box contains no yokes/straps; count is 0.0 cu in.
  5. Grounding fill trap per NEC 314.16(B)(5): Six #12 AWG EGCs enter the box. Under NEC 2020 / CEC 2022, up to 4.0 EGCs count as 1.0 allowance ($1.0 \times 2.25\text{ cu in} = 2.25\text{ cu in}$). Each additional EGC over 4.0 adds a 0.25 allowance ($2.0 \times 0.25 = 0.50$ allowance, or $0.50 \times 2.25\text{ cu in} = 1.13\text{ cu in}$). Total ground multiplier is $1.50 \times 2.25\text{ cu in} = 3.38\text{ cu in}$.
  6. Total calculation: $18.00\text{ cu in} + 3.38\text{ cu in} = 21.38\text{ cu in}$. Standard 4 x 2-1/8 in square box (30.30 cu in per Table 314.16(A)) is required.
