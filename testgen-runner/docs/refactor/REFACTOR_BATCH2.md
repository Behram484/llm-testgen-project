# Runner 重构 · 第二批：Failure Parsing 与 Classification 泛化

**目标**：提升 runner 对不同 CUT / benchmark case 的通用性，移除 Calculator-specific 硬编码。专注 **failure parsing + classification**，暂不纳入 validator 泛化。

**前置**：Batch 1 已封板归档。

---

## 阶段：Batch 2 草案审阅完成

- 已确认 Batch 2 聚焦 failure parsing 与 classification 的通用化
- 已决定暂不把 validator 泛化并入本批，避免范围扩散
- 已补充：`missing_import` 改为中性 unresolved symbol 类别；`unsupported_signature` 改为通用 signature/type mismatch 类别
- 已决定新增「日志样本级验证」作为 Batch 2 的必要验证层

---

## 清单

### [x] Item 1: `parse_surefire_failures` 泛化 ✅

**位置**：`runner.py` 约 163–290 行

**修改点**：
1. 方法名提取逻辑改为通用，不再硬编码 `add|subtract|mul|div|clamp`（如用 `\b(\w+)\s*\([^)]*\)` 匹配任意方法调用）
2. `static_reference` 使用实际 `fname`（从 compile_loc 解析），`static_by_method` 改为 `(fname, method) -> lines`
3. 将 `[missing_import]` 改为 **`[unresolved_symbol]`**（parser 只报告现象，不预设为 import 问题）
4. 将 `[unsupported_signature]` 改为 **`[method_signature_mismatch]`**
5. 同步更新 `COMPILE_FAILURE_PREFIXES` 与 `classify_failures` 中的匹配前缀

**实施提醒**：检查所有依赖这些标签的地方是否同步更新：`is_compile_failure`、`classify_failures`、`build_failure_diagnosis`、任何基于旧标签的统计或日志。

**完成记录**：已更新 `COMPILE_FAILURE_PREFIXES`、`classify_failures` 中 `unresolved_symbol` / `method_signature_mismatch` 的 regex 与 suggested_action；`static_by_method` 类型为 `dict[tuple[str, str], list[int]]`；classifier 中 method 匹配改为 `\S+` 以支持 `?`。样本级验证脚本 `validate_batch2_item1.py` 已通过。

**Batch 2 / Item 2–3 审阅结果**：`classify_failures()` 已支持 `cut_class_name`；`method_signature_mismatch` 与 `unresolved_symbol` wording 已去 Calculator 化；repair 主流程调用方已显式传入 `cut_class_name`；`static_reference` diagnosis 已改为不假设默认构造器的中性表述（"Create or reuse an instance of {cut}, then call instance.{method}(...) instead of {cut}.{method}(...)"）。

**Batch 2 / Item 2–3 完成记录**：`classify_failures()` 已支持 `cut_class_name`；`static_reference` diagnosis 已改为不假设具体构造方式的中性表述；`method_signature_mismatch` 与 `unresolved_symbol` wording 已完成去 Calculator 化；repair 主流程调用方已显式传入 `cut_class_name`；样本级验证通过，进入真实 case 回归阶段。

**Batch 2 / Item 4 回归结果**：Region 真实 case 回归通过。注入 `NonExistentClass` + `Region.contains(r)` 触发 compile-phase 失败；`mvn clean test` 产生 COMPILATION ERROR；parser 正确输出 `[unresolved_symbol]`、`[static_reference]`；classifier 与 diagnosis 使用 Region 非 Calculator；`is_compile_failure()` 正确分流。补充：中文 locale 下 javac 输出「找不到符号」，已扩展 `missing_sym` 正则以支持。

**Batch 2 封板前 smoke test**：`smoke_compile_repair.py` 验证真实 runner compile-failure 分流。向 active RegionTest 注入 compile 错误 → `run_maven`（与 runner 相同）→ `parse_surefire_failures` → `is_compile_failure` → repair_type=COMPILE REPAIR → 使用 `compile_repair_template` 构建 prompt。通过。

---

### [x] Item 2: `classify_failures` 泛化 ✅

**位置**：`runner.py` 约 303–480 行

**修改点**：
1. 增加参数 `cut_class_name: str = ""`
2. `static_reference`：diagnosis 改为基于 `cut_class_name`，如 `{cut}.{method}(...)`，不保留 Calculator 硬编码
3. `method_signature_mismatch`：diagnosis 已为通用 API/signature 检查提示，无 int-only / double 等 Calculator-specific 语义
4. `unresolved_symbol`：diagnosis 保持中性，不预设为 import 问题
5. diagnosis wording 去除 Calculator-specific 假设，仅保留 CUT-aware 命名

---

### [x] Item 3: 调用方更新 ✅

**修改点**：
- `classify_failures(failures)` → `classify_failures(failures, cut_class_name)`
- 调用处：约 1338、1428 行，已改为 `classify_failures(failures, cut_class_name)`

---

### [x] Item 4: Batch 2 验证 ✅

**第一层：日志样本级验证**

至少准备 4 类 Maven failure log 样本：
- unresolved symbol / package mismatch
- static reference
- wrong method call / signature mismatch
- semantic assert mismatch

验证：parser 输出、classifier 输出、diagnosis 文本是否合理；compile failure 是否仍被正确识别。

**第二层：真实 case 回归**

- Region 等 compile-failure / access-scope case
- 能触发 semantic mismatch 的 case

确认 parser 输出更泛化，且未破坏原有 repair 分支。

---

## 验证原则

- 每改一项做一次最小验证
- 样本级验证优先于端到端回归
- 不改变 failure 的语义，仅使提示与 CUT 一致、类别更中性

---

## Batch 2 回归阶段总结

* 已完成 parser 与 classifier 的通用化回归
* 已验证 `unresolved_symbol`、`static_reference`、compile/semantic 分流、CUT-aware diagnosis 正常工作
* 已解决 locale、样本边界、Maven 增量编译、Windows shell 环境等验证过程中的问题
* 已补充真实 runner compile-failure smoke test，确认 compile repair 分支未受新标签影响
* **Batch 2 可封板归档**

---

## 完成标准

- [x] 4 项全部完成
- [ ] 无新增 linter 报错
- [ ] 日志样本级验证通过
- [ ] Region 与代表性 CUT 回归通过
- [ ] 未引入新的误判或漏判

---

## 完成记录（实施后填写）

**Batch 2 / Item 1 完成记录**

- 已完成 `parse_surefire_failures()` 泛化
- compile failure 标签已由 `missing_import` / `unsupported_signature` 升级为 `unresolved_symbol` / `method_signature_mismatch`
- 方法名提取与 `static_reference` 聚合逻辑已去除 Calculator-specific 假设
- 标签传播链已检查通过：parser、`COMPILE_FAILURE_PREFIXES`、`is_compile_failure()`、classifier、diagnosis 保持一致
- 样本级验证通过，可进入 Item 2

| 日期 | 验证结果 |
|------|----------|
| 2025-03-08 | Item 1 完成。新标签：`unresolved_symbol`、`method_signature_mismatch`。parse/classify/is_compile_failure/build_diagnosis 样本级验证通过。 |
| 2025-03-11 | Item 4 完成。Region 真实 case 回归通过；标签、diagnosis、is_compile_failure 均正确；补充中文 locale 支持。 |
| 2025-03-11 | 封板前 smoke test 通过。smoke_compile_repair.py 验证 compile repair 分支正确进入。Batch 2 可封板归档。 |
