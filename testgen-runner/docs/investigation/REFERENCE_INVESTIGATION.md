# Reference 失败调查

**现象**：post-fix baseline 中 Reference 在 65.5s 内失败，stuck_at=unknown。

**调查结果**（2026-03-12 03:53 运行）：

| 项目 | 结果 |
|------|------|
| stuck_at | **repair_exceeded** |
| elapsed | 295.0s |
| 结论 | 与 Calculator、Region 一致，runner 已 CUT-agnostic |

Reference 完整走完 generation → validator → mvn test → repair loop，在 10 次 repair 后达到 repair_exceeded。之前的 unknown 可能来自更早的短时运行或不同环境。

**mvn_test / pitest / mutation_score / repair_attempts 显示 ?**：失败 run 不写 summary，validation 脚本从 summary 解析这些字段，故为 ?。stuck_at 由 `_infer_stuck_stage` 从 runner 的 stdout 解析得到，正确识别为 repair_exceeded。
