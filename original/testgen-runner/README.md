# testgen-runner

LLM-driven JUnit 5 test generation pipeline for Java Maven projects (Ollama).

## Quick Start

```bash
python runner.py config/config_calculator.json
python batch_runner.py --only Region
```

`config/config.json` also supports:

- `mvn_timeout_sec` — Maven subprocess (default `300`; `<= 0` disables).
- `ollama_timeout_sec` — each `ollama run` call (default `180`; `<= 0` disables).
- `max_repair_attempts` — repair loop cap (default `10`; values `< 1` are clamped to `1`).
- `artifact_write_mode` — `full` (default) writes prompts and raw LLM outputs under `output/`; `minimal` skips those to cut disk I/O on large batches.

Maven: `mvn_test_fail_*.log` is written only when that Maven run **fails** (success no longer spams a log). Timeouts still write `*_timeout_*.log` under `output/logs/`.

## Batch workflow (40 CUTs)

1. **Smoke test**: With `artifact_write_mode: minimal`, run one previously failing CUT (e.g. `batch_runner.py --only CommandLine`) and confirm `summary/` + failure logs are enough to debug.
2. **Full batch**: Run `batch_runner.py`, then **`python summarize_batch.py`** — reads `output/batch_results.txt` (pass rate, `stuck_at` / `reached`) and optionally `output/summary/runs_table.txt` (use `--runs-last N` if the table has a long history).
3. **Deep dive one CUT**: Copy `config.json`, set `artifact_write_mode: full`, point `cut_path` at that CUT, re-run `runner.py`.
4. **Prune disk after batch**: `python cleanup_runner_output.py --dry-run` then **`python cleanup_runner_output.py --yes`** — keeps `output/summary/` and `output/batch_results.txt` (and by default `last_successful/`). Add `--drop-last-successful` only if you accept losing reference tests for the next run.

## Tests

Parser / validator regression (no Maven or Ollama required):

```bash
python -m unittest tests.test_parser -v
```

## Directory Structure

| Path | Purpose |
|------|---------|
| `runner.py` | Main pipeline: generate → validate → mvn test → repair → pitest → mutation augment |
| `mutant_summary.py` | PIT mutation report parsing for augmentation prompt |
| `batch_runner.py` | Batch runner: auto-discover and run all CUTs |
| `summarize_batch.py` | Aggregate pass rate / failure buckets from `batch_results.txt` + `runs_table.txt` |
| `cleanup_runner_output.py` | Delete bulky `output/` artifacts; keep `summary/` and `batch_results.txt` |
| `smoke_compile_repair.py` | Smoke test for compile repair flow |
| `config/` | Per-CUT configs (Calculator, Region, Reference) |
| `prompts/` | Generation and repair prompt templates |
| `tests/` | Unit tests (`test_parser.py`: Surefire parsing, test extraction, validation) |
| `output/` | Run artifacts (generated tests, logs, summary) |
| `docs/` | Documentation (refactor history, investigation, planning) |
| `archive/` | Validation scripts, historical evidence |

## Docs Layout

- `docs/refactor/` — Batch 1–4 refactor records
- `docs/investigation/` — Prompt fixes, code review, Reference investigation
- `docs/planning/` — Experiment matrix, baseline, report structure

## Output

Run results go to `output/`. See `output/README.md` for subdirectory descriptions.
