#!/usr/bin/env python3
"""
Batch 3 Item 2 (Rule 2) regression: class declaration check.

Verifies:
1. public class ExpectedName -> PASS
2. class ExpectedName -> PASS
3. ExpectedName only in comment/string, wrong class declared -> FAIL
4. Wrong class declared -> FAIL
5. public final class ExpectedName -> PASS
"""
import sys
from pathlib import Path

_RUNNER_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_RUNNER_ROOT))
from runner import validate_test_code

EXPECTED = "RegionTest"
PKG = "org.templateit"
CUT = "Region"

# Minimal valid body for pass cases
BODY = """
  @Test void testX() { Assertions.assertEquals(1, 1); }
"""


def main():
    print("=== Batch 3 Item 2: Rule 2 Class Declaration Regression ===\n")

    cases = [
        (
            "public class ExpectedName",
            f"package {PKG};\nimport org.junit.jupiter.api.Test;\npublic class {EXPECTED} {{\n{BODY}\n}}",
            True,
        ),
        (
            "class ExpectedName (package-private)",
            f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass {EXPECTED} {{\n{BODY}\n}}",
            True,
        ),
        (
            "ExpectedName only in comment, wrong class declared",
            f"package {PKG};\n// class {EXPECTED}\nimport org.junit.jupiter.api.Test;\nclass OtherTest {{\n{BODY}\n}}",
            False,
        ),
        (
            "Wrong class declared",
            f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass WrongTest {{\n{BODY}\n}}",
            False,
        ),
        (
            "public final class ExpectedName",
            f"package {PKG};\nimport org.junit.jupiter.api.Test;\npublic final class {EXPECTED} {{\n{BODY}\n}}",
            True,
        ),
    ]

    ok_count = 0
    for name, code, expect_pass in cases:
        ok, reasons = validate_test_code(code, EXPECTED, CUT, PKG)
        match = ok == expect_pass
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
