# Archive

归档目录：保留重构正确性证据与回归基线，不参与日常开发，但可随时复跑验证。

## 目录结构

| 目录 | 内容 |
|------|------|
| `refactor_validation/` | Batch 2–4 专项回归脚本 |
| `Dataset_V1/` | 早期实验数据（3_gaj、5_templateit 等），从 Project 根目录移入 |

## 使用方式

从 `testgen-runner` 根目录运行（需在 testgen-runner 下执行）：

```bash
cd d:\Project\testgen-runner
python archive/refactor_validation/validate_batch2_item1.py
python archive/refactor_validation/validate_batch2_regression.py
python archive/refactor_validation/validate_batch3_item1.py
python archive/refactor_validation/validate_batch3_item2.py
python archive/refactor_validation/validate_batch3_item3.py
python archive/refactor_validation/validate_batch3_rule9.py
python archive/refactor_validation/validate_batch4_item1.py
```

脚本已配置 `sys.path`，会正确导入 `runner` 模块。

## 不删除的原因

- 重构正确性的证据
- 若某次修改破坏旧行为，可作回归基线
- 项目记录、答辩、论文 implementation 说明时可引用
