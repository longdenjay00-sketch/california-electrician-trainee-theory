"""
tests/test_check_vault.py

Pytest suite validating tools/check_vault.py against all failure modes:
- Missing or malformed frontmatter (source, last-verified, prereqs)
- Broken wikilinks
- Missing worked solutions in exercises
- Quoting >25 consecutive words from /vault/_sources
- Full integration check on the active repo
"""

import sys
from pathlib import Path
import pytest

# Ensure tools module can be imported
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.check_vault import (
    check_frontmatter,
    check_wikilinks,
    check_exercises,
    check_note_quotes,
    build_source_ngrams,
    build_valid_targets,
    run_checks,
    LintError,
)


def test_frontmatter_valid():
    lines = [
        "---\n",
        'source: "NEC Table 310.16"\n',
        'last-verified: "2026-11-06"\n',
        "prereqs:\n",
        "  - [[grounding-vs-bonding]]\n",
        "---\n",
        "# Valid Note\n",
    ]
    errors = check_frontmatter(Path("vault/test.md"), lines, "vault/test.md")
    assert errors == []


def test_frontmatter_missing_opening_delimiter():
    lines = [
        'source: "NEC 250"\n',
        'last-verified: "2026-11-06"\n',
        "prereqs: []\n",
        "---\n",
    ]
    errors = check_frontmatter(Path("vault/test.md"), lines, "vault/test.md")
    assert len(errors) == 1
    assert "missing opening '---'" in errors[0].message
    assert errors[0].line_number == 1


def test_frontmatter_missing_closing_delimiter():
    lines = [
        "---\n",
        'source: "NEC 250"\n',
        'last-verified: "2026-11-06"\n',
        "prereqs: []\n",
        "# Content without closing\n",
    ]
    errors = check_frontmatter(Path("vault/test.md"), lines, "vault/test.md")
    assert len(errors) == 1
    assert "unclosed YAML frontmatter" in errors[0].message


def test_frontmatter_missing_required_keys():
    # Lacks 'prereqs' and 'last-verified'
    lines = [
        "---\n",
        'source: "NEC 250"\n',
        "---\n",
        "# Content\n",
    ]
    errors = check_frontmatter(Path("vault/test.md"), lines, "vault/test.md")
    assert len(errors) == 2
    messages = [e.message for e in errors]
    assert any("last-verified" in m for m in messages)
    assert any("prereqs" in m for m in messages)


def test_wikilinks_valid_and_broken():
    valid_targets = {"grounding-vs-bonding", "branch-circuit-sizing"}
    lines = [
        "# Branch Circuits\n",
        "Valid link: [[grounding-vs-bonding]].\n",
        "Valid link with anchor and label: [[branch-circuit-sizing#sec-1|Sizing Rule]].\n",
        "Broken link here: [[non-existent-note]].\n",
    ]
    errors = check_wikilinks(Path("vault/test.md"), lines, "vault/test.md", valid_targets)
    assert len(errors) == 1
    assert errors[0].line_number == 4
    assert "broken wikilink '[[non-existent-note]]'" in errors[0].message


def test_exercises_valid():
    lines = [
        "# Exercises\n",
        "## Problem 1: Easy\n",
        "Calculate 120.0 V / 10.0 A = 12.0 ohms.\n",
        "- **Worked Solution:**\n",
        "  1. Step one.\n",
        "## Problem 2: Medium\n",
        "Continuous load.\n",
        "- Worked solution:\n",
        "  1. 16.0 A * 1.25 = 20.0 A.\n",
    ]
    errors = check_exercises(Path("exercises/test.md"), lines, "exercises/test.md")
    assert errors == []


def test_exercises_missing_worked_solution():
    lines = [
        "# Exercises\n",
        "## Problem 1: Easy\n",
        "Calculate 120.0 V / 10.0 A.\n",
        "- **Worked Solution:**\n",
        "  1. Step one.\n",
        "## Problem 2: Medium\n",
        "What is the ampacity?\n",
        "Answer is 20.0 A.\n",  # No worked solution!
    ]
    errors = check_exercises(Path("exercises/test.md"), lines, "exercises/test.md")
    assert len(errors) == 1
    assert errors[0].line_number == 6
    assert "exercise lacks a worked solution" in errors[0].message


def test_exercises_file_with_no_problems():
    lines = [
        "# Exercises Intro\n",
        "This file has general remarks but no problem definitions.\n",
    ]
    errors = check_exercises(Path("exercises/test.md"), lines, "exercises/test.md")
    assert len(errors) == 1
    assert "contains no problem definitions" in errors[0].message


def test_quoting_detection_over_25_words(tmp_path):
    # Create mock _sources directory with 30 words
    sources_dir = tmp_path / "_sources"
    sources_dir.mkdir()
    source_words = [f"token{i}" for i in range(30)]
    source_file = sources_dir / "statute.txt"
    source_file.write_text(" ".join(source_words), encoding="utf-8")

    ngrams = build_source_ngrams(sources_dir, n=26)
    assert len(ngrams) == 5  # 30 - 26 + 1 = 5

    # Case 1: Note quotes exactly 25 words -> MUST PASS
    pass_lines = [
        "# Note\n",
        " ".join(source_words[:25]) + "\n",
    ]
    pass_errors = check_note_quotes(
        tmp_path / "note_pass.md", pass_lines, "vault/note_pass.md", ngrams, n=26
    )
    assert pass_errors == []

    # Case 2: Note quotes 26 consecutive words -> MUST FAIL
    fail_lines = [
        "# Note\n",
        "Line two introductory text.\n",
        " ".join(source_words[2:28]) + "\n",
    ]
    fail_errors = check_note_quotes(
        tmp_path / "note_fail.md", fail_lines, "vault/note_fail.md", ngrams, n=26
    )
    assert len(fail_errors) == 1
    assert fail_errors[0].line_number == 3
    assert "quotes more than 25 consecutive words" in fail_errors[0].message


def test_run_checks_on_live_repository():
    # The active repo must pass all checks cleanly
    errors = run_checks(REPO_ROOT)
    assert errors == [], f"Repository failed integrity check: {[str(e) for e in errors]}"
