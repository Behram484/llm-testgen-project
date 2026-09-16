# Experimental data — supporting CSVs

This directory contains the aggregated experimental data underlying the
results, tables, and figures in the dissertation. All CSVs were exported from
the runs collected on RunPod (NVIDIA A6000 / A40, 48 GB VRAM, Linux) across
the eight conditions of the 2 × 2 × 2 factorial under both pipelines plus the
follow-up experiments. They are provided so the headline numbers in
Chapter 4 can be checked directly without re-running the pipeline.

## File index

| File | Rows | What it is |
| --- | --- | --- |
| `grand_cut_level_results.csv` | 2,240 | One row per CUT × condition × run. Columns: `pipeline`, `model`, `attempts`, `profile`, `run`, `cut`, `status`, baseline / augmented mutation scores, `delta_pp`, `source_dir`. Master record. |
| `grand_success_per_run.csv` | 56 | Per-run success counts (one row per pipeline × model × prompt × attempts × run). Used to derive Section 4.1 / 4.2 success rates. |
| `grand_success_summary.csv` | 20 | Per-condition (3-run aggregate) success summary. Each row = one cell of the factorial. Drives Tables 1, 2, 4. |
| `grand_mutation_per_run.csv` | 56 | Per-run mutation analysis: PIT-completed cases, baseline / augmented mean MS, mean Δ. |
| `grand_mutation_summary.csv` | 20 | Per-condition mutation aggregate. Drives Table 3. |
| `grand_key_comparisons.csv` | 16 | Pre-computed reference-vs-experiment contrasts (e.g. ANSI-fixed vs original). One row per planned comparison. |
| `grand_summary.md` | — | Narrative summary of the eight conditions and the follow-up runs. |

## Pipeline / condition vocabulary

The CSVs use these short codes:

- `pipeline`: `original`, `ansi_fixed`, `guided_lite_ansi`, `ansi_last_successful`
- `model`: `32b` (Qwen2.5-Coder 32B Q4) or `6.7b` (DeepSeek-Coder 6.7B Q4)
- `profile`: `baseline`, `detailed`, `guided_lite`
- `attempts`: `5` or `15` (`max_repair_attempts`)
- `run`: `1`, `2`, `3` (independent repetition)
- `status`: `SUCCESS`, `FAILED`, `TIMEOUT`

## Mapping to dissertation tables and figures

| Thesis | Source CSV(s) |
| --- | --- |
| Table 1 (original 8-cell success) | `grand_success_summary.csv` filtered `pipeline == original` |
| Table 2 (original vs ANSI-fixed) | `grand_success_summary.csv` paired by `model × profile × attempts` + `grand_key_comparisons.csv` |
| Table 3 (mutation scores per condition) | `grand_mutation_summary.csv` filtered `pipeline == ansi_fixed` |
| Table 4 (follow-up — guided-lite, last-successful) | `grand_success_summary.csv` filtered `pipeline ∈ {guided_lite_ansi, ansi_last_successful}` |
| Table 5 (failure category distribution) | derived from per-CUT logs (not in this archive); `grand_cut_level_results.csv` shows per-CUT success/fail status |
| Figure 2 (5 vs 15 attempts) | `grand_success_summary.csv` ANSI-fixed cells |
| Figure 3 (mutation Δ per config) | `grand_mutation_summary.csv` ANSI-fixed cells |
| Figure 4 (follow-up vs comparator) | `grand_success_summary.csv` follow-ups vs ANSI-fixed comparators |
| Figure E1 (per-CUT dumbbell) | `grand_cut_level_results.csv` aggregated per CUT |
| Figure E2 (per-CUT × condition heatmap) | `grand_cut_level_results.csv` aggregated per CUT × condition (ANSI-fixed only) |
| Table E1 (Wilcoxon / McNemar p-values) | derived from `grand_cut_level_results.csv` paired per-CUT |
| Appendix D Tables D1, D2 | `grand_cut_level_results.csv` pivoted by CUT × condition |

## Reproducing key numbers from the CSVs

Two quick spot-checks for the headline finding:

1. **ANSI fix on 32B-baseline-5** (Section 4.2, "43.3% → 86.7%"):
   - In `grand_success_summary.csv`: rows `(original, 32b, 5, baseline)` and
     `(ansi_fixed, 32b, 5, baseline)` give `success_rate_percent` 43.33 and
     86.67.
2. **Mutation Δ on 32B configurations** (Section 4.3, "+14.6 to +19.4 pp"):
   - In `grand_mutation_summary.csv`: rows where `pipeline == ansi_fixed`
     and `model == 32b` give `mean_delta_pp` ranging 14.63 → 19.36.

A simple Python check:

```python
import csv
with open('grand_success_summary.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        if row['pipeline'] in ('original', 'ansi_fixed') and \
           row['model'] == '32b' and row['profile'] == 'baseline' and \
           row['attempts'] == '5':
            print(row['pipeline'], row['success_rate_percent'])
```

## Notes

- The `source_dir` column in `grand_cut_level_results.csv` references local
  paths used during data collection (e.g. `D:\report\report writing\...`).
  These are kept verbatim for provenance; they are not used by any of the
  CSVs themselves.
- All data is the result of completed pipeline runs; no synthetic or
  manually edited rows are present.
- The CSVs use UTF-8 with BOM (the `﻿` byte is preserved on the first
  header line). Most tools handle this transparently; in Python, decode
  with `encoding='utf-8-sig'`.
