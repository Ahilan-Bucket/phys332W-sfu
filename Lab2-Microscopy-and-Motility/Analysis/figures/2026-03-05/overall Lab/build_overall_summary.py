"""
Build comprehensive summary of ALL diffusion data from 2026-03-05.
Uses Nathan's exact Faxen correction factors.
Outputs: CSV, summary text, comparison plots.
"""
import os
import re
import csv
import math
import sys

# Add analysis dir to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
sys.path.insert(0, ANALYSIS_DIR)
import diffusion_calculator as dc

# ── Nathan's Faxen Correction Factors ──────────────────────────────────
# Min Wall = midplane (best case), Max Wall = touching wall (worst case)
# Grouped by bead size: 1µm, 2.1µm, 3µm, 5µm (same for all solvents)
NATHAN_FAXEN = {
    1.0:  (0.986, 0.561),
    2.0:  (0.971, 0.560),  # Nathan uses 2.0, our beads are 2.1
    2.1:  (0.971, 0.560),
    3.0:  (0.959, 0.559),
    5.0:  (0.932, 0.557),
}

# ── Map conditions to Nathan's sample IDs ──────────────────────────────
# Nathan's ordering: S1-S4 = 1µm (ace,water,20gly,40gly)
#                    S5-S8 = 2µm, S9-S12 = 3µm, S13-S16 = 5µm
def get_nathan_id(bead_um, solvent, pct):
    """Map (bead, solvent, pct) to Nathan's S1-S16 ID."""
    bead_key = round(bead_um)  # 2.1 -> 2
    if bead_key == 2:
        bead_key = 2
    base = {1: 0, 2: 4, 3: 8, 5: 12}[bead_key]
    if 'acetone' in solvent.lower() or 'ace' in solvent.lower():
        offset = 1
    elif pct == 0 or 'water' in solvent.lower():
        offset = 2
    elif pct <= 25:
        offset = 3
    elif pct <= 45:
        offset = 4
    else:
        offset = 2  # fallback
    return f"S{base + offset}"


# ── Parse a summary.txt file ──────────────────────────────────────────
def parse_summary(filepath):
    """Extract key values from a summary.txt file."""
    result = {}
    try:
        with open(filepath, 'r') as f:
            text = f.read()
    except:
        return None

    # Bead diameter
    m = re.search(r'Bead diameter:\s*([\d.]+)\s*um', text)
    if m:
        result['bead_um'] = float(m.group(1))
    else:
        return None

    # Solute
    m = re.search(r'Solute:\s*([\d.]+)%\s*(\w+)', text)
    if m:
        result['solute_pct'] = float(m.group(1))
        result['solvent'] = m.group(2)
    else:
        result['solute_pct'] = 0
        result['solvent'] = 'Water'

    # Viscosity
    m = re.search(r'Viscosity.*?:\s*([\d.]+)\s*mPa', text)
    if m:
        result['eta_mPas'] = float(m.group(1))

    # Number of segments/particles
    m = re.search(r'segments?.*?:\s*(\d+)', text, re.IGNORECASE)
    if m:
        result['n_segments'] = int(m.group(1))

    m = re.search(r'displacement steps.*?:\s*(\d+)', text, re.IGNORECASE)
    if m:
        result['n_steps'] = int(m.group(1))

    # Noise-corrected D values (preferred)
    m = re.search(r'Direct Variance:\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
    if m:
        result['D_var'] = float(m.group(1))
        result['D_var_err'] = float(m.group(2))
    else:
        # Try older format
        m = re.search(r'Method 1 \(Direct Variance\):\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
        if m:
            result['D_var'] = float(m.group(1))
            result['D_var_err'] = float(m.group(2))

    m = re.search(r'Gaussian Fit:\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
    if m:
        result['D_gauss'] = float(m.group(1))
        result['D_gauss_err'] = float(m.group(2))
    else:
        m = re.search(r'Method 2 \(Gaussian Fit\):\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
        if m:
            result['D_gauss'] = float(m.group(1))
            result['D_gauss_err'] = float(m.group(2))

    # Raw D values (before noise subtraction)
    m = re.search(r'Variance:\s*([\d.]+)\s+Gauss:\s*([\d.]+)\s+MSD:\s*([\d.]+)', text)
    if m:
        result['D_var_raw'] = float(m.group(1))
        result['D_gauss_raw'] = float(m.group(2))
        result['D_msd_raw'] = float(m.group(3))

    # MSD slope D
    m = re.search(r'MSD Slope:\s*([\d.]+)', text)
    if m:
        result['D_msd'] = float(m.group(1))
    elif 'D_msd_raw' in result:
        result['D_msd'] = max(0, result['D_msd_raw'] - 0.0180)  # manual noise subtract

    # D_theory values from the summary
    m = re.search(r'D_0 \((?:uncorrected|base)\):\s*([\d.]+)', text)
    if m:
        result['D0_file'] = float(m.group(1))

    m = re.search(r'D_mid:\s*([\d.]+)', text)
    if m:
        result['D_mid_file'] = float(m.group(1))

    # Alpha
    m = re.search(r'alpha\s*=\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
    if m:
        result['alpha'] = float(m.group(1))
        result['alpha_err'] = float(m.group(2))

    # Classification
    m = re.search(r'\((Sub-diffusive|Normal diffusion|Super-diffusive)\)', text)
    if m:
        result['classification'] = m.group(1)

    return result


# ── Scan all directories ──────────────────────────────────────────────
BASE = os.path.join(os.path.dirname(__file__), '..')
all_data = []

for dirname in sorted(os.listdir(BASE)):
    dirpath = os.path.join(BASE, dirname)
    summary_path = os.path.join(dirpath, 'summary.txt')

    if not os.path.isfile(summary_path):
        continue

    # Only R-series and S-series tracker results
    if not (dirname.startswith('r') or dirname.startswith('s')):
        continue
    if 'Calibration' in dirname or '2026-03-05' in dirname:
        continue

    data = parse_summary(summary_path)
    if data is None:
        continue

    # Extract trial info from dirname
    data['dirname'] = dirname

    # Extract series (r or s)
    if dirname.startswith('r'):
        m = re.match(r'r(\d+)', dirname)
        if m:
            data['condition_id'] = f"R{m.group(1)}"
            data['series'] = 'R'
    elif dirname.startswith('s'):
        m = re.match(r's(\d+)', dirname)
        if m:
            data['condition_id'] = f"S{m.group(1)}"
            data['series'] = 'S-slide'

    # Extract trial number
    m = re.search(r'trial(\d+)', dirname)
    data['trial'] = int(m.group(1)) if m else 1

    # Get Nathan's Faxen factors for this bead size
    bead = data['bead_um']
    f_min, f_max = NATHAN_FAXEN.get(bead, NATHAN_FAXEN.get(round(bead), (0.96, 0.56)))
    data['F_min_wall'] = f_min  # midplane, best case
    data['F_max_wall'] = f_max  # touching wall, worst case

    # Compute D_theory using Nathan's Faxen
    if 'D0_file' in data:
        D0 = data['D0_file']
    else:
        D0 = data.get('D_mid_file', 0) / f_min  # back-calculate D0

    data['D0'] = D0
    data['D_theory_max'] = D0 * f_min  # best case (midplane)
    data['D_theory_min'] = D0 * f_max  # worst case (touching wall)

    # Solvent label for plotting
    pct = data.get('solute_pct', 0)
    solv = data.get('solvent', 'Water')
    if pct == 0 or 'water' in solv.lower():
        data['solvent_label'] = 'Water'
    elif 'glycerol' in solv.lower() or 'gly' in solv.lower():
        data['solvent_label'] = f'{pct:.0f}% Gly'
    elif 'acetone' in solv.lower() or 'ace' in solv.lower():
        data['solvent_label'] = f'{pct:.0f}% Ace'
    else:
        data['solvent_label'] = solv

    all_data.append(data)

print(f"Found {len(all_data)} trial summaries")

# ── Write CSV ──────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.dirname(__file__)
csv_path = os.path.join(OUTPUT_DIR, 'overall_data_summary.csv')

fields = [
    'condition_id', 'series', 'trial', 'bead_um', 'solvent_label', 'solute_pct',
    'eta_mPas', 'n_segments', 'n_steps',
    'D_var', 'D_var_err', 'D_gauss', 'D_gauss_err', 'D_msd',
    'D_var_raw', 'D_gauss_raw', 'D_msd_raw',
    'D0', 'F_min_wall', 'F_max_wall', 'D_theory_max', 'D_theory_min',
    'alpha', 'alpha_err', 'classification',
    'dirname'
]

with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    for row in sorted(all_data, key=lambda x: (x.get('series',''), x.get('bead_um',0), x.get('solvent_label',''), x.get('trial',1))):
        writer.writerow(row)

print(f"CSV written: {csv_path}")

# ── Write Summary Text ────────────────────────────────────────────────
txt_path = os.path.join(OUTPUT_DIR, 'overall_summary.txt')

with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("=" * 120 + "\n")
    f.write("OVERALL DATA SUMMARY — 2026-03-05 Batch Analysis\n")
    f.write("All R-series (Sessions 7-8) and S-series (Sessions 5-6) Tracker Results\n")
    f.write("=" * 120 + "\n\n")

    f.write(f"Total trials analysed: {len(all_data)}\n")
    r_count = sum(1 for d in all_data if d.get('series') == 'R')
    s_count = sum(1 for d in all_data if d.get('series') == 'S-slide')
    f.write(f"  R-series (Sessions 7-8): {r_count} trials\n")
    f.write(f"  S-series (Sessions 5-6): {s_count} trials\n\n")

    f.write("Nathan's Faxen Correction Factors:\n")
    f.write("  Bead    F_min (midplane)   F_max (touching wall)\n")
    for bead in [1.0, 2.1, 3.0, 5.0]:
        fm, fx = NATHAN_FAXEN[bead]
        f.write(f"  {bead:4.1f} µm     {fm:.3f}              {fx:.3f}\n")
    f.write("\n")
    f.write("D_theory range: D_min = D0 × F_max (worst, near wall) to D_max = D0 × F_min (best, midplane)\n\n")

    # Detailed per-condition table
    f.write("-" * 140 + "\n")
    header = f"{'ID':<6} {'Trial':>5} {'Bead':>5} {'Solvent':<10} {'Series':<7} {'D_var':>7} {'±':>5} {'D_gauss':>7} {'±':>5} {'D_msd':>7} {'D0':>7} {'D_max':>7} {'D_min':>7} {'Ratio':>6} {'α':>6} {'Class':<15}"
    f.write(header + "\n")
    f.write("-" * 140 + "\n")

    prev_cond = None
    for row in sorted(all_data, key=lambda x: (
        x.get('series',''),
        {'Water':0, '20% Gly':1, '20% Ace':2, '36% Gly':3, '40% Gly':4, '40% Ace':5, '100% Ace':6, '100% Gly':7}.get(x.get('solvent_label',''), 99),
        x.get('bead_um',0),
        x.get('trial',1)
    )):
        cond = (row.get('series',''), row.get('solvent_label',''), row.get('bead_um',0))
        if prev_cond and cond != prev_cond:
            f.write("\n")  # blank line between conditions
        prev_cond = cond

        D_var = row.get('D_var', 0)
        D_var_err = row.get('D_var_err', 0)
        D_gauss = row.get('D_gauss', 0)
        D_gauss_err = row.get('D_gauss_err', 0)
        D_msd = row.get('D_msd', 0)
        D0 = row.get('D0', 0)
        D_max = row.get('D_theory_max', 0)
        D_min = row.get('D_theory_min', 0)
        alpha = row.get('alpha', 0)

        # Ratio: D_var / D_theory_max (midplane prediction)
        ratio = D_var / D_max if D_max > 0 else 0

        line = f"{row.get('condition_id','?'):<6} {row.get('trial',1):>5} {row.get('bead_um',0):>5.1f} {row.get('solvent_label','?'):<10} {row.get('series','?'):<7} "
        line += f"{D_var:>7.4f} {D_var_err:>5.4f} {D_gauss:>7.4f} {D_gauss_err:>5.4f} {D_msd:>7.4f} "
        line += f"{D0:>7.4f} {D_max:>7.4f} {D_min:>7.4f} {ratio:>6.2f} {alpha:>6.3f} {row.get('classification','?'):<15}"
        f.write(line + "\n")

    f.write("\n" + "=" * 120 + "\n")
    f.write("KEY: D_var = Direct Variance, D_gauss = Gaussian Fit, D_msd = MSD Slope (all noise-corrected, µm²/s)\n")
    f.write("     D0 = Stokes-Einstein (no wall), D_max = D0×F_min (midplane), D_min = D0×F_max (touching wall)\n")
    f.write("     Ratio = D_var / D_max,  α = MSD exponent (1.0 = normal Brownian)\n")
    f.write("     All D values in µm²/s. Noise floor: D_noise = 0.0180 µm²/s\n")

print(f"Summary written: {txt_path}")

# ── Build aggregated condition-level data for plotting ─────────────────
from collections import defaultdict
import statistics

# Group by (bead, solvent_label, series)
groups = defaultdict(list)
for row in all_data:
    key = (row['bead_um'], row['solvent_label'], row.get('series', '?'))
    groups[key].append(row)

agg_path = os.path.join(OUTPUT_DIR, 'overall_aggregated.csv')
agg_fields = [
    'bead_um', 'solvent_label', 'series', 'n_trials',
    'D_var_mean', 'D_var_std', 'D_gauss_mean', 'D_gauss_std', 'D_msd_mean',
    'D0', 'D_theory_max', 'D_theory_min',
    'ratio_var', 'ratio_gauss',
    'alpha_mean', 'alpha_std',
    'in_theory_range'
]

agg_rows = []
for key in sorted(groups.keys(), key=lambda k: (k[2], k[0], k[1])):
    rows = groups[key]
    bead, solvent, series = key

    d_vars = [r.get('D_var', 0) for r in rows]
    d_gauss = [r.get('D_gauss', 0) for r in rows]
    d_msds = [r.get('D_msd', 0) for r in rows if 'D_msd' in r]
    alphas = [r.get('alpha', 0) for r in rows if 'alpha' in r]

    D0 = rows[0].get('D0', 0)
    D_max = rows[0].get('D_theory_max', 0)
    D_min = rows[0].get('D_theory_min', 0)

    d_var_mean = statistics.mean(d_vars)
    d_gauss_mean = statistics.mean(d_gauss)
    d_msd_mean = statistics.mean(d_msds) if d_msds else 0

    d_var_std = statistics.stdev(d_vars) if len(d_vars) > 1 else 0
    d_gauss_std = statistics.stdev(d_gauss) if len(d_gauss) > 1 else 0
    alpha_mean = statistics.mean(alphas) if alphas else 0
    alpha_std = statistics.stdev(alphas) if len(alphas) > 1 else 0

    ratio_var = d_var_mean / D_max if D_max > 0 else 0
    ratio_gauss = d_gauss_mean / D_max if D_max > 0 else 0

    # Check if measured D falls within theory range [D_min, D_max]
    in_range = D_min <= d_var_mean <= D_max

    agg_rows.append({
        'bead_um': bead, 'solvent_label': solvent, 'series': series,
        'n_trials': len(rows),
        'D_var_mean': d_var_mean, 'D_var_std': d_var_std,
        'D_gauss_mean': d_gauss_mean, 'D_gauss_std': d_gauss_std,
        'D_msd_mean': d_msd_mean,
        'D0': D0, 'D_theory_max': D_max, 'D_theory_min': D_min,
        'ratio_var': ratio_var, 'ratio_gauss': ratio_gauss,
        'alpha_mean': alpha_mean, 'alpha_std': alpha_std,
        'in_theory_range': 'YES' if in_range else 'no'
    })

with open(agg_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=agg_fields)
    writer.writeheader()
    for row in agg_rows:
        writer.writerow(row)

print(f"Aggregated CSV written: {agg_path}")

# Print aggregated table to console
print("\n" + "=" * 130)
print(f"{'Bead':>5} {'Solvent':<10} {'Ser':>4} {'N':>2} {'D_var':>7} {'err':>5} {'D_gauss':>7} {'D_msd':>7} | {'D0':>7} {'D_max':>7} {'D_min':>7} | {'Ratio':>6} {'alpha':>6} {'InRange':>7}")
print("=" * 130)
for row in agg_rows:
    print(f"{row['bead_um']:>5.1f} {row['solvent_label']:<10} {row['series']:>4} {row['n_trials']:>2} "
          f"{row['D_var_mean']:>7.4f} {row['D_var_std']:>5.4f} {row['D_gauss_mean']:>7.4f} {row['D_msd_mean']:>7.4f} | "
          f"{row['D0']:>7.4f} {row['D_theory_max']:>7.4f} {row['D_theory_min']:>7.4f} | "
          f"{row['ratio_var']:>6.2f} {row['alpha_mean']:>6.3f} {row['in_theory_range']:>7}")
print("=" * 130)
