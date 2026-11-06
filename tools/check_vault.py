#!/usr/bin/env python3
"""
tools/check_vault.py

Integrity validator for California Electrician Trainee Theory repository.
Enforces:
1. Every note in /vault has frontmatter keys: 'source', 'last-verified', 'prereqs'.
2. All [[wikilinks]] in /vault and /exercises resolve to existing notes.
3. Every exercise in /exercises includes a worked solution.
4. No note quotes >25 consecutive words from any source file in /vault/_sources.

Outputs errors strictly in 'file:line: message' format and returns non-zero on error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Set, Tuple

import yaml

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|\n#]+)(?:#[^\]|\n]+)?(?:\|[^\]|\n]+)?\]\]")
PROBLEM_HEADING_PATTERN = re.compile(
    r"^(#{1,6})\s+.*?\b(problem|exercise|drill)\b.*$", re.IGNORECASE
)
WORKED_SOLUTION_PATTERN = re.compile(r"\bworked\s+solution\b", re.IGNORECASE)
WORD_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
REQUIRED_FRONTMATTER_KEYS = {"source", "last-verified", "prereqs"}


class LintError(NamedTuple):
    file_path: str
    line_number: int
    message: str

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line_number}: {self.message}"


def extract_frontmatter(lines: List[str]) -> Tuple[dict | None, int, str | None]:
    """
    Extracts frontmatter dict, end line index (1-based), and error message if any.
    Returns (data, end_line, error).
    """
    if not lines or lines[0].strip() != "---":
        return None, 1, "missing opening '---' for YAML frontmatter"

    closing_idx = -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            closing_idx = idx
            break

    if closing_idx == -1:
        return None, 1, "unclosed YAML frontmatter (missing closing '---')"

    raw_yaml = "".join(lines[1:closing_idx])
    try:
        data = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as exc:
        err_line = 1
        if hasattr(exc, "problem_mark") and exc.problem_mark is not None:
            err_line = exc.problem_mark.line + 2
        return None, err_line, f"invalid YAML frontmatter: {exc}"

    if not isinstance(data, dict):
        return None, 1, "frontmatter must be a YAML mapping/dictionary"

    return data, closing_idx + 1, None


def check_frontmatter(file_path: Path, lines: List[str], rel_path: str) -> List[LintError]:
    """Validates required frontmatter keys."""
    errors: List[LintError] = []
    data, end_line, err = extract_frontmatter(lines)
    if err is not None:
        errors.append(LintError(rel_path, end_line if end_line else 1, err))
        return errors

    assert data is not None
    for key in sorted(REQUIRED_FRONTMATTER_KEYS):
        if key not in data or data[key] is None:
            errors.append(
                LintError(
                    rel_path,
                    1,
                    f"frontmatter missing required key '{key}'",
                )
            )

    return errors


def build_valid_targets(repo_root: Path) -> Set[str]:
    """Collects set of valid wikilink targets across the repository."""
    targets: Set[str] = set()
    vault_dir = repo_root / "vault"
    if not vault_dir.is_dir():
        return targets

    for md_file in vault_dir.rglob("*.md"):
        if "_sources" in md_file.parts:
            continue
        rel_from_vault = md_file.relative_to(vault_dir).as_posix()
        rel_from_root = md_file.relative_to(repo_root).as_posix()

        # Stem name (e.g. 'grounding-vs-bonding')
        targets.add(md_file.stem)
        # Relative paths with/without extension
        targets.add(rel_from_vault)
        if rel_from_vault.endswith(".md"):
            targets.add(rel_from_vault[:-3])
        targets.add(rel_from_root)
        if rel_from_root.endswith(".md"):
            targets.add(rel_from_root[:-3])

    return targets


def check_wikilinks(
    file_path: Path, lines: List[str], rel_path: str, valid_targets: Set[str]
) -> List[LintError]:
    """Finds any broken [[wikilinks]]."""
    errors: List[LintError] = []
    for line_idx, line in enumerate(lines, start=1):
        for match in WIKILINK_PATTERN.finditer(line):
            target = match.group(1).strip()
            # Normalize leading slash or whitespace
            target_norm = target.lstrip("/").strip()
            if target_norm.endswith(".md"):
                target_norm_no_ext = target_norm[:-3]
            else:
                target_norm_no_ext = target_norm

            if (
                target not in valid_targets
                and target_norm not in valid_targets
                and target_norm_no_ext not in valid_targets
            ):
                errors.append(
                    LintError(
                        rel_path,
                        line_idx,
                        f"broken wikilink '[[{target}]]'",
                    )
                )
    return errors


def check_exercises(file_path: Path, lines: List[str], rel_path: str) -> List[LintError]:
    """Ensures each exercise/problem section has a worked solution."""
    errors: List[LintError] = []
    problems: List[Tuple[int, int, str]] = []  # (line_idx, heading_level, heading_text)

    for line_idx, line in enumerate(lines, start=1):
        match = PROBLEM_HEADING_PATTERN.match(line)
        if match:
            heading_level = len(match.group(1))
            heading_text = line.strip()
            problems.append((line_idx, heading_level, heading_text))

    if not problems:
        errors.append(
            LintError(
                rel_path,
                1,
                "exercise file contains no problem definitions (expected '## Problem ...')",
            )
        )
        return errors

    for i, (p_line, p_level, p_text) in enumerate(problems):
        start_idx = p_line - 1
        end_idx = len(lines)
        for j in range(i + 1, len(problems)):
            next_line, next_level, _ = problems[j]
            if next_level <= p_level:
                end_idx = next_line - 1
                break

        section_text = "".join(lines[start_idx:end_idx])
        if not WORKED_SOLUTION_PATTERN.search(section_text):
            errors.append(
                LintError(
                    rel_path,
                    p_line,
                    f"exercise lacks a worked solution: '{p_text}'",
                )
            )

    return errors


def tokenize_words(text: str) -> List[str]:
    """Tokenize lowercase words."""
    return [m.group(0).lower() for m in WORD_TOKEN_PATTERN.finditer(text)]


def build_source_ngrams(sources_dir: Path, n: int = 26) -> Dict[Tuple[str, ...], str]:
    """
    Builds a dictionary of n-grams (default 26 words) from all files in /vault/_sources.
    Maps n-gram tuple -> source filename.
    """
    ngrams: Dict[Tuple[str, ...], str] = {}
    if not sources_dir.is_dir():
        return ngrams

    for source_file in sources_dir.rglob("*"):
        if source_file.is_file() and not source_file.name.startswith("."):
            try:
                content = source_file.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            words = tokenize_words(content)
            if len(words) >= n:
                for idx in range(len(words) - n + 1):
                    gram = tuple(words[idx : idx + n])
                    if gram not in ngrams:
                        ngrams[gram] = source_file.name
    return ngrams


def check_note_quotes(
    file_path: Path,
    lines: List[str],
    rel_path: str,
    source_ngrams: Dict[Tuple[str, ...], str],
    n: int = 26,
) -> List[LintError]:
    """
    Detects if note quotes >25 consecutive words from any source file.
    """
    errors: List[LintError] = []
    if not source_ngrams:
        return errors

    # Track words with line numbers
    words_with_lines: List[Tuple[str, int]] = []
    for line_idx, line in enumerate(lines, start=1):
        for match in WORD_TOKEN_PATTERN.finditer(line):
            words_with_lines.append((match.group(0).lower(), line_idx))

    if len(words_with_lines) < n:
        return errors

    reported_spans: Set[int] = set()
    for idx in range(len(words_with_lines) - n + 1):
        gram = tuple(w[0] for w in words_with_lines[idx : idx + n])
        if gram in source_ngrams:
            first_line = words_with_lines[idx][1]
            if first_line not in reported_spans:
                src_name = source_ngrams[gram]
                errors.append(
                    LintError(
                        rel_path,
                        first_line,
                        f"quotes more than 25 consecutive words from /vault/_sources/{src_name}",
                    )
                )
                reported_spans.add(first_line)

    return errors


def run_checks(repo_root: Path) -> List[LintError]:
    """Runs all checks across the repository and returns list of LintErrors."""
    errors: List[LintError] = []
    vault_dir = repo_root / "vault"
    exercises_dir = repo_root / "exercises"
    sources_dir = vault_dir / "_sources"

    valid_targets = build_valid_targets(repo_root)
    source_ngrams = build_source_ngrams(sources_dir, n=26)

    # 1. Check notes in /vault
    if vault_dir.is_dir():
        for note_file in sorted(vault_dir.rglob("*.md")):
            if "_sources" in note_file.parts:
                continue
            rel_path = note_file.relative_to(repo_root).as_posix()
            try:
                lines = note_file.read_text(encoding="utf-8").splitlines(keepends=True)
            except OSError as exc:
                errors.append(LintError(rel_path, 1, f"cannot read file: {exc}"))
                continue

            errors.extend(check_frontmatter(note_file, lines, rel_path))
            errors.extend(check_wikilinks(note_file, lines, rel_path, valid_targets))
            errors.extend(check_note_quotes(note_file, lines, rel_path, source_ngrams, n=26))

    # 2. Check exercises in /exercises
    if exercises_dir.is_dir():
        for ex_file in sorted(exercises_dir.rglob("*.md")):
            rel_path = ex_file.relative_to(repo_root).as_posix()
            try:
                lines = ex_file.read_text(encoding="utf-8").splitlines(keepends=True)
            except OSError as exc:
                errors.append(LintError(rel_path, 1, f"cannot read file: {exc}"))
                continue

            errors.extend(check_exercises(ex_file, lines, rel_path))
            errors.extend(check_wikilinks(ex_file, lines, rel_path, valid_targets))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify California Electrician Trainee Theory vault and exercises integrity."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Root path of repository (default: current directory)",
    )
    args = parser.parse_args()

    repo_root = args.root.resolve()
    errors = run_checks(repo_root)

    if errors:
        for err in errors:
            print(str(err), file=sys.stderr)
        print(f"\nFAIL: Found {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("PASS: Vault and exercises integrity verified successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
