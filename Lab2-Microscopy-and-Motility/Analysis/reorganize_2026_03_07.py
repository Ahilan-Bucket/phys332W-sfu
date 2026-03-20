"""
Reorganize all analysis from figures/2026-03-05 into figures/2026-03-07
with proper S-series / R-series / Overall Lab structure.

Structure created:
  figures/2026-03-07/
  ├── S-series (Feb 26)/
  │   ├── <per-dataset folders>/
  │   │   ├── *.png, summary.txt, readme.txt, trackresults.txt
  │   │   └── presentation plots/  (*.pdf)
  │   └── overall session/
  │       ├── s_series_data.csv
  │       ├── s_series_summary.txt
  │       └── s_series_*.png
  ├── R-series (March 3)/
  │   ├── <per-dataset folders>/
  │   │   ├── *.png, summary.txt, readme.txt, trackresults.txt
  │   │   └── presentation plots/  (*.pdf)
  │   └── overall session/
  │       ├── r_series_data.csv
  │       ├── r_series_summary.txt
  │       └── r_series_*.png
  ├── Calibration/
  │   └── noise files
  └── Overall Lab/
      ├── overall_data_summary.csv
      ├── overall_aggregated.csv
      ├── overall_summary.txt
      └── *.png (comparison plots, histograms)
"""

import os
import re
import csv
import shutil
import sys
import math
from collections import defaultdict
import statistics

# ── Paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(SCRIPT_DIR, 'figures', '2026-03-05')
TARGET_DIR = os.path.join(SCRIPT_DIR, 'figures', '2026-03-07')

S_SERIES_DIR = os.path.join(TARGET_DIR, 'S-series (Feb 26)')
R_SERIES_DIR = os.path.join(TARGET_DIR, 'R-series (March 3)')
CALIBRATION_DIR = os.path.join(TARGET_DIR, 'Calibration')
OVERALL_DIR = os.path.join(TARGET_DIR, 'Overall Lab')

# Add analysis dir to path for diffusion_calculator
sys.path.insert(0, SCRIPT_DIR)
import diffusion_calculator as dc

# ── Nathan's Faxen Correction Factors ──────────────────────────────────
NATHAN_FAXEN = {
    1.0:  (0.986, 0.561),
    2.0:  (0.971, 0.560),
    2.1:  (0.971, 0.560),
    3.0:  (0.959, 0.559),
    5.0:  (0.932, 0.557),
}

# ── Nathan's 4x4 condition matrix ──────────────────────────────────────
# Maps R-slide condition IDs to descriptions
NATHAN_MATRIX = {
    'R1':  '1.0 um, Water',       'R2':  '2.1 um, Water',
    'R3':  '3.0 um, Water',       'R4':  '5.0 um, Water',
    'R5':  '1.0 um, 20% Gly',     'R6':  '2.1 um, 20% Gly',
    'R7':  '3.0 um, 20% Gly',     'R8':  '5.0 um, 20% Gly',
    'R9':  '1.0 um, 40% Gly',     'R10': '2.1 um, 40% Gly',
    'R11': '3.0 um, 40% Gly',     'R12': '5.0 um, 40% Gly',
    'R13': '1.0 um, Acetone',     'R14': '2.1 um, Acetone',
    'R15': '3.0 um, Acetone',     'R16': '5.0 um, Acetone',
}


def parse_summary(filepath):
    """Extract key values from a summary.txt file."""
    result = {}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
    except Exception:
        return None

    m = re.search(r'Bead diameter:\s*([\d.]+)\s*um', text)
    if m:
        result['bead_um'] = float(m.group(1))
    else:
        return None

    m = re.search(r'Solute:\s*([\d.]+)%\s*(\w+)', text)
    if m:
        result['solute_pct'] = float(m.group(1))
        result['solvent'] = m.group(2)
    else:
        result['solute_pct'] = 0
        result['solvent'] = 'Water'

    m = re.search(r'Viscosity.*?:\s*([\d.]+)\s*mPa', text)
    if m:
        result['eta_mPas'] = float(m.group(1))

    m = re.search(r'Temperature:\s*([\d.]+)\s*C', text)
    if m:
        result['temp_C'] = float(m.group(1))

    m = re.search(r'(\d+)\s*frames?,\s*(\d+)\s*particles?,\s*(\d+)\s*segments?,\s*(\d+)\s*steps', text)
    if m:
        result['n_frames'] = int(m.group(1))
        result['n_particles'] = int(m.group(2))
        result['n_segments'] = int(m.group(3))
        result['n_steps'] = int(m.group(4))

    # Noise-corrected D values
    m = re.search(r'Direct Variance:\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
    if m:
        result['D_var'] = float(m.group(1))
        result['D_var_err'] = float(m.group(2))

    m = re.search(r'Gaussian Fit:\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
    if m:
        result['D_gauss'] = float(m.group(1))
        result['D_gauss_err'] = float(m.group(2))

    m = re.search(r'MSD Slope:\s*([\d.]+)', text)
    if m:
        result['D_msd'] = float(m.group(1))

    # Raw D values
    m = re.search(r'Variance:\s*([\d.]+)\s+Gauss:\s*([\d.]+)\s+MSD:\s*([\d.]+)', text)
    if m:
        result['D_var_raw'] = float(m.group(1))
        result['D_gauss_raw'] = float(m.group(2))
        result['D_msd_raw'] = float(m.group(3))

    # D0 from file
    m = re.search(r'D_0 \((?:uncorrected|base)\):\s*([\d.]+)', text)
    if m:
        result['D0_file'] = float(m.group(1))

    # Alpha
    m = re.search(r'alpha\s*=\s*([\d.]+)\s*\+/-\s*([\d.]+)', text)
    if m:
        result['alpha'] = float(m.group(1))
        result['alpha_err'] = float(m.group(2))

    # Classification
    m = re.search(r'\((Sub-diffusive|Normal diffusion|Super-diffusive)\)', text)
    if m:
        result['classification'] = m.group(1)

    # Pixel size and frame rate
    m = re.search(r'Pixel size:\s*([\d.]+)\s*um/px', text)
    if m:
        result['pixel_size'] = float(m.group(1))

    m = re.search(r'Frame rate:\s*([\d.]+)\s*fps', text)
    if m:
        result['fps'] = float(m.group(1))

    return result


def get_solvent_label(solute_pct, solvent):
    """Convert solute info to a clean label."""
    pct = solute_pct
    solv = solvent.lower() if solvent else 'water'
    if pct == 0 or 'water' in solv:
        return 'Water'
    elif 'glycerol' in solv or 'gly' in solv:
        return f'{pct:.0f}% Gly'
    elif 'acetone' in solv or 'ace' in solv:
        return f'{pct:.0f}% Ace'
    return solvent


def classify_directory(dirname):
    """Classify a directory as S-series, R-series, Calibration, or other."""
    if dirname.startswith('s'):
        return 'S'
    elif dirname.startswith('r'):
        return 'R'
    elif 'calibration' in dirname.lower() or 'Calibration' in dirname:
        return 'CAL'
    else:
        return 'OTHER'


def copy_dataset(src_dir, dst_dir):
    """Copy a dataset directory, restructuring presentation/ -> presentation plots/."""
    os.makedirs(dst_dir, exist_ok=True)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)

        if item == 'presentation' and os.path.isdir(src_path):
            # Rename presentation/ -> presentation plots/
            pres_dst = os.path.join(dst_dir, 'presentation plots')
            os.makedirs(pres_dst, exist_ok=True)
            for pdf_file in os.listdir(src_path):
                shutil.copy2(os.path.join(src_path, pdf_file), pres_dst)
        elif os.path.isfile(src_path):
            shutil.copy2(src_path, dst_dir)


# ══════════════════════════════════════════════════════════════════════
# STEP 1: Create folder structure
# ══════════════════════════════════════════════════════════════════════
print("=" * 80)
print("STEP 1: Creating folder structure")
print("=" * 80)

for d in [S_SERIES_DIR, R_SERIES_DIR, CALIBRATION_DIR, OVERALL_DIR]:
    os.makedirs(d, exist_ok=True)
    print(f"  Created: {os.path.relpath(d, TARGET_DIR)}")

os.makedirs(os.path.join(S_SERIES_DIR, 'overall session'), exist_ok=True)
os.makedirs(os.path.join(R_SERIES_DIR, 'overall session'), exist_ok=True)
print(f"  Created: S-series (Feb 26)/overall session/")
print(f"  Created: R-series (March 3)/overall session/")

# ══════════════════════════════════════════════════════════════════════
# STEP 2: Copy datasets into series folders
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("STEP 2: Copying datasets into series folders")
print("=" * 80)

s_count = 0
r_count = 0
cal_count = 0
skipped = []

all_data = []

for dirname in sorted(os.listdir(SOURCE_DIR)):
    src_path = os.path.join(SOURCE_DIR, dirname)
    if not os.path.isdir(src_path):
        continue

    # Skip special directories
    if dirname in ('overall Lab', '2026-03-05', '5mu-0_5p'):
        skipped.append(dirname)
        continue

    # Skip old-format directories (from 2026-02-05 data, not 2026-03-05)
    if dirname in ('1mu-0_5p_225x-Results',
                    '1mu-21c-1isto224w-0_5p-trackresults',
                    '5mu-21c-1isto6_5w-0_5p-trackresults'):
        skipped.append(f"{dirname} (old format, from 2026-02-05)")
        continue

    series = classify_directory(dirname)

    if series == 'S':
        dst = os.path.join(S_SERIES_DIR, dirname)
        copy_dataset(src_path, dst)
        s_count += 1
        series_label = 'S-slide'
    elif series == 'R':
        dst = os.path.join(R_SERIES_DIR, dirname)
        copy_dataset(src_path, dst)
        r_count += 1
        series_label = 'R'
    elif series == 'CAL':
        dst = os.path.join(CALIBRATION_DIR)
        # Copy calibration files directly
        for item in os.listdir(src_path):
            shutil.copy2(os.path.join(src_path, item), dst)
        cal_count += 1
        continue
    else:
        skipped.append(dirname)
        continue

    # Parse summary for data collection
    summary_path = os.path.join(src_path, 'summary.txt')
    if os.path.isfile(summary_path):
        data = parse_summary(summary_path)
        if data is not None:
            data['dirname'] = dirname
            data['series'] = series_label

            # Extract condition ID
            if series == 'R':
                m = re.match(r'r(\d+)', dirname)
                if m:
                    data['condition_id'] = f"R{m.group(1)}"
            elif series == 'S':
                m = re.match(r's(\d+)', dirname)
                if m:
                    snum = m.group(1)
                    # Handle s2a, s2b, s2c as S2
                    data['condition_id'] = f"S{snum.rstrip('abcdefgh')}"

            # Extract trial number
            m_trial = re.search(r'trial(\d+)', dirname)
            data['trial'] = int(m_trial.group(1)) if m_trial else 1

            # Solvent label
            data['solvent_label'] = get_solvent_label(
                data.get('solute_pct', 0), data.get('solvent', 'Water'))

            # Nathan's Faxen factors
            bead = data['bead_um']
            f_min, f_max = NATHAN_FAXEN.get(bead,
                NATHAN_FAXEN.get(round(bead), (0.96, 0.56)))
            data['F_min_wall'] = f_min
            data['F_max_wall'] = f_max

            # Theory D
            D0 = data.get('D0_file', 0)
            data['D0'] = D0
            data['D_theory_max'] = D0 * f_min
            data['D_theory_min'] = D0 * f_max

            all_data.append(data)

print(f"\n  S-series copied: {s_count} datasets")
print(f"  R-series copied: {r_count} datasets")
print(f"  Calibration copied: {cal_count}")
if skipped:
    print(f"  Skipped: {', '.join(skipped)}")
print(f"\n  Total trials with parsed data: {len(all_data)}")


# ══════════════════════════════════════════════════════════════════════
# STEP 3: Build per-series summaries
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("STEP 3: Building per-series summaries")
print("=" * 80)

CSV_FIELDS = [
    'condition_id', 'series', 'trial', 'bead_um', 'solvent_label', 'solute_pct',
    'eta_mPas', 'temp_C', 'n_frames', 'n_particles', 'n_segments', 'n_steps',
    'D_var', 'D_var_err', 'D_gauss', 'D_gauss_err', 'D_msd',
    'D_var_raw', 'D_gauss_raw', 'D_msd_raw',
    'D0', 'F_min_wall', 'F_max_wall', 'D_theory_max', 'D_theory_min',
    'alpha', 'alpha_err', 'classification',
    'dirname'
]


def write_series_summary(series_data, series_name, output_dir):
    """Write CSV and text summary for a series."""
    csv_path = os.path.join(output_dir, f'{series_name}_data.csv')
    txt_path = os.path.join(output_dir, f'{series_name}_summary.txt')

    # Sort data
    sorted_data = sorted(series_data, key=lambda x: (
        x.get('bead_um', 0),
        {'Water': 0, '20% Gly': 1, '20% Ace': 2, '36% Gly': 3,
         '40% Gly': 4, '40% Ace': 5, '100% Ace': 6}.get(x.get('solvent_label', ''), 99),
        x.get('trial', 1)
    ))

    # Write CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction='ignore')
        writer.writeheader()
        for row in sorted_data:
            writer.writerow(row)

    # Write text summary
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        if 's_series' in series_name:
            f.write("S-SERIES DATA SUMMARY (Sessions 5-6, Feb 26 2026)\n")
            f.write("Slide-mounted samples, initial optimization runs\n")
        else:
            f.write("R-SERIES DATA SUMMARY (Sessions 7-8, March 3 2026)\n")
            f.write("Nathan's 4x4 matrix: 4 bead sizes x 4 solvents\n")
        f.write("=" * 120 + "\n\n")

        f.write(f"Total trials: {len(sorted_data)}\n\n")

        # Count by condition
        cond_counts = defaultdict(int)
        for row in sorted_data:
            key = f"{row.get('bead_um', 0):.1f} um, {row.get('solvent_label', '?')}"
            cond_counts[key] += 1
        f.write("Conditions covered:\n")
        for cond, count in sorted(cond_counts.items()):
            f.write(f"  {cond}: {count} trial(s)\n")

        f.write("\n" + "-" * 120 + "\n")
        header = (f"{'ID':<6} {'Tr':>2} {'Bead':>5} {'Solvent':<10} "
                  f"{'eta':>6} {'D_var':>7} {'+-':>5} {'D_gau':>7} "
                  f"{'D_msd':>7} {'D0':>7} {'D_max':>7} {'D_min':>7} "
                  f"{'Ratio':>6} {'alpha':>6} {'Class':<15}")
        f.write(header + "\n")
        f.write("-" * 120 + "\n")

        prev_bead = None
        for row in sorted_data:
            bead = row.get('bead_um', 0)
            if prev_bead is not None and bead != prev_bead:
                f.write("\n")
            prev_bead = bead

            D_var = row.get('D_var', 0)
            D_var_err = row.get('D_var_err', 0)
            D_gauss = row.get('D_gauss', 0)
            D_msd = row.get('D_msd', 0)
            D0 = row.get('D0', 0)
            D_max = row.get('D_theory_max', 0)
            D_min = row.get('D_theory_min', 0)
            alpha = row.get('alpha', 0)
            ratio = D_var / D_max if D_max > 0 else 0

            line = (f"{row.get('condition_id', '?'):<6} {row.get('trial', 1):>2} "
                    f"{bead:>5.1f} {row.get('solvent_label', '?'):<10} "
                    f"{row.get('eta_mPas', 0):>6.3f} "
                    f"{D_var:>7.4f} {D_var_err:>5.4f} {D_gauss:>7.4f} "
                    f"{D_msd:>7.4f} {D0:>7.4f} {D_max:>7.4f} {D_min:>7.4f} "
                    f"{ratio:>6.2f} {alpha:>6.3f} {row.get('classification', '?'):<15}")
            f.write(line + "\n")

        f.write("\n" + "=" * 120 + "\n")
        f.write("KEY: D values in um^2/s | Ratio = D_var/D_max | alpha = MSD exponent\n")
        f.write("     D0 = Stokes-Einstein | D_max = D0*F_min(midplane) | D_min = D0*F_max(wall)\n")
        f.write("     Noise floor: D_noise = 0.0180 um^2/s (subtracted from all measurements)\n")

    print(f"  Written: {os.path.basename(csv_path)}, {os.path.basename(txt_path)}")
    return sorted_data


# Split data by series
s_data = [d for d in all_data if d.get('series') == 'S-slide']
r_data = [d for d in all_data if d.get('series') == 'R']

s_session_dir = os.path.join(S_SERIES_DIR, 'overall session')
r_session_dir = os.path.join(R_SERIES_DIR, 'overall session')

print(f"\n  S-series: {len(s_data)} trials")
write_series_summary(s_data, 's_series', s_session_dir)

print(f"  R-series: {len(r_data)} trials")
write_series_summary(r_data, 'r_series', r_session_dir)


# ══════════════════════════════════════════════════════════════════════
# STEP 4: Build Overall Lab summary
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("STEP 4: Building Overall Lab summary")
print("=" * 80)

# Write combined CSV
csv_path = os.path.join(OVERALL_DIR, 'overall_data_summary.csv')
sorted_all = sorted(all_data, key=lambda x: (
    x.get('series', ''),
    x.get('bead_um', 0),
    {'Water': 0, '20% Gly': 1, '20% Ace': 2, '36% Gly': 3,
     '40% Gly': 4, '40% Ace': 5, '100% Ace': 6}.get(x.get('solvent_label', ''), 99),
    x.get('trial', 1)
))

with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction='ignore')
    writer.writeheader()
    for row in sorted_all:
        writer.writerow(row)
print(f"  CSV: {os.path.basename(csv_path)} ({len(sorted_all)} trials)")

# Build aggregated condition-level data
groups = defaultdict(list)
for row in all_data:
    key = (row['bead_um'], row['solvent_label'], row.get('series', '?'))
    groups[key].append(row)

agg_rows = []
for key in sorted(groups.keys(), key=lambda k: (k[2], k[0], k[1])):
    rows = groups[key]
    bead, solvent, series = key

    d_vars = [r.get('D_var', 0) for r in rows]
    d_gauss = [r.get('D_gauss', 0) for r in rows]
    d_msds = [r.get('D_msd', 0) for r in rows if r.get('D_msd') is not None]
    alphas = [r.get('alpha', 0) for r in rows if r.get('alpha') is not None]

    D0 = rows[0].get('D0', 0)
    D_max = rows[0].get('D_theory_max', 0)
    D_min = rows[0].get('D_theory_min', 0)

    d_var_mean = statistics.mean(d_vars) if d_vars else 0
    d_gauss_mean = statistics.mean(d_gauss) if d_gauss else 0
    d_msd_mean = statistics.mean(d_msds) if d_msds else 0
    d_var_std = statistics.stdev(d_vars) if len(d_vars) > 1 else 0
    d_gauss_std = statistics.stdev(d_gauss) if len(d_gauss) > 1 else 0
    alpha_mean = statistics.mean(alphas) if alphas else 0
    alpha_std = statistics.stdev(alphas) if len(alphas) > 1 else 0

    ratio_var = d_var_mean / D_max if D_max > 0 else 0
    in_range = D_min <= d_var_mean <= D_max

    agg_rows.append({
        'bead_um': bead, 'solvent_label': solvent, 'series': series,
        'n_trials': len(rows),
        'D_var_mean': d_var_mean, 'D_var_std': d_var_std,
        'D_gauss_mean': d_gauss_mean, 'D_gauss_std': d_gauss_std,
        'D_msd_mean': d_msd_mean,
        'D0': D0, 'D_theory_max': D_max, 'D_theory_min': D_min,
        'ratio_var': ratio_var,
        'alpha_mean': alpha_mean, 'alpha_std': alpha_std,
        'in_theory_range': 'YES' if in_range else 'no'
    })

agg_path = os.path.join(OVERALL_DIR, 'overall_aggregated.csv')
agg_fields = [
    'bead_um', 'solvent_label', 'series', 'n_trials',
    'D_var_mean', 'D_var_std', 'D_gauss_mean', 'D_gauss_std', 'D_msd_mean',
    'D0', 'D_theory_max', 'D_theory_min', 'ratio_var',
    'alpha_mean', 'alpha_std', 'in_theory_range'
]
with open(agg_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=agg_fields)
    writer.writeheader()
    for row in agg_rows:
        writer.writerow(row)
print(f"  Aggregated: {os.path.basename(agg_path)} ({len(agg_rows)} conditions)")

# Write comprehensive text summary
txt_path = os.path.join(OVERALL_DIR, 'overall_summary.txt')
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("=" * 130 + "\n")
    f.write("OVERALL LAB DATA SUMMARY\n")
    f.write("Brownian Motion Diffusion Coefficient Measurements\n")
    f.write("PHYS 382 Advanced Lab II — Lab 2: Microscopy and Motility\n")
    f.write("=" * 130 + "\n\n")

    f.write(f"Total trials analysed: {len(all_data)}\n")
    f.write(f"  R-series (Sessions 7-8, March 3): {len(r_data)} trials\n")
    f.write(f"  S-series (Sessions 5-6, Feb 26):  {len(s_data)} trials\n\n")

    # Conditions matrix
    f.write("CONDITIONS MATRIX:\n")
    f.write("-" * 80 + "\n")
    all_beads = sorted(set(d['bead_um'] for d in all_data))
    all_solvents = sorted(set(d['solvent_label'] for d in all_data),
        key=lambda s: {'Water': 0, '20% Gly': 1, '20% Ace': 2,
                       '36% Gly': 3, '40% Gly': 4, '40% Ace': 5,
                       '100% Ace': 6}.get(s, 99))

    f.write(f"{'Bead':>6}")
    for solv in all_solvents:
        f.write(f"  {solv:>10}")
    f.write("\n")

    for bead in all_beads:
        f.write(f"{bead:>5.1f}um")
        for solv in all_solvents:
            count = sum(1 for d in all_data
                       if d['bead_um'] == bead and d['solvent_label'] == solv)
            if count > 0:
                f.write(f"  {count:>10}")
            else:
                f.write(f"  {'--':>10}")
        f.write("\n")

    # Nathan's Faxen factors
    f.write("\n\nNathan's Faxen Correction Factors:\n")
    f.write("  Bead      F_min (midplane)   F_max (touching wall)\n")
    for bead in [1.0, 2.1, 3.0, 5.0]:
        fm, fx = NATHAN_FAXEN[bead]
        f.write(f"  {bead:4.1f} um      {fm:.3f}              {fx:.3f}\n")

    # Missing conditions
    f.write("\n\nMISSING from Nathan's 4x4 matrix:\n")
    for rid, desc in sorted(NATHAN_MATRIX.items()):
        rnum = int(rid[1:])
        has_data = any(d.get('condition_id') == rid for d in all_data)
        if not has_data:
            f.write(f"  {rid}: {desc} -- NO DATA COLLECTED\n")

    # Detailed per-trial table
    f.write("\n\n" + "=" * 140 + "\n")
    f.write("DETAILED PER-TRIAL DATA\n")
    f.write("=" * 140 + "\n")

    header = (f"{'#':>3} {'ID':<6} {'Ser':>3} {'Tr':>2} {'Bead':>5} {'Solvent':<10} "
              f"{'eta':>6} {'D_var':>7} {'+-':>5} {'D_gau':>7} "
              f"{'D_msd':>7} {'D0':>7} {'D_max':>7} {'D_min':>7} "
              f"{'Ratio':>6} {'alpha':>6} {'Class':<15} {'Dir':<40}")
    f.write(header + "\n")
    f.write("-" * 180 + "\n")

    for i, row in enumerate(sorted_all, 1):
        D_var = row.get('D_var', 0)
        D_max = row.get('D_theory_max', 0)
        ratio = D_var / D_max if D_max > 0 else 0

        line = (f"{i:>3} {row.get('condition_id', '?'):<6} "
                f"{row.get('series', '?'):>3} {row.get('trial', 1):>2} "
                f"{row.get('bead_um', 0):>5.1f} {row.get('solvent_label', '?'):<10} "
                f"{row.get('eta_mPas', 0):>6.3f} "
                f"{D_var:>7.4f} {row.get('D_var_err', 0):>5.4f} "
                f"{row.get('D_gauss', 0):>7.4f} "
                f"{row.get('D_msd', 0):>7.4f} "
                f"{row.get('D0', 0):>7.4f} {D_max:>7.4f} "
                f"{row.get('D_theory_min', 0):>7.4f} "
                f"{ratio:>6.2f} {row.get('alpha', 0):>6.3f} "
                f"{row.get('classification', '?'):<15} "
                f"{row.get('dirname', ''):<40}")
        f.write(line + "\n")

    # Aggregated summary
    f.write("\n\n" + "=" * 130 + "\n")
    f.write("AGGREGATED BY CONDITION (mean +/- std)\n")
    f.write("=" * 130 + "\n")

    header2 = (f"{'Bead':>5} {'Solvent':<10} {'Ser':>4} {'N':>2} "
               f"{'D_var':>7} {'+-':>5} {'D_gau':>7} {'D_msd':>7} "
               f"{'D0':>7} {'D_max':>7} {'D_min':>7} "
               f"{'Ratio':>6} {'alpha':>6} {'InRng':>5}")
    f.write(header2 + "\n")
    f.write("-" * 110 + "\n")

    for row in agg_rows:
        line = (f"{row['bead_um']:>5.1f} {row['solvent_label']:<10} "
                f"{row['series']:>4} {row['n_trials']:>2} "
                f"{row['D_var_mean']:>7.4f} {row['D_var_std']:>5.4f} "
                f"{row['D_gauss_mean']:>7.4f} {row['D_msd_mean']:>7.4f} "
                f"{row['D0']:>7.4f} {row['D_theory_max']:>7.4f} "
                f"{row['D_theory_min']:>7.4f} "
                f"{row['ratio_var']:>6.2f} {row['alpha_mean']:>6.3f} "
                f"{row['in_theory_range']:>5}")
        f.write(line + "\n")

    f.write("\n" + "=" * 130 + "\n")
    f.write("LEGEND:\n")
    f.write("  D_var = Direct Variance method (noise-corrected)\n")
    f.write("  D_gau = Gaussian Fit method (noise-corrected)\n")
    f.write("  D_msd = MSD Slope method (noise-corrected)\n")
    f.write("  D0    = Stokes-Einstein (no wall correction)\n")
    f.write("  D_max = D0 * F_min (midplane, best case Faxen)\n")
    f.write("  D_min = D0 * F_max (touching wall, worst case Faxen)\n")
    f.write("  Ratio = D_var / D_max (1.0 = perfect match to midplane theory)\n")
    f.write("  alpha = MSD exponent (1.0 = normal Brownian diffusion)\n")
    f.write("  InRng = D_min <= D_var <= D_max?\n")
    f.write("  All D values in um^2/s. Noise floor: D_noise = 0.0180 um^2/s\n")
    f.write("=" * 130 + "\n")

print(f"  Summary: {os.path.basename(txt_path)}")


# ══════════════════════════════════════════════════════════════════════
# STEP 5: Generate plots
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("STEP 5: Generating plots")
print("=" * 80)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Color scheme
SOLVENT_COLORS = {
    'Water': '#2196F3',
    '20% Gly': '#4CAF50',
    '36% Gly': '#8BC34A',
    '40% Gly': '#FF9800',
    '41% Gly': '#FF9800',
    '20% Ace': '#9C27B0',
    '40% Ace': '#E91E63',
    '100% Ace': '#F44336',
}

BEAD_MARKERS = {1.0: 'o', 2.1: 's', 3.0: '^', 5.0: 'D'}
SERIES_STYLES = {'R': '-', 'S-slide': '--'}


def save_fig(fig, path, dpi=200):
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {os.path.relpath(path, TARGET_DIR)}")


# ── PLOT 1: D measured vs D theory (1:1 with Faxen band) ──────────
def plot_d_vs_theory(data, output_path, title_suffix=''):
    fig, ax = plt.subplots(figsize=(8, 7))

    # 1:1 line
    max_d = max(max(d.get('D_theory_max', 0.01) for d in data),
                max(d.get('D_var', 0.01) for d in data)) * 1.2
    lims = [0, max_d]
    ax.plot(lims, lims, 'k-', lw=1, alpha=0.5, label='1:1 (perfect match)')

    # Faxen band: measured = theory * F_max/F_min
    xs = np.linspace(0, max_d, 100)
    # worst case: measured = theory * (F_max/F_min) ~ 0.57
    ax.fill_between(xs, xs * 0.55, xs, alpha=0.1, color='gray',
                    label='Faxen band (wall to midplane)')

    for row in data:
        D_th = row.get('D_theory_max', 0)
        D_m = row.get('D_var', 0)
        bead = row.get('bead_um', 3.0)
        solv = row.get('solvent_label', 'Water')
        ser = row.get('series', 'R')

        marker = BEAD_MARKERS.get(bead, 'o')
        color = SOLVENT_COLORS.get(solv, '#666')
        edge = 'black' if ser == 'R' else 'gray'

        ax.plot(D_th, D_m, marker=marker, color=color, markersize=8,
                markeredgecolor=edge, markeredgewidth=0.8, alpha=0.8)

    # Legend entries
    for bead, marker in sorted(BEAD_MARKERS.items()):
        ax.plot([], [], marker=marker, color='gray', markersize=8,
                linestyle='None', label=f'{bead} um')
    for solv, color in SOLVENT_COLORS.items():
        if any(d.get('solvent_label') == solv for d in data):
            ax.plot([], [], 'o', color=color, markersize=8,
                    linestyle='None', label=solv)

    ax.set_xlabel('D_theory (midplane Faxen) [um^2/s]', fontsize=12)
    ax.set_ylabel('D_measured (variance method) [um^2/s]', fontsize=12)
    ax.set_title(f'Measured vs Theory Diffusion Coefficient{title_suffix}', fontsize=13)
    ax.legend(fontsize=8, loc='upper left', ncol=2)
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    save_fig(fig, output_path)


# ── PLOT 2: All-trials histogram (D_var) ──────────────────────────
def plot_all_trials_histogram(data, output_path, title_suffix=''):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'All Trials Histogram{title_suffix}', fontsize=14, fontweight='bold')

    # Panel 1: D_var distribution by bead size
    ax = axes[0, 0]
    for bead in sorted(set(d['bead_um'] for d in data)):
        vals = [d.get('D_var', 0) for d in data if d['bead_um'] == bead]
        ax.hist(vals, bins=15, alpha=0.5, label=f'{bead} um ({len(vals)} trials)')
    ax.set_xlabel('D_var [um^2/s]')
    ax.set_ylabel('Count')
    ax.set_title('D (Variance) by Bead Size')
    ax.legend(fontsize=8)

    # Panel 2: D_var distribution by solvent
    ax = axes[0, 1]
    for solv in sorted(set(d['solvent_label'] for d in data),
                       key=lambda s: {'Water': 0, '20% Gly': 1, '20% Ace': 2,
                                      '36% Gly': 3, '40% Gly': 4, '40% Ace': 5,
                                      '100% Ace': 6}.get(s, 99)):
        vals = [d.get('D_var', 0) for d in data if d['solvent_label'] == solv]
        color = SOLVENT_COLORS.get(solv, '#666')
        ax.hist(vals, bins=12, alpha=0.5, color=color,
                label=f'{solv} ({len(vals)})')
    ax.set_xlabel('D_var [um^2/s]')
    ax.set_ylabel('Count')
    ax.set_title('D (Variance) by Solvent')
    ax.legend(fontsize=8)

    # Panel 3: alpha distribution
    ax = axes[1, 0]
    alphas = [d.get('alpha', 0) for d in data if d.get('alpha') is not None]
    ax.hist(alphas, bins=20, color='#607D8B', alpha=0.7, edgecolor='white')
    ax.axvline(x=1.0, color='red', linestyle='--', lw=2, label='alpha=1 (Brownian)')
    ax.set_xlabel('MSD Exponent (alpha)')
    ax.set_ylabel('Count')
    ax.set_title(f'MSD Exponent Distribution (N={len(alphas)})')
    ax.legend()

    # Panel 4: Ratio D_var/D_theory by condition
    ax = axes[1, 1]
    ratios = []
    labels = []
    colors = []
    for row in sorted(data, key=lambda x: (x.get('bead_um', 0), x.get('solvent_label', ''))):
        D_max = row.get('D_theory_max', 0)
        if D_max > 0:
            ratio = row.get('D_var', 0) / D_max
            ratios.append(ratio)
            labels.append(f"{row.get('bead_um', 0):.0f}um-{row.get('solvent_label', '?')}")
            colors.append(SOLVENT_COLORS.get(row.get('solvent_label', ''), '#666'))

    x_pos = range(len(ratios))
    ax.bar(x_pos, ratios, color=colors, alpha=0.7, edgecolor='white')
    ax.axhline(y=1.0, color='green', linestyle='--', lw=2, label='Perfect match')
    ax.axhline(y=0.57, color='red', linestyle=':', lw=1.5, label='Max wall (F~0.56)')
    ax.set_ylabel('D_var / D_theory_max')
    ax.set_title('Theory Agreement Ratio (all trials)')
    ax.legend(fontsize=8)
    ax.set_xticks([])

    plt.tight_layout()
    save_fig(fig, output_path)


# ── PLOT 3: D vs 1/r and D vs eta (physics check) ────────────────
def plot_physics_trends(data, output_path, title_suffix=''):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig.suptitle(f'Physics Trend Verification{title_suffix}', fontsize=14, fontweight='bold')

    # Panel 1: D vs 1/r (should be linear per Stokes-Einstein)
    ax = axes[0]
    for solv in sorted(set(d['solvent_label'] for d in data),
                       key=lambda s: {'Water': 0, '20% Gly': 1, '20% Ace': 2,
                                      '36% Gly': 3, '40% Gly': 4, '40% Ace': 5,
                                      '100% Ace': 6}.get(s, 99)):
        subset = [d for d in data if d['solvent_label'] == solv]
        if not subset:
            continue

        # Group by bead size, take mean
        bead_groups = defaultdict(list)
        for d in subset:
            bead_groups[d['bead_um']].append(d.get('D_var', 0))

        inv_r = [1.0 / (b / 2) for b in sorted(bead_groups.keys())]
        d_mean = [statistics.mean(bead_groups[b]) for b in sorted(bead_groups.keys())]
        color = SOLVENT_COLORS.get(solv, '#666')

        ax.plot(inv_r, d_mean, 'o-', color=color, label=solv, markersize=8)

        # Theory line
        D0_vals = [statistics.mean([d.get('D_theory_max', 0) for d in subset if d['bead_um'] == b])
                   for b in sorted(bead_groups.keys())]
        ax.plot(inv_r, D0_vals, '--', color=color, alpha=0.4)

    ax.set_xlabel('1/r [1/um]', fontsize=11)
    ax.set_ylabel('D_var [um^2/s]', fontsize=11)
    ax.set_title('D vs 1/r (Stokes-Einstein: D ~ 1/r)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Panel 2: D vs eta (should be ~ 1/eta)
    ax = axes[1]
    for bead in sorted(set(d['bead_um'] for d in data)):
        subset = [d for d in data if d['bead_um'] == bead]
        if not subset:
            continue

        eta_groups = defaultdict(list)
        for d in subset:
            eta_groups[round(d.get('eta_mPas', 1), 2)].append(d.get('D_var', 0))

        etas = sorted(eta_groups.keys())
        d_mean = [statistics.mean(eta_groups[e]) for e in etas]
        marker = BEAD_MARKERS.get(bead, 'o')

        ax.plot(etas, d_mean, marker=marker, linestyle='-', label=f'{bead} um',
                markersize=8)

    ax.set_xlabel('Viscosity [mPa.s]', fontsize=11)
    ax.set_ylabel('D_var [um^2/s]', fontsize=11)
    ax.set_title('D vs Viscosity (D ~ 1/eta)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 3: D_var vs D_gauss correlation
    ax = axes[2]
    dv = [d.get('D_var', 0) for d in data]
    dg = [d.get('D_gauss', 0) for d in data]
    colors_scatter = [SOLVENT_COLORS.get(d.get('solvent_label', ''), '#666') for d in data]

    ax.scatter(dv, dg, c=colors_scatter, alpha=0.7, s=40, edgecolors='black', linewidths=0.5)
    mx = max(max(dv), max(dg)) * 1.1
    ax.plot([0, mx], [0, mx], 'k--', lw=1, alpha=0.5, label='1:1')
    ax.set_xlabel('D_var [um^2/s]', fontsize=11)
    ax.set_ylabel('D_gauss [um^2/s]', fontsize=11)
    ax.set_title('Variance vs Gaussian Methods')
    ax.set_aspect('equal')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, output_path)


# ── PLOT 4: Bar chart comparison (R-series) ──────────────────────
def plot_bar_comparison(data, output_path, title_suffix=''):
    # Filter R-series only for the bar chart
    r_only = [d for d in data if d.get('series') == 'R']
    if not r_only:
        r_only = data  # fallback to all data

    # Group by condition
    cond_groups = defaultdict(list)
    for d in r_only:
        key = f"R{re.match(r'r(\\d+)', d.get('dirname', '')).group(1) if re.match(r'r(\\d+)', d.get('dirname', '')) else '?'}"
        cond_groups[key].append(d)

    # Sort by Nathan's matrix order
    ordered_keys = sorted(cond_groups.keys(),
                         key=lambda k: int(k[1:]) if k[1:].isdigit() else 99)

    n = len(ordered_keys)
    if n == 0:
        return

    fig, ax = plt.subplots(figsize=(max(12, n * 0.8), 7))

    x = np.arange(n)
    width = 0.2

    d_var_means = []
    d_gauss_means = []
    d_msd_means = []
    d_theory_maxs = []
    d_theory_mins = []
    bar_labels = []
    bar_colors = []

    for key in ordered_keys:
        rows = cond_groups[key]
        d_var_means.append(statistics.mean([r.get('D_var', 0) for r in rows]))
        d_gauss_means.append(statistics.mean([r.get('D_gauss', 0) for r in rows]))
        msds = [r.get('D_msd', 0) for r in rows if r.get('D_msd') is not None]
        d_msd_means.append(statistics.mean(msds) if msds else 0)
        d_theory_maxs.append(rows[0].get('D_theory_max', 0))
        d_theory_mins.append(rows[0].get('D_theory_min', 0))

        bead = rows[0].get('bead_um', 0)
        solv = rows[0].get('solvent_label', '?')
        bar_labels.append(f"{key}\n{bead}um\n{solv}")
        bar_colors.append(SOLVENT_COLORS.get(solv, '#666'))

    ax.bar(x - 1.5*width, d_var_means, width, label='D_var', color='#1976D2', alpha=0.8)
    ax.bar(x - 0.5*width, d_gauss_means, width, label='D_gauss', color='#388E3C', alpha=0.8)
    ax.bar(x + 0.5*width, d_msd_means, width, label='D_msd', color='#F57C00', alpha=0.8)

    # Theory range as error bars
    theory_mid = [(mx + mn) / 2 for mx, mn in zip(d_theory_maxs, d_theory_mins)]
    theory_err = [(mx - mn) / 2 for mx, mn in zip(d_theory_maxs, d_theory_mins)]
    ax.errorbar(x + 1.5*width, theory_mid, yerr=theory_err, fmt='kD', markersize=6,
                capsize=4, label='Theory [min, max]', zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels(bar_labels, fontsize=7, ha='center')
    ax.set_ylabel('D [um^2/s]', fontsize=12)
    ax.set_title(f'R-Series: 3 Methods vs Theory{title_suffix}', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    save_fig(fig, output_path)


# ── PLOT 5: Comprehensive 6-panel overview ────────────────────────
def plot_comprehensive_overview(data, output_path):
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('OVERALL LAB: Brownian Motion Diffusion Analysis\n'
                 f'Total: {len(data)} trials across {len(set(d["solvent_label"] for d in data))} '
                 f'solvents and {len(set(d["bead_um"] for d in data))} bead sizes',
                 fontsize=14, fontweight='bold')

    # Panel (0,0): D_measured vs D_theory scatter
    ax = axes[0, 0]
    for row in data:
        D_th = row.get('D_theory_max', 0)
        D_m = row.get('D_var', 0)
        marker = BEAD_MARKERS.get(row.get('bead_um', 3), 'o')
        color = SOLVENT_COLORS.get(row.get('solvent_label', ''), '#666')
        edge = 'black' if row.get('series') == 'R' else 'gray'
        ax.plot(D_th, D_m, marker=marker, color=color, markersize=7,
                markeredgecolor=edge, markeredgewidth=0.6, alpha=0.8)
    mx = max(max(d.get('D_theory_max', 0.01) for d in data),
             max(d.get('D_var', 0.01) for d in data)) * 1.1
    ax.plot([0, mx], [0, mx], 'k-', lw=1, alpha=0.5)
    ax.fill_between([0, mx], [0, 0], [0, mx * 0.57], alpha=0.08, color='red')
    ax.set_xlabel('D_theory [um^2/s]')
    ax.set_ylabel('D_measured [um^2/s]')
    ax.set_title('Measured vs Theory (1:1)')
    ax.set_xlim([0, mx])
    ax.set_ylim([0, mx])
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Panel (0,1): D vs 1/r
    ax = axes[0, 1]
    for solv in sorted(set(d['solvent_label'] for d in data)):
        subset = [d for d in data if d['solvent_label'] == solv]
        bead_groups = defaultdict(list)
        for d in subset:
            bead_groups[d['bead_um']].append(d.get('D_var', 0))
        inv_r = [1.0 / (b / 2) for b in sorted(bead_groups.keys())]
        d_mean = [statistics.mean(bead_groups[b]) for b in sorted(bead_groups.keys())]
        color = SOLVENT_COLORS.get(solv, '#666')
        ax.plot(inv_r, d_mean, 'o-', color=color, label=solv, markersize=6)
    ax.set_xlabel('1/r [1/um]')
    ax.set_ylabel('D_var [um^2/s]')
    ax.set_title('D vs 1/r (Stokes-Einstein)')
    ax.legend(fontsize=6)
    ax.grid(True, alpha=0.3)

    # Panel (0,2): D vs eta
    ax = axes[0, 2]
    for bead in sorted(set(d['bead_um'] for d in data)):
        subset = [d for d in data if d['bead_um'] == bead]
        eta_groups = defaultdict(list)
        for d in subset:
            eta_groups[round(d.get('eta_mPas', 1), 2)].append(d.get('D_var', 0))
        etas = sorted(eta_groups.keys())
        d_mean = [statistics.mean(eta_groups[e]) for e in etas]
        marker = BEAD_MARKERS.get(bead, 'o')
        ax.plot(etas, d_mean, marker=marker, linestyle='-', label=f'{bead} um', markersize=7)
    ax.set_xlabel('Viscosity [mPa.s]')
    ax.set_ylabel('D_var [um^2/s]')
    ax.set_title('D vs Viscosity (D ~ 1/eta)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel (1,0): alpha histogram
    ax = axes[1, 0]
    alphas_r = [d.get('alpha', 0) for d in data if d.get('series') == 'R' and d.get('alpha')]
    alphas_s = [d.get('alpha', 0) for d in data if d.get('series') == 'S-slide' and d.get('alpha')]
    if alphas_r:
        ax.hist(alphas_r, bins=15, alpha=0.6, color='#1976D2', label=f'R-series (N={len(alphas_r)})')
    if alphas_s:
        ax.hist(alphas_s, bins=12, alpha=0.6, color='#F57C00', label=f'S-series (N={len(alphas_s)})')
    ax.axvline(x=1.0, color='red', linestyle='--', lw=2, label='alpha=1')
    ax.set_xlabel('MSD Exponent (alpha)')
    ax.set_ylabel('Count')
    ax.set_title('MSD Exponent Distribution')
    ax.legend(fontsize=8)

    # Panel (1,1): D_var histogram by solvent
    ax = axes[1, 1]
    for solv in ['Water', '20% Gly', '40% Gly', '100% Ace', '20% Ace', '40% Ace', '36% Gly']:
        vals = [d.get('D_var', 0) for d in data if d.get('solvent_label') == solv]
        if vals:
            color = SOLVENT_COLORS.get(solv, '#666')
            ax.hist(vals, bins=10, alpha=0.5, color=color, label=f'{solv} ({len(vals)})')
    ax.set_xlabel('D_var [um^2/s]')
    ax.set_ylabel('Count')
    ax.set_title('D Distribution by Solvent')
    ax.legend(fontsize=7)

    # Panel (1,2): Ratio heatmap-style
    ax = axes[1, 2]
    all_beads = sorted(set(d['bead_um'] for d in data))
    all_solvents = sorted(set(d['solvent_label'] for d in data),
        key=lambda s: {'Water': 0, '20% Gly': 1, '20% Ace': 2,
                       '36% Gly': 3, '40% Gly': 4, '40% Ace': 5,
                       '100% Ace': 6}.get(s, 99))

    ratio_matrix = np.full((len(all_beads), len(all_solvents)), np.nan)
    for i, bead in enumerate(all_beads):
        for j, solv in enumerate(all_solvents):
            subset = [d for d in data if d['bead_um'] == bead and d['solvent_label'] == solv]
            if subset:
                D_vars = [d.get('D_var', 0) for d in subset]
                D_maxs = [d.get('D_theory_max', 1) for d in subset]
                if statistics.mean(D_maxs) > 0:
                    ratio_matrix[i, j] = statistics.mean(D_vars) / statistics.mean(D_maxs)

    im = ax.imshow(ratio_matrix, cmap='RdYlGn', vmin=0, vmax=1.2, aspect='auto')
    ax.set_xticks(range(len(all_solvents)))
    ax.set_xticklabels(all_solvents, fontsize=8, rotation=45, ha='right')
    ax.set_yticks(range(len(all_beads)))
    ax.set_yticklabels([f'{b} um' for b in all_beads], fontsize=9)
    ax.set_title('Ratio D_var/D_theory (1.0 = match)')

    # Add text annotations
    for i in range(len(all_beads)):
        for j in range(len(all_solvents)):
            val = ratio_matrix[i, j]
            if not np.isnan(val):
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                       fontsize=9, fontweight='bold',
                       color='white' if val < 0.4 else 'black')

    fig.colorbar(im, ax=ax, shrink=0.8, label='Ratio')

    plt.tight_layout()
    save_fig(fig, output_path)


# Generate all plots for Overall Lab
plot_d_vs_theory(all_data,
    os.path.join(OVERALL_DIR, 'D_measured_vs_theory_overall.png'),
    ' (All Trials)')

plot_all_trials_histogram(all_data,
    os.path.join(OVERALL_DIR, 'all_trials_histogram.png'),
    ' (All Data)')

plot_physics_trends(all_data,
    os.path.join(OVERALL_DIR, 'physics_trends_overall.png'),
    ' (All Data)')

plot_bar_comparison(all_data,
    os.path.join(OVERALL_DIR, 'D_bar_comparison_R_series.png'))

plot_comprehensive_overview(all_data,
    os.path.join(OVERALL_DIR, 'overall_6panel.png'))

# Generate per-series plots
if s_data:
    plot_d_vs_theory(s_data,
        os.path.join(S_SERIES_DIR, 'overall session', 's_series_D_vs_theory.png'),
        ' (S-series)')
    plot_all_trials_histogram(s_data,
        os.path.join(S_SERIES_DIR, 'overall session', 's_series_histogram.png'),
        ' (S-series)')
    plot_physics_trends(s_data,
        os.path.join(S_SERIES_DIR, 'overall session', 's_series_physics_trends.png'),
        ' (S-series)')

if r_data:
    plot_d_vs_theory(r_data,
        os.path.join(R_SERIES_DIR, 'overall session', 'r_series_D_vs_theory.png'),
        ' (R-series)')
    plot_all_trials_histogram(r_data,
        os.path.join(R_SERIES_DIR, 'overall session', 'r_series_histogram.png'),
        ' (R-series)')
    plot_physics_trends(r_data,
        os.path.join(R_SERIES_DIR, 'overall session', 'r_series_physics_trends.png'),
        ' (R-series)')
    plot_bar_comparison(r_data,
        os.path.join(R_SERIES_DIR, 'overall session', 'r_series_bar_comparison.png'))


# ══════════════════════════════════════════════════════════════════════
# STEP 6: Final verification
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("STEP 6: Verification")
print("=" * 80)

# Count files in target
def count_files(directory):
    total = 0
    for root, dirs, files in os.walk(directory):
        total += len(files)
    return total

def count_dirs(directory):
    total = 0
    for root, dirs, files in os.walk(directory):
        total += len(dirs)
    return total

print(f"\nTarget directory: {TARGET_DIR}")
print(f"  Total files:       {count_files(TARGET_DIR)}")
print(f"  Total directories: {count_dirs(TARGET_DIR)}")

# Per-section counts
for section in ['S-series (Feb 26)', 'R-series (March 3)', 'Calibration', 'Overall Lab']:
    section_path = os.path.join(TARGET_DIR, section)
    if os.path.exists(section_path):
        n_files = count_files(section_path)
        n_dirs = count_dirs(section_path)
        print(f"  {section}: {n_dirs} dirs, {n_files} files")

# Check data coverage
print(f"\nData Coverage:")
print(f"  S-series datasets: {s_count}")
print(f"  R-series datasets: {r_count}")
print(f"  Total parsed trials: {len(all_data)}")

# Check for missing R conditions
print(f"\n  Nathan's 4x4 Matrix coverage:")
for rnum in range(1, 17):
    rid = f"R{rnum}"
    count = sum(1 for d in r_data if d.get('condition_id') == rid)
    desc = NATHAN_MATRIX.get(rid, '?')
    status = f"{count} trial(s)" if count > 0 else "MISSING"
    print(f"    {rid}: {desc} -- {status}")

print("\n" + "=" * 80)
print("REORGANIZATION COMPLETE!")
print("=" * 80)
