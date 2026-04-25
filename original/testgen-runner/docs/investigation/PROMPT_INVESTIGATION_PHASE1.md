# Prompt Effectiveness Investigation – Phase 1

**日期**：2026-03-12  
**目标**：针对两类失败模式做有针对性调查

---

## 两类失败模式（已明确）

| 模式 | CUT | 症状 |
|------|-----|------|
| **repair_exceeded** | Calculator, Reference | 主链路通，repair 在工作，但模型未收敛 |
| **repair_validation_fail** | Region | repair 产物不合法，连 validator 都过不了 |

---

## 线 A：Region invalid_repaired 分析

### Artifact

- `invalid_repaired_v19_r1.txt`
- `invalid_repaired_reasons_v19_r1.txt`

### 根因（已定位）

**1. Validator 拒绝原因**

```
Missing expected class declaration: RegionTest_v19
```

模型输出 `class RegionTest`，而 validator 期望 `class RegionTest_v19`。

**2. 更深层问题：repair prompt 硬编码了 Calculator**

`repair_prompt_v19_r1.txt` 显示：

- `package uk.sussex.testgen` — 硬编码，Region 应为 `org.templateit`
- `For this CUT: add(int,int), subtract(int,int), mul(int,int,int), div(int,int,int), clamp(int,int,int)` — Calculator API
- 语义要求：add/subtract/mul/div/clamp — 全部为 Calculator

**3. 模型行为**

模型按 prompt 要求生成了 add/subtract/mul/div/clamp 等测试，但 Region 的 API 是 contains、setStartReference、setEndReference、start、end。  
因此模型在 prompt 引导下生成了错误的 CUT 测试。

### 结论

**Region 的 repair_validation_fail 不是单纯 prompt 表述问题，而是 repair prompt 中 Calculator 硬编码导致。**

`semantic_repair.txt` 与 `compile_repair.txt` 中均有：

- 硬编码 `package uk.sussex.testgen`
- 硬编码 Calculator API 描述
- 硬编码 Calculator 语义要求

---

## 线 B：Calculator / Reference repair_exceeded

（待补充：分析 failure progression、anti-stuck、regenerate 效果）

---

## 建议修复（优先）

### 1. 去除 repair prompt 的 Calculator 硬编码

- `package`：改为占位符，由 runner 注入实际 package
- CUT API 描述：改为由 CUT 代码/签名推导，或移除固定描述
- 语义要求：移除 Calculator 专属语义，改为通用说明

### 2. 强化 class name 约束

- 明确要求：输出 class 名必须与 `{TEST_CLASS_NAME}` 完全一致
- 强调：不要改成 `RegionTest` 或其它名称

### 3. 更强约束版 repair prompt（Phase 1 对比）

- 只输出完整 Java test class，不输出解释
- 保留 package / imports / class name
- 只修改 failing methods，passed methods 不改
- compile failure 优先修 API / signature / syntax
- semantic failure 只根据 failure diagnosis 改 assertion/调用
- 不删除 `@Test`
- 不改 test class name
- 不输出 markdown fence

---

## 下一步

1. ~~**修复 repair prompt 硬编码**~~ → **已完成**（见 `PROMPT_TEMPLATE_FIX.md`）
2. 再做小规模 repair prompt 对比
3. 观察 repair_validation_fail 与 repair_exceeded 是否下降

---

## 修复记录（2026-03-12）

已执行 Prompt Template Generalization Fix：

- `build_prompt` 新增 `package_name` 与 `{PACKAGE}` 占位符
- `semantic_repair.txt`、`compile_repair.txt`、`baseline_behavior.txt`、`mutation_augment.txt` 去除 Calculator 硬编码
- 强化 class name 约束
