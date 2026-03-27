# 实验矩阵设计

**目的**：为第二层（方法效果）实验提供清晰、可执行的实验设计，避免「继续修系统」的循环。

**研究问题**：*How effectively can LLM-driven pipelines generate high-quality unit tests for diverse Java classes?*

---

## 一、实验变量总览

| 维度 | 变量 | 当前取值 | 实验用途 |
|------|------|----------|----------|
| **CUT** | 被测 Java 类 | Calculator, Region, Reference | 跨类泛化能力 |
| **generation_profile** | 生成 prompt 模板 | baseline, baseline_behavior, (reasoning, structured) | 不同 prompt 风格效果 |
| **repair** | 修复 prompt | 自动选择 semantic / compile | 或可扩展为可配置对比 |
| **mutation_augment** | 是否启用 mutation 增强 | true / false | 增强对 mutation score 的影响 |

---

## 二、实验矩阵（推荐执行顺序）

### Phase 0：前置（必须完成）

| 步骤 | 内容 | 产出 |
|------|------|------|
| 0.1 | 查清 Reference `unknown` | 明确 stuck_at 阶段 |
| 0.2 | 跑完整 post-fix baseline | 3 个 CUT 的最终 stuck_at 表 |

---

### Phase 1：Generation Profile 对比（核心实验）

**目标**：比较不同 generation prompt 的测试生成效果。

| 实验 ID | CUT | generation_profile | mutation_augment | 重复次数 |
|---------|-----|--------------------|------------------|----------|
| P1-Calc-Base | Calculator | baseline | true | 3 |
| P1-Calc-Behavior | Calculator | baseline_behavior | true | 3 |
| P1-Reg-Base | Region | baseline | true | 3 |
| P1-Reg-Behavior | Region | baseline_behavior | true | 3 |
| P1-Ref-Base | Reference | baseline | true | 3 |
| P1-Ref-Behavior | Reference | baseline_behavior | true | 3 |

**配置方式**：修改 `config/config_*.json` 中的 `generation_profile`。

**已有 prompt 模板**：
- `baseline.txt`：简洁版，要求少
- `baseline_behavior.txt`：行为导向，强调语义推导（当前默认）

**可选扩展**（若时间允许）：
- `reasoning.txt`：加入 "Think step by step about CUT behavior..."
- `structured.txt`：要求按 method × scenario 结构化输出

**指标**：
- 首轮 mvn 通过率（first-pass success）
- 平均 repair 次数
- 最终 stuck_at 分布（success / repair_exceeded / repair_stuck / ...）
- baseline mutation score

---

### Phase 2：Mutation Augment 开关对比

**目标**：评估 mutation augmentation 对 mutation score 的提升。

| 实验 ID | CUT | generation_profile | mutation_augment | 重复次数 |
|---------|-----|--------------------|------------------|----------|
| P2-Calc-On | Calculator | baseline_behavior | true | 3 |
| P2-Calc-Off | Calculator | baseline_behavior | false | 3 |
| P2-Reg-On | Region | baseline_behavior | true | 3 |
| P2-Reg-Off | Region | baseline_behavior | false | 3 |
| P2-Ref-On | Reference | baseline_behavior | true | 3 |
| P2-Ref-Off | Reference | baseline_behavior | false | 3 |

**指标**：
- baseline_mutation_score vs augmented_mutation_score（on 时）
- augmentation_success 比例
- 对比 on/off 的 baseline_mutation_score（控制变量：同一 CUT、同一 profile）

---

### Phase 3：Repair 风格对比（可选，需扩展）

**当前行为**：repair 由失败类型自动选择
- compile failure → `compile_repair.txt`
- semantic failure → `semantic_repair.txt`

**若要做对比实验**，需在 config 中增加 `repair_style_override`（或类似）：
- `auto`（默认）：按失败类型选择
- `semantic_only`：强制用 semantic_repair（即使 compile 失败也尝试）
- `compile_only`：强制用 compile_repair

**实验设计**（示例）：
- 对易产生 compile failure 的 CUT，对比 auto vs compile_only
- 对易产生 semantic failure 的 CUT，对比 auto vs semantic_only

**优先级**：可放在 Phase 1/2 之后，若时间紧张可省略。

---

## 三、实验执行流程

### 单次实验运行

```bash
cd d:\Project\testgen-runner
python runner.py config/config_calculator.json
# 或 config_region.json, config_reference.json
```

### 批量运行脚本（建议编写）

```bash
# 示例：Phase 1 全部运行
for profile in baseline baseline_behavior; do
  for cut in calculator region reference; do
    # 修改 config 中 generation_profile
    python runner.py config/config_${cut}.json
    # 保存到 output/phase1_${cut}_${profile}_runN/
  done
done
```

可编写 `run_experiment_batch.py` 接受参数：`--phase 1 --cut calculator --profile baseline_behavior --repeat 3`。

---

## 四、结果汇总表模板

### Phase 1 结果表

| CUT | profile | run | stuck_at | repair_count | first_pass | baseline_mutation |
|-----|---------|-----|----------|--------------|------------|-------------------|
| Calculator | baseline | 1 | ... | ... | Y/N | ... |
| Calculator | baseline | 2 | ... | ... | Y/N | ... |
| ... | ... | ... | ... | ... | ... | ... |

### Phase 2 结果表

| CUT | mutation_augment | run | baseline_mutation | augmented_mutation | augmentation_success |
|-----|------------------|-----|--------------------|--------------------|-----------------------|
| Calculator | on | 1 | ... | ... | Y/N |
| Calculator | off | 1 | ... | - | - |
| ... | ... | ... | ... | ... | ... |

---

## 五、与 Report 的对应

| 实验 phase | Report 位置 |
|------------|-------------|
| Phase 0 | Experimental Preparation / Infrastructure Validation |
| Phase 1 | Main Experiments - RQ1: Prompt/Profile Effectiveness |
| Phase 2 | Main Experiments - RQ2: Mutation Augmentation Impact |
| Phase 3 | Main Experiments - RQ3 (optional): Repair Style Comparison |
| 结果分析 | Discussion - 为何某些 CUT 易成功、repair_exceeded 成因 |

---

## 六、检查清单

- [ ] Reference unknown 已查清
- [ ] 完整 post-fix baseline 已跑完
- [ ] Phase 1 实验矩阵已执行（至少 baseline vs baseline_behavior）
- [ ] Phase 2 mutation on/off 对比已执行
- [ ] 结果已汇总到表格
- [ ] 可回答：*How effectively can LLM-driven pipelines generate high-quality unit tests for diverse Java classes?*
