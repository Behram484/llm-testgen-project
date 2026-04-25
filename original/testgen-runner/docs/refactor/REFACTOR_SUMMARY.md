# Runner 重构 · 总览（Batch 1–4）

**用途**：一周后回来也能一眼看懂「已经解决了什么问题」。  
**原则**：新 batch 应由实验失败驱动，不由「还能再优化一点」驱动。

**当前状态**：本版已冻结为 **pre-experiment validation candidate**。不再主动开 Batch 5，直接进入系统级验证。

**2026-03-12 Prompt Template Fix**：修复 repair/generation/mutation prompt 中 Calculator 硬编码（package、API、语义）。见 `PROMPT_TEMPLATE_FIX.md`。**Region 验证**：repair_validation_fail → repair_exceeded，修复有效。

**当前阶段**：不再开结构性 batch，进入 post-fix baseline + prompt/profile effectiveness 对比。

---

## 各 Batch 一句话结论

| Batch | 结论 |
|-------|------|
| **Batch 1** | 行为等价重构：统一 postprocess、activation/write、failure 解析，移除 Calculator 默认 |
| **Batch 2** | Failure parsing 泛化：`unresolved_symbol` / `method_signature_mismatch`，CUT-aware diagnosis |
| **Batch 3** | Validator 泛化与 false-positive 清理：qualified assertion、class 声明、assertion 白名单、CUT heuristic 下沉 |
| **Batch 4** | Repair target extraction 泛化：支持非 `test*` 方法名，保持 compile failure 安全 |

---

## 改动函数一览

| Batch | 函数 | 改动要点 |
|-------|------|----------|
| 1 | `activate_and_write_test` | 新增，统一激活与写入 |
| 1 | `postprocess_llm_test` | 新增，统一 LLM 输出后处理 |
| 1 | `parse_assert_mismatch` | 新增，共享 assert mismatch 解析 |
| 1 | `next_version` | 移除 Calculator 默认参数 |
| 2 | `parse_surefire_failures` | 方法名泛化、`unresolved_symbol` / `method_signature_mismatch`、`static_by_method` 键改为 (fname, method) |
| 2 | `classify_failures` | 新增 `cut_class_name`，`static_reference` / `method_signature_mismatch` 通用化 |
| 2 | `COMPILE_FAILURE_PREFIXES` | 更新为新标签 |
| 3 | `validate_test_code` | Rule 2/4/5/6/7c/9 调整，新增 `require_cut_reference` |
| 3 | `ensure_assert_imports` | 新增 `_has_unqualified_assert`，支持 assertTrue/assertNotNull/fail 等 |
| 4 | `get_failed_test_names` | 方法名匹配放宽为任意合法 Java 标识符，排除 `java` |

---

## 回归脚本与通过状态

| 脚本 | 覆盖 | 状态 |
|------|------|------|
| `archive/refactor_validation/validate_batch2_item1.py` | parse/classify/is_compile_failure/diagnosis 样本 | ✓ |
| `archive/refactor_validation/validate_batch2_regression.py` | Region 真实 compile failure | ✓ |
| `smoke_compile_repair.py` | 真实 runner compile repair 分流 | ✓ |
| `archive/refactor_validation/validate_batch3_item1.py` | Rule 5/6 qualified assertion | ✓ |
| `archive/refactor_validation/validate_batch3_item2.py` | Rule 2 class 声明 | ✓ |
| `archive/refactor_validation/validate_batch3_item3.py` | Rule 4 + ensure_assert_imports | ✓ |
| `archive/refactor_validation/validate_batch3_rule9.py` | Rule 9 CUT heuristic | ✓ |
| `archive/refactor_validation/validate_batch4_item1.py` | get_failed_test_names + extract_methods_by_name | ✓ |

---

## 冻结版本

- **Batch 1**：REFACTOR_BATCH1.md
- **Batch 2**：REFACTOR_BATCH2.md，archive/refactor_validation/validate_batch2_*.py，smoke_compile_repair.py
- **Batch 3**：REFACTOR_BATCH3.md，archive/refactor_validation/validate_batch3_*.py
- **Batch 4**：REFACTOR_BATCH4.md，archive/refactor_validation/validate_batch4_item1.py

---

## Pre-Experiment Validation（已就绪）

**脚本**：`batch_runner.py`

**用法**：
```bash
python pre_experiment_validation.py              # Region + Reference
python pre_experiment_validation.py --region-only
python pre_experiment_validation.py --reference-only
```

**配置**：
- `config/config_region.json`：Region CUT
- `config/config_reference.json`：Reference CUT

**目标**：验证整条链路未被 4 个 batch 改坏。

**建议 CUT**：
1. **Calculator**（若有独立项目）
2. **Region**（当前 config）
3. **一个新的非 Calculator CUT**（如 Reference）

**每 CUT 记录**：validator 是否通过、初次 mvn test 是否通过、repair 次数、最终是否成功、failure stage、是否需人工介入、mutation score（若开 PIT/augment）

**验证维度**：
- 生成 → validator → mvn test → repair → pitest → mutation augment
- validator 是否误杀
- compile failure / runtime failure 解析是否稳定
- failed method extraction 是否稳定
- repair prompt 抓到的方法是否正确
- augmentation 分支是否容易出现 artifact 混乱

**本轮验证重点**：不是「成没成」本身，而是上述结构性问题是否暴露。

**通过标准**：
- **SUCCESS**：完整流程跑通
- **REPAIR_EXCEEDED**：主链路 intact，LLM 未能修复（随机性）→ 可进入实验
- **VALIDATION_FAIL / MVN_NO_PARSE / COMPILE_FAIL** 等：结构性问题 → 需排查

**结果文件**：`batch_results.txt`

---

## 已知边界（非 blocker，实验时留意）

以下 4 点**不是现在必须返工的 blocker**，但建议记下，避免实验时反复怀疑。

| 点 | 描述 | 风险 |
|----|------|------|
| 1 | `extract_java_code()` heuristic start 只找 `package` / `import` / `public class`，不主动找普通 `class Xxx`。若 LLM 输出无 code fence、无 package/import、只有 `class XxxTest { ... }` 且前面有 prose，可能把 prose 一并保留。 | 中低 |
| 2 | `parse_assert_mismatch()` / programmatic fix 偏向简单 `assertEquals`。字符串、集合、带空格的 actual、复杂断言形式可能提取不稳或 aggressive fix 较粗。 | 实验驱动后再扩 |
| 3 | augmentation 成功后若走了 programmatic fix，`aug_path` 产物可能不是最终 patched 版本（active_test_file / last_successful_path 会更新，但 `_aug.java` 不一定同步）。 | 低 |
| 4 | `parse_surefire_failures()` 的 runtime error 解析依赖当前 Maven/Surefire 格式，格式变化可能漏解析。 | 验证时重点观察 |

---

## Pre-Experiment 验证结论（2026-03-12）

**主结论**：runner 主链路已通，结构性问题不是当前主瓶颈。当前失败更多是 **LLM repair effectiveness** 问题。

| CUT | stuck_at | 解读 |
|-----|----------|------|
| Calculator | repair_exceeded | 进入 repair loop，模型未收敛 |
| Region | **repair_validation_fail** | LLM 的 repair 输出未通过 validator |
| Reference | repair_exceeded | 新 CUT 泛化有效，模型未收敛 |

**repair effectiveness 由四类因素共同决定**：prompt + model + task 难度 + repair 策略。其中 prompt 很可能是第一嫌疑人之一。

---

## Prompt Effectiveness Investigation（下一步）

**不要开 Batch 5 改架构**，而是做 **小规模 prompt/profile 对比**，先把 `repair_exceeded` 压下去。

### 最小可行对比

| 变量 | 选项 |
|------|------|
| generation prompt | 当前 baseline / 更严格的 test-generation |
| repair prompt | 当前版本 / 更强调「仅改失败方法、严格依据 diagnosis」 |
| programmatic fix | off / on |

### 关键观察指标（优先于 mutation score）

- 初次 validator 通过率
- 初次 mvn test 通过率
- repair 成功率
- 平均 repair 次数
- repair_exceeded 比例

### 判断逻辑

若 prompt 改完，repair_exceeded 明显下降 → 找到当前最值得优化的地方。

---

## 实验准备（prompt 选择后）

- 定义实验矩阵：baseline / programmatic fix / mutation augment / CUT 类型
- 固定评估指标：validator 通过率、mvn 通过率、repair 次数、mutation score、失败类型分布
- 固定样本集：选定 CUT 集合，保持可比性
