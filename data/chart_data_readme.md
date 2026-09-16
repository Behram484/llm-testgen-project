# Chart data for Original vs ANSI-fixed success rates

## Which data matches the screenshot?

The screenshot corresponds to the 5-attempt Original vs ANSI-fixed comparison. Use:

- `chart_original_vs_ansi_5_attempts.csv`
- X-axis: `chart_label`
- Series 1: `original_rate_percent_1dp`
- Series 2: `ansi_fixed_rate_percent_1dp`

Values:

| Condition | Original | ANSI-fixed |
|---|---:|---:|
| 32B baseline | 43.3 | 86.7 |
| 32B detailed | 45.0 | 81.7 |
| 6.7B baseline | 27.5 | 58.3 |
| 6.7B detailed | 20.8 | 49.2 |

## 15-attempt version of the same chart

Use `chart_original_vs_ansi_15_attempts.csv` with the same chart setup:

- X-axis: `chart_label`
- Series 1: `original_rate_percent_1dp`
- Series 2: `ansi_fixed_rate_percent_1dp`

Values:

| Condition | Original | ANSI-fixed |
|---|---:|---:|
| 32B baseline | 48.3 | 83.3 |
| 32B detailed | 44.2 | 80.0 |
| 6.7B baseline | 30.0 | 63.3 |
| 6.7B detailed | 29.2 | 56.7 |

## If the chart is about repair budget instead

If you want a chart comparing whether 15 repair attempts helped compared with 5 attempts, use `chart_repair_budget_effect_ansi_fixed.csv` instead. That table only uses ANSI-fixed runs:

- X-axis: `chart_label`
- Series 1: `ansi_fixed_5_attempts_rate_percent_1dp`
- Series 2: `ansi_fixed_15_attempts_rate_percent_1dp`

Values:

| Condition | 5 attempts | 15 attempts | Delta |
|---|---:|---:|---:|
| 32B baseline | 86.7 | 83.3 | -3.34 pp |
| 32B detailed | 81.7 | 80.0 | -1.67 pp |
| 6.7B baseline | 58.3 | 63.3 | +5.00 pp |
| 6.7B detailed | 49.2 | 56.7 | +7.50 pp |

## Source

All files were derived from `grand_success_summary.csv` in this folder. Success is counted as `Status = SUCCESS`; failed and timeout cases are unsuccessful. Each full condition has 3 runs x 40 CUTs = 120 total cases.
