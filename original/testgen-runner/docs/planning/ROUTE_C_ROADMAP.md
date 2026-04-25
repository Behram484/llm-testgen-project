# Route C: 路线图 (Roadmap)

## 1. Failure Classifier 细化（已完成）

将 unknown 拆分为：
- `compile_error` – 编译失败
- `wrong_method_call` – 方法签名不匹配（required: X but found: Y）
- `missing_import` – 符号未找到
- `runtime_error` – 测试抛出意外异常（如 ArithmeticException）

实现：`parse_surefire_failures` 和 `classify_failures` 已支持上述类型。

---

## 2. Generation 行为导向（已完成）

- 新增 `baseline_behavior.txt`：首轮生成时要求模型思考「What CUT behavior is this test verifying?」
- 配置 `generation_profile`: `baseline_behavior`
- 修复仍用 `semantic_repair.txt`

目标：generation 已是行为导向，repair 只做微调。

---

## 3. Mutation Feedback 提前（规划中）

**当前流程：**
```
generation → mvn test → repair loop → mvn success → PIT (mutation)
```

**目标流程：**
```
generation → mvn test → quick PIT → surviving mutants summary → targeted test augmentation
```

**思路：**
- PIT 不再仅作为最终评分器
- 在 mvn 通过后，尽早跑一次 quick PIT
- 生成 surviving mutants 摘要（哪些行为未被覆盖）
- 将摘要作为 LLM 的 targeted test augmentation 输入

**效果：**
- LLM 知道：哪些行为还没被测到
- 不再仅知道：哪条 assertion 错了

**参考：** 已有研究表明 mutation feedback 是强 test guidance signal。

---

## 配置变更

- `config.json` 新增 `generation_profile`: `"baseline_behavior"`
- 首轮生成使用 `baseline_behavior.txt`，repair 使用 `semantic_repair.txt`

## 后续可扩展

- `boundary_mismatch`：将 assert_mismatch 中边界值错误单独分类
- `null_behavior`：NPE 等 null 相关失败
- 更细的 compile error 分类（如 missing_symbol vs wrong_type）
