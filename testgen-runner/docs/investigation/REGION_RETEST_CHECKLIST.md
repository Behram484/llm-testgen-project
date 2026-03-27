# Region 回测检查清单（Post Prompt Template Fix）

**目的**：确认 repair_validation_fail 是否被消除，修复是否有效。

**运行**：`python batch_runner.py --only Region`

---

## 重点观察 4 项

| 项 | 修复前 | 修复后 |
|----|--------|--------|
| 1. stuck_at | repair_validation_fail | **repair_exceeded** ✓ |
| 2. invalid_repaired_reasons | Missing expected class declaration: RegionTest_v19 | **无**（10 轮均过 validator）✓ |
| 3. repair 输出 API | add/subtract/mul/div/clamp（错误） | **contains, setStartReference 等** ✓ |
| 4. 失败性质 | prompt 模板残留 | 模型未收敛（真实能力）✓ |

---

## 记录位置

- 结果表：`output/validation_post_prompt_fix.txt`
- 每 CUT 结论：`output/batch_results.txt`
- invalid_repaired：`output/invalid_repaired/invalid_repaired_v*_r*.txt`
- invalid_repaired_reasons：`output/invalid_repaired_reasons/`

---

## 判断标准

- **修复有效**：repair_validation_fail 消失或明显下降；repair 输出使用真实 Region API
- **可进入更干净实验**：即使仍 fail，失败更可能是模型真实能力问题
