# 路线 A：止血改动 (Route A: Stop the Bleeding)

根据诊断，已完成以下三项改动，使系统减少「修补器化」，恢复一定探索能力。

---

## 1. 去除 Calculator 硬编码

**改动：**
- `cut_class_name` 从 `cut_path` 动态推导：`cut_file.stem`（如 Calculator.java → Calculator）
- `active_test_class_name` = `cut_class_name` + "Test"
- `validate_test_code()` 增加参数 `cut_class_name`，不再写死 "Calculator"
- `next_version()`、类名替换等均基于 CUT 名称

**效果：** 支持任意 CUT，不再局限于 Calculator。

---

## 2. 默认禁用 apply_programmatic_fix

**改动：**
- config.json 新增 `enable_programmatic_fix: false`
- 仅当 `enable_programmatic_fix: true` 时，在连续相同失败后才会用 actual 回填 expected

**效果：** 避免用实现当 oracle，降低假阳性通过风险。

---

## 3. 连续相同失败后触发重新生成

**改动：**
- config.json 新增 `regenerate_after_same_failures: 2`
- 连续 2 次相同失败时，不再继续 repair，而是 **REGENERATE**：用新 prompt 重新生成完整测试类
- 仅在 regenerate 仍失败且 `enable_programmatic_fix: true` 时，才尝试 programmatic fix

**效果：** 在坏基础上打补丁改为「重新采样」，更符合 self-repair 研究结论。

---

## 配置示例

```json
{
  "enable_programmatic_fix": false,
  "regenerate_after_same_failures": 2
}
```

---

## 后续方向（路线 B / C）

- 路线 B：失败分类器、缩短 passed hint、repair prompt 改为「补强」而非「修错」
- 路线 C：尽早引入 mutation-guided repair，PIT 不只在最后评分
