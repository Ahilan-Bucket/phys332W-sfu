import matplotlib
matplotlib.use('Agg')
import sys
sys.stdout.reconfigure(encoding='utf-8')

DATA = r"D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Data"

JOBS = [
    (DATA + "\\2026-03-03\\r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi",            1.0,   0.0, "glycerol", 19.0),
    (DATA + "\\2026-03-03\\r5-1mu-0_5p-1_15ul-water-400ul-gly-100ul-trial1.avi",  1.0,  20.0, "glycerol", 19.0),
    (DATA + "\\2026-03-03\\r3-trial1.avi",                                          3.0,   0.0, "glycerol", 19.0),
    (DATA + "\\2026-03-03\\r14-2_1mu-0_5p-4ul-acetone-498ul-trial1.avi",           2.1, 100.0, "acetone",  19.0),
]

FORCE_REPROCESS = True

# Read the full pipeline, inject our overrides, and exec
with open('_run_pipeline.py', 'r', encoding='utf-8') as f:
    src = f.read()

# Replace FORCE_REPROCESS = False -> True in the source
src = src.replace("FORCE_REPROCESS = False", "FORCE_REPROCESS = True", 1)

# Find where Cell 1 ends (right before Cell 2)
cell2_idx = src.find("# CELL 2\n")
# Find where JOBS list starts — replace everything from line 1 to just before constants
# The constants start at "# --- Pipeline versioning ---"
const_idx = src.find("# --- Pipeline versioning ---")

if const_idx < 0 or cell2_idx < 0:
    print("ERROR: Could not find markers")
    sys.exit(1)

# Build: our header + constants section + Cell 2 onwards
# The constants section runs from const_idx to cell2_idx
# We need the imports at the top too
import_section = """import matplotlib
matplotlib.use('Agg')
import sys
sys.stdout.reconfigure(encoding='utf-8')

"""

# Our JOBS override
jobs_section = '''
DATA = r"D:\\Documents\\SFU\\PHYS382-AdvancedLab\\phys332w-sfu-GIT\\phys332W-sfu\\Lab2-Microscopy-and-Motility\\Data"

JOBS = [
    (DATA + r"\\2026-03-03\\r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi",            1.0,   0.0, "glycerol", 19.0),
    (DATA + r"\\2026-03-03\\r5-1mu-0_5p-1_15ul-water-400ul-gly-100ul-trial1.avi",  1.0,  20.0, "glycerol", 19.0),
    (DATA + r"\\2026-03-03\\r3-trial1.avi",                                          3.0,   0.0, "glycerol", 19.0),
    (DATA + r"\\2026-03-03\\r14-2_1mu-0_5p-4ul-acetone-498ul-trial1.avi",           2.1, 100.0, "acetone",  19.0),
]

'''

# Combine: constants (with FORCE_REPROCESS already replaced) + print JOBS + Cell 2 onwards
full = import_section + jobs_section + src[const_idx:]

exec(compile(full, '_test_subset_exec', 'exec'))
