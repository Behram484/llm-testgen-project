import re
from pathlib import Path

src = Path(r"D:\Project\testgen-lab\src\main\java")
cuts = sorted(src.rglob("*.java"))

header = f"{'CUT':<30} {'LOC':>5} {'PubMethods':>10}"
print(header)
print("-" * len(header))
for f in cuts:
    code = f.read_text(encoding="utf-8", errors="replace")
    loc = len(code.splitlines())
    cls_name = f.stem
    pub = re.findall(
        r"^\s*public\s+(?:static\s+|final\s+|synchronized\s+|abstract\s+)*"
        r"[A-Za-z_<>\[\]?, ]+\s+[A-Za-z_]\w*\s*\(",
        code,
        re.MULTILINE,
    )
    ctors = re.findall(
        rf"^\s*public\s+{re.escape(cls_name)}\s*\(",
        code,
        re.MULTILINE,
    )
    real_pub = [
        p for p in pub
        if " class " not in p and " interface " not in p and " enum " not in p
    ]
    total = len(real_pub) + len(ctors)
    print(f"{cls_name:<30} {loc:>5} {total:>10}")
