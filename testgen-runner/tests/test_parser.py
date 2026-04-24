"""
Unit tests for parse_surefire_failures, extract_test_methods, validate_test_code.

Maven snippets are shaped to match the current regexes in runner.py.
Run: python -m unittest tests.test_parser -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Repo root (parent of tests/)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from runner import (  # noqa: E402
    build_failure_family_key,
    build_sticky_failure_key,
    clean_special_tokens,
    extract_test_methods,
    normalize_failure_line_for_sticky_key,
    parse_surefire_failures,
    validate_test_code,
)


# --- Realistic Maven / Surefire-style fixtures ---

MVN_COMPILE_UNRESOLVED = """
[INFO] -------------------------------------------------------------
[ERROR] COMPILATION ERROR :
[INFO] -------------------------------------------------------------
[ERROR] /home/user/proj/src/test/java/org/demo/FooTest.java:[22,13] cannot find symbol
  symbol:   method bar()
  location: variable x of type org.demo.Foo
[INFO] 1 error
[INFO] BUILD FAILURE
"""

MVN_COMPILE_WRONG_TYPES = """
[ERROR] COMPILATION ERROR :
[ERROR] D:\\\\proj\\\\src\\\\test\\\\java\\\\org\\\\demo\\\\FooTest.java:[14,9] error: incompatible types
  required: int
  found:    java.lang.String
"""

MVN_COMPILE_SIGNATURE_MISMATCH = """
[ERROR] COMPILATION ERROR :
[ERROR] /x/CalcTest.java:[8,5] error: cannot be applied to given types;
  reason: no unique maximal instance exists for type variable T
"""

MVN_ASSERT_EQUALS = """
[INFO] Running org.example.CalcTest
[ERROR] Tests run: 2, Failures: 1
CalcTest.testAdd:42 expected: <2> but was: <3>
"""

MVN_ASSERT_THROWS = """
RegionTest.testBoundary:12 Expected java.lang.IllegalArgumentException to be thrown, but nothing was thrown
"""

MVN_RUNTIME_ERROR = """
CalculatorTest.testDiv:38 ? ArithmeticException / by zero
"""

MVN_UNRESOLVED_COMPILATION = """\
FooTest.<init>:5 Unresolved compilation problems:
	The method undefined() is undefined for the type Bar
	The type Baz cannot be resolved
"""

MVN_SUCCESS_NO_FAILURES = """
[INFO] BUILD SUCCESS
[INFO] Total time: 3.456 s
"""

MVN_NO_PARSE_COMPILE = """
[ERROR] Some random failure without Test.java location markers
[ERROR] COMPILATION ERROR :
"""

# --- New fixtures for robustness tests ---

# Bug 1a: relative path (no leading slash) with bracket coords
MVN_COMPILE_RELATIVE_PATH = """
[ERROR] COMPILATION ERROR :
[ERROR] FooTest.java:[22,13] cannot find symbol
  symbol:   method bar()
  location: variable x of type org.demo.Foo
"""

# Bug 1b: javac native format — colon-separated, no brackets
MVN_COMPILE_JAVAC_NATIVE = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/FooTest.java:22: error: cannot find symbol
  symbol:   method bar()
"""

# Bug 1c: COMPILATION ERROR present but completely unrecognised format
MVN_COMPILE_NO_LOCATION = """
[ERROR] COMPILATION ERROR :
[ERROR] Some opaque error message with no file reference
"""

# Bug 2: Surefire 3.x splits method name and assertion onto separate lines
MVN_SUREFIRE3_ASSERTION = """
[INFO] Running org.example.CalcTest
[ERROR] CalcTest.testAdd -- Time elapsed: 0.01 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <2> but was: <3>
[ERROR] Tests run: 1, Failures: 1
"""

# Bug 3: expected/actual values contain '>' (generic type)
MVN_ASSERT_GENERIC_VALUE = """
CalcTest.testMap:10 expected: <Map<String,Integer>{a=1}> but was: <{}>
"""

# Bug 4: Windows encoding variants for the runtime-error separator
MVN_RUNTIME_DOUBLE_ARROW = """
CalculatorTest.testDiv:38 >> ArithmeticException / by zero
"""
MVN_RUNTIME_GUILLEMET = """
CalculatorTest.testDiv:38 \u00bb ArithmeticException / by zero
"""

# Bug 5: Unresolved compilation problem block indented with spaces (not tabs)
MVN_UNRESOLVED_SPACES = """\
FooTest.<init>:5 Unresolved compilation problems:
    The method undefined() is undefined for the type Bar
    The type Baz cannot be resolved
"""

# Windows CRLF line endings
MVN_CRLF_ASSERT = (
    "[INFO] Running org.example.CalcTest\r\n"
    "CalcTest.testAdd:42 expected: <2> but was: <3>\r\n"
)

# Real log: Surefire 3.x <<< ERROR! (NoClassDefFoundError — Calculator actual log)
MVN_SUREFIRE3_CLASS_ERROR = """\
[ERROR] Tests run: 1, Failures: 0, Errors: 1, Skipped: 0, Time elapsed: 0.037 s <<< FAILURE! -- in calculator.CalculatorTest
[ERROR] calculator.CalculatorTest -- Time elapsed: 0.037 s <<< ERROR!
java.lang.NoClassDefFoundError: Calculator
\tat java.base/java.lang.Class.getDeclaredFields0(Native Method)
Caused by: java.lang.ClassNotFoundException: Calculator
[ERROR] Errors:
[ERROR]   CalculatorTest ? NoClassDefFound Calculator
[ERROR] Tests run: 1, Failures: 0, Errors: 1, Skipped: 0
"""

# Real log: java.lang.Error: Unresolved compilation problems (no <init>: prefix)
MVN_JAVALANGERROR_UNRESOLVED = """\
[ERROR] org.RegionTest.testContainsWhenReferenceIsOutside -- Time elapsed: 0.038 s <<< ERROR!
java.lang.Error: \nUnresolved compilation problems: \n\tReference cannot be resolved to a type\n\tRegion cannot be resolved to a type\n
\tat org.RegionTest.testContainsWhenReferenceIsOutside(RegionTest.java:21)
[ERROR]   RegionTest.testContainsWhenReferenceIsOutside:21  Unresolved compilation problems:
\tReference cannot be resolved to a type
\tRegion cannot be resolved to a type
"""

# Surefire 3.x: no duplicate when two-line path and summary-line both hit same failure
MVN_SUREFIRE3_NO_DUPLICATE = """\
[ERROR] org.ReferenceTest.testFoo -- Time elapsed: 0.016 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <true> but was: <false>
\tat org.ReferenceTest.testFoo(ReferenceTest.java:28)
[ERROR] Failures:
[ERROR]   ReferenceTest.testFoo:28 expected: <true> but was: <false>
"""


class TestStickyFailureKey(unittest.TestCase):
    """Regression: sticky key stable when only line numbers / values change."""

    def test_assert_mismatch_ignores_line_and_values(self) -> None:
        a = "- CalcTest.testAdd:42 expected 2, but actual was 3"
        b = "- CalcTest.testAdd:99 expected 9, but actual was 8"
        self.assertEqual(
            build_sticky_failure_key([a]),
            build_sticky_failure_key([b]),
        )
        # Exact full-text key would differ; sticky is what drives regen with same_sticky_count.
        self.assertNotEqual("|".join(sorted([a])), "|".join(sorted([b])))

    def test_unresolved_symbol_java_line_normalized(self) -> None:
        a = "- [unresolved_symbol] FooTest.java:22: cannot find symbol"
        b = "- [unresolved_symbol] FooTest.java:99: cannot find symbol"
        self.assertEqual(build_sticky_failure_key([a]), build_sticky_failure_key([b]))

    def test_sticky_key_includes_failure_count_suffix(self) -> None:
        one = build_sticky_failure_key(["- [runtime_error] X:1: y"])
        two = build_sticky_failure_key(
            ["- [runtime_error] X:1: y", "- [runtime_error] Z:2: w"]
        )
        self.assertTrue(one.endswith("|n=1"), one)
        self.assertTrue(two.endswith("|n=2"), two)
        self.assertNotEqual(one, two)

    def test_empty_sticky_uses_hash_so_different_raw_differs(self) -> None:
        # Whitespace-only lines normalize to empty; raw payload differs -> different h
        k1 = build_sticky_failure_key([" "])
        k2 = build_sticky_failure_key(["  "])
        self.assertTrue(k1.startswith("empty_sticky|"), k1)
        self.assertTrue(k2.startswith("empty_sticky|"), k2)
        self.assertNotEqual(k1, k2)

    def test_empty_sticky_same_raw_same_key(self) -> None:
        self.assertEqual(build_sticky_failure_key([" \t"]), build_sticky_failure_key([" \t"]))

    def test_wrong_method_call_same_family_after_normalize(self) -> None:
        a = "- [wrong_method_call] FooTest:8 method add - required int,int but found String"
        b = "- [wrong_method_call] FooTest:15 method add - required long,long but found Object"
        self.assertEqual(
            build_sticky_failure_key([a]),
            build_sticky_failure_key([b]),
        )

    def test_normalize_strips_java_path_and_bracket_coords(self) -> None:
        raw = (
            "[ERROR] D:\\\\proj\\\\FooTest.java:[14,9] error: cannot find symbol"
        )
        n = normalize_failure_line_for_sticky_key(raw)
        self.assertNotIn("14", n)
        self.assertNotIn("9", n)
        self.assertIn("[#,#]", n)


class TestParseSurefireFailures(unittest.TestCase):
    def test_compile_unresolved_symbol(self) -> None:
        out = parse_surefire_failures(MVN_COMPILE_UNRESOLVED)
        self.assertTrue(out, "expected at least one failure line")
        self.assertTrue(any("[unresolved_symbol]" in f for f in out), out)

    def test_compile_wrong_method_call_required_found(self) -> None:
        out = parse_surefire_failures(MVN_COMPILE_WRONG_TYPES)
        self.assertTrue(any("[wrong_method_call]" in f for f in out), out)

    def test_compile_method_signature_mismatch(self) -> None:
        out = parse_surefire_failures(MVN_COMPILE_SIGNATURE_MISMATCH)
        self.assertTrue(any("[method_signature_mismatch]" in f for f in out), out)

    def test_assert_equals(self) -> None:
        out = parse_surefire_failures(MVN_ASSERT_EQUALS)
        self.assertEqual(len(out), 1)
        self.assertIn("CalcTest.testAdd", out[0])
        self.assertIn("expected 2", out[0])
        self.assertIn("actual was 3", out[0])

    def test_assert_throws_nothing_thrown(self) -> None:
        out = parse_surefire_failures(MVN_ASSERT_THROWS)
        self.assertEqual(len(out), 1)
        self.assertIn("RegionTest.testBoundary", out[0])
        self.assertIn("IllegalArgumentException", out[0])

    def test_runtime_error_question_mark(self) -> None:
        out = parse_surefire_failures(MVN_RUNTIME_ERROR)
        self.assertEqual(len(out), 1)
        self.assertIn("[runtime_error]", out[0])
        self.assertIn("CalculatorTest.testDiv", out[0])
        self.assertIn("ArithmeticException", out[0])

    def test_unresolved_compilation_problem_block(self) -> None:
        out = parse_surefire_failures(MVN_UNRESOLVED_COMPILATION)
        self.assertTrue(out)
        self.assertTrue(all("[unresolved_symbol]" in f for f in out), out)
        self.assertTrue(any("undefined()" in f for f in out), out)

    def test_build_success_empty(self) -> None:
        self.assertEqual(parse_surefire_failures(MVN_SUCCESS_NO_FAILURES), [])

    def test_compile_section_but_no_test_java_marker_returns_generic_fallback(self) -> None:
        """COMPILATION ERROR present but no parseable location → generic [compile_error] fallback."""
        out = parse_surefire_failures(MVN_NO_PARSE_COMPILE)
        self.assertEqual(len(out), 1, out)
        self.assertIn("[compile_error]", out[0])

    # --- Bug 1: compile_loc path-format robustness ---

    def test_compile_relative_path_no_leading_slash(self) -> None:
        """FooTest.java:[line,col] without a preceding directory separator."""
        out = parse_surefire_failures(MVN_COMPILE_RELATIVE_PATH)
        self.assertTrue(out, "expected at least one failure line")
        self.assertTrue(any("[unresolved_symbol]" in f for f in out), out)

    def test_compile_javac_native_colon_format(self) -> None:
        """/path/FooTest.java:22: error: … (no square brackets)."""
        out = parse_surefire_failures(MVN_COMPILE_JAVAC_NATIVE)
        self.assertTrue(out, "expected at least one failure line")
        self.assertTrue(
            any("[unresolved_symbol]" in f or "[compile_error]" in f for f in out), out
        )

    # --- Bug 2: Surefire 3.x multi-line assertion ---

    def test_surefire3_assertion_split_across_lines(self) -> None:
        """Surefire 3 puts method name on one line and assertion detail on the next."""
        out = parse_surefire_failures(MVN_SUREFIRE3_ASSERTION)
        self.assertEqual(len(out), 1, out)
        self.assertIn("CalcTest.testAdd", out[0])
        self.assertIn("expected 2", out[0])
        self.assertIn("actual was 3", out[0])

    # --- Bug 3: values containing '>' ---

    def test_assert_equals_generic_value_not_truncated(self) -> None:
        """Expected/actual values with embedded '>' (generics) must not be truncated."""
        out = parse_surefire_failures(MVN_ASSERT_GENERIC_VALUE)
        self.assertEqual(len(out), 1, out)
        self.assertIn("Map<String,Integer>", out[0])
        self.assertIn("actual was {}", out[0])

    # --- Bug 4: Windows encoding variants for runtime-error separator ---

    def test_runtime_error_double_arrow_separator(self) -> None:
        """Separator '>>' (common on Windows console) must match."""
        out = parse_surefire_failures(MVN_RUNTIME_DOUBLE_ARROW)
        self.assertEqual(len(out), 1, out)
        self.assertIn("[runtime_error]", out[0])
        self.assertIn("ArithmeticException", out[0])

    def test_runtime_error_guillemet_separator(self) -> None:
        """Separator '»' (Unicode U+00BB) must match."""
        out = parse_surefire_failures(MVN_RUNTIME_GUILLEMET)
        self.assertEqual(len(out), 1, out)
        self.assertIn("[runtime_error]", out[0])
        self.assertIn("ArithmeticException", out[0])

    # --- Bug 5: Unresolved compilation problem with space indentation ---

    def test_unresolved_compilation_problem_space_indent(self) -> None:
        """Symbol lines indented with spaces (not tabs) must be captured."""
        out = parse_surefire_failures(MVN_UNRESOLVED_SPACES)
        self.assertTrue(out, out)
        self.assertTrue(all("[unresolved_symbol]" in f for f in out), out)
        self.assertTrue(any("undefined()" in f for f in out), out)

    # --- CRLF line endings ---

    def test_crlf_line_endings_normalised(self) -> None:
        """Windows \\r\\n line endings must not break assertion parsing."""
        out = parse_surefire_failures(MVN_CRLF_ASSERT)
        self.assertEqual(len(out), 1, out)
        self.assertIn("CalcTest.testAdd", out[0])
        self.assertIn("expected 2", out[0])

    # --- Real log format tests ---

    def test_surefire3_class_level_error_noclassdef(self) -> None:
        """<<< ERROR! (not FAILURE!) class-level error must produce a [runtime_error] entry."""
        out = parse_surefire_failures(MVN_SUREFIRE3_CLASS_ERROR)
        self.assertTrue(out, "expected at least one failure")
        self.assertTrue(any("[runtime_error]" in f for f in out), out)
        self.assertTrue(any("CalculatorTest" in f for f in out), out)
        self.assertTrue(any("NoClassDefFoundError" in f or "class-level error" in f for f in out), out)

    def test_javalangerror_unresolved_compilation_problems(self) -> None:
        """java.lang.Error: Unresolved compilation problems without <init>: prefix."""
        out = parse_surefire_failures(MVN_JAVALANGERROR_UNRESOLVED)
        self.assertTrue(out, "expected at least one failure")
        self.assertTrue(any("[unresolved_symbol]" in f for f in out), out)
        self.assertTrue(any("Reference" in f or "Region" in f for f in out), out)

    def test_surefire3_no_duplicate_when_summary_line_also_matches(self) -> None:
        """Surefire 3.x two-line path + summary-line must not emit duplicate entries."""
        out = parse_surefire_failures(MVN_SUREFIRE3_NO_DUPLICATE)
        self.assertEqual(len(out), 1, f"expected exactly 1 failure, got: {out}")
        self.assertIn("expected true", out[0])
        self.assertIn("actual was false", out[0])

    def test_dedup_assert_equals_same_line(self) -> None:
        dup = MVN_ASSERT_EQUALS + "\n" + MVN_ASSERT_EQUALS.strip()
        out = parse_surefire_failures(dup)
        self.assertEqual(len(out), 1)


class TestExtractTestMethods(unittest.TestCase):
    def test_two_tests(self) -> None:
        java = """
package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class FooTest {
    @Test
    void testOne() {
        assertEquals(1, 1);
    }

    @Test
    void testTwo() {
        assertTrue(true);
    }
}
"""
        m = extract_test_methods(java)
        self.assertEqual(set(m), {"testOne", "testTwo"})
        self.assertIn("@Test", m["testOne"])
        self.assertIn("void testOne()", m["testOne"])
        self.assertIn("assertEquals(1, 1)", m["testOne"])

    def test_annotation_on_previous_line(self) -> None:
        java = """
public class XTest {
    @Test
    @DisplayName("x")
    void withMeta() {
        assertEquals(0, 0);
    }
}
"""
        m = extract_test_methods(java)
        self.assertIn("withMeta", m)
        self.assertIn("@DisplayName", m["withMeta"])

    def test_empty_no_tests(self) -> None:
        self.assertEqual(extract_test_methods("class NoTest {}"), {})


class TestCleanSpecialTokens(unittest.TestCase):
    def test_removes_ansi_cursor_sequences_from_ollama_output(self) -> None:
        java = (
            "package org.example;\n"
            "public class FooTest {\n"
            "  void t() {\n"
            "    Foo foo = new Foo()\x1b[5D\x1b[K\n"
            "Foo();\n"
            "  }\n"
            "}\n"
        )
        cleaned = clean_special_tokens(java)
        self.assertNotIn("\x1b", cleaned)
        self.assertNotIn("[5D", cleaned)
        self.assertNotIn("[K", cleaned)
        self.assertIn("Foo foo = new Foo();", cleaned)

    def test_preserves_newlines_tabs_and_unicode(self) -> None:
        java = "class X {\n\tString s = \"é\";\x07\n}\n"
        cleaned = clean_special_tokens(java)
        self.assertNotIn("\x07", cleaned)
        self.assertIn("\n\tString", cleaned)
        self.assertIn("\"é\"", cleaned)


class TestValidateTestCode(unittest.TestCase):
    def _valid_body(self) -> str:
        return """package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class CalcTest {
    @Test
    void adds() {
        assertEquals(2, 1 + 1);
    }
}
"""

    def test_valid_ok(self) -> None:
        ok, reasons = validate_test_code(
            self._valid_body(),
            "CalcTest",
            "Calculator",
            "org.example",
            require_cut_reference=False,
        )
        self.assertTrue(ok, reasons)
        self.assertEqual(reasons, [])

    def test_valid_with_cut_reference(self) -> None:
        code = self._valid_body().replace("1 + 1", "new Calculator().add(1, 1)")
        ok, reasons = validate_test_code(
            code,
            "CalcTest",
            "Calculator",
            "org.example",
            require_cut_reference=True,
        )
        self.assertTrue(ok, reasons)

    def test_missing_package(self) -> None:
        code = self._valid_body().replace("package org.example;\n\n", "")
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("package" in r for r in reasons))

    def test_wrong_class_name(self) -> None:
        ok, reasons = validate_test_code(
            self._valid_body(),
            "WrongName",
            "Calculator",
            "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("class declaration" in r for r in reasons))

    def test_missing_test_annotation(self) -> None:
        code = self._valid_body().replace("@Test", "")
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("@Test" in r for r in reasons))

    def test_missing_assertion(self) -> None:
        code = self._valid_body().replace("assertEquals(2, 1 + 1);", "// no assert")
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("assertion" in r.lower() for r in reasons))

    def test_assert_equals_without_static_import(self) -> None:
        code = """package org.example;
import org.junit.jupiter.api.Test;
public class CalcTest {
    @Test
    void adds() { assertEquals(2, 2); }
}
"""
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("static import" in r for r in reasons))

    def test_assertions_qualified_no_static_import_needed(self) -> None:
        code = """package org.example;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Assertions;
public class CalcTest {
    @Test
    void adds() { Assertions.assertEquals(2, 2); }
}
"""
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertTrue(ok, reasons)

    def test_require_cut_reference_missing(self) -> None:
        ok, reasons = validate_test_code(
            self._valid_body(),
            "CalcTest",
            "Calculator",
            "org.example",
            require_cut_reference=True,
        )
        self.assertFalse(ok)
        self.assertTrue(any("under test" in r for r in reasons))

    def test_banned_token(self) -> None:
        code = self._valid_body().replace("1 + 1", "1 + 1 // IntegerPointerException")
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("banned" in r for r in reasons))

    def test_markdown_fence_rejected(self) -> None:
        code = self._valid_body() + "\n// ```\n"
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("markdown" in r for r in reasons))

    def test_java_assert_rejected(self) -> None:
        # Validator matches Java assert with parentheses: assert (condition)
        code = self._valid_body().replace(
            "assertEquals(2, 1 + 1);",
            "assert (1 + 1 == 2);",
        )
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
        )
        self.assertFalse(ok)
        self.assertTrue(any("JUnit" in r for r in reasons), reasons)


    def test_allow_empty_passes_with_no_tests(self) -> None:
        """allow_empty=True: a compilable class with no @Test methods should pass validation."""
        code = """package org.example;

public class CalcTest {
}
"""
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
            allow_empty=True,
        )
        self.assertTrue(ok, reasons)
        self.assertEqual(reasons, [])

    def test_allow_empty_false_still_rejects_no_tests(self) -> None:
        """allow_empty=False (default): class without @Test must still be rejected."""
        code = """package org.example;

public class CalcTest {
}
"""
        ok, reasons = validate_test_code(
            code, "CalcTest", "Calculator", "org.example",
            allow_empty=False,
        )
        self.assertFalse(ok)
        self.assertTrue(any("@Test" in r or "assertion" in r for r in reasons), reasons)


if __name__ == "__main__":
    unittest.main()
