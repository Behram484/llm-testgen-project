import csv
from pathlib import Path
from collections import Counter

rows = list(csv.DictReader(Path(r'D:\Project\testgen-runner\cut_feature_table.csv').open(encoding='utf-8')))
n = len(rows)

schema = {
    'Statefulness': {'stateless','light_state','stateful'},
    'TransformationType': {'numeric_math','string_text','byte_codec','config_format','collection_helper','parsing_matching','time_dependent','mixed_other'},
    'DependencyBurden': {'self_contained','light_dependency','multi_class_dependency'},
    'OracleClarity': {'clear','moderate','hard'},
}
dirty = []
for i, r in enumerate(rows, 1):
    for col, valid in schema.items():
        if r[col] not in valid:
            dirty.append("Row {} ({}): {}={!r} not in {}".format(i, r['CUT'], col, r[col], valid))

if dirty:
    print('DIRTY VALUES FOUND:')
    for d in dirty:
        print('  ' + d)
else:
    print('Schema validation: ALL {} ROWS CLEAN'.format(n))

print()
for col in ['OracleClarity', 'DependencyBurden']:
    c = Counter(r[col] for r in rows)
    print('{} distribution:'.format(col))
    for k, v in sorted(c.items(), key=lambda x: -x[1]):
        print('  {:<25} {:>3}  ({:.0f}%)'.format(k, v, v/n*100))
    print()

print('Changed rows verification:')
for r in rows:
    if r['CUT'] in ('HtmlEncoder', 'StringUtils', 'SAXPathException', 'GridLayout2'):
        print('  {} -> DependencyBurden={}, OracleClarity={}'.format(r['CUT'], r['DependencyBurden'], r['OracleClarity']))
