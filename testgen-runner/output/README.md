# testgen-runner output directory

Artifacts from LLM-based test generation and repair runs.

| Directory | Description |
|-----------|-------------|
| `generated_tests/` | Extracted test classes (e.g. `CalculatorTest_v1.java`) |
| `prompt/` | Prompts used for generation |
| `raw_llm/` | Raw model outputs from generation |
| `repair_prompt/` | Prompts used for repair |
| `raw_repair/` | Raw model outputs from repair |
| `invalid_extracted/` | Invalid generation outputs (failed validation) |
| `invalid_reasons/` | Reasons for invalid generation |
| `invalid_repaired/` | Invalid repair outputs (failed validation) |
| `invalid_repaired_reasons/` | Reasons for invalid repair |
| `logs/` | Maven and PIT logs |
| `logs/mvn_test_fail/` | Maven test failure logs |
| `logs/pitest_fail/` | PIT mutation test failure logs |
| `summary/` | Experiment statistics (`summary_v*.txt`, `runs_table.txt`) |
| `last_successful/` | Last successful test baseline (e.g. `CalculatorTest.java`) |
