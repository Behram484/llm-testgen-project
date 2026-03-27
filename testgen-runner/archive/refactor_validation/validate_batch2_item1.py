#!/usr/bin/env python3
"""
Batch 2 Item 1 sample-level validation.
Verifies: parse_surefire_failures, classify_failures, is_compile_failure, build_failure_diagnosis.
"""
import sys
from pathlib import Path

_RUNNER_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_RUNNER_ROOT))
from runner import (
    parse_surefire_failures,
    classify_failures,
    is_compile_failure,
    build_failure_diagnosis,
    COMPILE_FAILURE_PREFIXES,
)

# --- Sample Maven outputs ---
SAMPLE_UNRESOLVED = """
[ERROR] /path/RegionTest.java:[12,9] cannot find symbol
  symbol:   class Reference
  location: class org.templateit.RegionTest
"""
# method_signature_mismatch: has unsupported_sig but NOT required/found (wrong_method_call takes precedence when both exist)
SAMPLE_SIGNATURE_MISMATCH = """
[ERROR] /path/RegionTest.java:[15,20] method getArea in class Region cannot be applied to given types;
  reason: wrong number of arguments; expected 2 but got 3
"""
SAMPLE_STATIC_REF = """
[ERROR] /path/RegionTest.java:[12,9] non-static method getArea(int,int) cannot be referenced from a static context
[ERROR] /path/RegionTest.java:[14,9] non-static method getArea(int,int) cannot be referenced from a static context
"""
SAMPLE_ASSERT = """
RegionTest.testArea:42 expected:<10> but was:<0>
"""


def main():
    print("=== Batch 2 Item 1 Sample Validation ===\n")

    # 1. COMPILE_FAILURE_PREFIXES
    print("1. COMPILE_FAILURE_PREFIXES:")
    for p in COMPILE_FAILURE_PREFIXES:
        print(f"   - {p}")
    assert "[unresolved_symbol]" in COMPILE_FAILURE_PREFIXES
    assert "[method_signature_mismatch]" in COMPILE_FAILURE_PREFIXES
    assert "[missing_import]" not in COMPILE_FAILURE_PREFIXES
    assert "[unsupported_signature]" not in COMPILE_FAILURE_PREFIXES
    print("   OK: new tags present, old tags removed\n")

    # 2. parse_surefire_failures
    print("2. parse_surefire_failures output:")
    for name, mvn in [
        ("unresolved_symbol", "COMPILATION ERROR\n" + SAMPLE_UNRESOLVED),
        ("method_signature_mismatch", "COMPILATION ERROR\n" + SAMPLE_SIGNATURE_MISMATCH),
        ("static_reference", "COMPILATION ERROR\n" + SAMPLE_STATIC_REF),
        ("assert", SAMPLE_ASSERT),
    ]:
        failures = parse_surefire_failures(mvn)
        print(f"   {name}: {failures[:1]!r}...")
        if "unresolved" in name:
            assert any("[unresolved_symbol]" in f for f in failures)
        elif "signature" in name:
            assert any("[method_signature_mismatch]" in f for f in failures)
        elif "static" in name:
            assert any("[static_reference]" in f for f in failures)
        elif "assert" in name:
            assert any("expected" in f and "actual" in f for f in failures)
    print("   OK: parser produces correct tags\n")

    # 3. classify_failures (with cut_class_name for CUT-aware diagnosis)
    print("3. classify_failures output:")
    failures_unres = parse_surefire_failures("COMPILATION ERROR\n" + SAMPLE_UNRESOLVED)
    failures_sig = parse_surefire_failures("COMPILATION ERROR\n" + SAMPLE_SIGNATURE_MISMATCH)
    failures_static = parse_surefire_failures("COMPILATION ERROR\n" + SAMPLE_STATIC_REF)
    cls_unres = classify_failures(failures_unres, "Region")
    cls_sig = classify_failures(failures_sig, "Region")
    cls_static = classify_failures(failures_static, "Region")
    for c in cls_unres:
        print(f"   unresolved: type={c.failure_type}, action={c.suggested_action[:60]}...")
        assert c.failure_type == "unresolved_symbol"
    for c in cls_sig:
        print(f"   signature:  type={c.failure_type}, action={c.suggested_action[:60]}...")
        assert c.failure_type == "method_signature_mismatch"
    for c in cls_static:
        print(f"   static_ref: type={c.failure_type}, action={c.suggested_action[:70]}...")
        assert c.failure_type == "static_reference"
        assert "Region" in c.suggested_action and "Calculator" not in c.suggested_action
    print("   OK: classifier maps to correct failure_type; static_reference uses cut_class_name\n")

    # 4. is_compile_failure
    print("4. is_compile_failure:")
    assert is_compile_failure(failures_unres)
    assert is_compile_failure(failures_sig)
    assert not is_compile_failure(parse_surefire_failures(SAMPLE_ASSERT))
    print("   OK: compile vs semantic correctly identified\n")

    # 5. build_failure_diagnosis
    print("5. build_failure_diagnosis:")
    diag = build_failure_diagnosis(cls_unres + cls_sig)
    print("   " + diag.replace("\n", "\n   "))
    assert "[unresolved_symbol]" in diag
    assert "[method_signature_mismatch]" in diag
    print("   OK: diagnosis text includes new tags\n")

    print("=== All validations passed ===")


if __name__ == "__main__":
    main()
