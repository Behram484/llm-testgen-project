#!/usr/bin/env python3
"""
Batch 3 Item 1 regression: Rule 5/6 qualified assertion false-positive fix.

Verifies:
- Assertions.assertEquals(...) without static import -> PASS
- Assertions.assertThrows(...) without static import -> PASS
- assertEquals(...) without static import -> FAIL
- assertThrows(...) without static import -> FAIL
"""
import sys
from pathlib import Path

_RUNNER_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_RUNNER_ROOT))
from runner import validate_test_code


def main():
    print("=== Batch 3 Item 1: Rule 5/6 Regression ===\n")

    base = "package org.templateit;\nimport org.junit.jupiter.api.Test;\nclass RegionTest {\n  @Test void testX() {\n"
    suffix = "\n  }\n}"

    cases = [
        ("Assertions.assertEquals (no static import)", base + "Assertions.assertEquals(1, 1);" + suffix, True),
        ("Assertions.assertThrows (no static import)", base + "Assertions.assertThrows(RuntimeException.class, () -> {});" + suffix, True),
        ("assertEquals (no static import)", base + "assertEquals(1, 1);" + suffix, False),
        ("assertThrows (no static import)", base + "assertThrows(RuntimeException.class, () -> {});" + suffix, False),
    ]

    ok_count = 0
    for name, code, expect_pass in cases:
        ok, reasons = validate_test_code(code, "RegionTest", "Region", "org.templateit")
        match = (expect_pass and ok) or (not expect_pass and not ok and any("Missing static import" in r for r in reasons))
        status = "OK" if match else "FAIL"
        if match:
            ok_count += 1
        print(f"  {status}: {name}")
        if not match:
            print(f"         expected pass={expect_pass}, got ok={ok}, reasons={reasons}")

    print(f"\n{ok_count}/{len(cases)} passed")
    return 0 if ok_count == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
