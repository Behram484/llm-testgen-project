# Single-CUT Isolation Fix

**问题**：`mvn test` 默认运行整个 test suite，导致 Region 运行时 ReferenceTest 等无关测试一起执行，repair 目标失真、结果不可信。

**修复**（2026-03-12）：

1. **mvn test**：增加 `-Dtest={test_class_fqn}`，仅运行当前 CUT 的测试类
   - Region → `-Dtest=org.templateit.RegionTest`
   - Reference → `-Dtest=org.templateit.ReferenceTest`
   - Calculator → `-Dtest=uk.sussex.testgen.CalculatorTest`

2. **pitest**：`targetClasses` 与 `targetTests` 改为单类
   - `targetClasses={package}.{cut_class}`（如 org.templateit.Region）
   - `targetTests={test_class_fqn}`（如 org.templateit.RegionTest）

**验证**：运行 `python runner.py config/config_region.json`，日志应显示 `Single-CUT isolation: mvn test -Dtest=org.templateit.RegionTest`，且 repair 失败仅来自 RegionTest。
