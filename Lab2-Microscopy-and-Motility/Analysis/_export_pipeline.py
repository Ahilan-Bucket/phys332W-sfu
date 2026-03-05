"""Export notebook cells to _run_pipeline.py for headless execution."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

NB_PATH = r'D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Analysis\Lab2_Analysis_Pipeline.ipynb'
OUT_PATH = r'D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Analysis\_run_pipeline.py'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

lines = [
    '# Auto-generated from Lab2_Analysis_Pipeline.ipynb',
    '# Run with: python _run_pipeline.py',
    'import matplotlib',
    "matplotlib.use('Agg')",
    'import sys',
    "sys.stdout.reconfigure(encoding='utf-8')",
    '',
]

for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    src = cell['source']
    if isinstance(src, list):
        src = ''.join(src)
    lines.append(f'# {"=" * 70}')
    lines.append(f'# CELL {i}')
    lines.append(f'# {"=" * 70}')
    lines.append(src)
    lines.append('')

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Exported {len(nb["cells"])} cells to {OUT_PATH}')
