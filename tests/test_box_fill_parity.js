#!/usr/bin/env node
/**
 * tests/test_box_fill_parity.js
 *
 * Asserts parity between JavaScript engine in tools/web/box-fill.html
 * and Python reference implementation in tools/box_fill.py across all
 * cases defined in tests/cases.json.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execFileSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const CASES_FILE = path.join(REPO_ROOT, 'tests', 'cases.json');
const HTML_FILE = path.join(REPO_ROOT, 'tools', 'web', 'box-fill.html');
const PY_SCRIPT = path.join(REPO_ROOT, 'tools', 'box_fill.py');

// 1. Load test cases
const rawCases = fs.readFileSync(CASES_FILE, 'utf8');
const testCases = JSON.parse(rawCases).box_fill;

// 2. Extract and evaluate JS from tools/web/box-fill.html
const htmlContent = fs.readFileSync(HTML_FILE, 'utf8');
const scriptMatch = htmlContent.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/i);
if (!scriptMatch) {
  console.error('FAIL: No <script> block found in box-fill.html');
  process.exit(1);
}

const sandbox = { module: { exports: {} }, console };
vm.createContext(sandbox);
vm.runInContext(scriptMatch[1], sandbox);

const jsEngine = sandbox.module.exports;
if (typeof jsEngine.calculateBoxFill !== 'function') {
  console.error('FAIL: calculateBoxFill is not exported from box-fill.html');
  process.exit(1);
}

console.log(`Loaded ${testCases.length} test cases from ${path.basename(CASES_FILE)}`);

let passedCount = 0;
let failedCount = 0;

for (const testCase of testCases) {
  const { id, description, input, expected } = testCase;

  // Execute JavaScript calculation
  const jsResult = jsEngine.calculateBoxFill(input);

  // Execute Python calculation via CLI
  const pyOutput = execFileSync('python3', [PY_SCRIPT, '--json', JSON.stringify(input)], {
    encoding: 'utf8'
  });
  const pyResult = JSON.parse(pyOutput);

  // Assert Parity: JS vs Python
  const errors = [];
  if (jsResult.total_cu_in !== pyResult.total_cu_in) {
    errors.push(`Total cu in mismatch: JS=${jsResult.total_cu_in} vs PY=${pyResult.total_cu_in}`);
  }
  if (jsResult.total_cm3 !== pyResult.total_cm3) {
    errors.push(`Total cm3 mismatch: JS=${jsResult.total_cm3} vs PY=${pyResult.total_cm3}`);
  }
  if (jsResult.breakdown.length !== pyResult.breakdown.length) {
    errors.push(`Breakdown length mismatch: JS=${jsResult.breakdown.length} vs PY=${pyResult.breakdown.length}`);
  } else {
    for (let i = 0; i < jsResult.breakdown.length; i++) {
      const jsRow = jsResult.breakdown[i];
      const pyRow = pyResult.breakdown[i];
      if (jsRow.total_vol_cu_in !== pyRow.total_vol_cu_in) {
        errors.push(`Row ${i} vol mismatch: JS=${jsRow.total_vol_cu_in} vs PY=${pyRow.total_vol_cu_in}`);
      }
    }
  }

  // Assert against expected baseline
  if (expected) {
    if (jsResult.total_cu_in !== expected.total_cu_in) {
      errors.push(`Expected cu in mismatch: got ${jsResult.total_cu_in}, expected ${expected.total_cu_in}`);
    }
    if (jsResult.total_cm3 !== expected.total_cm3) {
      errors.push(`Expected cm3 mismatch: got ${jsResult.total_cm3}, expected ${expected.total_cm3}`);
    }
  }

  if (errors.length > 0) {
    console.error(`[FAIL] ${id}: ${description}`);
    errors.forEach(e => console.error(`  - ${e}`));
    failedCount++;
  } else {
    console.log(`[PASS] ${id} -> ${jsResult.total_cu_in} cu in (${jsResult.total_cm3} cm³)`);
    passedCount++;
  }
}

console.log(`\nSummary: ${passedCount} passed, ${failedCount} failed.`);
if (failedCount > 0) {
  process.exit(1);
} else {
  console.log('SUCCESS: JS calculation in box-fill.html matches Python reference with 100% parity.');
}
