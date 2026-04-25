#!/usr/bin/env python3
"""
Batch 3 Rule 9 regression: CUT reference as optional heuristic.

Verifies:
1. require_cut_reference=False (default): code without CUT ref -> PASS
2. require_cut_reference=True: code without CUT ref -> FAIL
3. require_cut_reference=False: code with CUT ref -> PASS
4. require_cut_reference=True: code with CUT ref -> PASS
"""
import sys
from pathlib import Path

_RUNNER_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_RUNNER_ROOT))
from runner import validate_test_code

PKG = "org.templateit"
CUT = "Bar"  # Use CUT not in class name (RegionTest contains "Region")
CLASS = "RegionTest"

# Valid test but no CUT reference (tests something else - e.g. utility)
CODE_NO_CUT = f"""package {PKG};
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class {CLASS} {{
  @Test void testX() {{ assertTrue(true); }}
}}
"""

# Valid test with CUT reference
CODE_WITH_CUT = f"""package {PKG};
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class {CLASS} {{
  @Test void testX() {{ Bar r = new Bar(); assertTrue(r != null); }}
}}
"""


def main():
    print("=== Batch 3 Rule 9: CUT Reference Heuristic Regression ===\n")

    # 1. Default (require_cut_reference=False): no CUT ref -> PASS
    ok1, _ = validate_test_code(CODE_NO_CUT, CLASS, CUT, PKG)
    print(f"  1. Default, no CUT ref: {'PASS' if ok1 else 'FAIL'}")

    # 2. require_cut_reference=True: no CUT ref -> FAIL
    ok2, r2 = validate_test_code(CODE_NO_CUT, CLASS, CUT, PKG, require_cut_reference=True)
    print(f"  2. require_cut_reference=True, no CUT ref: {'FAIL' if not ok2 else 'PASS (unexpected)'}")

    # 3. Default: with CUT ref -> PASS
    ok3, _ = validate_test_code(CODE_WITH_CUT, CLASS, CUT, PKG)
    print(f"  3. Default, with CUT ref: {'PASS' if ok3 else 'FAIL'}")

    # 4. require_cut_reference=True: with CUT ref -> PASS
    ok4, _ = validate_test_code(CODE_WITH_CUT, CLASS, CUT, PKG, require_cut_reference=True)
    print(f"  4. require_cut_reference=True, with CUT ref: {'PASS' if ok4 else 'FAIL'}")

    passed = sum([ok1, not ok2, ok3, ok4])
    print(f"\n  {passed}/4 passed")
    return 0 if passed == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
