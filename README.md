# California Electrician Trainee Theory

A structured, open-source theoretical curriculum and rigorous problem repository designed for California Electrician Trainees (ETs) preparing for state certification under the Department of Industrial Relations (DIR) and Division of Labor Standards Enforcement (DLSE).

---

## The Rung Map

Progress follows an unbroken learning pipeline from initial comprehension to mastery:

```
read ───► download ───► practice ───► fix ───► contribute ───► teach
```

| Rung | Phase | Action | Criteria |
| :--- | :--- | :--- | :--- |
| **1. Read** | Concept Intake | Study atomic theory notes in `/vault` | Understand code scope, definitions, and formulas. |
| **2. Download** | Local Harness | Clone or sync locally into Termux / Linux | Offline access to obsidian notes and automated test tooling. |
| **3. Practice** | Drills | Work graded problems in `/exercises` | Solve 3 tiers per concept: Easy, Medium, and Trap. |
| **4. Fix** | Error Analysis | Debug calculation mismatches | Track weak spots against official NEC / CEC articles. |
| **5. Contribute** | Upstream Quality | Submit code updates via PR or issue | File `stale-reg` or `unclear-note` tickets; submit fixes. |
| **6. Teach** | Mastery | Guide apprentices on job sites and forums | Articulate code rules succinctly without reading text verbatim. |

---

## Repository Structure

```
.
├── vault/          # Atomic Markdown notes with YAML frontmatter & [[wikilinks]]
│   └── _sources/   # Upstream reference digests (strictly quoted under 25 words)
├── exercises/      # 3 graded problems per concept (Easy, Medium, Trap) + worked solutions
├── progress/       # Curriculum roadmaps, checklists, and competency trackers
├── docs/           # State certification requirements, study paths, and trade formulas
├── tools/          # Verification scripts (check_vault.py linter)
└── tests/          # Pytest suite validating test harness and vault integrity
```

---

## Pedagogical Standard

1. **Vault Constraint:** No concept is tested in `/exercises` that is not formally defined in `/vault`.
2. **Three-Tier Problem Design:**
   - **Easy:** Direct formula or table lookup.
   - **Medium:** Multi-step calculation with derating or adjustment factors.
   - **Trap:** Real-world constraint (e.g., continuous duty 125%, terminal temp limits 110.14(C), ambient derating).
3. **Rigorous Units:** Units are required on every single number (`240 V`, `16 A`, `3840 VA`).
4. **Citation Over Quotation:** We cite code references (e.g., `NEC 210.19(A)(1)`, `CEC Table 310.16`). We never copy copyrighted code text verbatim.

---

## Tooling & CI Verification

Integrity is enforced automatically on push via `tools/check_vault.py` and GitHub Actions:
- Frontmatter validation (`source`, `last-verified`, `prereqs`).
- Dead [[wikilink]] detection.
- Missing worked solution detection.
- Plagiarism/over-quoting guard (>25 consecutive words from `/vault/_sources`).

Run checks locally:
```bash
python tools/check_vault.py
pytest tests/
```

---

## Licenses

- Educational Content: [Creative Commons Attribution-ShareAlike 4.0 International](LICENSE)
- Automation & Code: [MIT License](CODE-LICENSE)
