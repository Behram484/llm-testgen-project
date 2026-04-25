# Post-Fix Baseline

**目的**：建立修复后完整基线，形成修复前/后对照表。

**运行**：2026-03-12 03:40，`python batch_runner.py`

---

## 修复前 vs 修复后

| CUT       | 修复前 stuck_at           | 修复后 stuck_at | 变化 |
|-----------|---------------------------|-----------------|------|
| Calculator| repair_exceeded           | repair_exceeded | 一致（无 repair_validation_fail） |
| Region    | repair_validation_fail    | repair_exceeded | ✓ 结构问题消除 |
| Reference | repair_exceeded           | repair_exceeded | ✓ 已确认（2026-03-12 调查） |

---

## 结果摘要

- **Calculator**：478.5s，repair_exceeded，mvn/pitest 均 SUCCESS（来自 summary）
- **Region**：588.0s，repair_exceeded，mvn/pitest 均 SUCCESS
- **Reference**：295s，repair_exceeded（与 Calculator、Region 一致）

---

## 下一步

1. ~~查清 Reference 的 unknown~~ ✓ 已确认 repair_exceeded
2. **进入 prompt/profile effectiveness 对比**：见 `EXPERIMENT_MATRIX.md` Phase 1
