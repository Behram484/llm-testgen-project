# testgen-runner 代码审查报告

## 已修复问题

### 1. 编译错误解析中的乱码字符 (runner.py:182)
- **问题**：`fnd_pattern` 中 `�ҵ�` 为乱码，可能原为中文「找到」
- **修复**：改为 `找到`，与 `req_pattern` 中的 `需要` 对应

### 2. 文件读取编码容错 (runner.py:54-55)
- **问题**：`read_text` 未使用 `errors="replace"`，遇到非法 UTF-8 会抛 `UnicodeDecodeError`
- **修复**：添加 `errors="replace"`，与 `pit_package_index.read_text()` 等调用保持一致

---

## 架构与逻辑

### 流程正确性
- **Baseline 生成 → 激活 → mvn test → repair 循环 → PIT**：逻辑清晰
- **Mutation augmentation**：在 PIT 成功后、有 surviving mutants 时触发
- **Programmatic fix**：baseline 与 augmentation 均支持，顺序正确（先 normal 再 aggressive）

### 变量作用域
- `stubborn_methods` 仅在 `not is_compile_failure` 时定义，使用时已做判断 ✓
- `augmentation_success` 在 augmentation 块内正确赋值 ✓

---

## 潜在问题与建议

### 1. 硬编码的包名 (中优先级)
**位置**：`mutant_summary.py`、`runner.py` 中 `validate_test_code`、PIT 路径

```python
# mutant_summary.py
return project_root / "target" / "pit-reports" / "uk.sussex.testgen" / "index.html"
```

**影响**：扩展到 SF110 等不同包的项目时需改代码

**建议**：从 `cut_path` 推导包名，例如 `uk/sussex/testgen` → `uk.sussex.testgen`

---

### 2. CUT 方法名硬编码 (低优先级)
**位置**：`runner.py` 第 187、210、363 行

```python
method_sig = re.compile(r"\b(add|subtract|mul|div|clamp)\s*\([^)]+\)", re.I)
```

**影响**：仅适用于 Calculator，其他 CUT 需扩展

**建议**：从 CUT 源码解析方法名，或通过 config 传入

---

### 3. extract_test_methods 的边界情况 (低优先级)
**位置**：`runner.py:638-670`

- 字符串内的 `{`、`}` 会导致括号匹配错误
- 匿名内部类、嵌套类可能影响解析

**影响**：对简单测试类影响小，复杂结构可能解析错误

**建议**：当前可接受；若遇问题可考虑用 `javalang` 等解析器

---

### 4. ensure_assert_imports 的边界情况 (低优先级)
**位置**：`runner.py:658-696`

当无 `package`、无 `import` 时，`last_import_idx = -1`，可能不插入 import。

**影响**：正常 Java 测试文件通常有 package，实际影响有限

---

### 5. run_ollama 超时 (低优先级)
**位置**：`runner.py:709`

```python
def run_ollama(model: str, prompt: str, timeout_sec: int = 180) -> str:
```

**建议**：大模型或长 prompt 时 180 秒可能不足，可考虑在 config 中增加 `ollama_timeout`

---

### 6. append_run_to_runs_table 的 run_end_time (极低)
**说明**：函数内部用 `time.time()` 作为结束时间，与调用方可能略有偏差。

**影响**：可忽略，仅影响统计精度。

---

## 代码质量

### 优点
- 模块划分清晰：`runner.py` 主流程，`mutant_summary.py` 解析
- 错误处理较完整：validation、repair、revert 均有覆盖
- 实验指标记录完整：baseline/augmented mutation score、tests_generated、augmentation_success
- 注释与文档充分

### 可改进
- `runner.py` 约 1600 行，可考虑拆分为 `repair.py`、`augmentation.py` 等
- 部分 magic number（如 `regenerate_after_same_failures=2`）可集中到 config

---

## 扩展 SF110 前的检查清单

- [ ] 从 `cut_path` 推导 PIT 包路径，替代硬编码 `uk.sussex.testgen`
- [ ] 支持从 config 或 CUT 解析方法名，替代硬编码 `add|subtract|mul|div|clamp`
- [ ] `validate_test_code` 中的 `uk.sussex.testgen` 改为可配置
- [ ] 增加批量运行模式（遍历多个 CUT）
- [ ] 增加构建失败/超时时的跳过逻辑

---

## 总结

当前实现结构清晰、逻辑正确，已修复编码与文件读取相关问题。扩展至 SF110 时，主要需解决包名与方法名的硬编码，其余可逐步优化。
