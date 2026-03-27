#!/usr/bin/env python3
"""
Remove bulky artifacts under output/, keep small metadata for reports.

Default keeps:
  - output/summary/   (runs_table.txt, summary_v*.txt)
  - output/batch_results.txt (if present)
  - output/last_successful/ (optional; needed for next runs using successful_ref)

Removes typical dirs: generated_tests, logs, prompt, raw_*, repair_*, invalid_*, mutation_*.

Usage:
  python cleanup_runner_output.py --dry-run
  python cleanup_runner_output.py --yes
  python cleanup_runner_output.py --yes --drop-last-successful
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

RUNNER_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = RUNNER_ROOT / "output"

# Top-level entries under output/ to delete (dirs)
DIRS_TO_REMOVE = (
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
)

FILES_AT_ROOT = ()  # batch_results kept


def main() -> int:
    ap = argparse.ArgumentParser(description="Prune runner output/ after a batch.")
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Runner output directory",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print actions only")
    ap.add_argument(
        "--yes",
        action="store_true",
        help="Required to actually delete (safety)",
    )
    ap.add_argument(
        "--drop-last-successful",
        action="store_true",
        help="Also remove last_successful/ (next runs lose successful_ref hints)",
    )
    args = ap.parse_args()
    root: Path = args.output_dir
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    to_remove: list[Path] = []
    for name in DIRS_TO_REMOVE:
        p = root / name
        if p.exists():
            to_remove.append(p)
    if args.drop_last_successful:
        ls = root / "last_successful"
        if ls.exists():
            to_remove.append(ls)

    if not to_remove:
        print("Nothing to remove.")
        return 0

    print("Planned removals:")
    for p in to_remove:
        print(f"  {p}")
    if args.dry_run or not args.yes:
        if not args.yes:
            print("\nRe-run with --yes to delete (or only --dry-run to preview).")
        return 0

    for p in to_remove:
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        else:
            p.unlink(missing_ok=True)
        print(f"Removed {p}")
    print("Kept: summary/, batch_results.txt (if any)" +
          ("" if args.drop_last_successful else ", last_successful/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
