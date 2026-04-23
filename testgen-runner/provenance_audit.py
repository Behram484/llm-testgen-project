"""
Provenance audit: byte-compare every CUT in testgen-lab against SF110 originals.
Outputs a Markdown table with match status for each class.
"""
import os
import sys
from pathlib import Path

TESTGEN_SRC = Path(r"D:\Project\testgen-lab\src\main\java")
SF110_ROOT = Path(r"D:\Project\DataBase\SF110-20130704-src")

# Pre-index: filename -> list of paths in SF110 (only src/main/java, skip evosuite-tests)
def build_sf110_index():
    index = {}
    for root, dirs, files in os.walk(SF110_ROOT):
        root_p = Path(root)
        # Only match source files, not evosuite-generated tests
        if "evosuite-tests" in str(root_p) or "src/test" in str(root_p).replace("\\", "/"):
            continue
        for f in files:
            if f.endswith(".java"):
                index.setdefault(f, []).append(root_p / f)
    return index

def files_identical(a: Path, b: Path) -> bool:
    return a.read_bytes() == b.read_bytes()

def get_package(java_file: Path) -> str:
    for line in java_file.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("package "):
            return stripped.split("package ", 1)[1].rstrip(";").strip()
    return "(no package)"

def main():
    print("Building SF110 file index...", file=sys.stderr)
    sf110_index = build_sf110_index()
    print(f"Indexed {sum(len(v) for v in sf110_index.values())} SF110 source files.", file=sys.stderr)

    cuts = sorted(TESTGEN_SRC.rglob("*.java"))
    print(f"Found {len(cuts)} CUT files.\n", file=sys.stderr)

    results = []
    for cut in cuts:
        name = cut.name
        pkg = get_package(cut)
        candidates = sf110_index.get(name, [])

        if not candidates:
            results.append((cut.stem, pkg, "NO_MATCH", "-", "-"))
            continue

        # Try to find exact byte match first
        matched_path = None
        matched_status = None
        for sf_path in candidates:
            if files_identical(cut, sf_path):
                matched_path = sf_path
                matched_status = "BYTE_IDENTICAL"
                break

        if matched_status == "BYTE_IDENTICAL":
            rel = matched_path.relative_to(SF110_ROOT)
            project = str(rel).split(os.sep)[0]
            results.append((cut.stem, pkg, matched_status, project, str(rel)))
            continue

        # No byte match — find best candidate by package match
        best = None
        for sf_path in candidates:
            sf_pkg = get_package(sf_path)
            if sf_pkg == pkg:
                best = sf_path
                break
        if best is None:
            best = candidates[0]

        rel = best.relative_to(SF110_ROOT)
        project = str(rel).split(os.sep)[0]

        # Characterize difference
        cut_text = cut.read_text(encoding="utf-8", errors="replace")
        sf_text = best.read_text(encoding="utf-8", errors="replace")

        if cut_text == sf_text:
            status = "TEXT_IDENTICAL"
        else:
            # Check if only whitespace/encoding differs
            cut_norm = "".join(cut_text.split())
            sf_norm = "".join(sf_text.split())
            if cut_norm == sf_norm:
                status = "WHITESPACE_ONLY_DIFF"
            else:
                # Count differing lines
                cut_lines = cut_text.splitlines()
                sf_lines = sf_text.splitlines()
                diff_count = 0
                for i in range(max(len(cut_lines), len(sf_lines))):
                    a = cut_lines[i] if i < len(cut_lines) else ""
                    b = sf_lines[i] if i < len(sf_lines) else ""
                    if a != b:
                        diff_count += 1
                status = f"DIFFERS ({diff_count} lines)"

        results.append((cut.stem, pkg, status, project, str(rel)))

    # Print Markdown table
    print("| # | Class | Package | Status | SF110 Project | SF110 Path |")
    print("|---|-------|---------|--------|---------------|------------|")
    for i, (cls, pkg, status, proj, path) in enumerate(results, 1):
        print(f"| {i} | {cls} | `{pkg}` | **{status}** | {proj} | `{path}` |")

    # Summary
    identical = sum(1 for r in results if r[2] == "BYTE_IDENTICAL")
    text_id = sum(1 for r in results if r[2] == "TEXT_IDENTICAL")
    ws_only = sum(1 for r in results if r[2] == "WHITESPACE_ONLY_DIFF")
    no_match = sum(1 for r in results if r[2] == "NO_MATCH")
    differs = sum(1 for r in results if r[2].startswith("DIFFERS"))
    total = len(results)

    print(f"\n## Summary")
    print(f"- Total CUTs: {total}")
    print(f"- BYTE_IDENTICAL: {identical}")
    print(f"- TEXT_IDENTICAL (same text, different encoding): {text_id}")
    print(f"- WHITESPACE_ONLY_DIFF: {ws_only}")
    print(f"- DIFFERS: {differs}")
    print(f"- NO_MATCH in SF110: {no_match}")

    if identical == total:
        print(f"\n**ALL {total} CUTs are byte-identical to SF110 originals. Benchmark purity: PURE.**")
    elif identical + text_id == total:
        print(f"\n**All {total} CUTs match SF110 at text level. {text_id} have encoding-only differences.**")

if __name__ == "__main__":
    main()
