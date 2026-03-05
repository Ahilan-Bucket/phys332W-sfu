import matplotlib
matplotlib.use('Agg')
import sys
sys.stdout.reconfigure(encoding='utf-8')

DATA = r"D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Data"

JOBS = [
    (DATA + "\\2026-03-03\\r8-5mu-0_5p-20ul-water-390ul-gly-100ul-trial1.avi",  5.0, 20.0, "glycerol", 19.0),
    (DATA + "\\2026-03-03\\r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi",           1.0,  0.0, "glycerol", 19.0),
]

FORCE_REPROCESS = True

# Read the full pipeline, inject our overrides, and exec
with open('_run_pipeline.py', 'r', encoding='utf-8') as f:
    src = f.read()

# Replace FORCE_REPROCESS = False -> True in the source
src = src.replace("FORCE_REPROCESS = False", "FORCE_REPROCESS = True", 1)

# Find where Cell 1 ends (right before Cell 2)
cell2_idx = src.find("# CELL 2\n")
# The constants start at "# --- Pipeline versioning ---"
const_idx = src.find("# --- Pipeline versioning ---")

if const_idx < 0 or cell2_idx < 0:
    print("ERROR: Could not find markers")
    sys.exit(1)

import_section = """import matplotlib
matplotlib.use('Agg')
import sys
sys.stdout.reconfigure(encoding='utf-8')

"""

jobs_section = '''
DATA = r"D:\\Documents\\SFU\\PHYS382-AdvancedLab\\phys332w-sfu-GIT\\phys332W-sfu\\Lab2-Microscopy-and-Motility\\Data"

JOBS = [
    (DATA + r"\\2026-03-03\\r8-5mu-0_5p-20ul-water-390ul-gly-100ul-trial1.avi",  5.0, 20.0, "glycerol", 19.0),
    (DATA + r"\\2026-03-03\\r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi",           1.0,  0.0, "glycerol", 19.0),
]

'''

full = import_section + jobs_section + src[const_idx:]
exec(compile(full, '_test_r8_r1_exec', 'exec'))
