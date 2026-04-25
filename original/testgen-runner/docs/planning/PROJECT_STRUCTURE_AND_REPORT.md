# Project 结构与 Report 定位

**用途**：明确各阶段工作在 report 中的位置，避免把「系统修复」当成「研究主体」。

---

## 三层结构

| 层 | 目标 | 当前状态 |
|----|------|----------|
| **第一层：系统可用性** | runner 能否稳定处理不同 CUT；失败是结构问题还是模型问题 | 基本完成 |
| **第二层：方法效果** | 不同 Java class 上测试生成质量；成功率、mutation score、profile 对比 | 待开始 |
| **第三层：解释与分析** | 为何某些 class 易成功；repair_exceeded 成因；discussion/conclusion | 后续 |

---

## Report 中的位置

### 不是主实验结果，而是支撑性内容

**Method / System Setup**：runner 流程、generation → validation → repair → pitest

**Experimental Preparation / Infrastructure Validation**：
- validator false positive 清理
- CUT-agnostic repair target extraction
- prompt template generalization
- Region 从 repair_validation_fail → repair_exceeded 作为「系统误差被清除」的证据

**Main Experiments**（主角）：不同 Java class 表现、profile 对比、mutation score、success rate

---

## 定稿表述

> 为了评估系统在不同 Java classes 上自动生成高质量测试的能力，首先对实验基础设施进行了校准，消除了 validator 误判、CUT-specific prompt contamination 和 repair target extraction 偏差等系统性问题，从而确保后续实验结果反映的是模型与方法本身，而非实验管线缺陷。

> 完成正式实验前的系统校准，并把失败从「系统/模板缺陷」尽可能转移为「模型真实能力限制」，从而确保最终对不同 Java classes 的测试生成效果评估是可信的。

---

## 下一步

1. 查清 Reference 的 `unknown` 失败阶段
2. 进入 prompt/profile effectiveness 对比实验
