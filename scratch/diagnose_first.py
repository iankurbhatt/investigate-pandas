import json
with open('investigate.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'read_csv' in source:
            print(f"Cell {idx}: has read_csv")
            print(source)
