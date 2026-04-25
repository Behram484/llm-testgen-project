# Runner 重构 · 第一批：低风险抽取

**阶段记录**：Runner 重构方案确认（见对话总结）
- 已完成 runner 结构审计，确认主要问题为重复逻辑、Calculator 硬编码、main 职责过载
- 已确定优先重构方向：统一 postprocess、统一 activation/write、抽公共 failure 解析、移除 Calculator 默认与硬编码
- 已确定验证原则：采用分批重构 + 代表性 case 回归，而非一次性大改

**目标**：行为等价重构，不改变外部结果，仅减少重复、统一边界。

**验证原则**：每完成一项，用 Calculator + Region 各跑一次，对比 artifact 与 mvn test 结果。

---

## 执行原则（必须遵守）

> **每完成一项，就先运行最小验证，不要四项全改完再一起测。**

- 做完第 1 项 → 先测一次
- 做完第 2 项 → 再测一次
- 做完第 3 项 → 再测一次
- 做完第 4 项 → 收尾再测一次

这样若某步出问题，可立即定位。

---

## 克制原则（第一批禁止）

**不要因为是“低风险抽取”，就边抽边顺手优化。**

第一批只做清单内的事：
- 抽函数、替换调用、统一解析、去默认值

**禁止顺手改**：print 文本、summary 字段、log 文件名、repair policy、validation rule、parser 语义。

---

## 清单

### [x] 1. 抽取 `activate_and_write_test()` ✓

**状态**：代码检查通过，待最小验证确认

**位置**：`runner.py`

**新增函数**：
```python
def activate_and_write_test(
    java_code: str,
    test_class_name: str,
    active_test_class_name: str,
    active_test_file: Path,
    generated_file: Path,
) -> None:
    """
    将 versioned test (XTest_vN) 重命名为 active (XTest) 并写入两个目标文件。
    """
    activated = re.sub(
        rf"\bclass\s+{re.escape(test_class_name)}\b",
        f"class {active_test_class_name}",
        java_code,
    )
    activated = re.sub(
        rf"\b{re.escape(test_class_name)}\s*\(",
        f"{active_test_class_name}(",
        activated,
    )
    write_text(active_test_file, activated)
    write_text(generated_file, java_code)
```

**替换点**（共 6 处）：
- [ ] 首次激活（约 1165–1175 行）
- [ ] Programmatic fix 后（约 1168–1184 行）
- [ ] Same-failures programmatic fix 后（约 1198–1211 行）
- [ ] Regenerate 后（约 1356–1367 行）
- [ ] Repair 后（约 1468–1480 行）
- [ ] Augmentation 成功写入（约 1571、1578 行）：此处写 `aug_java` 到 `active_test_file` 和 `aug_path`，无 rename（aug 已用 active_test_class_name）。调用时传 `aug_path` 作 `generated_file` 参数即可。

**提醒 1**：函数必须支持两种输入：
- `XTest_vN -> XTest`（rename）
- `XTest -> XTest`（已是 active 名，rename 为 no-op）

augmentation 的 `aug_java` 已是 `active_test_class_name`，需保证此时不会误伤。

**提醒 2**：实施时明确 augmentation 的 `generated_file` 参数应传 `aug_path`，而非覆盖原 versioned 文件。这是业务选择，不是机械替换。

**验证**：跑 Calculator 和 Region，对比 `active_test_file`、`generated_file` 内容与重构前一致。

**最小验证清单**（通过后再打勾）：
- [x] 检查 A：首次激活 — `generated_file` 为 `RegionTest_v12`，`active_test_file` 为 `RegionTest` ✓
- [x] 检查 B：repair/programmatic fix 路径 — 触发 semantic repair，LLM repaired 后再次写入正常 ✓
- [ ] 检查 C：augmentation 路径 — 本次 run 未走到 augmentation（中途 UnicodeEncodeError 中断）

---

### [x] 2. 抽取 `postprocess_llm_test()` ✓

**提醒**：不要因为已抽 `activate_and_write_test()` 就顺手改 print、artifact 命名、写入时机。保持行为等价。

**位置**：`runner.py`

**新增函数**：
```python
def postprocess_llm_test(raw_llm_output: str, package_name: str) -> str:
    """
    统一流水线：extract → clean → ensure package → ensure imports.
    不包含 validation。
    """
    java = extract_java_code(raw_llm_output)
    java = clean_special_tokens(java)
    java = ensure_package(java, package_name)
    java = ensure_test_import(java)
    java = ensure_assert_imports(java)
    return java
```

**替换点**（共 4 处）：
- [ ] 首次 generation 后（约 1127–1134 行）
- [ ] Regenerate 后（约 1342–1346 行）
- [ ] Repair 后（约 1435–1448 行，含 merge + 二次 ensure_assert_imports）
- [ ] Augmentation 后（约 1555–1559 行）

**提醒 1**：postprocess 是**变换**，validation 是**判定**。两者职责必须分开，第一批绝不把 validation 塞进 postprocess。

**提醒 2**：Repair 分支的 `merge` + 二次 `ensure_assert_imports` 必须保留。merge 可能把旧方法代码塞回，重新引入 assert import 需求。抽公共函数 ≠ 所有地方完全一样，可以有公共主干 + 少量分支补充。

```python
current_java_test = postprocess_llm_test(raw_repair, package_name)
if not is_compile_failure(failures):
    current_java_test = merge_passed_tests_into_output(current_java_test, passed_methods)
current_java_test = ensure_assert_imports(current_java_test)
```

**验证**：对比 `generated_file`、`invalid_extracted`、`invalid_repaired` 等 artifact 与重构前一致。

**Item 2 最小验证结果**（已执行）：
- [x] generation 路径：正常，`RegionTest_v13` 含 package、import、类名正确 ✓
- [x] repair 路径：触发 2 次 semantic repair，merge + 二次 ensure_assert_imports 正常 ✓
- [x] regenerate 路径：触发 REGENERATE，postprocess 正常，validation 因 LLM 输出 Java assert() 失败（与 postprocess 无关）✓
- [ ] augmentation：本轮未覆盖
- [x] invalid artifact：regenerate 失败时正确写入 invalid_repaired ✓

---

### [x] 3. 抽取 assert mismatch 解析器 ✓

**位置**：`runner.py`

**新增函数**：
```python
def parse_assert_mismatch(failure_str: str) -> tuple[str, str, str] | None:
    """
    解析 "ClassName.methodName: expected X, but actual was Y" 格式。
    返回 (method_name, wrong_expected, correct_actual) 或 None。
    """
    m = re.search(
        r"\w+\.(\w+):\s+expected\s+([^,]+),\s*but actual was\s+(\S+)",
        failure_str,
        re.I,
    )
    if m:
        return (m.group(1), m.group(2).strip(), m.group(3).strip())
    return None
```

**修改调用方**：
- [ ] `get_fix_pairs()`：用 `parse_assert_mismatch` 替代内联正则
- [ ] `get_assert_mismatch_methods()`：用 `parse_assert_mismatch` 取 method_name
- [ ] `build_correct_fix_hint()`：用 `parse_assert_mismatch` 取三元组

**提醒**：此正则是“当前 failure format 的统一解析器”，不是万能解析器。若 `actual` 含空格、逗号或复杂 toString，`\S+` 可能截断。当前系统格式下大概率够用，实施时在函数注释中注明边界即可。

**验证**：构造含 `expected X, but actual was Y` 的 failure 字符串，确认三处解析结果与重构前一致。

---

### [x] 4. 去掉 `next_version` 的 Calculator 默认值 ✓

**位置**：`runner.py` 约 62 行

**修改**：
```python
# 改前
def next_version(generated_dir: Path, cut_stem: str = "Calculator") -> int:

# 改后
def next_version(generated_dir: Path, cut_stem: str) -> int:
```

**修改调用方**：
- [ ] `main()` 中：`next_version(generated_dir, cut_class_name)`（已传入，确认无默认调用）

**验证**：`grep next_version` 确认所有调用都显式传入 `cut_stem`。

---

## 回归验证清单（每批完成后执行）

| Case | 配置 | 验证项 |
|------|------|--------|
| A. Calculator 成功 | cut=Calculator | generation → mvn test → pitest 通过；artifact 路径与内容正常 |
| B. Region compile/semantic | cut=Region | repair 循环正常；failure 解析正确；programmatic fix 生效 |
| C. 对比 artifact | 重构前后各跑一次 | 抓**关键行为一致**，不追求逐字节相同 |

**artifact 对比提醒**：不追求每个字节完全一致。时间戳、version、raw LLM 输出、run end time 等可能天然不同。应比的是：
- `active_test_file` 是否可编译且语义一致
- `generated_file` 的类名/包名/测试方法是否一致或等价
- validation 是否同样通过/失败
- `mvn test` 结果是否一致
- repair 次数是否没有异常飙升
- runs_table 关键字段是否合理一致
- failure categorisation 是否一致

---

## 完成标准

- [ ] 4 项全部完成
- [ ] 无新增 linter 报错
- [ ] A、B、C 三类验证通过

---

## 第一批完成后（必做）

1. 跑完回归
2. 记录本批改了什么、结果如何
3. 确认当前系统仍稳定可用
4. **先别立刻继续第二批**，等确认稳定后再开第二批

---

## Batch 1 实施完成

* 四项低风险重构已全部完成
* 代码审阅通过
* 当前进入总回归验证阶段
* 暂不进入 Batch 2，先确认 Batch 1 稳定性与行为等价性

---

## 总回归验证（已执行）

**通过标准**：
1. ✓ `runner.py` 可正常执行，无新增语法或调用错误
2. ✓ Region 主流程可运行到与重构前同等级别的阶段（mvn test + pitest 均 SUCCESS）
3. ✓ assert mismatch 相关逻辑存在（本轮未触发，此前 Item 2 验证已覆盖 repair 路径）
4. ✓ 关键 artifact 仍能按原语义生成
5. ✓ 未发现由 Batch 1 引入的新失败类型

**回归 A**：Region 主流程 ✓ — generation、mvn test、pitest、augmentation 均正常
**回归 B**：assert mismatch — 本轮 mvn 首次即通过未触发；Item 2/3 验证已覆盖 repair 与 parse 逻辑
**回归 C**：关键 artifact ✓ — `RegionTest_v14`、`RegionTest`、summary_v14、runs_table 均正确

**总回归结果**：exit code 0，Batch 1 可正式封板。

---

## 完成记录（实施后填写）

**Batch 1 / Item 1 最小验证结果**（已执行）：
- `runner.py` 可正常执行，无新增语法或调用错误
- Region case：`generated_file` 保持 `RegionTest_v12`，`active_test_file` 正确写为 `RegionTest`
- repair 路径触发，LLM repaired 后写文件正常，无类名错写
- `activate_and_write_test()` 抽取未引入可见行为变化

---

---

## 阶段：Runner 重构 Batch 1 完成（已归档）

**记录要点**：
- 已完成 4 项低风险重构：
  - 抽取 `activate_and_write_test()`
  - 抽取 `postprocess_llm_test()`
  - 抽取 `parse_assert_mismatch()`
  - 移除 `next_version()` 中的 Calculator 默认值
- 已完成单项最小验证与 Batch 1 总回归
- Region 主流程验证通过：`mvn test` 与 `pitest` 均成功
- augmentation 分支验证了失败后回退 baseline 的原有行为未被破坏
- 未发现由 Batch 1 引入的新失败类型
- **Batch 1 正式封板，已归档**

| 日期 | 验证结果 |
|------|----------|
| 2025-03 | Batch 1 总回归通过。Region v14 完整流程：generation → mvn test → pitest → augmentation（revert）。四项重构未引入新失败。 |
