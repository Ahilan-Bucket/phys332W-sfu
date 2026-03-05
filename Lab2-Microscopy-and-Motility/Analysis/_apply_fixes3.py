"""Fix Cell 4 regex patterns to match actual summary.txt format."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

NB_PATH = r'D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Analysis\Lab2_Analysis_Pipeline.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell4 = nb['cells'][4]['source']
if isinstance(cell4, list):
    cell4 = ''.join(cell4)

# Fix the regex patterns to match actual summary.txt format
# Actual format examples:
#   Bead diameter: 3.0 um
#   Solute: 0.0% Glycerol       (or  20.0% Glycerol  or  20.1% Acetone)
#   Viscosity: 0.981 mPa.s
#   Frame rate: 29.0 fps
#   Method 1 (Direct Variance): 0.1684 +/- 0.0215
#   Method 2 (Gaussian Fit):     0.1083 +/- 0.0124
#   Method 3 (MSD Slope):        0.1267 +/- 0.0284
#   D_theory (final): 0.1435 um^2/s
#   alpha = 0.704 +/- 0.084

replacements = [
    # Solute: "0.0% Glycerol" not "Glycerol: 0.0%"
    (
        "solute_str = _grab(r'(?:Glycerol|Acetone):\\s*([\\d.]+)\\s*%')",
        "solute_str = _grab(r'Solute:\\s*([\\d.]+)%')"
    ),
    # Solute type
    (
        "solute_type = 'acetone' if 'Acetone' in txt else 'glycerol'",
        "solute_type = 'acetone' if 'Acetone' in txt else 'glycerol'"
    ),
    # D_direct_variance → "Method 1 (Direct Variance): 0.1684"
    (
        "d_var_str = _grab(r'D_direct_variance\\s*=\\s*([\\d.eE+-]+)')",
        "d_var_str = _grab(r'Direct Variance\\):\\s*([\\d.eE+-]+)')"
    ),
    # D_gaussian_fit → "Method 2 (Gaussian Fit):     0.1083"
    (
        "d_gau_str = _grab(r'D_gaussian_fit\\s*=\\s*([\\d.eE+-]+)')",
        "d_gau_str = _grab(r'Gaussian Fit\\):\\s*([\\d.eE+-]+)')"
    ),
    # D_MSD → "Method 3 (MSD Slope):        0.1267"
    (
        "d_msd_str = _grab(r'D_MSD\\s*=\\s*([\\d.eE+-]+)')",
        "d_msd_str = _grab(r'MSD Slope\\):\\s*([\\d.eE+-]+)')"
    ),
    # D_theory → "D_theory (final): 0.1435"
    (
        "d_the_str = _grab(r'D_theory_faxen\\s*=\\s*([\\d.eE+-]+)')",
        "d_the_str = _grab(r'D_theory \\(final\\):\\s*([\\d.eE+-]+)')"
    ),
]

count = 0
for old, new in replacements:
    if old in cell4:
        cell4 = cell4.replace(old, new)
        count += 1

nb['cells'][4]['source'] = cell4
print(f'Fixed {count} regex patterns in Cell 4')

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Notebook saved.')
