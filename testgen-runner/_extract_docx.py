import zipfile, re
from pathlib import Path

docx = Path(r'd:\report\report writing\Final_draft_v7.docx')
with zipfile.ZipFile(docx) as z:
    xml = z.read('word/document.xml').decode('utf-8', errors='replace')

text = re.sub(r'<[^>]+>', ' ', xml)
text = re.sub(r'\s+', ' ', text)

keywords = [
    'method signature', 'METHOD_SIGNATURE', 'standard profile',
    'detailed profile', 'standard prompt', 'additionally inject',
    'public method', 'CUT source', 'standard generation',
    'guided-lite', 'guided_lite', 'instruction load',
    'prompt profile', 'generation profile',
]
for kw in keywords:
    idx = text.lower().find(kw.lower())
    if idx >= 0:
        snippet = text[max(0,idx-200):idx+300]
        print(f'--- found "{kw}" at pos {idx} ---')
        print(snippet.strip())
        print()
