#!/usr/bin/env python3
"""
Summarize batch experiment outcomes from:
  - output/batch_results.txt (one row per CUT; best for 40-CUT batches)
  - output/summary/runs_table.txt (append log; optional --last N for recent rows)

Usage:
  python summarize_batch.py
  python summarize_batch.py --runs-last 80
  python summarize_batch.py --batch-results path/to/batch_results.txt
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

RUNNER_ROOT = Path(__file__).resolve().parent
DEFAULT_BATCH = RUNNER_ROOT / "output" / "batch_results.txt"
DEFAULT_RUNS = RUNNER_ROOT / "output" / "summary" / "runs_table.txt"

# runs_table.tsv columns (0-based)
IDX_RESULT = 8
IDX_FAILURE_CAT = 9


def parse_batch_results(path: Path) -> list[dict[str, str]] | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|-"):
            continue
        parts = [p.strip() for p in line.split("|")]
        parts = [p for p in parts if p]
        if len(parts) < 3 or parts[0].upper() == "CUT":
            continue
        rows.append(
            {
                "cut": parts[0],
                "status": parts[1].upper(),
                "reached": parts[2] if len(parts) > 2 else "",
                "stuck_at": parts[3] if len(parts) > 3 else "",
            }
        )
    return rows or None


def summarize_batch_results(rows: list[dict[str, str]]) -> None:
    n = len(rows)
    by_status = Counter(r["status"] for r in rows)
    success = by_status.get("SUCCESS", 0)
    print(f"## From batch_results ({n} CUTs)")
    print(f"SUCCESS: {success}  FAILED: {by_status.get('FAILED', 0)}  "
          f"TIMEOUT: {by_status.get('TIMEOUT', 0)}  ERROR: {by_status.get('ERROR', 0)}")
    if n:
        print(f"Pass rate: {100.0 * success / n:.1f}%")
    stuck = Counter(r["stuck_at"] for r in rows if r["status"] != "SUCCESS")
    if stuck:
        print("\nFailure stuck_at (top):")
        for k, v in stuck.most_common(12):
            if k and k != "-":
                print(f"  {k}: {v}")
    reached = Counter(r["reached"] for r in rows if r["status"] != "SUCCESS")
    if reached:
        print("\nFailure reached (top):")
        for k, v in reached.most_common(12):
            if k and k != "-":
                print(f"  {k}: {v}")


def parse_runs_table(path: Path, last_n: int | None) -> list[list[str]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines:
        return []
    data: list[list[str]] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        data.append(line.split("\t"))
    if last_n is not None and last_n > 0:
        data = data[-last_n:]
    return data


def summarize_runs_table(rows: list[list[str]], tail_slice: bool) -> None:
    note = " (tail slice)" if tail_slice else ""
    print(f"\n## From runs_table ({len(rows)} row(s)){note}")
    if not rows:
        print("(no data)")
        return
    results = Counter()
    cats = Counter()
    for r in rows:
        if len(r) <= IDX_FAILURE_CAT:
            continue
        results[r[IDX_RESULT]] += 1
        cat = r[IDX_FAILURE_CAT] or "-"
        if r[IDX_RESULT] != "Success":
            cats[cat] += 1
    print("Result:")
    for k, v in results.most_common():
        print(f"  {k}: {v}")
    if cats:
        print("\nFailure_category (failed rows only):")
        for k, v in cats.most_common(20):
            print(f"  {k}: {v}")


def main() -> int:
    p = argparse.ArgumentParser(description="Summarize batch_results and/or runs_table.")
    p.add_argument(
        "--batch-results",
        type=Path,
        default=DEFAULT_BATCH,
        help="Path to batch_results.txt",
    )
    p.add_argument(
        "--runs-table",
        type=Path,
        default=DEFAULT_RUNS,
        help="Path to runs_table.txt",
    )
    p.add_argument(
        "--runs-last",
        type=int,
        default=None,
        metavar="N",
        help="Only last N data rows of runs_table (useful if table has long history)",
    )
    p.add_argument(
        "--runs-only",
        action="store_true",
        help="Skip batch_results; only print runs_table section",
    )
    args = p.parse_args()

    if not args.runs_only:
        br = parse_batch_results(args.batch_results)
        if br:
            summarize_batch_results(br)
        else:
            print(f"No batch table parsed from {args.batch_results} (missing or empty).")

    rt = parse_runs_table(args.runs_table, args.runs_last)
    summarize_runs_table(rt, tail_slice=args.runs_last is not None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
