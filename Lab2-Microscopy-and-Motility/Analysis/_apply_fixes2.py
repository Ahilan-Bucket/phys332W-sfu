"""Apply remaining fixes: add r7 data, fix mask circle, fix Cell 4 overall trends."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

NB_PATH = r'D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Analysis\Lab2_Analysis_Pipeline.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

def get_src(idx):
    s = nb['cells'][idx]['source']
    return ''.join(s) if isinstance(s, list) else s

def set_src(idx, s):
    nb['cells'][idx]['source'] = s

# =====================================================================
# ADD r7 videos to Cell 1
# =====================================================================
cell1 = get_src(1)

# Add path definitions (before JOBS LIST marker)
r7_paths = (
    '# --- r7: 3um in 20% glycerol (3ul stock, 397ul water, 100ul glycerol) ---\n'
    'r7_t1  = DATA + r"\\2026-03-03\\r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial1.avi"\n'
    'r7_t2  = DATA + r"\\2026-03-03\\r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial2.avi"\n'
    'r7_t3  = DATA + r"\\2026-03-03\\r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial3-best.avi"\n'
    '\n'
)

# Insert before JOBS LIST if not already there
if 'r7_t1' not in cell1:
    marker = '# --- JOBS LIST ---'
    cell1 = cell1.replace(marker, r7_paths + marker)
    print('Added r7 path definitions')
else:
    print('r7 paths already exist')

# Add r7 JOBS entries at end of list
# glycerol% = 100/(397+100) = 20.1%
r7_jobs = (
    '\n'
    '    # r7: 3um in 20% glycerol (3ul stock, 397ul water, 100ul glycerol)\n'
    "    (r7_t1,  3.0, 20.1, 'glycerol'),\n"
    "    (r7_t2,  3.0, 20.1, 'glycerol'),\n"
    "    (r7_t3,  3.0, 20.1, 'glycerol'),\n"
)

if 'r7_t1' not in cell1[cell1.find('JOBS = ['):]:
    # Find the closing bracket of JOBS
    old_end = "    (r5_t1,  1.0, 20.0, 'glycerol'),\n]"
    new_end = "    (r5_t1,  1.0, 20.0, 'glycerol')," + r7_jobs + ']'
    if old_end in cell1:
        cell1 = cell1.replace(old_end, new_end)
        print('Added r7 JOBS entries')
    else:
        print('ERROR: Could not find JOBS list end')
else:
    print('r7 JOBS already exist')

set_src(1, cell1)

# =====================================================================
# FIX mask circle radius in Cell 3 — use exact bead radius
# =====================================================================
cell3 = get_src(3)

# The current circle draws at 1.5x bead radius — change to 1x
old_circle = '        r_circle = max(5, int(_bead_radius_px * 1.5))'
new_circle = (
    '        # Circle radius = actual bead radius in pixels, so the green\n'
    '        # circle matches the physical bead size in the overlay image.\n'
    '        r_circle = max(3, int(_bead_radius_px))'
)
if old_circle in cell3:
    cell3 = cell3.replace(old_circle, new_circle)
    print('Fixed mask overlay circle to use exact bead radius')
else:
    print('ERROR: Could not find circle radius line')

set_src(3, cell3)

# =====================================================================
# FIX Cell 4 — Read ALL summary.txt files for trend plots
#   Currently it only uses batch_results (in-memory from current run).
#   When FORCE_REPROCESS=False, skipped videos are missing from the plots.
#   Fix: scan ALL figures/<date>/<video>/summary.txt files to rebuild the
#   full dataset, so trend plots ALWAYS include every video.
# =====================================================================

new_cell4 = r'''# ============================================================================
# CELL 4 — OVERALL TREND PLOTS (scans ALL output folders)
# ============================================================================
# This cell reads summary.txt from every processed video folder, so the
# trend plots always include ALL data — even videos skipped in this run.

import re
from pathlib import Path

FIGURES_ROOT = Path(os.getcwd()) / 'figures'

all_results = []
for summary_path in sorted(FIGURES_ROOT.rglob('summary.txt')):
    folder = summary_path.parent
    txt = summary_path.read_text(encoding='utf-8')

    # --- Parse key fields from summary.txt ---
    def _grab(pattern, default=None):
        m = re.search(pattern, txt)
        return m.group(1) if m else default

    video_name = folder.name
    bead_str  = _grab(r'Bead diameter:\s*([\d.]+)')
    solute_str = _grab(r'(?:Glycerol|Acetone):\s*([\d.]+)\s*%')
    solute_type = 'acetone' if 'Acetone' in txt else 'glycerol'
    eta_str   = _grab(r'Viscosity:\s*([\d.]+)\s*mPa')
    fps_str   = _grab(r'Frame rate:\s*([\d.]+)')
    d_var_str = _grab(r'D_direct_variance\s*=\s*([\d.eE+-]+)')
    d_gau_str = _grab(r'D_gaussian_fit\s*=\s*([\d.eE+-]+)')
    d_msd_str = _grab(r'D_MSD\s*=\s*([\d.eE+-]+)')
    d_the_str = _grab(r'D_theory_faxen\s*=\s*([\d.eE+-]+)')
    alpha_str = _grab(r'alpha\s*=\s*([\d.eE+-]+)')

    # Skip if essential fields are missing
    if not all([bead_str, eta_str, d_var_str, d_msd_str, d_the_str, alpha_str]):
        continue

    bead = float(bead_str)
    eta  = float(eta_str)
    fps  = float(fps_str) if fps_str else 29.0
    d_var = float(d_var_str)
    d_gau = float(d_gau_str) if d_gau_str else 0.0
    d_msd = float(d_msd_str)
    d_the = float(d_the_str)
    alpha = float(alpha_str)
    solute_pct = float(solute_str) if solute_str else 0.0

    # Build label
    if solute_type == 'acetone':
        solute_label = f'{solute_pct:.0f}%Ace'
    elif solute_pct > 0:
        solute_label = f'{solute_pct:.0f}%Gly'
    else:
        solute_label = 'Water'

    d_avg = np.mean([d_var, d_gau, d_msd])
    dev_pct = (d_avg - d_the) / d_the * 100 if d_the > 0 else 0

    all_results.append({
        'video': video_name, 'bead': bead, 'solute_pct': solute_pct,
        'solute_type': solute_type, 'solute_label': solute_label,
        'eta': eta, 'fps': fps,
        'd_var': d_var, 'd_gau': d_gau, 'd_msd': d_msd,
        'd_theory': d_the, 'd_avg': d_avg, 'dev_pct': dev_pct,
        'alpha': alpha,
    })

print(f'Loaded {len(all_results)} datasets from summary files for trend plots.')

if len(all_results) < 2:
    print('Not enough data for trend plots (need >= 2).')
else:
    # --- Colour / marker mapping ---
    def condition_key(r):
        return (r['bead'], r['solute_label'])

    unique_conditions = sorted(set(condition_key(r) for r in all_results))
    cmap = plt.cm.tab10
    cond_colors = {c: cmap(i / max(len(unique_conditions) - 1, 1))
                   for i, c in enumerate(unique_conditions)}
    cond_labels = {c: f'{c[0]} um, {c[1]}' for c in unique_conditions}

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    fig.suptitle('Overall Trends Across All Datasets', fontsize=15, weight='bold')

    # ---- (a) Parity plot: D_experiment vs D_theory ----
    ax = axes[0, 0]
    for cond in unique_conditions:
        pts = [r for r in all_results if condition_key(r) == cond]
        d_exp = [r['d_avg'] for r in pts]
        d_the = [r['d_theory'] for r in pts]
        ax.scatter(d_the, d_exp, color=cond_colors[cond], s=50,
                   label=cond_labels[cond], zorder=3)
    lim = max(ax.get_xlim()[1], ax.get_ylim()[1]) * 1.05
    ax.plot([0, lim], [0, lim], 'k--', alpha=0.3, label='Perfect agreement')
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.set_xlabel(r'$D_{\mathrm{theory}}$ (Stokes-Einstein + Faxen) [$\mu m^2/s$]')
    ax.set_ylabel(r'$D_{\mathrm{experiment}}$ (avg of 3 methods) [$\mu m^2/s$]')
    ax.set_title('Experiment vs Theory — Parity Plot')
    ax.legend(fontsize=7, loc='upper left')

    # ---- (b) D vs viscosity ----
    ax = axes[0, 1]
    for cond in unique_conditions:
        pts = [r for r in all_results if condition_key(r) == cond]
        ax.scatter([r['eta'] for r in pts], [r['d_avg'] for r in pts],
                   color=cond_colors[cond], s=50, label=cond_labels[cond], zorder=3)
    # Theory curve for 3 um beads
    eta_range = np.linspace(0.5, max(r['eta'] for r in all_results) * 1.1, 100)
    T_K = TEMPERATURE_C + 273.15
    D_curve = k_B * T_K / (6 * np.pi * (eta_range * 1e-3) * 1.5e-6) * 1e12
    ax.plot(eta_range, D_curve, 'k--', alpha=0.4, label='S-E theory (3 um)')
    # Theory marker x for each condition
    for cond in unique_conditions:
        pts = [r for r in all_results if condition_key(r) == cond]
        for r in pts:
            ax.scatter(r['eta'], r['d_theory'], marker='x', s=80,
                       color=cond_colors[cond], linewidths=2, zorder=4)
    ax.set_xlabel(r'$\eta$ [mPa$\cdot$s]')
    ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
    ax.set_title(r'D vs Viscosity (circles=exp, x=theory)')
    ax.legend(fontsize=7)

    # ---- (c) D vs bead size ----
    ax = axes[1, 0]
    for cond in unique_conditions:
        pts = [r for r in all_results if condition_key(r) == cond]
        ax.scatter([r['bead'] for r in pts], [r['d_avg'] for r in pts],
                   color=cond_colors[cond], s=50, label=cond_labels[cond], zorder=3)
        for r in pts:
            ax.scatter(r['bead'], r['d_theory'], marker='x', s=80,
                       color=cond_colors[cond], linewidths=2, zorder=4)
    # S-E curve in water at bead sizes
    d_range = np.linspace(0.5, 6, 100)
    eta_water = get_glycerol_viscosity(0, TEMPERATURE_C)
    D_curve_size = k_B * T_K / (6 * np.pi * eta_water * (d_range / 2 * 1e-6)) * 1e12
    ax.plot(d_range, D_curve_size, 'k--', alpha=0.4, label='S-E theory (water)')
    ax.set_xlabel(r'Bead diameter [$\mu m$]')
    ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
    ax.set_title(r'D vs Bead Size (circles=exp, x=theory)')
    ax.legend(fontsize=7)

    # ---- (d) Alpha exponent bar chart ----
    ax = axes[1, 1]
    names = [r['video'][-30:] for r in all_results]
    alphas = [r['alpha'] for r in all_results]
    colors = [cond_colors[condition_key(r)] for r in all_results]
    y_pos = np.arange(len(names))
    ax.barh(y_pos, alphas, color=colors, edgecolor='none', height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=6)
    ax.axvline(x=1.0, color='red', linestyle='--', alpha=0.7, label=r'$\alpha=1$ (Brownian)')
    ax.set_xlabel(r'MSD Exponent $\alpha$')
    ax.set_title(r'MSD Exponent $\alpha$ — Motion Classification')
    # Legend with condition colours
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=cond_colors[c], label=cond_labels[c])
                       for c in unique_conditions]
    legend_elements.append(plt.Line2D([0], [0], color='red', linestyle='--',
                                       label=r'$\alpha=1$ (Brownian)'))
    ax.legend(handles=legend_elements, fontsize=6, loc='lower right')

    plt.tight_layout()
    out_path = FIGURES_ROOT / 'overall_trends.png'
    fig.savefig(str(out_path), dpi=200, bbox_inches='tight')
    plt.show()
    print(f'Saved overall trend plot to: {out_path}')

    # --- Print the full batch table ---
    print(f'\n{"=" * 130}')
    print(f'{"COMPLETE RESULTS TABLE":^130}')
    print(f'{"=" * 130}')
    hdr = f'{"Video":<50} {"Bead":>5} {"Solute":>10} {"eta":>7} {"fps":>5} {"D_var":>8} {"D_gau":>8} {"D_msd":>8} {"D_SE+F":>8} {"Dev%":>7} {"alpha":>6}'
    print(hdr)
    print('-' * 130)
    for r in all_results:
        name = r['video'][:48]
        print(f'{name:<50} {r["bead"]:5.1f} {r["solute_label"]:>10} '
              f'{r["eta"]:7.3f} {r["fps"]:5.0f} '
              f'{r["d_var"]:8.4f} {r["d_gau"]:8.4f} {r["d_msd"]:8.4f} '
              f'{r["d_theory"]:8.4f} {r["dev_pct"]:+7.1f} {r["alpha"]:6.2f}')
    print('=' * 130)
'''

set_src(4, new_cell4)
print('FIX 5: Cell 4 replaced — now scans ALL summary.txt files for trend plots')

# Save
with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('\nAll fixes applied and saved.')
