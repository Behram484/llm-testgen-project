#!/usr/bin/env python3
"""
Batch 3 Item 3 regression: Broaden assertions + ensure_assert_imports alignment.

Verifies:
1. Assertions.assertTrue(...) no static import -> PASS
2. assertTrue(...) no static import -> PASS (ensure_assert_imports adds it)
3. Assertions.assertNotNull(...) no static import -> PASS
4. assertNotNull(...) no static import -> PASS (ensure_assert_imports adds it)
5. Assertions.fail(...) no static import -> PASS
6. Java assert(...) only, no JUnit assertion -> FAIL
"""
import sys
from pathlib import Path

_RUNNER_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_RUNNER_ROOT))
from runner import validate_test_code, ensure_assert_imports

PKG = "org.templateit"
CUT = "Region"
CLASS = "RegionTest"


def main():
    print("=== Batch 3 Item 3: Assertion + Import Regression ===\n")

    # 1. Assertions.assertTrue - no static import -> PASS
    c1 = f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass {CLASS} {{\n  @Test void testX() {{ Assertions.assertTrue(true); }}\n}}"
    ok1, _ = validate_test_code(c1, CLASS, CUT, PKG)
    print(f"  1. Assertions.assertTrue (no static import): {'PASS' if ok1 else 'FAIL'}")

    # 2. assertTrue - no static import -> ensure_assert_imports adds it, then validate passes
    c2_raw = f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass {CLASS} {{\n  @Test void testX() {{ assertTrue(true); }}\n}}"
    c2 = ensure_assert_imports(c2_raw)
    ok2, _ = validate_test_code(c2, CLASS, CUT, PKG)
    has_import = "import static org.junit.jupiter.api.Assertions.assertTrue" in c2
    print(f"  2. assertTrue (no static import) -> ensure_assert_imports adds it: {'PASS' if ok2 and has_import else 'FAIL'}")

    # 3. Assertions.assertNotNull - no static import -> PASS
    c3 = f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass {CLASS} {{\n  @Test void testX() {{ Assertions.assertNotNull(\"x\"); }}\n}}"
    ok3, _ = validate_test_code(c3, CLASS, CUT, PKG)
    print(f"  3. Assertions.assertNotNull (no static import): {'PASS' if ok3 else 'FAIL'}")

    # 4. assertNotNull - no static import -> ensure_assert_imports adds it
    c4_raw = f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass {CLASS} {{\n  @Test void testX() {{ assertNotNull(\"x\"); }}\n}}"
    c4 = ensure_assert_imports(c4_raw)
    ok4, _ = validate_test_code(c4, CLASS, CUT, PKG)
    has_import4 = "import static org.junit.jupiter.api.Assertions.assertNotNull" in c4
    print(f"  4. assertNotNull (no static import) -> ensure_assert_imports adds it: {'PASS' if ok4 and has_import4 else 'FAIL'}")

    # 5. Assertions.fail - no static import -> PASS
    c5 = f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass {CLASS} {{\n  @Test void testX() {{ Assertions.fail(\"not impl\"); }}\n}}"
    ok5, _ = validate_test_code(c5, CLASS, CUT, PKG)
    print(f"  5. Assertions.fail (no static import): {'PASS' if ok5 else 'FAIL'}")

    # 6. Java assert() only, no JUnit assertion -> FAIL
    c6 = f"package {PKG};\nimport org.junit.jupiter.api.Test;\nclass {CLASS} {{\n  @Test void testX() {{ assert 1 == 1; }}\n}}"
    ok6, _ = validate_test_code(c6, CLASS, CUT, PKG)
    print(f"  6. Java assert() only (no JUnit assertion): {'FAIL' if not ok6 else 'PASS (unexpected)'}")

    passed = sum([ok1, ok2 and has_import, ok3, ok4 and has_import4, ok5, not ok6])
    print(f"\n  {passed}/6 passed")
    return 0 if passed == 6 else 1


if __name__ == "__main__":
    sys.exit(main())
