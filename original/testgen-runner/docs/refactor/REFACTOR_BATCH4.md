# Runner 重构 · 第四批：Repair Target Extraction Generalization

**状态**：✅ **Batch 4 closed**（已封板归档）

**目标**：将 repair target extraction 从「依赖 test 前缀」泛化为「依赖 surefire failure 中真实方法名」，从而支持更通用的 JUnit 测试命名。

**前置**：Batch 1、Batch 2、Batch 3 已封板归档。

**背景**：`get_failed_test_names()` 当前使用 `\w+Test\.(test[A-Za-z0-9_]*):`，仅匹配以 `test` 开头的方法名。若 LLM 生成更通用命名（如 `shouldClampZeroValues`、`returnsEmptyRegionWhen...`），repair loop 无法正确提取失败方法名。

**验收标准**（提前写死）：
- `testAdd` 风格失败名能正常提取
- `shouldClampZeroValues` 风格失败名也能正常提取
- compile failure 仍**不会**被误当作测试方法名
- `extract_methods_by_name()` 与 repair prompt 的 failed methods 选择逻辑不回归
- Batch 2 smoke / Batch 3 回归不受影响

---

## 清单

### [x] Item 1: 放宽 `get_failed_test_names()` 方法名匹配 ✅

**位置**：`runner.py` 约 622–638 行

**修改点**：`\w+Test\.([a-zA-Z_][a-zA-Z0-9_]*):` 支持任意合法 Java 方法名；显式排除 `java` 避免 `File.java:line` 被误解析。

**完成**：回归脚本 `validate_batch4_item1.py` 六类样本通过；Batch 2 smoke、Batch 3 回归不受影响。

### [ ] Item 2: 回归验证

**样本**：
- `ClassNameTest.testAdd: ...` → 提取 `testAdd`
- `ClassNameTest.shouldClampZeroValues: ...` → 提取 `shouldClampZeroValues`
- `ClassNameTest.testSomething_123: ...` → 提取 `testSomething_123`
- 避免误解析 `ClassNameTest.java:7` 为方法 `java`

### [x] Item 3: 与 `extract_methods_by_name` 等调用方对齐 ✅

**修改点**：`extract_methods_by_name` 使用 `extract_test_methods` 的 `\bvoid\s+(\w+)\s*\(` 提取方法名，与 `get_failed_test_names` 返回的任意合法方法名兼容；回归中已验证 `shouldClampZeroValues` 可正确提取。

---

## 完成标准

- [ ] 3 项全部完成
- [ ] 无新增 linter 报错
- [ ] 回归样本通过
- [ ] repair 主流程未破坏

---

## 完成记录

| 日期 | 验证结果 |
|------|----------|
| 2025-03-11 | Item 1 完成。get_failed_test_names 支持通用方法名；排除 java 避免 compile failure 误解析。 |
| 2025-03-11 | Item 2、3 完成。回归 7 类样本通过；extract_methods_by_name 与调用方对齐。Batch 4 可封板。 |

---

## Batch 4 正式总结（归档用）

**Batch 4 completed: generalized repair target extraction to support non-`test*` JUnit method names while preserving compile-failure safety and downstream method extraction compatibility.**

**Batch 4 已完成**：完成 repair target extraction 泛化，支持非 `test*` 风格的 JUnit 方法名，同时保持 compile failure 安全性，并与下游方法提取逻辑兼容。

**已知边界**：当前匹配常见 ASCII Java 方法名；不刻意覆盖 `$` 或 Unicode 标识符；对当前实验场景足够。

**已冻结**：REFACTOR_BATCH4.md、validate_batch4_item1.py。
