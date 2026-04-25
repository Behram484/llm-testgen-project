#!/usr/bin/env python3
"""
Run a small prompt-profile follow-up study on a fixed CUT subset.

Typical usage:
  python run_prompt_profile_followup.py --clean-output
  python run_prompt_profile_followup.py --profiles standard,detailed,guided-lite --repeats 2 --clean-output

By default this script:
  - uses the current runner config as a base
  - overrides model / generation_profile / repair budget for the follow-up
  - runs only the CUTs listed in config/prompt_lite_subset_12.txt
  - archives each run's output/ directory under followup_runs/
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


RUNNER_ROOT = Path(__file__).resolve().parent
BATCH_RUNNER = RUNNER_ROOT / "batch_runner.py"
DEFAULT_BASE_CONFIG = RUNNER_ROOT / "config" / "config.json"
DEFAULT_CUTS_FILE = RUNNER_ROOT / "config" / "prompt_lite_subset_12.txt"
DEFAULT_OUTPUT_DIR = RUNNER_ROOT / "output"
DEFAULT_ARCHIVE_ROOT = RUNNER_ROOT / "followup_runs"

PROFILE_MAP = {
    "standard": "baseline_behavior",
    "baseline": "baseline_behavior",
    "baseline_behavior": "baseline_behavior",
    "detailed": "detailed_behavior",
    "detailed_behavior": "detailed_behavior",
    "guided-lite": "guided_lite_behavior",
    "guided_lite": "guided_lite_behavior",
    "guided_lite_behavior": "guided_lite_behavior",
}


def load_cut_subset(path: Path) -> list[str]:
    cuts: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        cuts.append(line)
    return cuts


def clean_output_dir(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for child in root.iterdir():
        if child.name == "README.md":
            continue
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
        else:
            child.unlink(missing_ok=True)


def ensure_output_clean(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    dirty = [child.name for child in root.iterdir() if child.name != "README.md"]
    if dirty:
        joined = ", ".join(sorted(dirty))
        raise RuntimeError(
            "output/ is not clean. Re-run with --clean-output, or archive/remove these first: "
            + joined
        )


def archive_output_dir(source: Path, target: Path) -> None:
    if not source.exists():
        raise RuntimeError(f"Expected output directory does not exist: {source}")
    if target.exists():
        raise RuntimeError(f"Archive target already exists: {target}")
    shutil.copytree(source, target)


def resolve_profiles(raw_profiles: str) -> list[tuple[str, str]]:
    profiles: list[tuple[str, str]] = []
    for raw in raw_profiles.split(","):
        label = raw.strip()
        if not label:
            continue
        key = label.lower()
        if key not in PROFILE_MAP:
            allowed = ", ".join(sorted(PROFILE_MAP))
            raise ValueError(f"Unknown profile '{label}'. Allowed values: {allowed}")
        profiles.append((label, PROFILE_MAP[key]))
    if not profiles:
        raise ValueError("No profiles selected.")
    return profiles


def main() -> int:
    ap = argparse.ArgumentParser(description="Run a prompt-profile follow-up study on a CUT subset.")
    ap.add_argument("--base-config", type=Path, default=DEFAULT_BASE_CONFIG, help="Base config JSON")
    ap.add_argument("--cuts-file", type=Path, default=DEFAULT_CUTS_FILE, help="CUT subset file")
    ap.add_argument(
        "--profiles",
        default="standard,detailed,guided-lite",
        help="Comma-separated profile labels: standard,detailed,guided-lite",
    )
    ap.add_argument("--repeats", type=int, default=1, help="Number of repeats per profile")
    ap.add_argument("--model", default="deepseek-coder:6.7b", help="Model override")
    ap.add_argument("--attempts", type=int, default=5, help="Repair budget override")
    ap.add_argument(
        "--artifact-write-mode",
        default="minimal",
        choices=("minimal", "full"),
        help="Artifact write mode override",
    )
    ap.add_argument(
        "--disable-mutation-augment",
        action="store_true",
        help="Disable mutation augmentation for a faster prompt-only follow-up",
    )
    ap.add_argument(
        "--archive-root",
        type=Path,
        default=DEFAULT_ARCHIVE_ROOT,
        help="Root directory for archived follow-up outputs",
    )
    ap.add_argument(
        "--clean-output",
        action="store_true",
        help="Remove existing output/ contents before each run and after archiving",
    )
    args = ap.parse_args()

    if args.repeats < 1:
        raise SystemExit("--repeats must be at least 1")
    if args.attempts < 1:
        raise SystemExit("--attempts must be at least 1")
    if not args.base_config.exists():
        raise SystemExit(f"Base config not found: {args.base_config}")
    if not args.cuts_file.exists():
        raise SystemExit(f"CUT subset file not found: {args.cuts_file}")

    profiles = resolve_profiles(args.profiles)
    cuts = load_cut_subset(args.cuts_file)
    if not cuts:
        raise SystemExit(f"No CUTs loaded from {args.cuts_file}")

    base_cfg = json.loads(args.base_config.read_text(encoding="utf-8"))
    session_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_root = args.archive_root / f"prompt_followup_{session_stamp}"
    session_root.mkdir(parents=True, exist_ok=False)

    session_manifest = {
        "timestamp": session_stamp,
        "base_config": str(args.base_config),
        "cuts_file": str(args.cuts_file),
        "cuts": cuts,
        "profiles": [label for label, _ in profiles],
        "model": args.model,
        "attempts": args.attempts,
        "artifact_write_mode": args.artifact_write_mode,
        "enable_mutation_augment": not args.disable_mutation_augment,
        "repeats": args.repeats,
    }
    (session_root / "session_manifest.json").write_text(
        json.dumps(session_manifest, indent=2),
        encoding="utf-8",
    )
    (session_root / "cuts.txt").write_text("\n".join(cuts) + "\n", encoding="utf-8")

    run_records: list[dict[str, object]] = []
    only_arg = ",".join(cuts)

    for label, generation_profile in profiles:
        for repeat_idx in range(1, args.repeats + 1):
            if args.clean_output:
                clean_output_dir(DEFAULT_OUTPUT_DIR)
            else:
                ensure_output_clean(DEFAULT_OUTPUT_DIR)

            cfg = dict(base_cfg)
            cfg["model"] = args.model
            cfg["generation_profile"] = generation_profile
            cfg["max_repair_attempts"] = args.attempts
            cfg["artifact_write_mode"] = args.artifact_write_mode
            cfg["enable_mutation_augment"] = not args.disable_mutation_augment

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".json",
                prefix=f"followup_{generation_profile}_",
                delete=False,
                encoding="utf-8",
            ) as tmp:
                json.dump(cfg, tmp, indent=2)
                tmp_path = Path(tmp.name)

            run_name = f"{label.replace(' ', '_')}_run{repeat_idx}"
            archive_dir = session_root / run_name
            command = [
                sys.executable,
                str(BATCH_RUNNER),
                "--config",
                str(tmp_path),
                "--only",
                only_arg,
            ]

            print("")
            print(f"=== Running {run_name} ===")
            print(f"profile={generation_profile}")
            print(f"cuts={only_arg}")
            result = subprocess.run(command, cwd=RUNNER_ROOT, check=False)

            archive_output_dir(DEFAULT_OUTPUT_DIR, archive_dir)
            (archive_dir / "used_config.json").write_text(
                json.dumps(cfg, indent=2),
                encoding="utf-8",
            )
            (archive_dir / "command.txt").write_text(
                " ".join(command) + "\n",
                encoding="utf-8",
            )
            (archive_dir / "exit_code.txt").write_text(f"{result.returncode}\n", encoding="utf-8")
            tmp_path.unlink(missing_ok=True)

            run_records.append(
                {
                    "run_name": run_name,
                    "profile_label": label,
                    "generation_profile": generation_profile,
                    "repeat": repeat_idx,
                    "exit_code": result.returncode,
                    "archive_dir": str(archive_dir),
                }
            )

            if args.clean_output:
                clean_output_dir(DEFAULT_OUTPUT_DIR)

    (session_root / "run_records.json").write_text(
        json.dumps(run_records, indent=2),
        encoding="utf-8",
    )

    print("")
    print(f"Archived follow-up runs under: {session_root}")
    print("Run summary:")
    for record in run_records:
        print(
            f"  {record['run_name']}: exit_code={record['exit_code']} "
            f"archive={record['archive_dir']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
