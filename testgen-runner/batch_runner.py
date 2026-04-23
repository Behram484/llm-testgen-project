#!/usr/bin/env python3
"""
Batch runner: auto-discover all CUT .java files and run the full pipeline for each.

Usage:
  python batch_runner.py                 # run all CUTs
  python batch_runner.py --only Region   # run only Region
  python batch_runner.py --config path/to/config.json
  python batch_runner.py --dry-run       # show what would run without executing
"""
import json
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

RUNNER_ROOT = Path(__file__).resolve().parent
RUNNER = RUNNER_ROOT / "runner.py"
BASE_CONFIG = RUNNER_ROOT / "config" / "config.json"
RESULTS_FILE = RUNNER_ROOT / "output" / "batch_results.txt"


def discover_cuts(project_root: Path) -> list[dict]:
    src_main = project_root / "src" / "main"
    if not src_main.exists():
        return []
    cuts = []
    for java_file in sorted(src_main.rglob("*.java")):
        rel = java_file.relative_to(project_root).as_posix()
        test_rel = rel.replace("src/main/java/", "src/test/java/").replace(".java", "Test.java")
        cuts.append({"name": java_file.stem, "cut_path": rel, "test_output_path": test_rel})
    return cuts


def run_one(cut: dict, base_cfg: dict) -> dict:
    cut_name = cut["name"]
    cfg = {**base_cfg, "cut_path": cut["cut_path"], "test_output_path": cut["test_output_path"]}

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", prefix=f"config_{cut_name}_", delete=False, encoding="utf-8"
    )
    json.dump(cfg, tmp, indent=2)
    tmp.close()

    start = datetime.now()
    try:
        result = subprocess.run(
            [sys.executable, str(RUNNER), tmp.name],
            cwd=RUNNER_ROOT,
            capture_output=True,
            text=True,
            timeout=900,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = (datetime.now() - start).total_seconds()
        out = result.stdout + "\n" + result.stderr
        summary = parse_summary(cut_name)
        summary["cut"] = cut_name
        summary["elapsed_sec"] = round(elapsed, 1)
        summary["status"] = "SUCCESS" if result.returncode == 0 else "FAILED"
        summary["reached"] = infer_reached(out, summary["status"])
        if result.returncode != 0:
            summary["stuck_at"] = infer_stuck_stage(out)
        return summary
    except subprocess.TimeoutExpired:
        return {"cut": cut_name, "status": "TIMEOUT", "stuck_at": "timeout"}
    except Exception as e:
        return {"cut": cut_name, "status": "ERROR", "stuck_at": str(e)}
    finally:
        Path(tmp.name).unlink(missing_ok=True)


def parse_summary(cut_name: str) -> dict:
    summary_dir = RUNNER_ROOT / "output" / "summary"
    if not summary_dir.exists():
        return {}
    needle = f"{cut_name}.java"
    candidates = []
    for f in summary_dir.glob("summary_v*.txt"):
        try:
            text = f.read_text(encoding="utf-8")
            if needle in text:
                candidates.append((f.stat().st_mtime, text))
        except Exception:
            pass
    if not candidates:
        return {}
    candidates.sort(reverse=True)
    out = {}
    for line in candidates[0][1].splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            k = k.strip().lower()
            if k in ("mvn_test", "pitest", "baseline_mutation_score", "augmented_mutation_score", "repair_attempts"):
                out[k] = v.strip()
    return {
        "mvn_test": out.get("mvn_test", "?"),
        "pitest": out.get("pitest", "?"),
        "baseline_mutation": out.get("baseline_mutation_score", "?"),
        "augmented_mutation": out.get("augmented_mutation_score", "-"),
        "repair_attempts": out.get("repair_attempts", "?"),
    }


def infer_stuck_stage(out: str) -> str:
    # Do not match bare "mvn_timeout" — stdout always contains mvn_timeout_sec= from config.
    checks = [
        ("validation_fail", "validator"),
        ("repair_validation_fail", "repair_validation_fail"),
        ("Maven timed out after", "mvn_timeout"),
        ("PITest/Maven timed out", "pitest_timeout"),
        ("mvn_no_parse", "mvn_no_parse"),
        ("repair_exceeded", "repair_exceeded"),
        ("pitest failed", "pitest"),
    ]
    for keyword, stage in checks:
        if keyword in out:
            return stage
    return "unknown"


def infer_reached(out: str, status: str) -> str:
    if status == "SUCCESS":
        return "done"
    stages = [
        ("pitest: SUCCESS", "pitest_ok"),
        ("RUNNING PITEST", "mvn_ok"),
        ("mvn test: SUCCESS", "mvn_ok"),
        ("RUNNING MVN TEST", "generated"),
        ("ACTIVATING TEST", "generated"),
        ("CALLING OLLAMA", "llm_called"),
    ]
    for keyword, reached in stages:
        if keyword in out:
            return reached
    return "init"


def format_table(results: list[dict]) -> str:
    lines = [
        f"## Batch results — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| CUT | Status | reached | stuck_at | baseline | augmented | repair | elapsed |",
        "|-----|--------|---------|----------|----------|-----------|--------|---------|",
    ]
    for r in results:
        lines.append(
            f"| {r.get('cut','?')} | {r.get('status','?')} | {r.get('reached','-')} "
            f"| {r.get('stuck_at','-')} | {r.get('baseline_mutation','?')} "
            f"| {r.get('augmented_mutation','-')} "
            f"| {r.get('repair_attempts','?')} | {r.get('elapsed_sec','?')} |"
        )
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    only_cuts: list[str] | None = None
    config_path = BASE_CONFIG
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        if idx + 1 < len(sys.argv):
            only_cuts = [s.strip() for s in sys.argv[idx + 1].split(",")]
    if "--config" in sys.argv:
        idx = sys.argv.index("--config")
        if idx + 1 < len(sys.argv):
            config_path = Path(sys.argv[idx + 1]).resolve()
        else:
            print("ERROR: --config requires a path")
            sys.exit(1)

    if not config_path.exists():
        print(f"ERROR: config not found: {config_path}")
        sys.exit(1)

    base_cfg = json.loads(config_path.read_text(encoding="utf-8"))
    project_root = Path(base_cfg["project_root"])
    cuts = discover_cuts(project_root)

    if not cuts:
        print(f"No .java files found under {project_root / 'src' / 'main'}")
        sys.exit(1)

    if only_cuts:
        names_lower = [n.lower() for n in only_cuts]
        cuts = [c for c in cuts if c["name"].lower() in names_lower]
        if not cuts:
            print(f"CUT(s) not found: {only_cuts}")
            sys.exit(1)

    print(f"=== Batch run: {[c['name'] for c in cuts]} ===")

    if dry_run:
        for c in cuts:
            print(f"  [DRY-RUN] {c['name']} ({c['cut_path']})")
        return

    results = []
    for cut in cuts:
        print(f"\nRunning: {cut['name']} ({cut['cut_path']})")
        r = run_one(cut, base_cfg)
        results.append(r)
        status = r.get("status")
        reached = r.get("reached", "-")
        stuck = r.get("stuck_at", "-")
        if status == "SUCCESS":
            print(f"  => {status}")
        else:
            print(f"  => {status} (reached: {reached}, stuck_at: {stuck})")

    table = format_table(results)
    print(f"\n{table}")

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(table + "\n", encoding="utf-8")
    print(f"\nSaved to: {RESULTS_FILE}")

    failed = [r for r in results if r.get("status") != "SUCCESS"]
    if failed:
        print(f"\n[!] {len(failed)} failed: {[r['cut'] for r in failed]}")
        sys.exit(1)
    print("\nAll CUTs passed.")


if __name__ == "__main__":
    main()
