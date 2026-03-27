# Prompt Fix Validation

**目的**：记录修复前/后对照，形成可追溯的因果验证。

---

## 1. 问题是什么

- Region 出现 `repair_validation_fail`：repair 产物被 validator 拒绝
- 根因：repair prompt 中残留 Calculator-specific 硬编码
  - `package uk.sussex.testgen`（Region 应为 org.templateit）
  - `For this CUT: add, subtract, mul, div, clamp`（Region 实际为 contains、setStartReference 等）
- 后果：模型被错误引导，输出 Calculator 测试 + 错误 class 名，系统性污染非 Calculator CUT 的实验结论

---

## 2. 修了什么

- `build_prompt()` 新增 `{PACKAGE}` 占位符，由 runner 注入真实 package
- `semantic_repair.txt`、`compile_repair.txt`、`baseline_behavior.txt`、`mutation_augment.txt` 去除 Calculator 硬编码
- 强化 class name 约束：必须与 `{TEST_CLASS_NAME}` 完全一致
- 明确：仅使用 `<CODE>` 中可见的 CUT API，不得假设 CUT 类型

---

## 3. 修复前后变化

| CUT    | 修复前 stuck_at           | 修复后 stuck_at | 变化 |
|--------|---------------------------|-----------------|------|
| Region | repair_validation_fail    | **repair_exceeded** | ✓ 结构问题消除 |

**结论**：repair 输出已合法，validator 不再拒绝。失败来自模型未收敛（repair 轮数超限），非 prompt 模板问题。

**repair 输出验证**（raw_repair_v22_r1）：
- package: `org.templateit` ✓
- class name: `RegionTest_v22` ✓
- API: contains, setStartReference, setEndReference, start, end ✓（无 add/subtract/mul/div/clamp）
- invalid_repaired: 无（10 轮 repair 均通过 validator）

**修复后运行**：2026-03-12 03:18，`python batch_runner.py --only Region`

---

## 定稿结论

> Prompt Template Generalization Fix successfully removed the Region-specific repair validation failure. After the fix, repaired outputs preserved the correct package, class name, and CUT API usage, and the previous Calculator-specific prompt contamination disappeared. The remaining failure mode is now `repair_exceeded`, indicating model non-convergence rather than prompt-template or runner-structure defects.

> Prompt 模板泛化修复已确认有效。修复后，Region 的 repair 输出不再因 class name、package 或 Calculator 风格 API 误导而被 validator 拒绝；`repair_validation_fail` 已被消除。当前剩余失败模式为 `repair_exceeded`，说明问题已从 prompt/runner 结构层转移到模型收敛能力层。
