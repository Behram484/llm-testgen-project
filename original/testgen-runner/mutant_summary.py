"""
Surviving mutants → MUTATION_SUMMARY 生成规则

从 PIT HTML 报告提取 surviving mutants，按方法聚合，并翻译成行为导向的摘要，
供 mutation_augment prompt 使用。

V1 设计：
- 输入：target/pit-reports/uk.sussex.testgen/Calculator.java.html
- 输出：简洁的 MUTATION_SUMMARY 文本
"""

import re
from pathlib import Path


# PIT 原始变异描述 → 行为薄弱点摘要（按关键词匹配，优先匹配更具体的）
MUTATION_TO_BEHAVIOR: list[tuple[str, str]] = [
    # 乘除运算符互换（如 a*b*c → a/b/c 或 a/b*c → a/b/c）
    (
        r"Replaced integer multiplication with division",
        "multiplication/division operator behavior is not fully constrained; "
        "current tests may not distinguish * from / in the expression",
    ),
    (
        r"Replaced integer division with multiplication",
        "division/multiplication operator behavior is not fully constrained",
    ),
    # 返回值被替换为 0
    (
        r"replaced int return with 0",
        "return value is weakly constrained; current tests may not reject zero-return behavior",
    ),
    # 加减运算符
    (
        r"Replaced integer addition with subtraction",
        "addition/subtraction operator behavior is not fully constrained",
    ),
    (
        r"Replaced integer subtraction with addition",
        "subtraction/addition operator behavior is not fully constrained",
    ),
    # 边界/条件
    (
        r"negated conditional|Negated conditional",
        "boundary or branch behavior is insufficiently tested",
    ),
    (
        r"Replaced.*condition boundary",
        "boundary condition behavior is not fully constrained",
    ),
    # 通用 fallback
    (
        r"replaced.*return",
        "return-value correctness is insufficiently specified",
    ),
]


def _mutation_desc_to_behavior(desc: str) -> str:
    """将 PIT 变异描述翻译成行为薄弱点。"""
    desc = desc.strip()
    for pattern, behavior in MUTATION_TO_BEHAVIOR:
        if re.search(pattern, desc, re.I):
            return behavior
    return "behavior is insufficiently tested"


def parse_surviving_mutants(html_content: str) -> list[tuple[str, str]]:
    """
    从 PIT 类级 HTML 中提取 surviving mutants。
    返回 [(method_name, mutation_description), ...]
    """
    # 匹配格式: "N. method : mutation desc → SURVIVED" 或 "method : mutation desc &rarr; SURVIVED"
    # 示例: "1. div : Replaced integer multiplication with division &rarr; SURVIVED<br/>"
    pattern = re.compile(
        r"(?:\d+\.\s+)?(\w+)\s*:\s*([^&]+?)\s*(?:&rarr;|→)\s*SURVIVED",
        re.IGNORECASE | re.DOTALL,
    )
    # 排除 HTML 标签中的假匹配（如 "Location : </b>div" 会匹配成 method=Location）
    skip_methods = {"Location", "Killed", "b", "span"}

    results = []
    for m in pattern.finditer(html_content):
        method = m.group(1).strip()
        desc = m.group(2).strip()
        if method in skip_methods:
            continue
        # 清理 HTML 标签和多余空白
        desc = re.sub(r"<[^>]+>", "", desc)
        desc = re.sub(r"\s+", " ", desc).strip()
        if method and desc and len(method) < 30:  # 方法名不会很长
            results.append((method, desc))
    return results


def build_mutation_summary(html_path: Path) -> str:
    """
    从 PIT HTML 报告生成 MUTATION_SUMMARY 文本。
    按方法聚合，每个方法 1–2 条行为薄弱点。
    """
    if not html_path.exists():
        return "No PIT report found. Cannot generate mutation summary."

    content = html_path.read_text(encoding="utf-8", errors="replace")
    surviving = parse_surviving_mutants(content)

    if not surviving:
        return "No surviving mutants. Mutation score is 100%."

    # 按方法聚合
    by_method: dict[str, list[str]] = {}
    for method, desc in surviving:
        behavior = _mutation_desc_to_behavior(desc)
        if method not in by_method:
            by_method[method] = []
        if behavior not in by_method[method]:
            by_method[method].append(behavior)

    # 生成摘要文本
    lines = []
    for method in sorted(by_method.keys()):
        behaviors = by_method[method]
        if len(behaviors) == 1:
            lines.append(f"- {method}: surviving mutant indicates {behaviors[0]}.")
        else:
            combined = "; ".join(behaviors[:2])  # 最多 2 条
            lines.append(f"- {method}: surviving mutants indicate {combined}.")

    return "\n".join(lines)


def parse_mutation_score(html_content: str) -> str | None:
    """
    从 PIT 包级或项目级 index.html 解析 Mutation Coverage（非 Line Coverage）。
    PIT 表格列顺序固定：Line Coverage | Mutation Coverage | Test Strength。
    只取第二列的 coverage_legend，即 Mutation Coverage。
    返回如 "10/11" 或 "91%"，解析不到则返回 None。
    """
    matches = re.findall(r'coverage_legend">(\d+%|\d+/\d+)', html_content)
    if len(matches) >= 2:
        return matches[1]  # Mutation Coverage = 第二列
    return matches[0] if matches else None


def get_pit_package_index_path(project_root: Path, package_name: str) -> Path:
    """PIT 包级 index: target/pit-reports/{package_name}/index.html"""
    return project_root / "target" / "pit-reports" / package_name / "index.html"


def get_pit_class_report_path(project_root: Path, cut_class_name: str, package_name: str) -> Path:
    """
    返回 PIT 类级 HTML 报告路径。
    结构: target/pit-reports/{package_name}/ClassName.java.html
    """
    return (
        project_root
        / "target"
        / "pit-reports"
        / package_name
        / f"{cut_class_name}.java.html"
    )
