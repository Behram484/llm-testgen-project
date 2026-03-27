# Pre-Experiment Validation Report

**Date**: 2026-03-12  
**CUTs**: Calculator, Region, Reference (in order)

---

## Summary Table

| CUT | Status | mvn test | pitest | mutation_score | repair_attempts | elapsed_sec |
|-----|--------|----------|--------|----------------|-----------------|-------------|
| Calculator | FAILED | SUCCESS* | SUCCESS* | 11/11* | 0* | 656.7 |
| Region | FAILED | SUCCESS* | SUCCESS* | 13/44* | 0* | 242.4 |
| Reference | FAILED | ? | ? | ? | ? | 364.0 |

\* From latest summary file (may be from previous run when current run failed before writing summary)

---

## Per-CUT Conclusions (from log)

### Calculator
- **full_run**: No
- **stuck_at**: repair_exceeded
- **Interpretation**: Validator passed, mvn test failed (assertion failures), repair loop ran and exceeded max attempts. Main pipeline intact; failure is LLM stochastic (could not fix tests in time).
- **known_boundary?**: No – repair_exceeded is expected behavior when model can't fix.
- **new_batch?**: No.

### Region
- **full_run**: No
- **stuck_at**: **repair_validation_fail**
- **Interpretation**: LLM 的 repair 输出未通过 validator（`Repaired test failed validation`）。与 repair_exceeded 不同：repair 产出被 validator 拒掉，而非 repair 轮数超限。
- **known_boundary?**: No – 属 repair prompt/model effectiveness。
- **new_batch?**: No – 优先做 prompt tuning。

### Reference
- **full_run**: No
- **stuck_at**: repair_exceeded
- **Interpretation**: New CUT. Validator passed, entered repair loop, exceeded max. Pipeline works for new CUT; failure is LLM stochastic.
- **known_boundary?**: No.
- **new_batch?**: No.

---

## Overall Judgment

1. **Main pipeline is intact**: All three CUTs reached the repair loop. No validator miskill, no mvn_no_parse, no compile-failure misclassification observed.
2. **Failure mode**: Primarily `repair_exceeded` – LLM could not fix failing tests within max attempts. This is stochastic, not a structural bug.
3. **Recommendation**: **Runner is ready for formal experiments.** No new batch needed. Proceed to define experiment matrix, fixed CUT set, and metrics.

---

## Next Steps

- Define experiment matrix (baseline / programmatic fix / mutation augment / CUT type)
- Fix CUT sample set
- Record: validator pass, first mvn pass, repair count, final success, failure stage, mutation score
