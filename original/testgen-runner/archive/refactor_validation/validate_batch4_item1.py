#!/usr/bin/env python3
"""
Batch 4 Item 1 regression: get_failed_test_names method name matching.

Verifies:
1. testAdd style -> extracts testAdd
2. shouldClampZeroValues style -> extracts shouldClampZeroValues
3. testSomething_123 style -> extracts testSomething_123
4. Compile failure: RegionTest.java:7 -> NOT extracted as method 'java'
"""
import sys
from pathlib import Path

_RUNNER_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_RUNNER_ROOT))
from runner import get_failed_test_names, extract_methods_by_name


def main():
    print("=== Batch 4 Item 1: get_failed_test_names Regression ===\n")

    cases = [
        (
            "testAdd style",
            ["CalculatorTest.testAdd: expected 5 but was 3"],
            {"testAdd"},
        ),
        (
            "shouldClampZeroValues style",
            ["RegionTest.shouldClampZeroValues:42 expected 0 but was 1"],
            {"shouldClampZeroValues"},
        ),
        (
            "testSomething_123 style",
            ["RegionTest.testSomething_123:10 expected X but was Y"],
            {"testSomething_123"},
        ),
        (
            "Compile failure (java:line) - must NOT extract 'java'",
            ["[unresolved_symbol] RegionTest.java:7: cannot find symbol"],
            set(),  # empty - no test method names from compile failures
        ),
        (
            "runtime_error format",
            ["[runtime_error] CalculatorTest.testDiv:38 unexpected exception"],
            {"testDiv"},
        ),
        (
            "mixed: testAdd + shouldReturn",
            [
                "CalculatorTest.testAdd: expected 5 but was 3",
                "RegionTest.shouldReturnEmpty:15 expected X but was Y",
            ],
            {"testAdd", "shouldReturnEmpty"},
        ),
    ]

    ok_count = 0
    for name, failures, expected in cases:
        got = get_failed_test_names(failures)
        match = got == expected
        status = "OK" if match else "FAIL"
        if match:
            ok_count += 1
        print(f"  {status}: {name}")
        if not match:
            print(f"         expected {expected}, got {got}")

    # Item 3: verify extract_methods_by_name works with non-test-prefix
    java_with_should = """
package org.templateit;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class RegionTest {
  @Test
  void shouldClampZeroValues() { assertEquals(0, 0); }
  @Test
  void testAdd() { assertEquals(5, 5); }
}
"""
    extracted = extract_methods_by_name(java_with_should, {"shouldClampZeroValues"})
    has_should = "shouldClampZeroValues" in extracted and "testAdd" not in extracted
    print(f"  {'OK' if has_should else 'FAIL'}: extract_methods_by_name with shouldClampZeroValues")
    if has_should:
        ok_count += 1

    print(f"\n  {ok_count}/{len(cases) + 1} passed")
    return 0 if ok_count == len(cases) + 1 else 1


if __name__ == "__main__":
    sys.exit(main())
