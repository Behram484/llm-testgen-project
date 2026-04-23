import hashlib
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from mutant_summary import (
    build_mutation_summary,
    get_pit_class_report_path,
    get_pit_package_index_path,
    parse_mutation_score,
)


# -----------------------------
# Config model
# -----------------------------
@dataclass
class RunnerConfig:
    project_root: Path
    cut_path: Path
    test_output_path: Path
    model: str
    prompt_profile: str
    generation_profile: str
    mvn_cmd: str
    enable_programmatic_fix: bool
    regenerate_after_same_failures: int
    enable_mutation_augment: bool
    # Ablation toggles (see config.json)
    inject_method_signatures_in_prompts: bool
    enable_cut_api_prepass: bool
    enable_compile_failure_family_regen: bool
    # <= 0 disables timeout (not recommended for demos)
    mvn_timeout_sec: int
    # LLM subprocess timeout; <= 0 disables (not recommended)
    ollama_timeout_sec: int
    max_repair_attempts: int
    # "full" = write prompts/raw LLM/repair traces; "minimal" = skip those (smaller I/O)
    artifact_write_mode: str

    @staticmethod
    def load(path: Path) -> "RunnerConfig":
        data = json.loads(path.read_text(encoding="utf-8"))
        prompt_profile = data.get("prompt_profile", "baseline")
        max_rep = int(data.get("max_repair_attempts", 10))
        if max_rep < 1:
            max_rep = 1
        mode = str(data.get("artifact_write_mode", "full")).strip().lower()
        if mode not in ("full", "minimal"):
            mode = "full"
        return RunnerConfig(
            project_root=Path(data["project_root"]),
            cut_path=Path(data["cut_path"]),
            test_output_path=Path(data["test_output_path"]),
            model=data["model"],
            mvn_cmd=data["mvn_cmd"],
            prompt_profile=prompt_profile,
            generation_profile=data.get("generation_profile", prompt_profile),
            enable_programmatic_fix=data.get("enable_programmatic_fix", False),
            regenerate_after_same_failures=data.get("regenerate_after_same_failures", 2),
            enable_mutation_augment=data.get("enable_mutation_augment", False),
            inject_method_signatures_in_prompts=data.get(
                "inject_method_signatures_in_prompts", True
            ),
            enable_cut_api_prepass=data.get("enable_cut_api_prepass", True),
            enable_compile_failure_family_regen=data.get(
                "enable_compile_failure_family_regen", True
            ),
            mvn_timeout_sec=int(data.get("mvn_timeout_sec", 300)),
            ollama_timeout_sec=int(data.get("ollama_timeout_sec", 180)),
            max_repair_attempts=max_rep,
            artifact_write_mode=mode,
        )


# -----------------------------
# Helpers
# -----------------------------
def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def artifacts_verbose(cfg: RunnerConfig) -> bool:
    return cfg.artifact_write_mode == "full"


def write_llm_artifact(cfg: RunnerConfig, path: Path, content: str) -> None:
    """Prompt / raw LLM / repair traces. Skipped in minimal mode."""
    if not artifacts_verbose(cfg):
        return
    write_text(path, content)


def next_version(generated_dir: Path, cut_stem: str) -> int:
    """
    Scan generated_dir for files like CalculatorTest_v<number>.java and return next number.
    """
    prefix = f"{cut_stem}Test_v"
    generated_dir.mkdir(parents=True, exist_ok=True)
    max_v = 0
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)\.java$")
    for f in generated_dir.glob("*.java"):
        m = pattern.match(f.name)
        if m:
            max_v = max(max_v, int(m.group(1)))
    return max_v + 1


def get_last_successful_path(cut_path: Path, output_dir: Path) -> Path:
    """Derive last_successful/<TestClass>.java from CUT path."""
    cut_stem = cut_path.stem  # e.g. Calculator
    test_class = f"{cut_stem}Test"  # CalculatorTest
    return output_dir / "last_successful" / f"{test_class}.java"


def ensure_output_subdirs(output_dir: Path) -> None:
    """Create output subdirs for classified artifacts."""
    for sub in (
        "generated_tests",
        "prompt",
        "raw_llm",
        "repair_prompt",
        "raw_repair",
        "invalid_extracted",
        "invalid_reasons",
        "invalid_repaired",
        "invalid_repaired_reasons",
        "mutation_prompt",
        "raw_mutation",
        "logs",
        "logs/mvn_test_fail",
        "logs/pitest_fail",
        "summary",
        "last_successful",
    ):
        (output_dir / sub).mkdir(parents=True, exist_ok=True)


def build_prompt(
    template: str,
    code: str,
    test_class_name: str,
    failures: list[str] | None = None,
    failed_methods: str | None = None,
    successful_ref: str | None = None,
    passed_tests_hint: str | None = None,
    anti_stuck_hint: str | None = None,
    mutation_summary: str | None = None,
    current_test_class: str | None = None,
    package_name: str | None = None,
    dependency_code: str | None = None,
    method_signatures: str | None = None,
) -> str:
    out = template.replace("<CODE>", code)
    if "{DEPENDENCY}" in out:
        out = out.replace(
            "{DEPENDENCY}",
            dependency_code if dependency_code else "",
        )
    out = out.replace("{TEST_CLASS_NAME}", test_class_name)
    if "{PACKAGE}" in out:
        out = out.replace("{PACKAGE}", package_name if package_name else "")
    if "{METHOD_SIGNATURES}" in out:
        out = out.replace(
            "{METHOD_SIGNATURES}",
            method_signatures if method_signatures else "No public method signatures detected.",
        )
    if "{MUTATION_SUMMARY}" in out:
        out = out.replace(
            "{MUTATION_SUMMARY}",
            mutation_summary if mutation_summary else "No mutation feedback available.",
        )
    if "{CURRENT_TEST_CLASS}" in out:
        out = out.replace(
            "{CURRENT_TEST_CLASS}",
            current_test_class if current_test_class else "(no current test class)",
        )
    if "{FAILURES}" in out:
        if failures:
            out = out.replace("{FAILURES}", "\n".join(failures))
        else:
            out = out.replace(
                "{FAILURES}",
                "No specific failures. Generate comprehensive tests.",
            )
    if "{FAILED_METHODS}" in out:
        out = out.replace(
            "{FAILED_METHODS}",
            failed_methods if failed_methods else "(no previous attempt)",
        )
    if "{SUCCESSFUL_REFERENCE}" in out:
        out = out.replace(
            "{SUCCESSFUL_REFERENCE}",
            successful_ref if successful_ref else "No previous successful test available.",
        )
    if "{PASSED_TESTS_HINT}" in out:
        out = out.replace(
            "{PASSED_TESTS_HINT}",
            passed_tests_hint if passed_tests_hint else "No partial success yet.",
        )
    if "{ANTI_STUCK_HINT}" in out:
        out = out.replace(
            "{ANTI_STUCK_HINT}",
            anti_stuck_hint if anti_stuck_hint else "",
        )
    return out.strip() + "\n"


def parse_surefire_failures(mvn_output: str) -> list[str]:
    """
    Parse Maven output for test/compile failures.
    Extracts:
    1) Assertion: expected <X> but was <Y> (assertEquals)
    2) AssertThrows: Expected X to be thrown, but nothing was thrown
    3) Compile: COMPILATION ERROR with wrong_method_call, unresolved_symbol, method_signature_mismatch
    4) Runtime: test threw unexpected exception (e.g. ArithmeticException)

    Robustness notes:
    - compile_loc accepts paths with or without a leading slash/backslash, and also
      the bare javac format  File.java:line:  (no brackets).
    - Surefire 3.x splits "ClassName.method" and "expected: <X> but was: <Y>" onto
      separate lines; a two-line sliding window handles that.
    - Expected/actual values that contain '>' (e.g. generics) are captured correctly
      by a non-greedy match anchored at ' but was:'.
    - Runtime-error separator accepts '?', '>>', '»', or '--' variants.
    - Unresolved-compilation-problem blocks accept both tab and space indentation.
    - If COMPILATION ERROR is present but no structured location can be parsed, a
      generic [compile_error] fallback is emitted so the repair loop is never skipped.
    """
    # Normalise line endings once so all patterns use plain \n
    mvn_output = mvn_output.replace("\r\n", "\n").replace("\r", "\n")

    failures = []
    seen = set()

    # --- Compilation errors (before test run) ---
    if "COMPILATION ERROR" in mvn_output or "Compilation failure" in mvn_output:
        # Accept:
        #   /path/FooTest.java:[22,13]   (Unix, Surefire 2.x style)
        #   D:\path\FooTest.java:[22,13] (Windows absolute, Surefire 2.x)
        #   FooTest.java:[22,13]         (relative path, no leading sep)
        #   /path/FooTest.java:22:       (javac native, colon-separated)
        compile_loc = re.compile(
            r"(?:[/\\][^\s]*[/\\]|(?<![:\w]))(\w+Test)\.java:\[(\d+),\d+\]"
            r"|(?:[/\\][^\s]*[/\\]|(?<![:\w]))(\w+Test)\.java:(\d+):",
            re.IGNORECASE,
        )
        req_pattern = re.compile(r"(?:required|需要)[:\s]+([^\n]+)", re.I)
        fnd_pattern = re.compile(r"(?:found|找到)[:\s]+([^\n]+)", re.I)
        missing_sym = re.compile(
            r"cannot find symbol|does not exist|package .+ does not exist|找不到符号",
            re.IGNORECASE,
        )
        method_sig = re.compile(r"\b(\w+)\s*\([^)]*\)", re.I)
        unsupported_sig = re.compile(
            r"cannot be applied to given types|possible lossy conversion from double to int",
            re.IGNORECASE,
        )
        lines_arr = mvn_output.splitlines()
        line_blocks: dict[tuple[str, str], str] = {}
        for i, line in enumerate(lines_arr):
            loc = compile_loc.search(line)
            if not loc:
                continue
            # Group 1+2 are bracket-format; group 3+4 are colon-format
            fname = loc.group(1) or loc.group(3)
            line_no = loc.group(2) or loc.group(4)
            key = (fname, line_no)
            block = "\n".join(lines_arr[i : i + 6])
            if key not in line_blocks or method_sig.search(block):
                line_blocks[key] = block
        static_by_method: dict[tuple[str, str], list[int]] = {}
        for (fname, line_no), block in sorted(line_blocks.items(), key=lambda x: (x[0][0], int(x[0][1]))):
            method_match = method_sig.search(block)
            method = method_match.group(1) if method_match else "?"
            if missing_sym.search(block):
                failures.append(
                    f"- [unresolved_symbol] {fname}.java:{line_no}: {block.strip()[:120]}"
                )
            else:
                req_m = req_pattern.search(block)
                fnd_m = fnd_pattern.search(block)
                if req_m and fnd_m:
                    req, fnd = req_m.group(1).strip()[:30], fnd_m.group(1).strip()[:30]
                    failures.append(
                        f"- [wrong_method_call] {fname}:{line_no} method {method} - required {req} but found {fnd}"
                    )
                elif unsupported_sig.search(block):
                    failures.append(
                        f"- [method_signature_mismatch] {fname}.java:{line_no} method {method} - argument types or count do not match CUT method signature"
                    )
                elif method_sig.search(block):
                    static_by_method.setdefault((fname, method), []).append(int(line_no))
                else:
                    failures.append(
                        f"- [compile_error] {fname}.java:{line_no}: {block.strip()[:120]}"
                    )
        for (fname, method), lines in sorted(static_by_method.items(), key=lambda x: (x[0][0], x[0][1])):
            lines_sorted = sorted(set(lines))
            line_range = f"{lines_sorted[0]}-{lines_sorted[-1]}" if len(lines_sorted) > 1 else str(lines_sorted[0])
            failures.append(
                f"- [static_reference] {fname}.java:{line_range} method {method} - instance method called statically"
            )
        if failures:
            return failures
        # Fallback: COMPILATION ERROR present but no structured location parsed.
        # Emit a generic entry so the repair loop is never silently skipped.
        return ["- [compile_error] compilation failed: could not parse error location from Maven output"]

    # --- Unresolved compilation problems (Eclipse JDT reports these as runtime Errors) ---
    if "Unresolved compilation problem" in mvn_output:
        # Pattern A: summary section — TestClass.<init>:N or TestClass.methodName:N
        #   e.g.  RegionTest.testFoo:21  Unresolved compilation problems:\n\tXxx cannot be resolved
        # Pattern B: stacktrace section — java.lang.Error:\nUnresolved compilation problems:\n\t...
        #   (no method reference prefix at all)
        # Both accept tab or space indentation for the symbol lines (Bug 5 fix).
        unresolved_pat = re.compile(
            r"(\w+Test)\.(?:<init>|\w+):(\d+)\s+Unresolved compilation problems?:\s*\n((?:[ \t][^\n]+\n?)+)",
        )
        for m in unresolved_pat.finditer(mvn_output):
            fname = m.group(1)
            symbols = set()
            for sym_line in m.group(3).splitlines():
                sym_line = sym_line.strip()
                if sym_line and sym_line not in seen:
                    seen.add(sym_line)
                    symbols.add(sym_line)
            for sym in sorted(symbols):
                failures.append(f"- [unresolved_symbol] {fname}.java: {sym}")
        if not failures:
            # Pattern B: bare block without a method-reference header
            #   java.lang.Error: \nUnresolved compilation problems: \n\tFoo cannot be resolved
            unresolved_bare = re.compile(
                r"Unresolved compilation problems?:\s*\n((?:[ \t][^\n]+\n?)+)",
            )
            all_syms: set[str] = set()
            for m in unresolved_bare.finditer(mvn_output):
                for sym_line in m.group(1).splitlines():
                    sym_line = sym_line.strip()
                    if sym_line and sym_line not in seen:
                        seen.add(sym_line)
                        all_syms.add(sym_line)
            for sym in sorted(all_syms):
                failures.append(f"- [unresolved_symbol] {sym}")
        if failures:
            return failures

    # --- Test failures (assertEquals) ---
    # Capture expected/actual with a non-greedy match so values containing '>'
    # (e.g. generic types) are handled correctly.
    pattern_equals = re.compile(
        r"(\w+\.\w+):\d+\s+expected:\s*<(.+?)>\s+but was:\s*<(.+?)>",
        re.IGNORECASE,
    )
    # Surefire 3.x splits the method reference and the error onto separate lines:
    #   [ERROR] CalcTest.testAdd -- Time elapsed: 0.01 s <<< FAILURE!
    #   org.opentest4j.AssertionFailedError: expected: <2> but was: <3>
    # re.search tries at every start position, so (\w+\.\w+) will match the
    # rightmost "ClassName.methodName" segment regardless of package depth.
    pattern_surefire3_method = re.compile(
        r"(\w+\.\w+)\s+--\s+Time elapsed:.*<<<\s+FAILURE",
        re.IGNORECASE,
    )
    pattern_surefire3_assert = re.compile(
        r"expected:\s*<(.+?)>\s+but was:\s*<(.+?)>",
        re.IGNORECASE,
    )
    # Surefire 3.x class-level ERROR (e.g. NoClassDefFoundError, ExceptionInInitializerError):
    #   [ERROR] calculator.CalculatorTest -- Time elapsed: 0.037 s <<< ERROR!
    #   java.lang.NoClassDefFoundError: Calculator
    pattern_surefire3_error = re.compile(
        r"(\w+\.\w+)\s+--\s+Time elapsed:.*<<<\s+ERROR",
        re.IGNORECASE,
    )
    pattern_throws = re.compile(
        r"(\w+\.\w+):\d+\s+Expected\s+([\w.]+)\s+to be thrown,\s*but nothing was thrown",
        re.IGNORECASE,
    )
    # Runtime errors separator may be '?', '>>', '»', or '--' depending on
    # Maven/JVM version and console encoding.
    pattern_runtime_err = re.compile(
        r"(\w+\.\w+):(\d+)\s+(?:[?]|>>|»|--)\s+(\S.*)",
        re.IGNORECASE,
    )
    # Exception class on the line immediately following a <<< ERROR! header.
    pattern_exception_class = re.compile(r"^([\w.]+(?:Error|Exception)[^\s:]*)", re.IGNORECASE)

    lines_list = mvn_output.splitlines()
    pending_surefire3_method: str | None = None
    pending_surefire3_error_class: str | None = None  # class-level ERROR latch
    # Dedup by formatted output string (in addition to raw-match key) so that
    # Surefire 3.x two-line path and the summary-line single-line path don't
    # both emit the same failure string.
    emitted: set[str] = set()

    def _append(entry: str) -> None:
        if entry not in emitted:
            emitted.add(entry)
            failures.append(entry)

    for line in lines_list:
        # --- Surefire 3.x: latch on FAILURE or ERROR header line ---
        m_sf3_err = pattern_surefire3_error.search(line)
        if m_sf3_err:
            pending_surefire3_error_class = m_sf3_err.group(1)
            pending_surefire3_method = None
            continue

        m_sf3 = pattern_surefire3_method.search(line)
        if m_sf3:
            pending_surefire3_method = m_sf3.group(1)
            pending_surefire3_error_class = None
            continue

        # --- Class-level ERROR: extract exception from next non-empty line ---
        if pending_surefire3_error_class:
            stripped = line.strip()
            if stripped:
                exc_m = pattern_exception_class.match(stripped)
                exc = exc_m.group(1) if exc_m else stripped.split()[0]
                _append(
                    f"- [runtime_error] {pending_surefire3_error_class}: "
                    f"class-level error {exc} - check imports and class name"
                )
                pending_surefire3_error_class = None
            continue

        # --- Single-line Surefire 2.x assertion format ---
        m = pattern_equals.search(line)
        if m:
            key = m.group(0)
            if key not in seen:
                seen.add(key)
                _append(f"- {m.group(1)}: expected {m.group(2)}, but actual was {m.group(3)}")
            pending_surefire3_method = None
            continue

        # --- Surefire 3.x: assertion detail on the line after the FAILURE header ---
        if pending_surefire3_method:
            m_a = pattern_surefire3_assert.search(line)
            if m_a:
                key = f"{pending_surefire3_method}:{m_a.group(0)}"
                if key not in seen:
                    seen.add(key)
                    _append(
                        f"- {pending_surefire3_method}: expected {m_a.group(1)}, but actual was {m_a.group(2)}"
                    )
                pending_surefire3_method = None
                continue

        m2 = pattern_throws.search(line)
        if m2:
            key = m2.group(0)
            if key not in seen:
                seen.add(key)
                _append(
                    f"- {m2.group(1)}: Expected {m2.group(2)} to be thrown, but nothing was thrown. "
                    f"The test wrongly expects an exception - fix the assertion."
                )
            continue
        m3 = pattern_runtime_err.search(line)
        if m3:
            key = m3.group(0)
            if key not in seen:
                seen.add(key)
                _append(
                    f"- [runtime_error] {m3.group(1)}:{m3.group(2)}: unexpected exception {m3.group(3).strip()}"
                )
    return failures


@dataclass
class ClassifiedFailure:
    """Structured failure for diagnosis."""

    test_method: str
    failure_type: str  # assert_mismatch | wrong_exception | wrong_method_call | compile_error | unresolved_symbol | method_signature_mismatch | runtime_error | unknown
    wrong_expected: str
    correct_actual: str
    suggested_action: str


def classify_failures(failures: list[str], cut_class_name: str = "") -> list[ClassifiedFailure]:
    """
    Classify raw failures into structured diagnosis.
    Returns list of ClassifiedFailure with type and suggested action.
    cut_class_name: class under test (e.g. Region, Calculator) for CUT-aware diagnosis.
    """
    classified = []
    for f in failures:
        # wrong_method_call: [wrong_method_call] File:line method X - required A but found B
        m_wrong = re.search(r"\[wrong_method_call]\s+(\w+):(\d+)\s+method\s+(\w+).+required\s+(.+?)\s+but found\s+(.+)", f, re.I)
        if m_wrong:
            classified.append(
                ClassifiedFailure(
                    test_method=m_wrong.group(3),
                    failure_type="wrong_method_call",
                    wrong_expected=m_wrong.group(4).strip(),
                    correct_actual=m_wrong.group(5).strip(),
                    suggested_action=(
                        "Fix method call signature: check CUT method parameters. "
                        f"Required: {m_wrong.group(4).strip()}; found: {m_wrong.group(5).strip()}. "
                        "Align test invocation with CUT API."
                    ),
                )
            )
            continue
        # unresolved_symbol
        m_miss = re.search(r"\[unresolved_symbol]\s+(\w+)\.java:(\d+)", f, re.I)
        if m_miss:
            classified.append(
                ClassifiedFailure(
                    test_method="?",
                    failure_type="unresolved_symbol",
                    wrong_expected="",
                    correct_actual="",
                    suggested_action=f"Symbol not found or inaccessible. Check package, import, or visibility. {f.strip()[:80]}",
                )
            )
            continue
        # method_signature_mismatch: argument types or count do not match
        m_unsup = re.search(
            r"\[method_signature_mismatch]\s+\w+\.java:(\d+)\s+method\s+(\S+)\s+-",
            f,
            re.I,
        )
        if m_unsup:
            method = m_unsup.group(2)
            classified.append(
                ClassifiedFailure(
                    test_method="?",
                    failure_type="method_signature_mismatch",
                    wrong_expected="(argument type or count mismatch)",
                    correct_actual="(check CUT method signature)",
                    suggested_action=(
                        f"Method {method}: argument types or count do not match CUT signature. "
                        "Check CUT method parameters and fix the invocation."
                    ),
                )
            )
            continue
        # static_reference: instance method called statically
        m_static = re.search(
            r"\[static_reference]\s+\w+\.java:([\d-]+)\s+method\s+(\w+)\s+-\s+instance method called statically",
            f,
            re.I,
        )
        if m_static:
            method = m_static.group(2)
            cut = cut_class_name or "CUT"
            classified.append(
                ClassifiedFailure(
                    test_method="?",
                    failure_type="static_reference",
                    wrong_expected=f"{cut}.{method}(...)",
                    correct_actual=f"instance.{method}(...)",
                    suggested_action=(
                        f"Instance method {method} was called statically. "
                        f"Create or reuse an instance of {cut}, then call instance.{method}(...) instead of {cut}.{method}(...)."
                    ),
                )
            )
            continue
        # compile_error (generic)
        m_comp = re.search(r"\[compile_error]\s+(\w+)\.java:(\d+)", f, re.I)
        if m_comp:
            classified.append(
                ClassifiedFailure(
                    test_method="?",
                    failure_type="compile_error",
                    wrong_expected="",
                    correct_actual="",
                    suggested_action=f"Fix compilation error at line {m_comp.group(2)}. {f.strip()[:80]}",
                )
            )
            continue
        # runtime_error: test threw unexpected exception
        m_run = re.search(r"\[runtime_error]\s+(\w+\.\w+):(\d+):\s+unexpected exception\s+(.+)", f, re.I)
        if m_run:
            exc = m_run.group(3).strip()
            test_method = m_run.group(1).split(".")[-1]  # e.g. testDiv
            classified.append(
                ClassifiedFailure(
                    test_method=test_method,
                    failure_type="runtime_error",
                    wrong_expected="(no exception expected)",
                    correct_actual=exc,
                    suggested_action=(
                        "Test threw unexpected exception. "
                        f"Re-verify expected behavior for this input. "
                        f"If exception is expected (e.g. div-by-zero), use assertThrows. "
                        f"(exception: {exc[:60]})"
                    ),
                )
            )
            continue
        # assert_mismatch
        m = re.search(r"\w+\.(\w+):\s+expected\s+([^,]+),\s*but actual was\s+(\S+)", f, re.I)
        if m:
            actual = m.group(3).strip()
            classified.append(
                ClassifiedFailure(
                    test_method=m.group(1),
                    failure_type="assert_mismatch",
                    wrong_expected=m.group(2).strip(),
                    correct_actual=actual,
                    suggested_action=(
                        "Re-verify what behavior this test intends to validate; "
                        "current assertion doesn't match runtime result; "
                        "rewrite assertion based on CUT semantics. "
                        f"(actual observed: {actual} — use as evidence, not as final answer)"
                    ),
                )
            )
            continue
        # wrong_exception
        m2 = re.search(r"\w+\.(\w+):\s+Expected\s+([\w.]+)\s+to be thrown", f, re.I)
        if m2:
            classified.append(
                ClassifiedFailure(
                    test_method=m2.group(1),
                    failure_type="wrong_exception",
                    wrong_expected=m2.group(2),
                    correct_actual="(no exception)",
                    suggested_action=(
                        "Re-verify what behavior this test intends to validate; "
                        "current assertion expects an exception but none was thrown; "
                        "rewrite assertion based on CUT semantics. "
                        "(actual runtime: no exception — use as evidence)"
                    ),
                )
            )
            continue
        # Fallback: unknown
        m3 = re.search(r"\w+\.(\w+):", f)
        if m3:
            classified.append(
                ClassifiedFailure(
                    test_method=m3.group(1),
                    failure_type="unknown",
                    wrong_expected="",
                    correct_actual="",
                    suggested_action=f.strip().lstrip("- "),
                )
            )
        else:
            classified.append(
                ClassifiedFailure(
                    test_method="?",
                    failure_type="unknown",
                    wrong_expected="",
                    correct_actual="",
                    suggested_action=f.strip().lstrip("- "),
                )
            )
    return classified


def build_failure_diagnosis(classified: list[ClassifiedFailure]) -> str:
    """
    Build structured failure diagnosis for repair prompt.
    Replaces raw failure list with categorized, actionable summary.
    """
    if not classified:
        return "No failures parsed."
    lines = []
    for c in classified:
        lines.append(
            f"- {c.test_method} [{c.failure_type}]: {c.suggested_action}"
        )
    return "\n".join(lines)


def parse_assert_mismatch(failure_str: str) -> tuple[str, str, str] | None:
    """
    解析 "ClassName.methodName: expected X, but actual was Y" 格式。
    返回 (method_name, wrong_expected, correct_actual) 或 None。
    actual 捕获到行尾以支持含空格/逗号的值。
    """
    m = re.search(
        r"\w+\.(\w+):\s+expected\s+([^,]+),\s*but actual was\s+(.+?)$",
        failure_str,
        re.I | re.MULTILINE,
    )
    if m:
        return (m.group(1), m.group(2).strip(), m.group(3).strip())
    return None


def get_fix_pairs(failures: list[str]) -> list[tuple[str, str, str]]:
    """Extract (method_name, wrong_expected, correct_actual) for programmatic patch."""
    pairs = []
    for f in failures:
        parsed = parse_assert_mismatch(f)
        if parsed:
            pairs.append(parsed)
    return pairs


def apply_programmatic_fix(java_code: str, fix_pairs: list[tuple[str, str, str]]) -> str:
    """
    当 LLM 无法修复时，用失败信息中的正确值直接修补 assertEquals。
    只替换同时满足以下条件的断言：方法名匹配、期望值与 wrong_expected 完全相同。
    跳过 wrong_expected == correct_actual 的对（无需修改）。
    """
    if not fix_pairs:
        return java_code
    methods = extract_test_methods(java_code)
    out = java_code
    for method_name, wrong, correct in fix_pairs:
        # Guard: if failure reports same expected and actual, nothing to patch
        if wrong == correct:
            continue
        if method_name not in methods:
            continue
        method_code = methods[method_name]
        # Surgical replacement: only touch assertEquals where the first argument
        # matches wrong_expected exactly — leaves correct assertions untouched.
        new_method = re.sub(
            r"assertEquals\s*\(\s*" + re.escape(wrong) + r"\s*,",
            f"assertEquals({correct},",
            method_code,
            count=1,
        )
        if new_method != method_code:
            out = out.replace(method_code, new_method, 1)
    return out


def get_assert_mismatch_methods(failures: list[str]) -> set[str]:
    """Extract method names that have assert_mismatch (expected X, actual Y)."""
    names = set()
    for f in failures:
        parsed = parse_assert_mismatch(f)
        if parsed:
            names.add(parsed[0])
    return names


def apply_programmatic_fix_aggressive(
    java_code: str, fix_pairs: list[tuple[str, str, str]], method_names: set[str]
) -> str:
    """
    当 normal fix 因 wrong 值变化无法匹配时，对 stubborn 方法强制替换第一个 assertEquals 的 expected。
    用于同一方法连续多轮 assert_mismatch 但 expected 值被 LLM 改来改去的情况。
    """
    if not fix_pairs or not method_names:
        return java_code
    methods = extract_test_methods(java_code)
    out = java_code
    for method_name, _wrong, correct in fix_pairs:
        if method_name not in methods or method_name not in method_names:
            continue
        method_code = methods[method_name]
        # 替换第一个 assertEquals(任意值, 为 assertEquals(correct,
        new_method = re.sub(
            r"assertEquals\s*\(\s*[^,]+\s*,",
            f"assertEquals({correct},",
            method_code,
            count=1,
        )
        if new_method != method_code:
            out = out.replace(method_code, new_method, 1)
    return out


def build_correct_fix_hint(failures: list[str]) -> str:
    """
    From failures like 'testAdd: expected 1, but actual was 0', extract the correct expected value.
    When LLM is stuck, inject this to tell it the answer directly.
    """
    hints = []
    for f in failures:
        parsed = parse_assert_mismatch(f)
        if parsed:
            method, wrong_expected, correct_actual = parsed
            hints.append(f"- {method}: use assertEquals({correct_actual}, ...) NOT {wrong_expected}")
        m2 = re.search(r"(\w+)\.(\w+):\s+Expected\s+[\w.]+\s+to be thrown", f, re.I)
        if m2:
            method = m2.group(2)
            hints.append(f"- {method}: remove assertThrows, use assertEquals with the actual result")
    if not hints:
        return ""
    return "CORRECT FIX (use these values):\n" + "\n".join(hints)


COMPILE_FAILURE_PREFIXES = (
    "[compile_error]",
    "[static_reference]",
    "[method_signature_mismatch]",
    "[wrong_method_call]",
    "[unresolved_symbol]",
)


def is_compile_failure(failures: list[str]) -> bool:
    """
    True if any failure is a compile-type (we cannot extract test method names).
    When True: do not merge passed methods; treat passed_methods as empty.
    """
    for f in failures:
        for prefix in COMPILE_FAILURE_PREFIXES:
            if prefix in f:
                return True
    return False


def get_failed_test_names(failures: list[str]) -> set[str]:
    """
    Extract test method names from failure strings.
    Matches ClassNameTest.methodName: (any valid Java method name).
    Excludes 'java' to avoid misparsing CalculatorTest.java:7 as method 'java'.
    E.g. 'CalculatorTest.testAdd: ...' -> {'testAdd'},
         'RegionTest.shouldClampZeroValues:42' -> {'shouldClampZeroValues'}.
    """
    names = set()
    for f in failures:
        m = re.search(r"\w+Test\.([a-zA-Z_][a-zA-Z0-9_]*):", f)
        if m:
            method = m.group(1)
            if method != "java":  # avoid compile failure: File.java:line
                names.add(method)
    return names


def extract_public_method_names(java_code: str, cut_class_name: str) -> set[str]:
    """Extract public method names (including constructor) from CUT source."""
    pattern = re.compile(
        r"^\s*public\s+(?:static\s+|final\s+|synchronized\s+|abstract\s+|native\s+|strictfp\s+)*"
        r"([A-Za-z_][A-Za-z0-9_<>\[\], ?]*)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",
        re.MULTILINE,
    )
    names: set[str] = set()
    for m in pattern.finditer(java_code):
        ret_or_class = m.group(1).strip()
        name = m.group(2).strip()
        if " class " in ret_or_class or " interface " in ret_or_class or " enum " in ret_or_class:
            continue
        names.add(name)
    # Constructor support
    names.add(cut_class_name)
    return names


def detect_cut_api_hallucinations(
    java_test_code: str,
    cut_class_name: str,
    allowed_method_names: set[str],
) -> list[str]:
    """
    Heuristic static gate:
    - Detect invalid static calls like CutClass.unknownMethod(...)
    - Detect invalid instance calls when receiver variable is typed as CutClass
    """
    issues: list[str] = []
    if not allowed_method_names:
        return issues

    # 1) Static calls: CutClass.method(...)
    static_pat = re.compile(rf"\b{re.escape(cut_class_name)}\.(\w+)\s*\(")
    for m in static_pat.finditer(java_test_code):
        method = m.group(1)
        if method not in allowed_method_names:
            issues.append(
                f"Unknown CUT static method call: {cut_class_name}.{method}(...)"
            )

    # 2) Instance calls where receiver declared as CutClass
    var_decl = re.compile(
        rf"\b{re.escape(cut_class_name)}\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|;)"
    )
    vars_of_cut = {m.group(1) for m in var_decl.finditer(java_test_code)}
    if vars_of_cut:
        var_pat = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\.(\w+)\s*\(")
        for m in var_pat.finditer(java_test_code):
            recv, method = m.group(1), m.group(2)
            if recv in vars_of_cut and method not in allowed_method_names:
                issues.append(
                    f"Unknown CUT instance method call: {recv}.{method}(...)"
                )

    # Deduplicate while preserving order
    seen: set[str] = set()
    deduped: list[str] = []
    for issue in issues:
        if issue not in seen:
            seen.add(issue)
            deduped.append(issue)
    return deduped


def build_failure_family_key(failures: list[str]) -> str:
    """
    Normalize failures into a 'family key' to detect repeated failure types
    even when line numbers/messages vary slightly between iterations.
    """
    tokens: list[str] = []
    for f in failures:
        m = re.search(r"\[([a-zA-Z_]+)\]", f)
        if m:
            tokens.append(m.group(1).lower())
            continue
        if "expected" in f.lower() and "actual was" in f.lower():
            m2 = re.search(r"\w+\.(\w+):", f)
            tokens.append(f"assert_mismatch:{m2.group(1) if m2 else '?'}")
            continue
        if "to be thrown" in f.lower():
            m3 = re.search(r"\w+\.(\w+):", f)
            tokens.append(f"wrong_exception:{m3.group(1) if m3 else '?'}")
            continue
        tokens.append("other")
    return "|".join(sorted(tokens))


def normalize_failure_line_for_sticky_key(f: str) -> str:
    """
    Strip volatile parts (paths, line numbers, concrete expected values) so that
    repeated failures still match after small Maven/code edits.
    Conservative: only removes obvious numeric/location noise.
    """
    s = f.strip()
    # FooTest:8 or FooTest.java:22 (compiler / diagnosis lines)
    s = re.sub(r"\b\w+Test:\d+\b", "XTest:#", s, flags=re.IGNORECASE)
    s = re.sub(r"\b\w+\.java:\d+\b", "_.java:#", s, flags=re.IGNORECASE)
    # Absolute/relative paths ending in .java (with optional :line:col)
    s = re.sub(
        r"[/\\][^\s:/\\]+\.java(?::\d+)?(?::\d+)?",
        "/_.java",
        s,
        flags=re.IGNORECASE,
    )
    # [line,col] in compiler output
    s = re.sub(r"\[\d+,\s*\d+\]", "[#,#]", s)
    # Test.method:LINE (Surefire / runtime) -> Test.method:#
    s = re.sub(r"(\.\w+):\d+\b", r"\1:#", s)
    # Trailing :digits after .java already reduced; bare :42 tokens
    s = re.sub(r"(?<![\w/])(?<!\.java):\d+\b", ":#", s)
    # Semantic assert line from parse_surefire_failures: "expected N, but actual was M"
    s = re.sub(
        r"expected\s+[^,\n]+,",
        "expected #,",
        s,
        count=1,
        flags=re.IGNORECASE,
    )
    s = re.sub(
        r"but\s+actual\s+was\s+[^\s\n]+",
        "but actual was #",
        s,
        count=1,
        flags=re.IGNORECASE,
    )
    # wrong_method_call "required ... but found ..." (truncate concrete types)
    s = re.sub(
        r"\brequired\s+[^\n]+?(?=\s+but\s+found\b)",
        "required #",
        s,
        count=1,
        flags=re.IGNORECASE,
    )
    s = re.sub(
        r"\bbut\s+found\s+.+",
        "but found #",
        s,
        count=1,
        flags=re.IGNORECASE,
    )
    return re.sub(r"\s+", " ", s).strip()


def build_sticky_failure_key(failures: list[str]) -> str:
    """
    Family key over normalized failure lines (primary 'same failure' signal).
    Appends |n=<count> so failure cardinality changes reset sticky matching.
    If every normalized line is empty, uses empty_sticky|n=...|h=<md5 prefix>
    over raw joined text so unrelated empties do not share one key.
    """
    if not failures:
        return "n=0|empty_batch"
    normalized = [normalize_failure_line_for_sticky_key(x) for x in failures]
    n = len(failures)
    if all(not x for x in normalized):
        raw_payload = "\n".join(failures)
        h = hashlib.md5(raw_payload.encode("utf-8", errors="replace")).hexdigest()[:12]
        return f"empty_sticky|n={n}|h={h}"
    base = build_failure_family_key(normalized)
    return f"{base}|n={n}"


def extract_methods_by_name(java_code: str, method_names: set[str]) -> str:
    """
    Extract only the specified test methods from java_code.
    Returns concatenated method bodies (annotation + signature + body) for each name.
    When method_names is empty (e.g. compile error), returns full class as fallback.
    """
    methods = extract_test_methods(java_code)
    if not method_names:
        return java_code  # fallback: full class when no specific methods (e.g. compile error)
    parts = []
    for name in sorted(method_names):
        if name in methods:
            parts.append(methods[name])
    return "\n\n".join(parts) if parts else "(no matching methods found)"


def extract_test_methods(java_code: str) -> dict[str, str]:
    """Extract @Test method name -> full method text (annotation + signature + body)."""
    methods = {}
    lines = java_code.splitlines()
    i = 0
    while i < len(lines):
        if "@Test" in lines[i]:
            # Collect from @Test to end of method (matching braces)
            start = i
            j = i + 1
            while j < len(lines) and not re.search(r"\bvoid\s+(\w+)\s*\(", lines[j]):
                j += 1
            if j >= len(lines):
                i += 1
                continue
            m = re.search(r"\bvoid\s+(\w+)\s*\(", lines[j])
            if not m:
                i += 1
                continue
            method_name = m.group(1)
            depth = 0
            for k in range(j, len(lines)):
                for c in lines[k]:
                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                if depth == 0 and "}" in lines[k]:
                    methods[method_name] = "\n".join(lines[start : k + 1])
                    i = k
                    break
        i += 1
    return methods


def count_test_methods(java_code: str) -> int:
    """Count @Test methods for experiment metrics."""
    return len(extract_test_methods(java_code))


def merge_passed_tests_into_output(
    llm_output: str, passed_methods: dict[str, str]
) -> str:
    """
    将已通过的测试方法强制合并进 LLM 输出，防止 LLM 改坏已通过的测试。
    """
    if not passed_methods:
        return llm_output
    llm_methods = extract_test_methods(llm_output)
    out = llm_output
    for name, correct_code in passed_methods.items():
        if name in llm_methods and llm_methods[name] != correct_code:
            out = out.replace(llm_methods[name], correct_code, 1)
    return out


def build_passed_tests_hint(
    java_code: str, failed_names: set[str]
) -> tuple[str, dict[str, str]]:
    """
    Build short hint for LLM: which tests passed (names only, no full code).
    Returns (hint_text, passed_methods_dict) for merge_passed_tests_into_output.
    """
    all_methods = extract_test_methods(java_code)
    passed_names = sorted(set(all_methods) - failed_names)
    passed_methods = {n: all_methods[n] for n in passed_names}
    if not passed_names:
        return "No tests passed yet. Fix all failing tests.", {}
    hint = f"Passed tests (keep unchanged): {', '.join(passed_names)}"
    return hint, passed_methods


def run_ollama(
    model: str,
    prompt: str,
    timeout_sec: int | None = 180,
) -> str:
    """
    Call: ollama run <model>
    Feed prompt via stdin, capture stdout.
    timeout_sec None or <= 0: no subprocess timeout (hang risk).
    """
    common = dict(
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    cmd = ["ollama", "run", model]
    if timeout_sec is not None and timeout_sec > 0:
        proc = subprocess.run(cmd, timeout=timeout_sec, **common)
    else:
        proc = subprocess.run(cmd, **common)
    if proc.returncode != 0:
        raise RuntimeError(
            "Ollama call failed.\n"
            f"Return code: {proc.returncode}\n"
            f"STDERR:\n{proc.stderr}\n"
            f"STDOUT:\n{proc.stdout}\n"
        )
    return proc.stdout


def extract_java_code(llm_output: str) -> str:
    """
    Extract Java test class from LLM output.
    Priority:
      1) ```java ... ```
      2) ``` ... ```
      3) from first occurrence of package/import/public class
    """
    # 1) ```java ... ```
    m = re.search(r"```java\s*(.*?)```", llm_output, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # 2) ``` ... ```
    m = re.search(r"```\s*(.*?)```", llm_output, flags=re.DOTALL)
    if m:
        return m.group(1).strip()

    # 3) heuristic start
    lines = llm_output.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("package ") or s.startswith("import ") or "public class" in s:
            start_idx = i
            break
    if start_idx is None:
        return llm_output.strip()
    return "\n".join(lines[start_idx:]).strip()


def clean_special_tokens(java_code: str) -> str:
    """
    Remove model special tokens that pollute Java code.
    E.g. <|...|>, <｜...｜>, </s>, <s>, etc.

    Edge cases to watch:
    - Space collapse (  + -> single space) can affect string literals/comments;
      consider line-only trimming if issues arise.
    - Token patterns may need expansion for new model output formats.
    """
    out = java_code
    # <|...|> style (e.g. <|endoftext|>, <|im_end|>)
    out = re.sub(r"<\|[^|]*\|>", "", out)
    # <｜...｜> Unicode variant
    out = re.sub(r"<｜[^｜]*｜>", "", out)
    # Common EOS tokens
    for tok in ["</s>", "<s>", "<EOS>", "<eos>"]:
        out = out.replace(tok, "")
    # Collapse multiple spaces/newlines introduced by removal
    out = re.sub(r"  +", " ", out)
    out = re.sub(r"\n\s*\n\s*\n+", "\n\n", out)
    return out.strip()


def parse_package_from_java(java_code: str) -> str:
    """
    Extract package name from CUT Java source.
    Returns e.g. 'org.templateit' or 'uk.sussex.testgen'.
    Raises ValueError if no package declaration found.
    """
    m = re.search(r"^\s*package\s+([\w.]+)\s*;", java_code, re.MULTILINE)
    if m:
        return m.group(1).strip()
    raise ValueError(
        "CUT Java source has no package declaration. "
        "The class under test must declare a package (e.g. package org.example;)."
    )


def extract_public_method_signatures(java_code: str) -> str:
    """
    Extract a conservative list of public method/constructor signatures from CUT code.
    Used to constrain LLM calls to existing APIs and reduce hallucinated invocations.
    """
    pattern = re.compile(
        r"^\s*public\s+(?:static\s+|final\s+|synchronized\s+|abstract\s+|native\s+|strictfp\s+)*"
        r"[^\n;{}]*\([^;\n{}]*\)\s*(?:throws[^{\n]+)?\{?",
        re.MULTILINE,
    )
    signatures: list[str] = []
    seen: set[str] = set()
    for m in pattern.finditer(java_code):
        sig = m.group(0).strip()
        if " class " in sig or " interface " in sig or " enum " in sig:
            continue
        if sig.endswith("{"):
            sig = sig[:-1].rstrip()
        # Normalize spacing for compact prompts.
        sig = re.sub(r"\s+", " ", sig)
        if sig not in seen:
            seen.add(sig)
            signatures.append(sig)
    if not signatures:
        return "No public method signatures detected."
    return "\n".join(f"- {s}" for s in signatures)


def has_invalid_test_method_name(java_code: str) -> bool:
    """
    Detect obviously invalid Java test method names, especially names containing spaces.
    Example of invalid:
        public void testClamp ZeroValues_ReturnsClampedValue() {
    """
    for line in java_code.splitlines():
        stripped = line.strip()

        if "void " in stripped and "(" in stripped and ")" in stripped:
            # Try to capture the token after 'void '
            after_void = stripped.split("void ", 1)[1]
            candidate = after_void.split("(", 1)[0].strip()

            # If method name contains spaces, it's invalid
            if " " in candidate:
                return True

            # If we couldn't match it as a valid Java identifier, treat as invalid
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", candidate):
                return True

    return False


def validate_test_code(
    java_code: str,
    expected_class_name: str,
    cut_class_name: str,
    package_name: str,
    *,
    require_cut_reference: bool = False,
    allow_empty: bool = False,
) -> tuple[bool, list[str]]:
    """
    Validator v2:
    Check whether generated Java test code is structurally safe enough
    to enter Maven compilation.

    require_cut_reference: when True, fail if cut_class_name not in code (CUT heuristic).
    When False (default), skip this check; validator stays CUT-agnostic.

    Returns:
        (ok, reasons)
    """
    reasons = []

    # Rule 1: required package
    required_package = f"package {package_name};"
    if required_package not in java_code:
        reasons.append(f"Missing required package declaration: {required_package}")

    # Rule 2: expected class declaration (not just substring)
    # Must have actual "class Xxx" or "public class Xxx" declaration
    class_decl = re.compile(
        rf"^\s*(?:public\s+)?(?:final\s+)?class\s+{re.escape(expected_class_name)}\b",
        re.MULTILINE,
    )
    if not class_decl.search(java_code):
        reasons.append(f"Missing expected class declaration: {expected_class_name}")

    # Rule 3: must contain @Test (skipped for intentionally empty test classes)
    if not allow_empty and "@Test" not in java_code:
        reasons.append("Missing @Test annotation")

    # Rule 4: must contain at least one JUnit assertion (not Java assert())
    # Skipped when allow_empty=True (LLM deliberately generated zero-method class)
    has_assert = (
        "assertEquals(" in java_code
        or "assertThrows(" in java_code
        or "assertTrue(" in java_code
        or "assertFalse(" in java_code
        or "assertNotNull(" in java_code
        or "assertNull(" in java_code
        or "assertDoesNotThrow(" in java_code
        or "fail(" in java_code
        or "Assertions.assertEquals(" in java_code
        or "Assertions.assertThrows(" in java_code
        or "Assertions.assertTrue(" in java_code
        or "Assertions.assertFalse(" in java_code
        or "Assertions.assertNotNull(" in java_code
        or "Assertions.assertNull(" in java_code
        or "Assertions.assertDoesNotThrow(" in java_code
        or "Assertions.fail(" in java_code
    )
    if not allow_empty and not has_assert:
        reasons.append("Missing assertion statements")

    # Rule 5: if unqualified assertEquals( is used, require exact or wildcard static import
    # Assertions.assertEquals(...) does NOT require static import
    if re.search(r"(?<!Assertions\.)assertEquals\s*\(", java_code):
        has_exact = "import static org.junit.jupiter.api.Assertions.assertEquals;" in java_code
        has_wildcard = "import static org.junit.jupiter.api.Assertions.*" in java_code
        if not has_exact and not has_wildcard:
            reasons.append("Missing static import for assertEquals")

    # Rule 6: if unqualified assertThrows( is used, require exact or wildcard static import
    # Assertions.assertThrows(...) does NOT require static import
    if re.search(r"(?<!Assertions\.)assertThrows\s*\(", java_code):
        has_exact = "import static org.junit.jupiter.api.Assertions.assertThrows;" in java_code
        has_wildcard = "import static org.junit.jupiter.api.Assertions.*" in java_code
        if not has_exact and not has_wildcard:
            reasons.append("Missing static import for assertThrows")

    # Rule 7: banned known-wrong tokens
    banned_tokens = [
        "assertThrowsException",
        "IntegerPointerException",
    ]
    for token in banned_tokens:
        if token in java_code:
            reasons.append(f"Contains banned token: {token}")

    # Rule 7c: Java assert() instead of JUnit assertions
    if re.search(r"\bassert(?!Equals|Throws|True|False)\s*\(", java_code):
        reasons.append(
            "Use JUnit assertions, not Java assert()."
        )

    # Rule 8: markdown residue
    if "```" in java_code:
        reasons.append("Contains markdown code fence")

    # Rule 9: optional CUT reference heuristic (off by default)
    if require_cut_reference and cut_class_name not in java_code:
        reasons.append(f"Does not reference class under test: {cut_class_name}")

    # Rule 10: obvious invalid method names
    if has_invalid_test_method_name(java_code):
        reasons.append("Invalid test method name detected")

    return len(reasons) == 0, reasons

def ensure_package(java_code: str, package_name: str) -> str:
    """
    Ensure the generated Java test contains the correct package declaration.
    - If wrong package exists (e.g. uk.sussex.testgen when CUT is org.templateit), replace it.
    - If missing, prepend it.
    """
    correct = f"package {package_name};"

    if correct in java_code:
        return java_code

    # Replace any wrong package (LLM often outputs uk.sussex.testgen from successful_ref)
    wrong = re.compile(r"^\s*package\s+[\w.]+\s*;", re.MULTILINE)
    if wrong.search(java_code):
        return wrong.sub(correct + "\n", java_code, count=1)

    return f"{correct}\n\n{java_code.lstrip()}"


def ensure_test_import(java_code: str) -> str:
    """Auto-add @Test annotation import if used but missing."""
    if "@Test" not in java_code or "import org.junit.jupiter.api.Test" in java_code:
        return java_code
    lines = java_code.splitlines()
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("import "):
            last_import_idx = i
    test_import = "import org.junit.jupiter.api.Test;"
    if last_import_idx >= 0:
        existing = "\n".join(lines[: last_import_idx + 1])
        if test_import not in existing:
            lines.insert(last_import_idx + 1, test_import)
    else:
        for i, line in enumerate(lines):
            if line.strip().startswith("package "):
                lines.insert(i + 1, test_import)
                break
    return "\n".join(lines)


def _has_unqualified_assert(java_code: str, name: str) -> bool:
    """True if unqualified Assertions.name(...) is used (needs static import)."""
    return bool(re.search(rf"(?<!Assertions\.){re.escape(name)}\s*\(", java_code))


def ensure_assert_imports(java_code: str) -> str:
    """Auto-add static import for unqualified JUnit assertions when missing."""
    has_wildcard = "import static org.junit.jupiter.api.Assertions.*" in java_code
    if has_wildcard:
        return java_code

    # Only add import when unqualified call exists (Assertions.xxx does not need it)
    assertions = [
        ("assertEquals", "import static org.junit.jupiter.api.Assertions.assertEquals;"),
        ("assertThrows", "import static org.junit.jupiter.api.Assertions.assertThrows;"),
        ("assertTrue", "import static org.junit.jupiter.api.Assertions.assertTrue;"),
        ("assertFalse", "import static org.junit.jupiter.api.Assertions.assertFalse;"),
        ("assertNotNull", "import static org.junit.jupiter.api.Assertions.assertNotNull;"),
        ("assertNull", "import static org.junit.jupiter.api.Assertions.assertNull;"),
        ("assertDoesNotThrow", "import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;"),
        ("fail", "import static org.junit.jupiter.api.Assertions.fail;"),
    ]
    imports_to_add = []
    existing = java_code
    for name, imp_line in assertions:
        if _has_unqualified_assert(java_code, name) and imp_line not in existing:
            imports_to_add.append(imp_line)
            existing += "\n" + imp_line  # avoid duplicate if same assertion used twice

    if not imports_to_add:
        return java_code

    lines = java_code.splitlines()
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("import "):
            last_import_idx = i

    if last_import_idx >= 0:
        existing = "\n".join(lines[: last_import_idx + 1])
        for imp in imports_to_add:
            if imp not in existing:
                lines.insert(last_import_idx + 1, imp)
                last_import_idx += 1
    else:
        for i, line in enumerate(lines):
            if line.strip().startswith("package "):
                for j, imp in enumerate(imports_to_add):
                    lines.insert(i + 1 + j, imp)
                break
    return "\n".join(lines)


def test_output_path_to_fqn(test_output_path: str) -> str:
    """Convert e.g. src/test/java/org/templateit/RegionTest.java to org.templateit.RegionTest."""
    s = Path(test_output_path).as_posix()
    if s.startswith("src/test/java/"):
        s = s[len("src/test/java/"):]
    return s.replace(".java", "").replace("/", ".")


# Synthetic exit code when subprocess.run hits timeout (Maven does not use this value).
MAVEN_TIMEOUT_RETURNCODE = -100


def _is_maven_runner_timeout(r: subprocess.CompletedProcess) -> bool:
    return r.returncode == MAVEN_TIMEOUT_RETURNCODE


def run_maven(
    mvn_cmd: str,
    project_root: Path,
    goals: list[str],
    *,
    timeout_sec: int | None = 300,
    timeout_log_path: Path | None = None,
) -> subprocess.CompletedProcess:
    """
    Run Maven. If timeout_sec is None or <= 0, no timeout is applied.
    On timeout, writes timeout_log_path (if set), prints to stderr, and returns
    CompletedProcess with returncode MAVEN_TIMEOUT_RETURNCODE.
    """
    cmd = [mvn_cmd] + goals
    common = dict(
        cwd=str(project_root),
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if timeout_sec is None or timeout_sec <= 0:
        return subprocess.run(cmd, **common)

    try:
        return subprocess.run(cmd, timeout=timeout_sec, **common)
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") if e.stdout is not None else ""
        err = (e.stderr or "") if e.stderr is not None else ""
        detail = (
            f"MAVEN_RUNNER_TIMEOUT after {timeout_sec}s\n"
            f"cmd: {cmd}\n"
            f"cwd: {project_root}\n\n"
            f"--- stdout (partial) ---\n{out}\n\n"
            f"--- stderr (partial) ---\n{err}\n"
        )
        if timeout_log_path is not None:
            timeout_log_path.parent.mkdir(parents=True, exist_ok=True)
            write_text(timeout_log_path, detail)
        print(
            f"ERROR: Maven timed out after {timeout_sec}s. "
            f"Details: {timeout_log_path or '(no log path)'}",
            file=sys.stderr,
        )
        full_stderr = f"MAVEN_RUNNER_TIMEOUT\n{detail}"
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=MAVEN_TIMEOUT_RETURNCODE,
            stdout=out,
            stderr=full_stderr,
        )


RUNS_TABLE_HEADER = (
    "Run\tModel\tstart\tEnd\tTotal time(min)\tInitial errors\tRepair count\t"
    "Error progression\tResult\tFailure_category\tProgrammatic_Fix_Used\t"
    "baseline_mutation\taugmented_mutation\ttests_generated\taugmentation_success\n"
)


def append_run_to_runs_table(
    output_dir: Path,
    v: int,
    model: str,
    run_start_str: str,
    run_start_time: float,
    repair_count: int,
    initial_errors: int | None,
    error_progression: list[int],
    result: str,
    failure_category: str = "-",
    programmatic_fix_used: str = "-",
    baseline_mutation: str = "-",
    augmented_mutation: str = "-",
    tests_generated: int | None = None,
    augmentation_success: str = "-",
) -> None:
    """Append a run record (success or failure) to runs_table.txt for statistics."""
    run_end_time = time.time()
    run_end_str = datetime.now().strftime("%H:%M")
    total_min = round((run_end_time - run_start_time) / 60, 1)
    init_err = initial_errors if initial_errors is not None else 0
    prog_str = "-".join(str(ep) for ep in error_progression) if error_progression else "-"
    tests_str = str(tests_generated) if tests_generated is not None else "-"
    runs_table = output_dir / "summary" / "runs_table.txt"
    if not runs_table.exists():
        runs_table.parent.mkdir(parents=True, exist_ok=True)
        runs_table.write_text(RUNS_TABLE_HEADER, encoding="utf-8")
    with runs_table.open("a", encoding="utf-8") as f:
        f.write(
            f"{v}\t{model}\t{run_start_str}\t{run_end_str}\t{total_min}\t{init_err}\t"
            f"{repair_count}\t{prog_str}\t{result}\t{failure_category}\t{programmatic_fix_used}\t"
            f"{baseline_mutation}\t{augmented_mutation}\t{tests_str}\t{augmentation_success}\n"
        )


def print_header(title: str) -> None:
    print("\n" + "=" * 6 + f" {title} " + "=" * 6)


def postprocess_llm_test(raw_llm_output: str, package_name: str) -> str:
    """
    统一流水线：extract → clean → ensure package → ensure imports.
    不包含 validation。
    """
    java = extract_java_code(raw_llm_output)
    java = clean_special_tokens(java)
    java = ensure_package(java, package_name)
    java = ensure_test_import(java)
    java = ensure_assert_imports(java)
    return java


def activate_and_write_test(
    java_code: str,
    test_class_name: str,
    active_test_class_name: str,
    active_test_file: Path,
    generated_file: Path,
) -> None:
    """
    将 versioned test (XTest_vN) 重命名为 active (XTest) 并写入两个目标文件。
    支持 test_class_name == active_test_class_name 的 no-op（如 augmentation）。
    """
    activated = re.sub(
        rf"\bclass\s+{re.escape(test_class_name)}\b",
        f"class {active_test_class_name}",
        java_code,
    )
    activated = re.sub(
        rf"\b{re.escape(test_class_name)}\s*\(",
        f"{active_test_class_name}(",
        activated,
    )
    write_text(active_test_file, activated)
    write_text(generated_file, java_code)


# -----------------------------
# Pipeline context & extracted phases
# -----------------------------
@dataclass
class PipelineContext:
    """Shared state for a single pipeline run."""
    cfg: RunnerConfig
    project_root: Path
    cut_file: Path
    code: str
    cut_class_name: str
    active_test_class_name: str
    test_class_name: str
    active_test_file: Path
    generated_file: Path
    test_class_fqn: str
    package_name: str
    method_signatures: str
    allowed_method_names: set[str]
    output_dir: Path
    prompts_dir: Path
    v: int
    run_start_str: str
    run_start_time: float
    successful_ref: str | None
    dependency_code: str | None
    semantic_repair_template: str
    compile_repair_template: str
    mvn_initial_goals: list[str]
    mvn_retry_goals: list[str]
    last_successful_path: Path


@dataclass
class RepairResult:
    """Output of the repair loop phase."""
    java_code: str
    repair_count: int
    initial_errors: int | None
    error_progression: list[int]
    programmatic_fix_used: bool


def _try_programmatic_fix(
    java_code: str,
    failures: list[str],
    enable: bool,
    aggressive_targets: set[str] | None = None,
) -> tuple[str, bool, list[tuple[str, str, str]]]:
    """Apply programmatic assertEquals fix. Returns (patched_code, changed, fix_pairs)."""
    if not enable or is_compile_failure(failures):
        return java_code, False, []
    fix_pairs = get_fix_pairs(failures)
    if not fix_pairs:
        return java_code, False, []
    patched = apply_programmatic_fix(java_code, fix_pairs)
    if patched == java_code and aggressive_targets:
        patched = apply_programmatic_fix_aggressive(java_code, fix_pairs, aggressive_targets)
    return patched, patched != java_code, fix_pairs


def _run_repair_loop(ctx: PipelineContext, java_test: str) -> RepairResult:
    """Run mvn test in a loop, repairing failures until success or max attempts."""
    repair_count = 0
    programmatic_fix_used = False
    last_failures_key: str | None = None
    last_sticky_key: str | None = None
    same_failures_count = 0
    same_sticky_count = 0
    method_stubborn_count: dict[str, int] = {}
    initial_errors: int | None = None
    error_progression: list[int] = []
    current = java_test
    is_first = True

    print(f"Single-CUT isolation: mvn test -Dtest={ctx.test_class_fqn}")

    while True:
        print_header("RUNNING MVN TEST")
        goals = ctx.mvn_initial_goals if is_first else ctx.mvn_retry_goals
        mvn_to = None if ctx.cfg.mvn_timeout_sec <= 0 else ctx.cfg.mvn_timeout_sec
        r = run_maven(
            ctx.cfg.mvn_cmd,
            ctx.project_root,
            goals,
            timeout_sec=mvn_to,
            timeout_log_path=(
                ctx.output_dir
                / "logs"
                / "mvn_test_fail"
                / f"mvn_timeout_v{ctx.v}_r{repair_count}.log"
            ),
        )
        is_first = False
        mvn_log = (r.stdout or "") + "\n" + (r.stderr or "")
        if r.returncode != 0:
            write_text(
                ctx.output_dir / "logs" / "mvn_test_fail" / f"mvn_test_fail_v{ctx.v}_r{repair_count}.log",
                mvn_log,
            )

        if r.returncode == 0:
            break

        if _is_maven_runner_timeout(r):
            append_run_to_runs_table(
                ctx.output_dir, ctx.v, ctx.cfg.model, ctx.run_start_str, ctx.run_start_time,
                repair_count, initial_errors, error_progression, "Fail", "mvn_timeout",
            )
            limit = ctx.cfg.mvn_timeout_sec
            raise RuntimeError(
                f"Maven subprocess timed out after {limit}s (repair round {repair_count}). "
                f"See output/logs/mvn_test_fail/mvn_timeout_v{ctx.v}_r{repair_count}.log"
            )

        failures = parse_surefire_failures(mvn_log)
        if not failures:
            append_run_to_runs_table(
                ctx.output_dir, ctx.v, ctx.cfg.model, ctx.run_start_str, ctx.run_start_time,
                repair_count, initial_errors, error_progression, "Fail", "mvn_no_parse",
            )
            raise RuntimeError(
                "mvn test failed (no assertion failures parsed, e.g. compile error). "
                "See output log in runner/output/"
            )

        err_count = len(failures)
        if initial_errors is None:
            initial_errors = err_count
        error_progression.append(err_count)

        if repair_count >= ctx.cfg.max_repair_attempts:
            append_run_to_runs_table(
                ctx.output_dir, ctx.v, ctx.cfg.model, ctx.run_start_str, ctx.run_start_time,
                repair_count, initial_errors, error_progression, "Fail", "repair_exceeded",
            )
            raise RuntimeError(
                f"Semantic repair exceeded max attempts ({ctx.cfg.max_repair_attempts}). "
                "See output log in runner/output/"
            )

        # Track per-method stubborn count for assert mismatches
        stubborn_methods: set[str] = set()
        if not is_compile_failure(failures):
            assert_mismatch_methods = get_assert_mismatch_methods(failures)
            for m in method_stubborn_count:
                if m not in assert_mismatch_methods:
                    method_stubborn_count[m] = 0
            for m in assert_mismatch_methods:
                method_stubborn_count[m] = method_stubborn_count.get(m, 0) + 1
            stubborn_methods = {m for m, c in method_stubborn_count.items() if c >= 2}

        # Pre-LLM programmatic fix
        patched, changed, fix_pairs = _try_programmatic_fix(
            current, failures, ctx.cfg.enable_programmatic_fix, stubborn_methods,
        )
        if changed:
            programmatic_fix_used = True
            print_header("PROGRAMMATIC FIX (applying correct expected values)")
            for mn, _, _ in fix_pairs:
                if mn in method_stubborn_count:
                    method_stubborn_count[mn] = 0
            current = patched
            activate_and_write_test(
                current, ctx.test_class_name, ctx.active_test_class_name,
                ctx.active_test_file, ctx.generated_file,
            )
            print("Applied programmatic fix. Retrying mvn test...")
            continue

        # Detect stuck: exact string OR normalized sticky key (paths/line nums/values stripped)
        failures_key = "|".join(sorted(failures))
        sticky_key = build_sticky_failure_key(failures)
        if failures_key == last_failures_key:
            same_failures_count += 1
        else:
            same_failures_count = 0
        if sticky_key == last_sticky_key:
            same_sticky_count += 1
        else:
            same_sticky_count = 0

        compile_family_regen = (
            ctx.cfg.enable_compile_failure_family_regen
            and is_compile_failure(failures)
            and same_sticky_count >= 1
        )
        should_try_regen = (
            same_failures_count >= ctx.cfg.regenerate_after_same_failures
            or same_sticky_count >= ctx.cfg.regenerate_after_same_failures
            or compile_family_regen
        )
        if should_try_regen:
                # Try simple programmatic fix before regenerating
                patched, changed, _ = _try_programmatic_fix(
                    current, failures, ctx.cfg.enable_programmatic_fix,
                )
                if changed:
                    programmatic_fix_used = True
                    print_header("PROGRAMMATIC FIX (same failures, applying correct values)")
                    current = patched
                    activate_and_write_test(
                        current, ctx.test_class_name, ctx.active_test_class_name,
                        ctx.active_test_file, ctx.generated_file,
                    )
                    same_failures_count = 0
                    same_sticky_count = 0
                    last_failures_key = None
                    last_sticky_key = None
                    print("Applied programmatic fix. Retrying mvn test...")
                    continue

                # Regenerate from scratch
                if should_try_regen:
                    print_header("REGENERATE (fresh candidate)")
                    print(
                        "Repeated failures detected "
                        f"(exact_same_count={same_failures_count + 1}, "
                        f"sticky_same_count={same_sticky_count + 1}, "
                        f"threshold={ctx.cfg.regenerate_after_same_failures}). "
                        "Regenerating from scratch instead of repair."
                    )
                    print(f"sticky_key={sticky_key!r}")
                    print(f"previous_sticky_key={last_sticky_key!r}")
                    regen_diagnosis = build_failure_diagnosis(
                        classify_failures(failures, ctx.cut_class_name)
                    )
                    if is_compile_failure(failures):
                        regen_failed_methods = current
                        regen_template = ctx.compile_repair_template
                    else:
                        regen_failed_names = get_failed_test_names(failures)
                        regen_failed_methods = extract_methods_by_name(
                            current, regen_failed_names
                        )
                        regen_template = ctx.semantic_repair_template
                    regen_prompt = (
                        "REGENERATE: Previous test failed repeatedly. Generate a completely "
                        "NEW test class. Do NOT copy or patch the failed code. Start fresh.\n\n"
                        + build_prompt(
                            regen_template, ctx.code, ctx.test_class_name,
                            failures=[regen_diagnosis],
                            failed_methods=regen_failed_methods,
                            successful_ref=ctx.successful_ref,
                            package_name=ctx.package_name,
                            dependency_code=ctx.dependency_code,
                            method_signatures=ctx.method_signatures,
                        )
                    )
                    oto = (
                        None
                        if ctx.cfg.ollama_timeout_sec <= 0
                        else ctx.cfg.ollama_timeout_sec
                    )
                    raw_regen = run_ollama(
                        ctx.cfg.model, regen_prompt, timeout_sec=oto,
                    )
                    current = postprocess_llm_test(raw_regen, ctx.package_name)
                    ok, reasons = validate_test_code(
                        current, ctx.test_class_name, ctx.cut_class_name,
                        ctx.package_name, require_cut_reference=True,
                        allow_empty=True,
                    )
                    if not ok:
                        append_run_to_runs_table(
                            ctx.output_dir, ctx.v, ctx.cfg.model, ctx.run_start_str,
                            ctx.run_start_time, repair_count, initial_errors,
                            error_progression, "Fail", "regen_validation_fail",
                        )
                        raise RuntimeError(
                            "Regenerated test failed validation.\n" + "\n".join(reasons)
                        )
                    activate_and_write_test(
                        current, ctx.test_class_name, ctx.active_test_class_name,
                        ctx.active_test_file, ctx.generated_file,
                    )
                    same_failures_count = 0
                    same_sticky_count = 0
                    last_failures_key = None
                    last_sticky_key = None
                    method_stubborn_count.clear()
                    repair_count += 1
                    print("Regenerated. Retrying mvn test...")
                    continue

        last_failures_key = failures_key
        last_sticky_key = sticky_key

        # LLM-based repair
        repair_type = "COMPILE REPAIR" if is_compile_failure(failures) else "SEMANTIC REPAIR"
        print_header(f"{repair_type} (LLM)")
        print(f"Repair attempt {repair_count + 1}/{ctx.cfg.max_repair_attempts}")
        print("Failures:\n" + "\n".join(failures))

        if is_compile_failure(failures):
            passed_hint = (
                "No passed tests (compile failure - failing methods unknown). "
                "Fix all compile errors."
            )
            passed_methods: dict[str, str] = {}
            failed_methods = current
        else:
            failed_names = get_failed_test_names(failures)
            passed_hint, passed_methods = build_passed_tests_hint(current, failed_names)
            failed_methods = extract_methods_by_name(current, failed_names)

        anti_stuck_hint = ""
        if same_failures_count >= 1 or same_sticky_count >= 1:
            correct_hint = build_correct_fix_hint(failures)
            anti_stuck_hint = (
                "CRITICAL: Your previous attempt produced the SAME failures. You MUST change "
                "your code. The correct expected value is the ACTUAL value from each failure. "
                "Do NOT output the same wrong code again.\n\n" + correct_hint
            )

        failure_diagnosis = build_failure_diagnosis(
            classify_failures(failures, ctx.cut_class_name)
        )
        repair_template = (
            ctx.compile_repair_template if is_compile_failure(failures)
            else ctx.semantic_repair_template
        )
        repair_prompt = build_prompt(
            repair_template, ctx.code, ctx.test_class_name,
            failures=[failure_diagnosis], failed_methods=failed_methods,
            successful_ref=ctx.successful_ref, passed_tests_hint=passed_hint,
            anti_stuck_hint=anti_stuck_hint, package_name=ctx.package_name,
            dependency_code=ctx.dependency_code,
            method_signatures=ctx.method_signatures,
        )
        write_llm_artifact(
            ctx.cfg,
            ctx.output_dir / "repair_prompt" / f"repair_prompt_v{ctx.v}_r{repair_count + 1}.txt",
            repair_prompt,
        )

        oto = (
            None if ctx.cfg.ollama_timeout_sec <= 0 else ctx.cfg.ollama_timeout_sec
        )
        raw_repair = run_ollama(ctx.cfg.model, repair_prompt, timeout_sec=oto)
        write_llm_artifact(
            ctx.cfg,
            ctx.output_dir / "raw_repair" / f"raw_repair_v{ctx.v}_r{repair_count + 1}.txt",
            raw_repair,
        )

        current = postprocess_llm_test(raw_repair, ctx.package_name)
        if not is_compile_failure(failures):
            current = merge_passed_tests_into_output(current, passed_methods)
        current = ensure_assert_imports(current)

        ok, reasons = validate_test_code(
            current, ctx.test_class_name, ctx.cut_class_name,
            ctx.package_name, require_cut_reference=True,
            allow_empty=True,
        )
        if not ok:
            invalid_path = (
                ctx.output_dir / "invalid_repaired"
                / f"invalid_repaired_v{ctx.v}_r{repair_count + 1}.txt"
            )
            reason_path = (
                ctx.output_dir / "invalid_repaired_reasons"
                / f"invalid_repaired_reasons_v{ctx.v}_r{repair_count + 1}.txt"
            )
            write_text(invalid_path, current)
            write_text(reason_path, "\n".join(reasons))
            append_run_to_runs_table(
                ctx.output_dir, ctx.v, ctx.cfg.model, ctx.run_start_str, ctx.run_start_time,
                repair_count, initial_errors, error_progression, "Fail",
                "repair_validation_fail",
            )
            raise RuntimeError(
                "Repaired test failed validation.\n"
                f"Reasons saved to: {reason_path}\n"
                f"Invalid code saved to: {invalid_path}"
            )

        activate_and_write_test(
            current, ctx.test_class_name, ctx.active_test_class_name,
            ctx.active_test_file, ctx.generated_file,
        )
        repair_count += 1
        print("LLM repaired. Retrying mvn test...")

    print("mvn test: SUCCESS")
    return RepairResult(
        current, repair_count, initial_errors, error_progression, programmatic_fix_used,
    )


def _run_mutation_augmentation(
    ctx: PipelineContext,
    mutation_summary_text: str,
    baseline_score: str | None,
    pitest_targets: list[str],
    pit_package_index: Path,
) -> tuple[str | None, str, bool]:
    """
    Run mutation-guided augmentation.
    Returns (augmented_score, augmentation_success, augmentation_programmatic_fix_used).
    """
    print_header("MUTATION-GUIDED AUGMENTATION")
    mutation_template = read_text(ctx.prompts_dir / "mutation_augment.txt")
    for ph in ("{TEST_CLASS_NAME}", "<CODE>", "{MUTATION_SUMMARY}", "{CURRENT_TEST_CLASS}"):
        if ph not in mutation_template:
            raise ValueError(f"mutation_augment.txt must contain {ph}")

    current_test_content = read_text(ctx.active_test_file)
    aug_prompt = build_prompt(
        mutation_template, ctx.code, ctx.active_test_class_name,
        mutation_summary=mutation_summary_text,
        current_test_class=current_test_content,
        package_name=ctx.package_name,
        dependency_code=ctx.dependency_code,
        method_signatures=ctx.method_signatures,
    )
    write_llm_artifact(
        ctx.cfg,
        ctx.output_dir / "mutation_prompt" / f"mutation_prompt_v{ctx.v}.txt",
        aug_prompt,
    )

    oto = None if ctx.cfg.ollama_timeout_sec <= 0 else ctx.cfg.ollama_timeout_sec
    raw_aug = run_ollama(ctx.cfg.model, aug_prompt, timeout_sec=oto)
    write_llm_artifact(
        ctx.cfg,
        ctx.output_dir / "raw_mutation" / f"raw_mutation_v{ctx.v}.txt",
        raw_aug,
    )

    aug_java = postprocess_llm_test(raw_aug, ctx.package_name)
    ok, reasons = validate_test_code(
        aug_java, ctx.active_test_class_name, ctx.cut_class_name,
        ctx.package_name, require_cut_reference=True,
    )
    if not ok:
        write_text(
            ctx.output_dir / "invalid_repaired" / f"invalid_mutation_aug_v{ctx.v}.txt",
            aug_java,
        )
        write_text(
            ctx.output_dir / "invalid_repaired_reasons"
            / f"invalid_mutation_aug_reasons_v{ctx.v}.txt",
            "\n".join(reasons),
        )
        print(f"Mutation augmentation failed validation: {reasons}")
        return None, "no", False

    aug_path = (
        ctx.output_dir / "generated_tests"
        / f"{ctx.active_test_class_name}_v{ctx.v}_aug.java"
    )
    activate_and_write_test(
        aug_java, ctx.active_test_class_name, ctx.active_test_class_name,
        ctx.active_test_file, aug_path,
    )
    print("Augmented test validated. Running mvn test...")

    mvn_to = None if ctx.cfg.mvn_timeout_sec <= 0 else ctx.cfg.mvn_timeout_sec
    r = run_maven(
        ctx.cfg.mvn_cmd,
        ctx.project_root,
        ctx.mvn_retry_goals,
        timeout_sec=mvn_to,
        timeout_log_path=(
            ctx.output_dir / "logs" / "mvn_test_fail" / f"mvn_timeout_v{ctx.v}_aug.log"
        ),
    )
    aug_fix_used = False
    if _is_maven_runner_timeout(r):
        print(
            f"Mutation augmentation: Maven timed out after {ctx.cfg.mvn_timeout_sec}s; "
            "reverting to baseline."
        )
        write_text(ctx.active_test_file, current_test_content)
        return None, "no", aug_fix_used
    if r.returncode != 0:
        mvn_log = (r.stdout or "") + "\n" + (r.stderr or "")
        write_text(
            ctx.output_dir / "logs" / "mvn_test_fail" / f"mvn_test_fail_v{ctx.v}_aug.log",
            mvn_log,
        )
        failures = parse_surefire_failures(mvn_log)
        patched, changed, _ = _try_programmatic_fix(
            aug_java, failures, ctx.cfg.enable_programmatic_fix,
            aggressive_targets=get_assert_mismatch_methods(failures),
        )
        if changed:
            aug_fix_used = True
            write_text(ctx.active_test_file, patched)
            print("Applied programmatic fix to augmentation. Retrying mvn test...")
            r = run_maven(
                ctx.cfg.mvn_cmd,
                ctx.project_root,
                ctx.mvn_retry_goals,
                timeout_sec=mvn_to,
                timeout_log_path=(
                    ctx.output_dir
                    / "logs"
                    / "mvn_test_fail"
                    / f"mvn_timeout_v{ctx.v}_aug_retry.log"
                ),
            )
        if _is_maven_runner_timeout(r):
            print(
                f"Mutation augmentation: Maven timed out after {ctx.cfg.mvn_timeout_sec}s "
                "(retry); reverting to baseline."
            )
            write_text(ctx.active_test_file, current_test_content)
            return None, "no", aug_fix_used
        if r.returncode != 0:
            write_text(
                ctx.output_dir / "logs" / "mvn_test_fail" / f"mvn_test_fail_v{ctx.v}_aug.log",
                (r.stdout or "") + "\n" + (r.stderr or ""),
            )
            print("Mutation augmentation: mvn test failed. Reverting to baseline.")
            write_text(ctx.active_test_file, current_test_content)
            return None, "no", aug_fix_used

    print("mvn test (post-aug): SUCCESS")
    print_header("RUNNING PITEST (post-augmentation)")
    r_pit = run_maven(
        ctx.cfg.mvn_cmd,
        ctx.project_root,
        pitest_targets,
        timeout_sec=mvn_to,
        timeout_log_path=(
            ctx.output_dir / "logs" / "pitest_fail" / f"pitest_timeout_v{ctx.v}_aug.log"
        ),
    )
    augmented_score = None
    if _is_maven_runner_timeout(r_pit):
        print(
            f"PITest (post-aug): Maven timed out after {ctx.cfg.mvn_timeout_sec}s. "
            f"See output/logs/pitest_fail/pitest_timeout_v{ctx.v}_aug.log"
        )
    elif r_pit.returncode == 0 and pit_package_index.exists():
        augmented_score = parse_mutation_score(
            pit_package_index.read_text(encoding="utf-8", errors="replace")
        )
        print(f"Augmented mutation score: {augmented_score} (baseline: {baseline_score})")
        write_text(ctx.last_successful_path, read_text(ctx.active_test_file))
        write_text(ctx.generated_file, read_text(ctx.active_test_file))
    else:
        print("PIT (post-aug) failed or report not found.")

    return augmented_score, "yes", aug_fix_used


def _write_run_summary(
    ctx: PipelineContext,
    repair: RepairResult,
    baseline_score: str | None,
    augmented_score: str | None,
    augmentation_success: str,
    augmentation_fix_used: bool,
) -> None:
    """Write summary file and append to runs_table."""
    final_test_content = read_text(ctx.active_test_file)
    tests_generated = count_test_methods(final_test_content)

    run_end_time = time.time()
    run_end_str = datetime.now().strftime("%H:%M")
    total_min = round((run_end_time - ctx.run_start_time) / 60, 1)
    init_err = repair.initial_errors if repair.initial_errors is not None else 0
    prog_str = (
        "-".join(str(ep) for ep in repair.error_progression)
        if repair.error_progression else "-"
    )

    summary = ctx.output_dir / "summary" / f"summary_v{ctx.v}.txt"
    summary_lines = [
        f"version=v{ctx.v}",
        f"model={ctx.cfg.model}",
        f"generation_profile={ctx.cfg.generation_profile}",
        f"cut={ctx.cut_file}",
        f"generated_test={ctx.generated_file}",
        f"activated_test={ctx.active_test_file}",
        "mvn_test=SUCCESS",
        "pitest=SUCCESS",
        f"baseline_mutation_score={baseline_score or '-'}",
        f"augmented_mutation_score={augmented_score or '-'}",
        f"tests_generated={tests_generated}",
        f"repair_attempts={repair.repair_count}",
        f"augmentation_success={augmentation_success}",
        f"augmentation_programmatic_fix_used={'Yes' if augmentation_fix_used else 'No'}",
        "",
        RUNS_TABLE_HEADER.strip(),
        (
            f"{ctx.v}\t{ctx.cfg.model}\t{ctx.run_start_str}\t{run_end_str}\t{total_min}\t"
            f"{init_err}\t{repair.repair_count}\t{prog_str}\tSuccess\t-\t"
            f"{'Yes' if repair.programmatic_fix_used else 'No'}\t"
            f"{baseline_score or '-'}\t{augmented_score or '-'}\t"
            f"{tests_generated}\t{augmentation_success}"
        ),
    ]
    write_text(summary, "\n".join(summary_lines) + "\n")

    append_run_to_runs_table(
        ctx.output_dir, ctx.v, ctx.cfg.model, ctx.run_start_str, ctx.run_start_time,
        repair.repair_count, repair.initial_errors, repair.error_progression, "Success",
        programmatic_fix_used="Yes" if repair.programmatic_fix_used else "No",
        baseline_mutation=baseline_score or "-",
        augmented_mutation=augmented_score or "-",
        tests_generated=tests_generated,
        augmentation_success=augmentation_success,
    )


# -----------------------------
# Main
# -----------------------------
def main(config_path_override: Path | None = None) -> None:
    runner_root = Path(__file__).resolve().parent
    config_path = config_path_override or (runner_root / "config" / "config.json")
    print(f"RUNNER FILE: {Path(__file__).resolve()}")
    print(f"CONFIG FILE: {config_path}")
    prompts_dir = runner_root / "prompts"
    output_dir = runner_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    ensure_output_subdirs(output_dir)

    cfg = RunnerConfig.load(config_path)
    print(f"enable_mutation_augment = {cfg.enable_mutation_augment}")
    print(
        "ablation: inject_method_signatures_in_prompts="
        f"{cfg.inject_method_signatures_in_prompts}, "
        f"enable_cut_api_prepass={cfg.enable_cut_api_prepass}, "
        f"enable_compile_failure_family_regen={cfg.enable_compile_failure_family_regen}"
    )
    print(
        f"mvn_timeout_sec={cfg.mvn_timeout_sec}"
        + (" (disabled)" if cfg.mvn_timeout_sec <= 0 else "")
    )
    print(
        f"ollama_timeout_sec={cfg.ollama_timeout_sec}"
        + (" (disabled)" if cfg.ollama_timeout_sec <= 0 else "")
    )
    print(f"max_repair_attempts={cfg.max_repair_attempts}")
    print(f"artifact_write_mode={cfg.artifact_write_mode}")

    project_root = cfg.project_root
    cut_file = project_root / cfg.cut_path
    active_test_file = project_root / cfg.test_output_path

    cut_class_name = cut_file.stem
    active_test_class_name = f"{cut_class_name}Test"
    generated_dir = output_dir / "generated_tests"
    v = next_version(generated_dir, cut_class_name)
    test_class_name = f"{active_test_class_name}_v{v}"
    generated_file = generated_dir / f"{test_class_name}.java"

    prompt_template_path = prompts_dir / f"{cfg.generation_profile}.txt"
    if not prompt_template_path.exists():
        raise FileNotFoundError(f"Generation prompt not found: {prompt_template_path}")

    code = read_text(cut_file)
    package_name = parse_package_from_java(code)
    # Surefire/PIT need the declared Java package, not the benchmark folder path.
    test_class_fqn = f"{package_name}.{active_test_class_name}"
    extracted_signatures = extract_public_method_signatures(code)
    method_signatures = (
        extracted_signatures
        if cfg.inject_method_signatures_in_prompts
        else "(Method signature injection disabled in config.)"
    )
    allowed_method_names = extract_public_method_names(code, cut_class_name)

    # Auto-discover dependency classes in the same directory
    dep_parts = []
    for sibling in sorted(cut_file.parent.glob("*.java")):
        if sibling.name != cut_file.name:
            dep_parts.append(f"// {sibling.name}\n{read_text(sibling)}")
    dependency_code = "\n\n".join(dep_parts) if dep_parts else None
    if dependency_code:
        dep_names = [f.name for f in cut_file.parent.glob("*.java") if f.name != cut_file.name]
        print(f"Found {len(dep_parts)} dependency class(es): {dep_names}")

    template = read_text(prompt_template_path)
    if "{TEST_CLASS_NAME}" not in template:
        raise ValueError(
            f"Prompt template {prompt_template_path} must contain {{TEST_CLASS_NAME}}."
        )

    last_successful_path = get_last_successful_path(cut_file, output_dir)
    successful_ref = read_text(last_successful_path) if last_successful_path.exists() else None

    # Load repair templates and validate placeholders
    semantic_repair_template = read_text(prompts_dir / "semantic_repair.txt")
    compile_repair_template = read_text(prompts_dir / "compile_repair.txt")
    for ph in ("{FAILURES}", "{FAILED_METHODS}", "{PASSED_TESTS_HINT}"):
        if ph not in semantic_repair_template:
            raise ValueError(f"semantic_repair.txt must contain {ph}.")
    for ph in ("{FAILURES}", "{FAILED_METHODS}"):
        if ph not in compile_repair_template:
            raise ValueError(f"compile_repair.txt must contain {ph}.")

    # Build generation prompt
    prompt = build_prompt(
        template, code, test_class_name,
        successful_ref=successful_ref,
        package_name=package_name,
        dependency_code=dependency_code,
        method_signatures=method_signatures,
    )
    write_llm_artifact(cfg, output_dir / "prompt" / f"prompt_v{v}.txt", prompt)
    print_header("GENERATED PROMPT")
    print(prompt)

    # --- Phase 1: Initial LLM generation ---
    run_start_time = time.time()
    run_start_str = datetime.now().strftime("%H:%M")
    print_header("CALLING OLLAMA")
    oto = None if cfg.ollama_timeout_sec <= 0 else cfg.ollama_timeout_sec
    raw = run_ollama(cfg.model, prompt, timeout_sec=oto)
    write_llm_artifact(cfg, output_dir / "raw_llm" / f"raw_llm_v{v}.txt", raw)

    java_test = postprocess_llm_test(raw, package_name)
    ok, reasons = validate_test_code(
        java_test, test_class_name, cut_class_name, package_name,
        require_cut_reference=True,
        allow_empty=True,
    )
    if not ok:
        bad_path = output_dir / "invalid_extracted" / f"invalid_extracted_v{v}.txt"
        reason_path = output_dir / "invalid_reasons" / f"invalid_reasons_v{v}.txt"
        write_text(bad_path, java_test)
        write_text(reason_path, "\n".join(reasons))
        append_run_to_runs_table(
            output_dir, v, cfg.model, run_start_str, run_start_time,
            0, None, [], "Fail", "validation_fail",
        )
        raise RuntimeError(
            "Extracted test code failed validation.\n"
            f"Reasons saved to: {reason_path}\n"
            f"Invalid code saved to: {bad_path}"
        )

    # Static API gate: try one compile-repair pass before first mvn run if hallucinated CUT calls are detected.
    api_issues = detect_cut_api_hallucinations(
        java_test, cut_class_name, allowed_method_names
    )
    if cfg.enable_cut_api_prepass and api_issues:
        print_header("STATIC API GATE")
        print("Detected possible hallucinated CUT calls; running one compile repair pre-pass.")
        prepass_prompt = build_prompt(
            compile_repair_template,
            code,
            test_class_name,
            failures=[f"- [wrong_method_call] {msg}" for msg in api_issues],
            failed_methods=java_test,
            successful_ref=successful_ref,
            package_name=package_name,
            dependency_code=dependency_code,
            method_signatures=method_signatures,
        )
        raw_prepass = run_ollama(cfg.model, prepass_prompt, timeout_sec=oto)
        prepass_test = postprocess_llm_test(raw_prepass, package_name)
        prepass_ok, _ = validate_test_code(
            prepass_test, test_class_name, cut_class_name, package_name,
            require_cut_reference=True,
            allow_empty=True,
        )
        prepass_issues = detect_cut_api_hallucinations(
            prepass_test, cut_class_name, allowed_method_names
        )
        if prepass_ok and not prepass_issues:
            java_test = prepass_test
            print("Static API pre-pass succeeded.")
        else:
            print("Static API pre-pass did not fully resolve issues; keeping original draft.")

    # Clean stale test files to prevent cross-CUT compile pollution
    test_root = project_root / "src" / "test" / "java"
    if test_root.exists():
        for f in test_root.rglob("*.java"):
            if f != active_test_file:
                f.unlink()
                print(f"Removed stale test file: {f.relative_to(test_root)}")

    activate_and_write_test(
        java_test, test_class_name, active_test_class_name,
        active_test_file, generated_file,
    )
    print_header("SAVED VERSIONED TEST")
    print(f"Saved: {generated_file}")
    print_header("ACTIVATING TEST")
    print(f"Activated: {active_test_file}")

    # Build pipeline context for subsequent phases
    ctx = PipelineContext(
        cfg=cfg, project_root=project_root, cut_file=cut_file, code=code,
        cut_class_name=cut_class_name, active_test_class_name=active_test_class_name,
        test_class_name=test_class_name, active_test_file=active_test_file,
        generated_file=generated_file, test_class_fqn=test_class_fqn,
        package_name=package_name, method_signatures=method_signatures,
        allowed_method_names=allowed_method_names,
        output_dir=output_dir, prompts_dir=prompts_dir,
        v=v, run_start_str=run_start_str, run_start_time=run_start_time,
        successful_ref=successful_ref, dependency_code=dependency_code,
        semantic_repair_template=semantic_repair_template,
        compile_repair_template=compile_repair_template,
        mvn_initial_goals=["-q", "clean", "test", f"-Dtest={test_class_fqn}"],
        mvn_retry_goals=["-q", "test", f"-Dtest={test_class_fqn}"],
        last_successful_path=last_successful_path,
    )

    # --- Phase 2: Repair loop ---
    repair = _run_repair_loop(ctx, java_test)

    # --- Phase 3: PITest baseline ---
    print_header("RUNNING PITEST")
    cut_class_fqn = f"{package_name}.{cut_class_name}"
    pitest_targets = [
        "-q", "test", "org.pitest:pitest-maven:mutationCoverage",
        f"-DtargetClasses={cut_class_fqn}",
        f"-DtargetTests={test_class_fqn}",
    ]
    pit_to = None if cfg.mvn_timeout_sec <= 0 else cfg.mvn_timeout_sec
    r_pit = run_maven(
        cfg.mvn_cmd,
        project_root,
        pitest_targets,
        timeout_sec=pit_to,
        timeout_log_path=output_dir / "logs" / "pitest_fail" / f"pitest_timeout_v{v}.log",
    )
    if _is_maven_runner_timeout(r_pit):
        append_run_to_runs_table(
            output_dir, v, cfg.model, run_start_str, run_start_time,
            repair.repair_count, repair.initial_errors, repair.error_progression,
            "Fail", "pitest_timeout",
        )
        raise RuntimeError(
            f"PITest/Maven timed out after {cfg.mvn_timeout_sec}s. "
            f"See output/logs/pitest_fail/pitest_timeout_v{v}.log"
        )
    if r_pit.returncode != 0:
        write_text(
            output_dir / "logs" / "pitest_fail" / f"pitest_fail_v{v}.log",
            (r_pit.stdout or "") + "\n" + (r_pit.stderr or ""),
        )
        append_run_to_runs_table(
            output_dir, v, cfg.model, run_start_str, run_start_time,
            repair.repair_count, repair.initial_errors, repair.error_progression,
            "Fail", "pitest_fail",
        )
        raise RuntimeError("pitest failed. See output log in runner/output/")

    write_text(last_successful_path, read_text(active_test_file))
    print(f"Saved successful test to {last_successful_path}")

    pit_package_index = get_pit_package_index_path(project_root, package_name)
    baseline_score = None
    if pit_package_index.exists():
        baseline_score = parse_mutation_score(
            pit_package_index.read_text(encoding="utf-8", errors="replace")
        )

    pit_class_report = get_pit_class_report_path(project_root, cut_class_name, package_name)
    mutation_summary_text = build_mutation_summary(pit_class_report)
    write_text(output_dir / "summary" / f"mutation_summary_v{v}.txt", mutation_summary_text)

    has_surviving = (
        "No surviving mutants" not in mutation_summary_text
        and "No PIT report found" not in mutation_summary_text
    )

    print_header("MUTATION FEEDBACK")
    print(f"Mutation augmentation enabled: {cfg.enable_mutation_augment}")
    print(f"Baseline mutation score: {baseline_score or '-'}")
    print(f"Surviving mutants: {'yes' if has_surviving else 'no'}")
    if has_surviving:
        preview = (
            mutation_summary_text[:120] + "..."
            if len(mutation_summary_text) > 120 else mutation_summary_text
        )
        print(f"Mutation summary: {preview}")
    if not cfg.enable_mutation_augment:
        print("Mutation augmentation skipped: disabled in config.")
    elif not has_surviving:
        print("Mutation augmentation skipped: no surviving mutants.")

    # --- Phase 4: Mutation augmentation ---
    augmented_score = None
    augmentation_success = "skip"
    augmentation_fix_used = False

    if cfg.enable_mutation_augment and has_surviving:
        augmented_score, augmentation_success, augmentation_fix_used = (
            _run_mutation_augmentation(
                ctx, mutation_summary_text, baseline_score,
                pitest_targets, pit_package_index,
            )
        )

    # --- Phase 5: Summary ---
    _write_run_summary(
        ctx, repair, baseline_score, augmented_score,
        augmentation_success, augmentation_fix_used,
    )

    print("pitest: SUCCESS")
    print_header("DONE")
    print(f"Run complete: v{v}")
    print(f"Artifacts: {output_dir}")


if __name__ == "__main__":
    config_path_arg = None
    if len(sys.argv) > 1:
        cfg_arg = Path(sys.argv[1])
        config_path_arg = (
            cfg_arg if cfg_arg.is_absolute()
            else Path(__file__).resolve().parent / cfg_arg
        )
    main(config_path_arg)
