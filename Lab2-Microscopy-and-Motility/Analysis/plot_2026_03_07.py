"""
Generate high-quality comparison plots for the 2026-03-07 reorganised data.
Reads CSVs from the reorganized folder structure and produces:
  - Per-series plots (S-series, R-series)
  - Overall Lab plots
Matches the quality standard of the original plot_overall.py.
"""
import csv
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from collections import defaultdict
import statistics

# ── Paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(SCRIPT_DIR, 'figures', '2026-03-07')
OVERALL_DIR = os.path.join(TARGET_DIR, 'Overall Lab')
S_SESSION = os.path.join(TARGET_DIR, 'S-series (Feb 26)', 'overall session')
R_SESSION = os.path.join(TARGET_DIR, 'R-series (March 3)', 'overall session')

# ── Color and marker scheme ──────────────────────────────────────────
SOLVENT_COLORS = {
    'Water':    '#2196F3',
    '20% Gly':  '#4CAF50',
    '36% Gly':  '#FF9800',
    '40% Gly':  '#F44336',
    '41% Gly':  '#F44336',
    '100% Ace': '#9C27B0',
    '20% Ace':  '#E91E63',
    '40% Ace':  '#E91E63',
}
BEAD_MARKERS = {1.0: 'o', 2.1: 's', 3.0: '^', 5.0: 'D'}
BEAD_SIZES   = {1.0: 60, 2.1: 70, 3.0: 80, 5.0: 90}
NOISE_FLOOR  = 0.0180  # um^2/s


def load_trial_csv(path):
    """Load per-trial CSV, casting numerics."""
    trials = []
    float_keys = ['bead_um', 'D_var', 'D_var_err', 'D_gauss', 'D_gauss_err',
                  'D_msd', 'D_var_raw', 'D_gauss_raw', 'D_msd_raw',
                  'D0', 'F_min_wall', 'F_max_wall', 'D_theory_max', 'D_theory_min',
                  'alpha', 'alpha_err', 'solute_pct', 'eta_mPas', 'temp_C']
    int_keys = ['trial', 'n_frames', 'n_particles', 'n_segments', 'n_steps']
    with open(path, 'r') as f:
        for row in csv.DictReader(f):
            for k in float_keys:
                try:
                    row[k] = float(row[k])
                except (ValueError, KeyError, TypeError):
                    row[k] = 0.0
            for k in int_keys:
                try:
                    row[k] = int(row[k])
                except (ValueError, KeyError, TypeError):
                    row[k] = 0
            trials.append(row)
    return trials


def aggregate_trials(trials):
    """Group trials by (bead, solvent_label, series) and compute means."""
    groups = defaultdict(list)
    for t in trials:
        key = (t['bead_um'], t.get('solvent_label', '?'), t.get('series', '?'))
        groups[key].append(t)

    agg = []
    for (bead, solv, series), rows in sorted(groups.items()):
        d_vars = [r['D_var'] for r in rows]
        d_gauss = [r['D_gauss'] for r in rows]
        d_msds = [r['D_msd'] for r in rows if r['D_msd'] > 0]
        alphas = [r['alpha'] for r in rows if r.get('alpha', 0) > 0]

        agg.append({
            'bead_um': bead,
            'solvent_label': solv,
            'series': series,
            'condition_id': rows[0].get('condition_id', '?'),
            'n_trials': len(rows),
            'D_var_mean': statistics.mean(d_vars) if d_vars else 0,
            'D_var_std': statistics.stdev(d_vars) if len(d_vars) > 1 else 0,
            'D_gauss_mean': statistics.mean(d_gauss) if d_gauss else 0,
            'D_gauss_std': statistics.stdev(d_gauss) if len(d_gauss) > 1 else 0,
            'D_msd_mean': statistics.mean(d_msds) if d_msds else 0,
            'D0': rows[0].get('D0', 0),
            'D_theory_max': rows[0].get('D_theory_max', 0),
            'D_theory_min': rows[0].get('D_theory_min', 0),
            'alpha_mean': statistics.mean(alphas) if alphas else 0,
            'alpha_std': statistics.stdev(alphas) if len(alphas) > 1 else 0,
        })
    return agg


def save_fig(fig, path, dpi=200):
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    relpath = os.path.relpath(path, TARGET_DIR)
    print(f"  Saved: {relpath}")


# ═══════════════════════════════════════════════════════════════════════
# PLOT: D_measured vs D_theory (1:1 scatter with Faxen band)
# ═══════════════════════════════════════════════════════════════════════
def plot_scatter_1to1(trials, output_path, title='Measured vs Theory', xlim=0.50):
    fig, ax = plt.subplots(figsize=(10, 9))

    d_range = np.linspace(0, xlim * 1.4, 100)
    ax.plot(d_range, d_range, 'k-', lw=1.5, label='1:1 (perfect match)', zorder=1)
    ax.fill_between(d_range, d_range * 0.561 / 0.986, d_range,
                    alpha=0.15, color='gray',
                    label='Faxen range (midplane to wall)', zorder=0)

    legend_entries = set()
    for t in trials:
        bead = t['bead_um']
        solv = t.get('solvent_label', '?')
        ser = t.get('series', 'R')
        D_th = t['D_theory_max']
        D_var = t['D_var']

        color = SOLVENT_COLORS.get(solv, '#888')
        marker = BEAD_MARKERS.get(bead, 'x')
        ms = BEAD_SIZES.get(bead, 50)
        edge = 'black' if ser == 'R' else 'none'
        alpha_v = 0.9 if ser == 'R' else 0.5

        label_key = f"{bead} um, {solv}"
        label = label_key if label_key not in legend_entries else None
        legend_entries.add(label_key)

        ax.scatter(D_th, D_var, c=color, marker=marker, s=ms,
                   edgecolors=edge, linewidths=0.8, alpha=alpha_v,
                   label=label, zorder=3)

    ax.axhline(y=NOISE_FLOOR, color='red', ls='--', lw=0.8, alpha=0.5)
    ax.text(xlim * 0.7, NOISE_FLOOR + 0.004, 'D_noise = 0.018',
            color='red', fontsize=8, alpha=0.7)

    ax.set_xlabel('D_theory (midplane Faxen) [um^2/s]', fontsize=13)
    ax.set_ylabel('D_measured (Variance method) [um^2/s]', fontsize=13)
    ax.set_title(title, fontsize=14)
    ax.set_xlim(-0.01, xlim)
    ax.set_ylim(-0.01, xlim)
    ax.set_aspect('equal')
    ax.legend(fontsize=8, loc='upper left', ncol=2, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    save_fig(fig, output_path)


# ═══════════════════════════════════════════════════════════════════════
# PLOT: Bar chart — D comparison by condition (with Faxen bands)
# ═══════════════════════════════════════════════════════════════════════
def plot_bar_chart(agg_data, output_path, title='Measured D vs Theory',
                   sort_by_theory=True):
    """Bar chart matching the quality of the original plot_overall.py Plot 2."""
    if not agg_data:
        print(f"  SKIP (no data): {output_path}")
        return

    # Sort by descending D_theory
    if sort_by_theory:
        agg_data = sorted(agg_data, key=lambda x: (-x['D_theory_max'], x['bead_um']))

    n = len(agg_data)
    fig, ax = plt.subplots(figsize=(max(14, n * 0.9), 8))

    x = np.arange(n)
    width = 0.18

    # Gray Faxen bands per condition
    for i, d in enumerate(agg_data):
        ax.fill_between([i - 0.4, i + 0.4], d['D_theory_min'], d['D_theory_max'],
                        alpha=0.2, color='gray', zorder=0)

    # 3-method bars with error bars
    ax.bar(x - width,
           [d['D_var_mean'] for d in agg_data], width,
           yerr=[d['D_var_std'] for d in agg_data],
           label='Variance', color='#2196F3', capsize=3, zorder=2)
    ax.bar(x,
           [d['D_gauss_mean'] for d in agg_data], width,
           yerr=[d.get('D_gauss_std', 0) for d in agg_data],
           label='Gaussian', color='#4CAF50', capsize=3, zorder=2)
    ax.bar(x + width,
           [d['D_msd_mean'] for d in agg_data], width,
           label='MSD Slope', color='#FF9800', capsize=3, zorder=2)

    # Theory markers: black _ for D_max (midplane), red _ for D_min (wall)
    ax.scatter(x, [d['D_theory_max'] for d in agg_data], marker='_', s=200,
               color='black', linewidths=2, label='D_max (midplane)', zorder=3)
    ax.scatter(x, [d['D_theory_min'] for d in agg_data], marker='_', s=200,
               color='red', linewidths=2, label='D_min (wall)', zorder=3)

    # X-axis labels
    labels = [f"{d['bead_um']}um\n{d['solvent_label']}\n(n={d['n_trials']})"
              for d in agg_data]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)

    ax.set_ylabel('D [um^2/s]', fontsize=13)
    ax.set_title(f'{title}\nGray band = [D_min(wall), D_max(midplane)]', fontsize=13)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, axis='y', alpha=0.3)

    # Noise floor
    ax.axhline(y=NOISE_FLOOR, color='red', ls='--', lw=0.8, alpha=0.4)
    ax.text(n - 1, NOISE_FLOOR + 0.003, 'noise floor', color='red',
            fontsize=8, alpha=0.6)
    ax.set_ylim(bottom=-0.005)

    fig.tight_layout()
    save_fig(fig, output_path)


# ═══════════════════════════════════════════════════════════════════════
# PLOT: D ratio trends (ratio vs bead size + ratio vs viscosity)
# ═══════════════════════════════════════════════════════════════════════
def plot_ratio_trends(trials, output_path, title_prefix=''):
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 6))

    wall_limit = 0.561 / 0.986

    # LEFT: ratio vs bead size
    for t in trials:
        D_th = t['D_theory_max']
        D_m = t['D_var']
        if D_th < 0.001:
            continue
        ratio = D_m / D_th
        bead = t['bead_um']
        solv = t.get('solvent_label', '?')

        color = SOLVENT_COLORS.get(solv, '#888')
        marker = BEAD_MARKERS.get(bead, 'x')
        ax_a.scatter(bead, ratio, c=color, marker=marker, s=80,
                     edgecolors='black', linewidths=0.5, alpha=0.8, zorder=3)

    ax_a.axhline(y=1.0, color='green', ls='-', lw=1.5, alpha=0.7, label='Perfect match')
    ax_a.axhline(y=wall_limit, color='orange', ls='--', lw=1, alpha=0.7,
                 label=f'Wall Faxen limit ({wall_limit:.2f})')
    ax_a.set_xlabel('Bead Diameter [um]', fontsize=12)
    ax_a.set_ylabel('D_measured / D_theory(midplane)', fontsize=12)
    ax_a.set_title(f'{title_prefix}Ratio vs Bead Size', fontsize=13)
    ax_a.set_xlim(0, 6)
    ax_a.set_ylim(-0.05, 1.6)
    ax_a.grid(True, alpha=0.3)

    # Custom legend with solvents + reference lines
    solv_handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=c,
                           markersize=8, label=s)
                    for s, c in SOLVENT_COLORS.items()
                    if any(t.get('solvent_label') == s for t in trials)]
    ref_handles = [
        Line2D([0], [0], color='green', lw=1.5, label='Perfect match'),
        Line2D([0], [0], color='orange', lw=1, ls='--', label='Wall limit'),
    ]
    ax_a.legend(handles=solv_handles + ref_handles, fontsize=8, loc='upper right')

    # RIGHT: ratio vs viscosity
    for t in trials:
        D_th = t['D_theory_max']
        D_m = t['D_var']
        if D_th < 0.001:
            continue
        ratio = D_m / D_th
        bead = t['bead_um']
        solv = t.get('solvent_label', '?')
        D0 = t['D0']
        if D0 > 0:
            kBT = 1.380649e-23 * 295.15
            r = bead / 2 * 1e-6
            eta = kBT / (6 * 3.14159 * D0 * 1e-12 * r) * 1e3
        else:
            eta = t.get('eta_mPas', 1.0)

        color = SOLVENT_COLORS.get(solv, '#888')
        marker = BEAD_MARKERS.get(bead, 'x')
        ax_b.scatter(eta, ratio, c=color, marker=marker, s=80,
                     edgecolors='black', linewidths=0.5, alpha=0.8, zorder=3)

    ax_b.axhline(y=1.0, color='green', ls='-', lw=1.5, alpha=0.7)
    ax_b.axhline(y=wall_limit, color='orange', ls='--', lw=1, alpha=0.7)
    ax_b.set_xlabel('Viscosity [mPa.s]', fontsize=12)
    ax_b.set_ylabel('D_measured / D_theory(midplane)', fontsize=12)
    ax_b.set_title(f'{title_prefix}Ratio vs Viscosity', fontsize=13)
    ax_b.set_xscale('log')
    ax_b.set_ylim(-0.05, 1.6)
    ax_b.grid(True, alpha=0.3)

    bead_handles = [Line2D([0], [0], marker=m, color='w', markerfacecolor='gray',
                           markersize=8, label=f'{b} um')
                    for b, m in BEAD_MARKERS.items()]
    ax_b.legend(handles=bead_handles, fontsize=9, loc='upper right')

    fig.tight_layout()
    save_fig(fig, output_path)


# ═══════════════════════════════════════════════════════════════════════
# PLOT: 4-panel overview (D vs 1/r, D vs eta, alpha dist, Var vs Gauss)
# ═══════════════════════════════════════════════════════════════════════
def plot_4panel(trials, agg_data, output_path, title='Overall Analysis'):
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # ── Panel A: D vs 1/r ──
    ax = axes[0, 0]
    r_agg = [d for d in agg_data if d.get('series') == 'R']
    for solv_label in ['Water', '20% Gly', '40% Gly', '100% Ace']:
        subset = [d for d in r_agg if d['solvent_label'] == solv_label]
        if not subset:
            continue
        subset.sort(key=lambda d: d['bead_um'])
        inv_r = [2.0 / d['bead_um'] for d in subset]
        d_th = [d['D_theory_max'] for d in subset]
        d_exp = [d['D_var_mean'] for d in subset]
        d_err = [d['D_var_std'] for d in subset]
        color = SOLVENT_COLORS.get(solv_label, '#888')
        ax.plot(inv_r, d_th, '--', color=color, lw=1.5, alpha=0.6)
        ax.errorbar(inv_r, d_exp, yerr=d_err, fmt='o', color=color,
                    capsize=3, markersize=6, label=solv_label, zorder=3)
    ax.set_xlabel('1/r [1/um]', fontsize=11)
    ax.set_ylabel('D [um^2/s]', fontsize=11)
    ax.set_title('(A) D vs 1/radius (Stokes-Einstein: D ~ 1/r)', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Panel B: D vs viscosity (log-log) ──
    ax = axes[0, 1]
    for bead in sorted(BEAD_MARKERS.keys()):
        subset = [d for d in r_agg if d['bead_um'] == bead]
        if not subset:
            continue
        etas = []
        d_th = []
        d_exp = []
        for d in subset:
            D0 = d['D0']
            if D0 > 0:
                kBT = 1.380649e-23 * 295.15
                r = bead / 2 * 1e-6
                eta = kBT / (6 * 3.14159 * D0 * 1e-12 * r) * 1e3
            else:
                eta = 1.0
            etas.append(eta)
            d_th.append(d['D_theory_max'])
            d_exp.append(d['D_var_mean'])
        marker = BEAD_MARKERS.get(bead, 'x')
        ax.plot(etas, d_th, '--', color='gray', lw=1, alpha=0.5)
        ax.scatter(etas, d_exp, marker=marker, s=80, edgecolors='black',
                   linewidths=0.5, label=f'{bead} um', zorder=3)
    ax.set_xlabel('Viscosity [mPa.s]', fontsize=11)
    ax.set_ylabel('D [um^2/s]', fontsize=11)
    ax.set_title('(B) D vs Viscosity (Stokes-Einstein: D ~ 1/eta)', fontsize=12)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, which='both')

    # ── Panel C: Alpha distribution ──
    ax = axes[1, 0]
    alphas_r = [t['alpha'] for t in trials if t.get('series') == 'R' and t.get('alpha', 0) > 0]
    alphas_s = [t['alpha'] for t in trials if t.get('series') == 'S-slide' and t.get('alpha', 0) > 0]
    if alphas_r:
        ax.hist(alphas_r, bins=15, range=(0, 1.8), alpha=0.6, color='#2196F3',
                label=f'R-series (n={len(alphas_r)})', edgecolor='black')
    if alphas_s:
        ax.hist(alphas_s, bins=15, range=(0, 1.8), alpha=0.5, color='#FF9800',
                label=f'S-series (n={len(alphas_s)})', edgecolor='black')
    ax.axvline(x=1.0, color='green', lw=2, ls='-', label='Normal diffusion (a=1)')
    ax.axvspan(0.8, 1.2, alpha=0.1, color='green')
    ax.set_xlabel('MSD Exponent (alpha)', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title('(C) Distribution of MSD Exponent alpha', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Panel D: Variance vs Gaussian ──
    ax = axes[1, 1]
    for t in trials:
        bead = t['bead_um']
        solv = t.get('solvent_label', '?')
        ser = t.get('series', 'R')
        color = SOLVENT_COLORS.get(solv, '#888')
        marker = BEAD_MARKERS.get(bead, 'x')
        edge = 'black' if ser == 'R' else 'none'
        alpha_v = 0.9 if ser == 'R' else 0.4
        ax.scatter(t['D_var'], t['D_gauss'], c=color, marker=marker, s=60,
                   edgecolors=edge, linewidths=0.5, alpha=alpha_v, zorder=3)
    d_line = np.linspace(0, 0.45, 100)
    ax.plot(d_line, d_line, 'k-', lw=1, alpha=0.5, label='1:1')
    ax.set_xlabel('D (Variance) [um^2/s]', fontsize=11)
    ax.set_ylabel('D (Gaussian) [um^2/s]', fontsize=11)
    ax.set_title('(D) Variance vs Gaussian Method Agreement', fontsize=12)
    ax.set_aspect('equal')
    ax.set_xlim(-0.01, 0.45)
    ax.set_ylim(-0.01, 0.45)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    n_trials = len(trials)
    fig.suptitle(f'{title} ({n_trials} trials, R + S series)',
                 fontsize=15, fontweight='bold', y=1.01)
    fig.tight_layout()
    save_fig(fig, output_path)


# ═══════════════════════════════════════════════════════════════════════
# PLOT: All-trials histogram (proper)
# ═══════════════════════════════════════════════════════════════════════
def plot_histograms(trials, output_path, title_suffix=''):
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    fig.suptitle(f'All Trials Histogram{title_suffix}', fontsize=14, fontweight='bold')

    # Panel 1: D_var by bead size
    ax = axes[0, 0]
    for bead in sorted(set(t['bead_um'] for t in trials)):
        vals = [t['D_var'] for t in trials if t['bead_um'] == bead]
        ax.hist(vals, bins=15, alpha=0.5,
                label=f'{bead} um ({len(vals)} trials)',
                edgecolor='black', linewidth=0.5)
    ax.axvline(x=NOISE_FLOOR, color='red', ls='--', lw=1, alpha=0.6)
    ax.set_xlabel('D_var [um^2/s]', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title('D (Variance) by Bead Size')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: D_var by solvent (FIXED: no negative axis)
    ax = axes[0, 1]
    solvent_order = ['Water', '20% Gly', '36% Gly', '40% Gly', '41% Gly',
                     '20% Ace', '40% Ace', '100% Ace']
    for solv in solvent_order:
        vals = [t['D_var'] for t in trials if t.get('solvent_label') == solv]
        if vals:
            color = SOLVENT_COLORS.get(solv, '#888')
            ax.hist(vals, bins=12, alpha=0.5, color=color,
                    label=f'{solv} ({len(vals)})',
                    edgecolor='black', linewidth=0.5)
    ax.axvline(x=NOISE_FLOOR, color='red', ls='--', lw=1, alpha=0.6)
    ax.set_xlabel('D_var [um^2/s]', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title('D (Variance) by Solvent')
    ax.legend(fontsize=8)
    ax.set_xlim(left=0)  # FORCE non-negative x-axis
    ax.grid(True, alpha=0.3)

    # Panel 3: alpha distribution
    ax = axes[1, 0]
    alphas = [t['alpha'] for t in trials if t.get('alpha', 0) > 0]
    ax.hist(alphas, bins=20, range=(0, 1.8), color='#607D8B', alpha=0.7,
            edgecolor='black', linewidth=0.5)
    ax.axvline(x=1.0, color='red', ls='--', lw=2, label='alpha=1 (Brownian)')
    ax.axvspan(0.8, 1.2, alpha=0.1, color='green')
    ax.set_xlabel('MSD Exponent (alpha)', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title(f'MSD Exponent Distribution (N={len(alphas)})')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Panel 4: Ratio bar chart per condition
    ax = axes[1, 1]
    # Group by condition and compute ratio
    cond_data = defaultdict(list)
    for t in trials:
        D_max = t['D_theory_max']
        if D_max > 0.001:
            ratio = t['D_var'] / D_max
            key = (t['bead_um'], t.get('solvent_label', '?'))
            cond_data[key].append(ratio)

    cond_keys = sorted(cond_data.keys(), key=lambda k: (-k[0], k[1]))
    # Sort so same bead sizes group together, descending
    cond_keys = sorted(cond_data.keys(), key=lambda k: (k[0], k[1]))

    x_pos = np.arange(len(cond_keys))
    means = [statistics.mean(cond_data[k]) for k in cond_keys]
    stds = [statistics.stdev(cond_data[k]) if len(cond_data[k]) > 1 else 0
            for k in cond_keys]
    colors = [SOLVENT_COLORS.get(k[1], '#888') for k in cond_keys]
    labels_x = [f"{k[0]}um\n{k[1]}" for k in cond_keys]

    ax.bar(x_pos, means, yerr=stds, capsize=3, color=colors, alpha=0.8,
           edgecolor='white', linewidth=0.5)
    ax.axhline(y=1.0, color='green', ls='--', lw=2, label='Perfect match')
    ax.axhline(y=0.561 / 0.986, color='red', ls=':', lw=1.5,
               label=f'Max wall (F~0.57)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels_x, fontsize=7, rotation=45, ha='right')
    ax.set_ylabel('D_var / D_theory_max', fontsize=11)
    ax.set_title('Theory Agreement Ratio by Condition')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    save_fig(fig, output_path)


# ═══════════════════════════════════════════════════════════════════════
# PLOT: Comprehensive 6-panel overview (heatmap)
# ═══════════════════════════════════════════════════════════════════════
def plot_6panel_overview(trials, agg_data, output_path):
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    n_total = len(trials)
    n_solvents = len(set(t.get('solvent_label', '?') for t in trials))
    n_beads = len(set(t['bead_um'] for t in trials))
    fig.suptitle(f'OVERALL LAB: Brownian Motion Diffusion Analysis\n'
                 f'Total: {n_total} trials across {n_solvents} solvents '
                 f'and {n_beads} bead sizes',
                 fontsize=14, fontweight='bold')

    # Panel (0,0): D scatter
    ax = axes[0, 0]
    for t in trials:
        D_th = t['D_theory_max']
        D_m = t['D_var']
        marker = BEAD_MARKERS.get(t['bead_um'], 'o')
        color = SOLVENT_COLORS.get(t.get('solvent_label', ''), '#666')
        edge = 'black' if t.get('series') == 'R' else 'gray'
        ax.plot(D_th, D_m, marker=marker, color=color, markersize=7,
                markeredgecolor=edge, markeredgewidth=0.6, alpha=0.8)
    mx = 0.50
    ax.plot([0, mx], [0, mx], 'k-', lw=1, alpha=0.5)
    ax.fill_between([0, mx], [0, 0], [0, mx * 0.561 / 0.986],
                    alpha=0.1, color='gray')
    ax.set_xlabel('D_theory [um^2/s]', fontsize=10)
    ax.set_ylabel('D_measured [um^2/s]', fontsize=10)
    ax.set_title('Measured vs Theory (1:1)')
    ax.set_xlim(-0.01, mx)
    ax.set_ylim(-0.01, mx)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Panel (0,1): D vs 1/r
    ax = axes[0, 1]
    r_agg = [d for d in agg_data if d.get('series') == 'R']
    for solv in ['Water', '20% Gly', '40% Gly', '100% Ace']:
        subset = sorted([d for d in r_agg if d['solvent_label'] == solv],
                       key=lambda d: d['bead_um'])
        if not subset:
            continue
        inv_r = [2.0 / d['bead_um'] for d in subset]
        d_exp = [d['D_var_mean'] for d in subset]
        d_th = [d['D_theory_max'] for d in subset]
        color = SOLVENT_COLORS.get(solv, '#888')
        ax.plot(inv_r, d_th, '--', color=color, lw=1, alpha=0.5)
        ax.plot(inv_r, d_exp, 'o-', color=color, label=solv, markersize=6)
    ax.set_xlabel('1/r [1/um]', fontsize=10)
    ax.set_ylabel('D [um^2/s]', fontsize=10)
    ax.set_title('D vs 1/r (Stokes-Einstein)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Panel (0,2): D vs eta
    ax = axes[0, 2]
    for bead in sorted(BEAD_MARKERS.keys()):
        subset = sorted([d for d in r_agg if d['bead_um'] == bead],
                       key=lambda d: d['D0'])
        if not subset:
            continue
        etas = []
        d_exp = []
        for d in subset:
            D0 = d['D0']
            if D0 > 0:
                kBT = 1.380649e-23 * 295.15
                r = bead / 2 * 1e-6
                eta = kBT / (6 * 3.14159 * D0 * 1e-12 * r) * 1e3
            else:
                eta = 1.0
            etas.append(eta)
            d_exp.append(d['D_var_mean'])
        marker = BEAD_MARKERS.get(bead, 'o')
        ax.plot(etas, d_exp, marker=marker, ls='-', label=f'{bead} um', markersize=7)
    ax.set_xlabel('Viscosity [mPa.s]', fontsize=10)
    ax.set_ylabel('D [um^2/s]', fontsize=10)
    ax.set_title('D vs Viscosity (D ~ 1/eta)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel (1,0): alpha histogram
    ax = axes[1, 0]
    alphas_r = [t['alpha'] for t in trials if t.get('series') == 'R' and t.get('alpha', 0) > 0]
    alphas_s = [t['alpha'] for t in trials if t.get('series') == 'S-slide' and t.get('alpha', 0) > 0]
    if alphas_r:
        ax.hist(alphas_r, bins=15, range=(0, 1.8), alpha=0.6, color='#2196F3',
                label=f'R-series (N={len(alphas_r)})', edgecolor='black')
    if alphas_s:
        ax.hist(alphas_s, bins=12, range=(0, 1.8), alpha=0.6, color='#FF9800',
                label=f'S-series (N={len(alphas_s)})', edgecolor='black')
    ax.axvline(x=1.0, color='red', ls='--', lw=2, label='alpha=1')
    ax.axvspan(0.8, 1.2, alpha=0.1, color='green')
    ax.set_xlabel('MSD Exponent (alpha)', fontsize=10)
    ax.set_ylabel('Count', fontsize=10)
    ax.set_title('MSD Exponent Distribution')
    ax.legend(fontsize=8)

    # Panel (1,1): D histogram by solvent
    ax = axes[1, 1]
    for solv in ['Water', '20% Gly', '40% Gly', '100% Ace', '20% Ace', '40% Ace', '36% Gly']:
        vals = [t['D_var'] for t in trials if t.get('solvent_label') == solv]
        if vals:
            color = SOLVENT_COLORS.get(solv, '#666')
            ax.hist(vals, bins=10, alpha=0.5, color=color,
                    label=f'{solv} ({len(vals)})', edgecolor='black', linewidth=0.5)
    ax.set_xlabel('D_var [um^2/s]', fontsize=10)
    ax.set_ylabel('Count', fontsize=10)
    ax.set_title('D Distribution by Solvent')
    ax.set_xlim(left=0)
    ax.legend(fontsize=7)

    # Panel (1,2): Ratio heatmap
    ax = axes[1, 2]
    all_beads = sorted(set(t['bead_um'] for t in trials))
    all_solvents_set = set(t.get('solvent_label', '?') for t in trials)
    solvent_order_map = {'Water': 0, '20% Gly': 1, '20% Ace': 2, '36% Gly': 3,
                         '40% Gly': 4, '41% Gly': 4, '40% Ace': 5, '100% Ace': 6}
    all_solvents = sorted(all_solvents_set, key=lambda s: solvent_order_map.get(s, 99))

    ratio_matrix = np.full((len(all_beads), len(all_solvents)), np.nan)
    for i, bead in enumerate(all_beads):
        for j, solv in enumerate(all_solvents):
            subset = [t for t in trials
                      if t['bead_um'] == bead and t.get('solvent_label') == solv]
            if subset:
                D_vars = [t['D_var'] for t in subset]
                D_maxs = [t['D_theory_max'] for t in subset]
                mean_max = statistics.mean(D_maxs)
                if mean_max > 0.001:
                    ratio_matrix[i, j] = statistics.mean(D_vars) / mean_max

    im = ax.imshow(ratio_matrix, cmap='RdYlGn', vmin=0, vmax=1.2, aspect='auto')
    ax.set_xticks(range(len(all_solvents)))
    ax.set_xticklabels(all_solvents, fontsize=8, rotation=45, ha='right')
    ax.set_yticks(range(len(all_beads)))
    ax.set_yticklabels([f'{b} um' for b in all_beads], fontsize=9)
    ax.set_title('Ratio D_var/D_theory (1.0 = match)')

    for i in range(len(all_beads)):
        for j in range(len(all_solvents)):
            val = ratio_matrix[i, j]
            if not np.isnan(val):
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=10, fontweight='bold',
                        color='white' if val < 0.3 else 'black')

    fig.colorbar(im, ax=ax, shrink=0.8, label='Ratio')

    plt.tight_layout()
    save_fig(fig, output_path)


# ═══════════════════════════════════════════════════════════════════════
# MAIN: Load data and generate all plots
# ═══════════════════════════════════════════════════════════════════════
print("=" * 80)
print("Generating plots for 2026-03-07 reorganised data")
print("=" * 80)

# Load overall data
overall_csv = os.path.join(OVERALL_DIR, 'overall_data_summary.csv')
all_trials = load_trial_csv(overall_csv)
all_agg = aggregate_trials(all_trials)
print(f"\nLoaded {len(all_trials)} trials, {len(all_agg)} aggregated conditions")

# Split by series
r_trials = [t for t in all_trials if t.get('series') == 'R']
s_trials = [t for t in all_trials if t.get('series') == 'S-slide']
r_agg = [a for a in all_agg if a.get('series') == 'R']
s_agg = [a for a in all_agg if a.get('series') == 'S-slide']
print(f"  R-series: {len(r_trials)} trials, {len(r_agg)} conditions")
print(f"  S-series: {len(s_trials)} trials, {len(s_agg)} conditions")

# ── Overall Lab plots ──
print(f"\n--- Overall Lab ---")
plot_scatter_1to1(all_trials,
    os.path.join(OVERALL_DIR, 'D_measured_vs_theory_overall.png'),
    'Measured vs Theoretical Diffusion Coefficient\nAll Conditions (R + S series)')

plot_bar_chart(all_agg,
    os.path.join(OVERALL_DIR, 'D_bar_comparison_all.png'),
    'All Conditions: Measured D (3 methods) vs Theory (Nathan Faxen range)')

plot_bar_chart(r_agg,
    os.path.join(OVERALL_DIR, 'D_bar_comparison_R_series.png'),
    'R-Series: Measured D (3 methods) vs Theory (Nathan Faxen range)')

plot_ratio_trends(all_trials,
    os.path.join(OVERALL_DIR, 'D_ratio_trends.png'),
    'All Data: ')

plot_histograms(all_trials,
    os.path.join(OVERALL_DIR, 'all_trials_histogram.png'),
    ' (All Data)')

plot_4panel(all_trials, all_agg,
    os.path.join(OVERALL_DIR, 'overall_4panel.png'),
    'Overall Analysis: 2026-03-05 Batch')

plot_6panel_overview(all_trials, all_agg,
    os.path.join(OVERALL_DIR, 'overall_6panel.png'))

# ── R-series plots ──
print(f"\n--- R-series ---")
plot_scatter_1to1(r_trials,
    os.path.join(R_SESSION, 'r_series_D_vs_theory.png'),
    'R-Series: Measured vs Theory\n(Sessions 7-8, March 3)')

plot_bar_chart(r_agg,
    os.path.join(R_SESSION, 'r_series_bar_comparison.png'),
    'R-Series: Measured D (3 methods) vs Theory (Nathan Faxen range)')

plot_ratio_trends(r_trials,
    os.path.join(R_SESSION, 'r_series_ratio_trends.png'),
    'R-Series: ')

plot_histograms(r_trials,
    os.path.join(R_SESSION, 'r_series_histogram.png'),
    ' (R-Series)')

# ── S-series plots ──
print(f"\n--- S-series ---")
plot_scatter_1to1(s_trials,
    os.path.join(S_SESSION, 's_series_D_vs_theory.png'),
    'S-Series: Measured vs Theory\n(Sessions 5-6, Feb 26)',
    xlim=0.40)

plot_bar_chart(s_agg,
    os.path.join(S_SESSION, 's_series_bar_comparison.png'),
    'S-Series: Measured D (3 methods) vs Theory (Nathan Faxen range)')

plot_ratio_trends(s_trials,
    os.path.join(S_SESSION, 's_series_ratio_trends.png'),
    'S-Series: ')

plot_histograms(s_trials,
    os.path.join(S_SESSION, 's_series_histogram.png'),
    ' (S-Series)')

plt.close('all')
print(f"\n{'=' * 80}")
print("All plots generated successfully!")
print(f"{'=' * 80}")
