# New Output Compare Grand Summary

This summary was regenerated from the current `batch_results.txt` files under `Original`, `ansi`, `guided_lite+ansi`, and `ANSI fix + last_successful enabled`.

Coverage: 2240 batch result rows from 56 run folders.

Success is counted as `Status = SUCCESS`; `FAILED` and `TIMEOUT` are counted as unsuccessful. Mutation means are unweighted means of per-suite percentages. Augmented mutation means and deltas use only rows with an augmented mutation score.

## Main Takeaways

- ANSI fixing is the dominant improvement: across the matched full-factorial conditions, ANSI fixed runs improve success by about +27.5 to +43.34 percentage points over Original.
- Model capability remains the main separator: under ANSI fixed conditions, 32B stays at 80.00-86.67% success, while 6.7B stays at 49.17-63.33%.
- Larger repair budgets help 6.7B but not 32B: ANSI fixed 15 attempts changes 6.7B by +5.00 to +7.50 pp, while 32B changes by -3.34 to -1.67 pp.
- Detailed prompting does not consistently improve success. In ANSI fixed full runs, baseline is higher than detailed for both models and both repair budgets.
- Guided-lite and last-successful variants do not beat the matched ANSI baseline in the available runs. Guided-lite 15-attempt and 32B guided-lite are single-run pilots.

## Success Rate Summary

| Pipeline | Model | Attempts | Prompt | Runs | Success | Failed | Timeout | Total | Success rate | Coverage |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| ansi_fixed | 32b | 5 | baseline | 3 | 104 | 16 | 0 | 120 | 86.67% | full_3_runs |
| ansi_fixed | 32b | 5 | detailed | 3 | 98 | 21 | 1 | 120 | 81.67% | full_3_runs |
| ansi_fixed | 32b | 15 | baseline | 3 | 100 | 20 | 0 | 120 | 83.33% | full_3_runs |
| ansi_fixed | 32b | 15 | detailed | 3 | 96 | 21 | 3 | 120 | 80% | full_3_runs |
| ansi_fixed | 6.7b | 5 | baseline | 3 | 70 | 47 | 3 | 120 | 58.33% | full_3_runs |
| ansi_fixed | 6.7b | 5 | detailed | 3 | 59 | 58 | 3 | 120 | 49.17% | full_3_runs |
| ansi_fixed | 6.7b | 15 | baseline | 3 | 76 | 43 | 1 | 120 | 63.33% | full_3_runs |
| ansi_fixed | 6.7b | 15 | detailed | 3 | 68 | 49 | 3 | 120 | 56.67% | full_3_runs |
| ansi_last_successful | 6.7b | 5 | baseline | 3 | 68 | 51 | 1 | 120 | 56.67% | full_3_runs |
| guided_lite_ansi | 32b | 5 | guided_lite | 1 | 30 | 10 | 0 | 40 | 75% | single_run_pilot |
| guided_lite_ansi | 6.7b | 5 | guided_lite | 3 | 61 | 55 | 4 | 120 | 50.83% | full_3_runs |
| guided_lite_ansi | 6.7b | 15 | guided_lite | 1 | 19 | 21 | 0 | 40 | 47.5% | single_run_pilot |
| original | 32b | 5 | baseline | 3 | 52 | 67 | 1 | 120 | 43.33% | full_3_runs |
| original | 32b | 5 | detailed | 3 | 54 | 65 | 1 | 120 | 45% | full_3_runs |
| original | 32b | 15 | baseline | 3 | 58 | 62 | 0 | 120 | 48.33% | full_3_runs |
| original | 32b | 15 | detailed | 3 | 53 | 67 | 0 | 120 | 44.17% | full_3_runs |
| original | 6.7b | 5 | baseline | 3 | 33 | 86 | 1 | 120 | 27.5% | full_3_runs |
| original | 6.7b | 5 | detailed | 3 | 25 | 95 | 0 | 120 | 20.83% | full_3_runs |
| original | 6.7b | 15 | baseline | 3 | 36 | 78 | 6 | 120 | 30% | full_3_runs |
| original | 6.7b | 15 | detailed | 3 | 35 | 85 | 0 | 120 | 29.17% | full_3_runs |

## Original vs ANSI Fixed

| Model | Attempts | Prompt | Original | ANSI fixed | Delta |
|---|---:|---|---:|---:|---:|
| 32b | 5 | baseline | 52/120 (43.33%) | 104/120 (86.67%) | +43.34 pp |
| 32b | 5 | detailed | 54/120 (45%) | 98/120 (81.67%) | +36.67 pp |
| 32b | 15 | baseline | 58/120 (48.33%) | 100/120 (83.33%) | +35 pp |
| 32b | 15 | detailed | 53/120 (44.17%) | 96/120 (80%) | +35.83 pp |
| 6.7b | 5 | baseline | 33/120 (27.5%) | 70/120 (58.33%) | +30.83 pp |
| 6.7b | 5 | detailed | 25/120 (20.83%) | 59/120 (49.17%) | +28.34 pp |
| 6.7b | 15 | baseline | 36/120 (30%) | 76/120 (63.33%) | +33.33 pp |
| 6.7b | 15 | detailed | 35/120 (29.17%) | 68/120 (56.67%) | +27.5 pp |

## Repair Budget Effect Under ANSI Fixed

| Model | Prompt | 5 attempts | 15 attempts | Delta |
|---|---|---:|---:|---:|
| 32b | baseline | 104/120 (86.67%) | 100/120 (83.33%) | -3.34 pp |
| 32b | detailed | 98/120 (81.67%) | 96/120 (80%) | -1.67 pp |
| 6.7b | baseline | 70/120 (58.33%) | 76/120 (63.33%) | +5 pp |
| 6.7b | detailed | 59/120 (49.17%) | 68/120 (56.67%) | +7.5 pp |

## Auxiliary Experiments

| Comparison | Reference | Experiment | Delta | Note |
|---|---:|---:|---:|---|
| Guided-lite vs ANSI baseline | 70/120 (58.33%) | 61/120 (50.83%) | -7.5 pp | guided-lite has full 3 runs |
| Guided-lite 15-attempt pilot vs ANSI baseline | 76/120 (63.33%) | 19/40 (47.5%) | -15.83 pp | guided-lite is single-run pilot; reference is full 3 runs |
| Guided-lite 32B pilot vs ANSI baseline | 104/120 (86.67%) | 30/40 (75%) | -11.67 pp | guided-lite is single-run pilot; reference is full 3 runs |
| Last-successful vs ANSI baseline | 70/120 (58.33%) | 68/120 (56.67%) | -1.66 pp | both full 3 runs |

## Mutation Score Summary

| Pipeline | Model | Attempts | Prompt | Successful suites | PIT-completed cases | Mean baseline mutation score | Augmented cases | Mean augmented mutation score | Mean delta |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| ansi_fixed | 32b | 5 | baseline | 104/120 | 104 | 62.69% | 43 | 78.89% | +14.63 pp |
| ansi_fixed | 32b | 5 | detailed | 98/120 | 98 | 59.55% | 36 | 73.96% | +15.91 pp |
| ansi_fixed | 32b | 15 | baseline | 100/120 | 100 | 63.79% | 44 | 79.16% | +15.66 pp |
| ansi_fixed | 32b | 15 | detailed | 96/120 | 96 | 59.92% | 43 | 77.91% | +19.38 pp |
| ansi_fixed | 6.7b | 5 | baseline | 70/120 | 70 | 60.84% | 16 | 68.34% | +8.71 pp |
| ansi_fixed | 6.7b | 5 | detailed | 59/120 | 59 | 62.44% | 12 | 73.04% | +6.65 pp |
| ansi_fixed | 6.7b | 15 | baseline | 76/120 | 76 | 61.96% | 21 | 55.3% | -3.34 pp |
| ansi_fixed | 6.7b | 15 | detailed | 68/120 | 68 | 56.38% | 14 | 67.4% | +10.26 pp |
| ansi_last_successful | 6.7b | 5 | baseline | 68/120 | 68 | 65.48% | 19 | 58.91% | +2.37 pp |
| guided_lite_ansi | 32b | 5 | guided_lite | 30/40 | 30 | 60.64% | 15 | 78.48% | +21.19 pp |
| guided_lite_ansi | 6.7b | 5 | guided_lite | 61/120 | 61 | 58.21% | 12 | 54.94% | +7.64 pp |
| guided_lite_ansi | 6.7b | 15 | guided_lite | 19/40 | 19 | 51.82% | 3 | 76.52% | +23.81 pp |
| original | 32b | 5 | baseline | 52/120 | 52 | 56.61% | 10 | 79.06% | +24.54 pp |
| original | 32b | 5 | detailed | 54/120 | 54 | 57.06% | 13 | 64.81% | +19.77 pp |
| original | 32b | 15 | baseline | 58/120 | 58 | 58.14% | 9 | 73.53% | +23.54 pp |
| original | 32b | 15 | detailed | 53/120 | 53 | 55.7% | 14 | 73.53% | +19.49 pp |
| original | 6.7b | 5 | baseline | 33/120 | 33 | 49.51% | 6 | 48.66% | -0.94 pp |
| original | 6.7b | 5 | detailed | 25/120 | 25 | 49.23% | 5 | 57.54% | +14.79 pp |
| original | 6.7b | 15 | baseline | 36/120 | 36 | 56.98% | 8 | 59.44% | +9.66 pp |
| original | 6.7b | 15 | detailed | 35/120 | 35 | 53.4% | 1 | 85.71% | +14.29 pp |

## Output Files

- `grand_success_summary.csv`: condition-level success rates.
- `grand_success_per_run.csv`: run-level success rates.
- `grand_mutation_summary.csv`: condition-level mutation score summary.
- `grand_mutation_per_run.csv`: run-level mutation score summary.
- `grand_key_comparisons.csv`: original-vs-ANSI, budget, guided-lite, and last-successful comparisons.
- `grand_cut_level_results.csv`: parsed CUT-level raw table from all included `batch_results.txt` files.
