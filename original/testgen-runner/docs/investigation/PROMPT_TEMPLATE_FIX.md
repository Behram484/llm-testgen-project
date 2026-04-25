# Prompt Template Generalization Fix

**性质**：Prompt template correctness issue（非 Batch 5 重构）

**日期**：2026-03-12

---

## 问题

repair / generation / mutation 相关 prompt 中残留 Calculator-specific 硬编码，导致：

- Region 的 repair 被错误引导（package uk.sussex.testgen、add/subtract/mul/div/clamp）
- repair 产物 class 名错误（输出 RegionTest 而非 RegionTest_v19）
- 非 Calculator CUT 被系统性误导，污染实验结论

---

## 修改范围

### 1. runner.py

- `build_prompt()` 新增 `package_name` 参数
- 支持 `{PACKAGE}` 占位符替换
- 所有调用 repair / regen / generation / mutation 的 `build_prompt` 传入 `package_name`

### 2. 修改的 prompt 文件

| 文件 | 修改 |
|------|------|
| `semantic_repair.txt` | package → {PACKAGE}；移除 Calculator API；强化 class name 约束 |
| `compile_repair.txt` | 同上 |
| `baseline_behavior.txt` | package → {PACKAGE}；移除 Calculator API 与语义 |
| `mutation_augment.txt` | package → {PACKAGE}；移除 Calculator API 与语义 |

### 3. 新增约束

- class 名必须与 `{TEST_CLASS_NAME}` 完全一致，不得改为简化名
- 仅使用 `<CODE>` 中可见的 CUT API，不得假设 CUT 是 Calculator
- 不预设 CUT API，由 CUT 源码和 failure diagnosis 驱动修复

---

## 验证

- `build_prompt` 对 semantic_repair 生成 `package org.templateit`，无 Calculator 引导
- `archive/refactor_validation/` 回归脚本通过

---

## 下一步

优先回测 Region（结果单独保存，便于修复前/后对照）：

```bash
python batch_runner.py --only Region
```

结果追加到 `output/validation_post_prompt_fix.txt`。

### 回测时重点观察 4 点

1. **stuck_at 是否变化**：是否仍为 repair_validation_fail，或变为 SUCCESS / repair_exceeded
2. **invalid_repaired_reasons 是否消失**：class name、package 是否守住
3. **repair 输出是否使用真实 Region API**：contains、setStartReference 等，而非 add/subtract/mul/div/clamp
4. **若仍失败，性质是否更“真实”**：排除 prompt 模板残留后的模型能力问题
