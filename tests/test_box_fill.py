"""
tests/test_box_fill.py

Unit and parity tests for box fill calculations.
Verifies Python engine against tests/cases.json and triggers Node parity check.
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_FILE = REPO_ROOT / "tests" / "cases.json"
NODE_PARITY_SCRIPT = REPO_ROOT / "tests" / "test_box_fill_parity.js"

sys.path.insert(0, str(REPO_ROOT))
from tools.box_fill import calculate_box_fill, VOLUME_PER_CONDUCTOR_CU_IN


def test_volume_per_conductor_constants():
    # Table 314.16(B) verified constants
    assert VOLUME_PER_CONDUCTOR_CU_IN["18"] == 1.50
    assert VOLUME_PER_CONDUCTOR_CU_IN["16"] == 1.75
    assert VOLUME_PER_CONDUCTOR_CU_IN["14"] == 2.00
    assert VOLUME_PER_CONDUCTOR_CU_IN["12"] == 2.25
    assert VOLUME_PER_CONDUCTOR_CU_IN["10"] == 2.50
    assert VOLUME_PER_CONDUCTOR_CU_IN["8"] == 3.00
    assert VOLUME_PER_CONDUCTOR_CU_IN["6"] == 5.00


def test_python_cases_json_compliance():
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)["box_fill"]

    for case in cases:
        case_id = case["id"]
        result = calculate_box_fill(case["input"])
        expected = case["expected"]
        assert result["total_cu_in"] == expected["total_cu_in"], f"{case_id} cu in mismatch"
        assert result["total_cm3"] == expected["total_cm3"], f"{case_id} cm3 mismatch"
        assert len(result["breakdown"]) == expected["breakdown_count"], f"{case_id} breakdown mismatch"


def test_node_parity_execution():
    """Runs tests/test_box_fill_parity.js and asserts exit code 0."""
    result = subprocess.run(
        ["node", str(NODE_PARITY_SCRIPT)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Node parity failed:\n{result.stderr}\n{result.stdout}"
    assert "SUCCESS: JS calculation in box-fill.html matches Python reference with 100% parity." in result.stdout
