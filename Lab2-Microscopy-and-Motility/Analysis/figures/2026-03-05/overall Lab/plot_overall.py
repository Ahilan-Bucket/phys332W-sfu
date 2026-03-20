"""
Generate comprehensive comparison plot:
  D_measured (3 methods) vs D_theory (Faxen range)
  For all conditions from R-series and S-series.
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from collections import defaultdict

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Read aggregated data ──────────────────────────────────────────────
agg_path = os.path.join(OUTPUT_DIR, 'overall_aggregated.csv')
data = []
with open(agg_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for key in ['bead_um', 'D_var_mean', 'D_var_std', 'D_gauss_mean', 'D_gauss_std',
                     'D_msd_mean', 'D0', 'D_theory_max', 'D_theory_min',
                     'ratio_var', 'ratio_gauss', 'alpha_mean', 'alpha_std']:
            row[key] = float(row[key])
        row['n_trials'] = int(row['n_trials'])
        data.append(row)

# ── Read per-trial data ──────────────────────────────────────────────
trial_path = os.path.join(OUTPUT_DIR, 'overall_data_summary.csv')
trials = []
with open(trial_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for key in ['bead_um', 'D_var', 'D_var_err', 'D_gauss', 'D_gauss_err',
                     'D0', 'D_theory_max', 'D_theory_min', 'alpha']:
            try:
                row[key] = float(row[key])
            except (ValueError, KeyError):
                row[key] = 0.0
        try:
            row['D_msd'] = float(row['D_msd'])
        except:
            row['D_msd'] = 0.0
        trials.append(row)

# ── Color and marker scheme ──────────────────────────────────────────
solvent_colors = {
    'Water': '#2196F3',
    '20% Gly': '#4CAF50',
    '36% Gly': '#FF9800',
    '40% Gly': '#F44336',
    '41% Gly': '#F44336',
    '100% Ace': '#9C27B0',
    '20% Ace': '#E91E63',
    '40% Ace': '#E91E63',
}

bead_markers = {1.0: 'o', 2.1: 's', 3.0: '^', 5.0: 'D'}
bead_sizes = {1.0: 60, 2.1: 70, 3.0: 80, 5.0: 90}

# ═══════════════════════════════════════════════════════════════════════
# PLOT 1: D_measured vs D_theory (1:1 plot) with Faxen band
# ═══════════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(1, 1, figsize=(10, 9))

# 1:1 line
d_range = np.linspace(0, 0.7, 100)
ax1.plot(d_range, d_range, 'k-', linewidth=1.5, label='1:1 (perfect match)', zorder=1)
ax1.fill_between(d_range, d_range * 0.561/0.986, d_range,
                 alpha=0.15, color='gray',
                 label='Faxen range (midplane to wall)', zorder=0)

# Plot each trial point
legend_entries = set()
for t in trials:
    bead = t['bead_um']
    solv = t['solvent_label']
    ser = t.get('series', 'R')
    D_th = t['D_theory_max']  # midplane theory
    D_var = t['D_var']
    D_gauss = t['D_gauss']

    color = solvent_colors.get(solv, '#888888')
    marker = bead_markers.get(bead, 'x')
    ms = bead_sizes.get(bead, 50)
    edge = 'black' if ser == 'R' else 'none'
    alpha_v = 0.9 if ser == 'R' else 0.5

    label_key = f"{bead} um, {solv}"
    label = label_key if label_key not in legend_entries else None
    legend_entries.add(label_key)

    ax1.scatter(D_th, D_var, c=color, marker=marker, s=ms,
                edgecolors=edge, linewidths=0.8, alpha=alpha_v,
                label=label, zorder=3)

ax1.set_xlabel('D_theory (midplane Faxen) [um^2/s]', fontsize=13)
ax1.set_ylabel('D_measured (Variance method) [um^2/s]', fontsize=13)
ax1.set_title('Measured vs Theoretical Diffusion Coefficient\n'
              'All Conditions (R + S series, 2026-03-05)', fontsize=14)
ax1.set_xlim(-0.01, 0.50)
ax1.set_ylim(-0.01, 0.50)
ax1.set_aspect('equal')
ax1.legend(fontsize=8, loc='upper left', ncol=2, framealpha=0.9)
ax1.grid(True, alpha=0.3)

# Add noise floor line
ax1.axhline(y=0.018, color='red', linestyle='--', linewidth=0.8, alpha=0.5)
ax1.text(0.35, 0.022, 'D_noise = 0.018', color='red', fontsize=8, alpha=0.7)

fig1.tight_layout()
fig1.savefig(os.path.join(OUTPUT_DIR, 'D_measured_vs_theory_overall.png'), dpi=200)
print(f"Plot 1 saved: D_measured_vs_theory_overall.png")

# ═══════════════════════════════════════════════════════════════════════
# PLOT 2: Bar chart — D comparison by condition (R-series only)
# ═══════════════════════════════════════════════════════════════════════
r_data = [d for d in data if d['series'] == 'R']
r_data.sort(key=lambda x: (-x['D_theory_max'], x['bead_um']))

fig2, ax2 = plt.subplots(1, 1, figsize=(16, 8))

x = np.arange(len(r_data))
width = 0.18

# Theory band
for i, d in enumerate(r_data):
    ax2.fill_between([i - 0.4, i + 0.4], d['D_theory_min'], d['D_theory_max'],
                     alpha=0.2, color='gray', zorder=0)

# Bars
bars_var = ax2.bar(x - width, [d['D_var_mean'] for d in r_data], width,
                   yerr=[d['D_var_std'] for d in r_data],
                   label='Variance', color='#2196F3', capsize=3, zorder=2)
bars_gauss = ax2.bar(x, [d['D_gauss_mean'] for d in r_data], width,
                     yerr=[d['D_gauss_std'] for d in r_data],
                     label='Gaussian', color='#4CAF50', capsize=3, zorder=2)
bars_msd = ax2.bar(x + width, [d['D_msd_mean'] for d in r_data], width,
                   label='MSD Slope', color='#FF9800', capsize=3, zorder=2)

# Theory markers
ax2.scatter(x, [d['D_theory_max'] for d in r_data], marker='_', s=200,
            color='black', linewidths=2, label='D_max (midplane)', zorder=3)
ax2.scatter(x, [d['D_theory_min'] for d in r_data], marker='_', s=200,
            color='red', linewidths=2, label='D_min (wall)', zorder=3)

# Labels
labels = [f"{d['bead_um']}um\n{d['solvent_label']}\n(n={d['n_trials']})" for d in r_data]
ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=8)
ax2.set_ylabel('D [um^2/s]', fontsize=13)
ax2.set_title('R-Series: Measured D (3 methods) vs Theory (Nathan Faxen range)\n'
              'Gray band = [D_min(wall), D_max(midplane)]', fontsize=13)
ax2.legend(fontsize=9, loc='upper right')
ax2.grid(True, axis='y', alpha=0.3)
ax2.axhline(y=0.018, color='red', linestyle='--', linewidth=0.8, alpha=0.4)
ax2.text(len(r_data)-1, 0.022, 'noise floor', color='red', fontsize=8, alpha=0.6)
ax2.set_ylim(bottom=-0.005)

fig2.tight_layout()
fig2.savefig(os.path.join(OUTPUT_DIR, 'D_bar_comparison_R_series.png'), dpi=200)
print(f"Plot 2 saved: D_bar_comparison_R_series.png")

# ═══════════════════════════════════════════════════════════════════════
# PLOT 3: D_var/D_theory ratio by bead size (trend analysis)
# ═══════════════════════════════════════════════════════════════════════
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: ratio vs bead size, colored by solvent
for t in trials:
    if t.get('series') != 'R':
        continue
    bead = t['bead_um']
    D_th = t['D_theory_max']
    D_m = t['D_var']
    ratio = D_m / D_th if D_th > 0.001 else 0
    solv = t['solvent_label']
    color = solvent_colors.get(solv, '#888')
    marker = bead_markers.get(bead, 'x')
    ax3a.scatter(bead, ratio, c=color, marker=marker, s=80, edgecolors='black',
                 linewidths=0.5, alpha=0.8, zorder=3)

ax3a.axhline(y=1.0, color='green', linestyle='-', linewidth=1.5, alpha=0.7, label='Perfect match')
ax3a.axhline(y=0.561/0.986, color='orange', linestyle='--', linewidth=1, alpha=0.7,
             label=f'Wall Faxen limit ({0.561/0.986:.2f})')
ax3a.set_xlabel('Bead Diameter [um]', fontsize=12)
ax3a.set_ylabel('D_measured / D_theory(midplane)', fontsize=12)
ax3a.set_title('R-Series: Ratio vs Bead Size', fontsize=13)
ax3a.set_xlim(0, 6)
ax3a.set_ylim(-0.05, 1.6)
ax3a.legend(fontsize=9)
ax3a.grid(True, alpha=0.3)

# Add solvent legend manually
from matplotlib.lines import Line2D
legend_handles = [Line2D([0],[0], marker='o', color='w', markerfacecolor=c, markersize=8, label=s)
                  for s, c in solvent_colors.items() if s in ['Water','20% Gly','40% Gly','100% Ace']]
ax3a.legend(handles=legend_handles + [
    Line2D([0],[0], color='green', linewidth=1.5, label='Perfect match'),
    Line2D([0],[0], color='orange', linewidth=1, linestyle='--', label='Wall limit'),
], fontsize=8, loc='upper right')

# RIGHT: ratio vs viscosity
for t in trials:
    if t.get('series') != 'R':
        continue
    D_th = t['D_theory_max']
    D_m = t['D_var']
    ratio = D_m / D_th if D_th > 0.001 else 0
    bead = t['bead_um']
    solv = t['solvent_label']
    # Get viscosity from D0 and bead size
    # D0 = kBT/(6*pi*eta*r) -> eta = kBT/(6*pi*D0*r)
    D0 = t['D0']
    if D0 > 0:
        kBT = 1.380649e-23 * 295.15
        r = bead / 2 * 1e-6
        eta = kBT / (6 * 3.14159 * D0 * 1e-12 * r) * 1e3  # mPa.s
    else:
        eta = 1.0

    color = solvent_colors.get(solv, '#888')
    marker = bead_markers.get(bead, 'x')
    ax3b.scatter(eta, ratio, c=color, marker=marker, s=80, edgecolors='black',
                 linewidths=0.5, alpha=0.8, zorder=3)

ax3b.axhline(y=1.0, color='green', linestyle='-', linewidth=1.5, alpha=0.7)
ax3b.axhline(y=0.561/0.986, color='orange', linestyle='--', linewidth=1, alpha=0.7)
ax3b.set_xlabel('Viscosity [mPa.s]', fontsize=12)
ax3b.set_ylabel('D_measured / D_theory(midplane)', fontsize=12)
ax3b.set_title('R-Series: Ratio vs Viscosity', fontsize=13)
ax3b.set_xscale('log')
ax3b.set_ylim(-0.05, 1.6)
ax3b.grid(True, alpha=0.3)

bead_handles = [Line2D([0],[0], marker=m, color='w', markerfacecolor='gray', markersize=8,
                        label=f'{b} um') for b, m in bead_markers.items()]
ax3b.legend(handles=bead_handles, fontsize=9, loc='upper right')

fig3.tight_layout()
fig3.savefig(os.path.join(OUTPUT_DIR, 'D_ratio_trends.png'), dpi=200)
print(f"Plot 3 saved: D_ratio_trends.png")

# ═══════════════════════════════════════════════════════════════════════
# PLOT 4: Combined 4-panel overview
# ═══════════════════════════════════════════════════════════════════════
fig4, axes = plt.subplots(2, 2, figsize=(16, 14))

# Panel A: D vs 1/bead_radius (should be linear for fixed eta)
ax = axes[0, 0]
for solv_label in ['Water', '20% Gly', '40% Gly', '100% Ace']:
    # Theory line
    beads = [1.0, 2.1, 3.0, 5.0]
    inv_r = [2.0/b for b in beads]  # 1/radius in 1/um

    d_th = []
    d_exp = []
    d_err = []
    for d in data:
        if d['series'] == 'R' and d['solvent_label'] == solv_label:
            d_th.append(d['D_theory_max'])
            d_exp.append(d['D_var_mean'])
            d_err.append(d['D_var_std'])

    color = solvent_colors.get(solv_label, '#888')
    if d_th:
        beads_found = [d['bead_um'] for d in data if d['series']=='R' and d['solvent_label']==solv_label]
        inv_r_found = [2.0/b for b in beads_found]
        ax.plot(inv_r_found, d_th, '--', color=color, linewidth=1.5, alpha=0.6)
        ax.errorbar(inv_r_found, d_exp, yerr=d_err, fmt='o', color=color,
                    capsize=3, markersize=6, label=solv_label, zorder=3)

ax.set_xlabel('1/r [1/um]', fontsize=11)
ax.set_ylabel('D [um^2/s]', fontsize=11)
ax.set_title('(A) D vs 1/radius (Stokes-Einstein: D ~ 1/r)', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Panel B: D vs viscosity (should be linear on log-log with slope -1)
ax = axes[0, 1]
for bead in [1.0, 2.1, 3.0, 5.0]:
    etas_th = []
    d_th = []
    d_exp = []

    for d in data:
        if d['series'] == 'R' and d['bead_um'] == bead:
            kBT = 1.380649e-23 * 295.15
            r = bead / 2 * 1e-6
            D0 = d['D0']
            if D0 > 0:
                eta = kBT / (6 * 3.14159 * D0 * 1e-12 * r) * 1e3
            else:
                eta = 1.0
            etas_th.append(eta)
            d_th.append(d['D_theory_max'])
            d_exp.append(d['D_var_mean'])

    marker = bead_markers.get(bead, 'x')
    if etas_th:
        ax.plot(etas_th, d_th, '--', color='gray', linewidth=1, alpha=0.5)
        ax.scatter(etas_th, d_exp, marker=marker, s=80, edgecolors='black',
                   linewidths=0.5, label=f'{bead} um', zorder=3)

ax.set_xlabel('Viscosity [mPa.s]', fontsize=11)
ax.set_ylabel('D [um^2/s]', fontsize=11)
ax.set_title('(B) D vs Viscosity (Stokes-Einstein: D ~ 1/eta)', fontsize=12)
ax.set_xscale('log')
ax.set_yscale('log')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, which='both')

# Panel C: Alpha distribution
ax = axes[1, 0]
alphas_r = [t['alpha'] for t in trials if t.get('series') == 'R' and t.get('alpha', 0) > 0]
alphas_s = [t['alpha'] for t in trials if t.get('series') == 'S-slide' and t.get('alpha', 0) > 0]

ax.hist(alphas_r, bins=15, range=(0, 1.8), alpha=0.6, color='#2196F3', label=f'R-series (n={len(alphas_r)})', edgecolor='black')
ax.hist(alphas_s, bins=15, range=(0, 1.8), alpha=0.5, color='#FF9800', label=f'S-series (n={len(alphas_s)})', edgecolor='black')
ax.axvline(x=1.0, color='green', linewidth=2, linestyle='-', label='Normal diffusion (a=1)')
ax.axvspan(0.8, 1.2, alpha=0.1, color='green')
ax.set_xlabel('MSD Exponent (alpha)', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('(C) Distribution of MSD Exponent alpha', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Panel D: Variance vs Gaussian agreement
ax = axes[1, 1]
for t in trials:
    bead = t['bead_um']
    solv = t['solvent_label']
    D_var = t['D_var']
    D_gauss = t['D_gauss']
    color = solvent_colors.get(solv, '#888')
    marker = bead_markers.get(bead, 'x')
    ser = t.get('series', 'R')
    alpha_v = 0.9 if ser == 'R' else 0.4
    ax.scatter(D_var, D_gauss, c=color, marker=marker, s=60,
               edgecolors='black' if ser=='R' else 'none',
               linewidths=0.5, alpha=alpha_v, zorder=3)

d_line = np.linspace(0, 0.45, 100)
ax.plot(d_line, d_line, 'k-', linewidth=1, alpha=0.5, label='1:1')
ax.set_xlabel('D (Variance) [um^2/s]', fontsize=11)
ax.set_ylabel('D (Gaussian) [um^2/s]', fontsize=11)
ax.set_title('(D) Variance vs Gaussian Method Agreement', fontsize=12)
ax.set_aspect('equal')
ax.set_xlim(-0.01, 0.45)
ax.set_ylim(-0.01, 0.45)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

fig4.suptitle('Overall Analysis: 2026-03-05 Batch (50 trials, R + S series)',
              fontsize=15, fontweight='bold', y=1.01)
fig4.tight_layout()
fig4.savefig(os.path.join(OUTPUT_DIR, 'overall_4panel.png'), dpi=200, bbox_inches='tight')
print(f"Plot 4 saved: overall_4panel.png")

plt.close('all')
print("\nAll plots generated successfully!")
