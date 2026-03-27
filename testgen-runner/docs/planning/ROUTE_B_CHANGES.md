# Route B: 再提智 (Improve Intelligence)

## 1. Failure Classifier

**Before:** `parse_surefire_failures()` returned raw strings like `"- CalculatorTest.testAdd: expected 4, but actual was 3"`.

**After:**
- Added `ClassifiedFailure` dataclass: `test_method`, `failure_type`, `wrong_expected`, `correct_actual`, `suggested_action`
- `classify_failures(failures)` → list of `ClassifiedFailure` with types:
  - `assert_mismatch`: expected vs actual
  - `wrong_exception`: expected exception but nothing thrown
  - `unknown`: fallback for unparsed formats
- `build_failure_diagnosis(classified)` → structured summary for prompt, e.g.:
  ```
  - testAdd [assert_mismatch]: Re-verify what behavior this test intends to validate; current assertion doesn't match runtime result; rewrite assertion based on CUT semantics. (actual observed: 3 — use as evidence, not as final answer)
  - testDiv [wrong_exception]: Re-verify what behavior this test intends to validate; current assertion expects an exception but none was thrown; rewrite assertion based on CUT semantics. (actual runtime: no exception — use as evidence)
  ```
- **Refinement**: Diagnosis centers on "re-verify behavior + rewrite based on CUT semantics", not "change expected to actual". `actual` is presented as evidence, not as the answer.

Repair and REGENERATE flows now pass `[failure_diagnosis]` to the prompt instead of raw failure text.

## 2. Shorten Passed Tests Hint

**Before:** `build_passed_tests_hint()` returned full method bodies for each passed test.

**After:** Returns only method names:
```
Passed tests (keep unchanged): testAdd, testClamp, testSubtract
```

`passed_methods` dict is still returned for `merge_passed_tests_into_output()` so correct code is preserved; the LLM no longer receives full passed code in the prompt.

## 3. Repair Prompt Reframe

**Before:** "Fix the failing tests" / "correct the failing assertions".

**After:** "Keep correct parts + strengthen tests for CUT behavior":
- Task: "strengthen it to properly verify the CUT (class under test) behavior"
- Focus: "For each failing test, ask: What CUT behavior is being tested? Then write an assertion that correctly verifies that behavior."
- Placeholder label: "Failure diagnosis (strengthen these tests for CUT behavior)"
- Closing: "Strengthen each failing test to properly verify the CUT behavior."

---

## Known Limitations / Risks (Route B)

1. **merge_passed_tests_into_output**: We reduced prompt pollution but still forcibly freeze passed code at post-processing. This is "减轻副作用", not "彻底解决结构冻结".

2. **suggested_action balance**: If diagnosis becomes too prescriptive (e.g. "remove assertThrows, use assertEquals"), the LLM may act as executor rather than analyzer. Current wording gives failure type + runtime phenomenon + evidence; model decides assertion form.

3. **unknown failure type**: Now refined in Route C — see `compile_error`, `wrong_method_call`, `missing_import`, `runtime_error`.

4. **Behavior-oriented repair vs generation**: Route B improves repair/regenerate; initial generation may still follow old habits (shallow happy path, weak assertions). Repair quality may improve before initial generation quality.
