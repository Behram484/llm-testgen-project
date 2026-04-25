# 项目文件夹审计清单

**审计日期**：2026-03-12  
**范围**：`d:\Project` 下所有目录  
**已执行**：`__pycache__`、`testgen-lab/target`、`repair_compile.txt` 已删；`Dataset V1` 已移入 `archive/Dataset_V1`

---

## 一、Project 根目录 (d:\Project)

| 目录/文件 | 功能 | 建议 |
|-----------|------|------|
| `.idea/` | JetBrains IDE (IntelliJ/PyCharm) 配置 | **保留**：IDE 工作区配置 |
| `.venv/` | Python 虚拟环境（若存在） | **先确认再删**：仅当确认 (1) 实际使用的 Python 来自 testgen-runner/.venv，(2) IDE 未绑定根目录 .venv，(3) 已用 `where python` / `pip list` 确认后，才考虑删。否则先别动 |
| `Dataset V1/` | 早期实验数据：3_gaj、5_templateit、5_templateit_region 等 Maven 项目副本，Calculator.java | **优先移 archive**：未被当前脚本引用，但 report 或 evolution 解释可能用到；确认不再需要后再删 |
| `testgen-lab/` | Maven 被测项目：Region、Reference、Calculator 等 CUT | **保留**：runner 的 project_root |
| `testgen-runner/` | 主实验平台：runner、validator、prompts | **保留**：核心代码 |

---

## 二、testgen-runner 目录

| 目录/文件 | 功能 | 建议 |
|-----------|------|------|
| `config/` | 通用配置：config.json（runner 和 batch_runner 共用模板） | **保留**：runner、batch_runner 依赖 |
| `prompts/` | 生成与修复 prompt 模板 | **保留**：runner 直接读取 |
| `output/` | 运行产物：generated_tests、raw_llm、repair_prompt、summary、logs 等 | **保留**：runner 写入；`ensure_output_subdirs` 会在下次运行时自动重建目录，删除只会丢失历史结果，不会导致 runner 永久失败 |
| `docs/` | 文档：refactor、investigation、planning | **保留**：报告与实验设计 |
| `archive/` | 重构回归脚本：validate_batch2_*.py、validate_batch3_*.py、validate_batch4_*.py | **保留**：回归验证证据，可复跑 |
| `.venv/` | Python 虚拟环境 | **保留**：运行 runner 所需 |
| `__pycache__/` | Python 字节码缓存 | **可删**：可随时由 Python 自动重建；git 通常忽略 |

---

## 三、testgen-runner/output 子目录

| 子目录 | 功能 | 建议 |
|--------|------|------|
| `generated_tests/` | 生成的测试类（*Test_v1.java 等） | **保留**；可定期清理过时版本 |
| `prompt/` | 生成用 prompt 快照 | **保留** |
| `raw_llm/` | LLM 原始输出 | **保留**；可定期清理特别旧的 |
| `raw_repair/` | 修复阶段 LLM 原始输出 | **保留**；可定期清理特别旧的 |
| `repair_prompt/` | 修复用 prompt 快照 | **保留** |
| `mutation_prompt/` | mutation augment 用 prompt | **保留** |
| `raw_mutation/` | mutation augment 原始输出 | **保留** |
| `invalid_extracted/` | 未通过 validator 的提取结果 | **保留**：调试用 |
| `invalid_reasons/` | 上述失败原因 | **保留** |
| `invalid_repaired/` | 修复后仍 invalid 的代码 | **保留** |
| `invalid_repaired_reasons/` | 上述失败原因 | **保留** |
| `logs/` | mvn_test_fail、pitest_fail 日志 | **保留** |
| `summary/` | summary_v*.txt、runs_table.txt | **保留** |
| `last_successful/` | 上次成功测试基线（供后续参考） | **保留** |

**原则**：当前先保留；实验稳定后可按版本清理旧产物（raw_*、过时 generated_tests、重复日志）。

---

## 四、testgen-lab 目录

| 目录 | 功能 | 建议 |
|------|------|------|
| `src/main/java/` | 被测 Java 源码（Region、Reference、Calculator 等） | **保留** |
| `src/test/java/` | 测试类（runner 写入） | **保留** |
| `target/` | Maven 编译产物 | **可删**：`mvn clean` 可重建；git 通常忽略 |

---

## 五、执行建议

### 可直接执行

- 删 `__pycache__/`
- 删 `testgen-lab/target/`
- 保留 `config/`、`prompts/`、`output/`、`docs/`、`archive/`
- 保留 `testgen-lab/`、`testgen-runner/`

### 先确认再执行

| 项目 | 操作 | 前提 |
|------|------|------|
| 根目录 `.venv/` | 删 | 确认 Python 来自 testgen-runner/.venv，IDE 未绑定根 .venv |
| `prompts/repair_compile.txt` | 删 | 全文搜索确认无引用（已确认：runner、batch_runner、docs 均无引用） |
| `Dataset V1/` | 移 archive 或删 | 优先移 archive；确认 report/实验不再需要后再删 |

### 两轮执行（风险最低）

**第一轮（安全清理）**：删 `__pycache__/`、`testgen-lab/target/`

**第二轮（确认后清理）**：`repair_compile.txt`（删）、`Dataset V1/`（优先移 archive）、根目录 `.venv/`（确认后删）

---

## 六、不建议删除

- `archive/refactor_validation/`：虽为历史脚本，但用于回归验证，可复跑
- `config/config.json`：smoke_compile_repair、validate_batch2_regression 等依赖
- `output/` 下各子目录：runner 的 `ensure_output_subdirs` 会在下次运行时自动重建；删除只会丢失历史结果，不会导致 runner 永久失败
