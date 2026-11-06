# Contributing to California Electrician Trainee Theory

We welcome contributions to strengthen California Electrician Trainee (ET) curriculum, practice problems, and reference documentation.

---

## 1. Core Principles

1. **No Direct NEC Reproduction:**
   Never copy or reproduce raw National Electrical Code (NEC / NFPA 70) or California Electrical Code (CEC / Title 24, Part 3) text. Reference articles, sections, and tables by official citation only (e.g., `NEC 250.66`, `CEC Table 310.16`).
2. **Units on Every Number:**
   Every physical quantity, numeric answer, and intermediate calculation must include explicit SI or US customary units (e.g., `120 V`, `15 A`, `1800 VA`, `0.75 in`, `75 °C`). Bare numbers are rejected.
3. **Problem Structure:**
   When adding exercises for any concept, provide exactly three graded problems:
   - **Easy:** Direct definition or single-step formula evaluation.
   - **Medium:** Standard trade calculation involving derating, adjustment, or table cross-referencing.
   - **Trap:** A realistic real-world or exam question containing an edge case (e.g., continuous load 125% rule, ambient temp correction, terminal temperature limitations 110.14(C)).
4. **Worked Solutions:**
   Every problem must be accompanied by an unambiguous worked solution demonstrating the mathematical steps and citations.

---

## 2. Vault Note Standards

Every note inside `/vault` must contain complete YAML frontmatter:

```yaml
---
source: "CEC 2022 / NEC 2020 Article 250.66"
last-verified: "2026-11-06"
prereqs:
  - "[[grounding-vs-bonding]]"
---
```

- `source`: Valid official code standard, bulletin, or curriculum citation.
- `last-verified`: ISO date (`YYYY-MM-DD`) when the citation was last confirmed against current California regulations.
- `prereqs`: List of prerequisite wikilinks (`[[note-name]]`). Broken wikilinks fail CI checks.
- Length restriction: Quoting more than 25 consecutive words from any reference document in `/vault/_sources` is forbidden.

---

## 3. Pull Request Workflow

1. Fork the repository and create a topical branch (`git checkout -b fix/table-310-16-temp`).
2. Verify all vault integrity checks pass locally:
   ```bash
   python tools/check_vault.py
   pytest tests/
   ```
3. Commit with atomic commit messages (one-line subject, blank line, one-line body).
4. Open a Pull Request referencing any related issues.
