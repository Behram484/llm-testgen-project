# Mutation-Guided V1 接入规划

## 状态：已实现

## 控制流

```
main()
  ├── generation → mvn test → repair loop
  ├── mvn test: SUCCESS
  ├── PIT (第一次)
  ├── pitest: SUCCESS
  │
  ├── 解析 baseline_mutation_score，生成 mutation_summary_v{v}.txt
  │
  ├── [if enable_mutation_augment and has_surviving_mutants]
  │   ├── mutation augment (LLM 一次)
  │   ├── extract + clean + ensure_imports + validate
  │   ├── mvn test → 失败则 revert 到 baseline
  │   ├── PIT (第二次)
  │   └── 记录 augmented_mutation_score
  │
  └── 保存 last_successful, summary (含 baseline/augmented mutation score)
```

## 配置

`config.json` 增加 `enable_mutation_augment: false`。设为 `true` 启用 mutation augmentation。

## Artifact 结构

```
output/
├── mutation_prompt/          # mutation_augment prompt
├── raw_mutation/             # LLM augmentation 原始输出
├── generated_tests/
│   └── CalculatorTest_v{v}_aug.java   # augmentation 通过 validate 的版本
├── summary/
│   ├── mutation_summary_v{v}.txt     # surviving mutants 摘要（每次 PIT 后生成）
│   └── summary_v{v}.txt              # 含 baseline_mutation_score, augmented_mutation_score
```

## 使用

1. 正常运行 `py runner.py`，baseline 成功后会自动生成 `mutation_summary_v{v}.txt`
2. 在 `config.json` 中设置 `"enable_mutation_augment": true`
3. 再次运行，在 PIT 通过且存在 surviving mutants 时会执行 augmentation
