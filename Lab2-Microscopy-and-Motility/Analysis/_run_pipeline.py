#!/usr/bin/env python
# coding: utf-8
import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')  # headless backend — no GUI windows

# # Lab 2 — Batch Particle Tracking & Diffusion Analysis
# 
# **PHYS 382 Advanced Lab — Microscopy & Motility**
# 
# This notebook processes **multiple videos** in one run:
# 1. Define a `JOBS` list — each entry is a video path + bead size + glycerol %
# 2. **Run All Cells** — each video gets its own output folder
# 3. Already-processed videos are **skipped automatically** (checks for `summary.txt`)
# 4. To reprocess a video, delete its output folder or set `FORCE_REPROCESS = True`
# 
# ### Pipeline per video
# 1. Particle tracking (temporal median background, connected components, Hungarian linking)
# 2. Track segmentation (split at jumps, filter short/stationary)
# 3. Trajectory plot in physical units
# 4. Displacement histogram + Gaussian fit → D (variance & Gaussian methods)
# 5. MSD analysis + power-law fit → D (MSD slope) and α exponent
# 6. Stokes-Einstein comparison
# 7. Summary saved to `figures/{date}/{filename}/`

# In[1]:


# ============================================================================
# CELL 1 — JOBS & SHARED CONSTANTS
# ============================================================================

# --- Data root ---
DATA = r"D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Data"

# --- Session 5 (2026-02-24) ---
mu3    = DATA + r"\2026-02-24\3um-0_5p-0pgly-test-1burstcount.avi"
trial1 = DATA + r"\2026-02-24\3um-0_5p-4_9pstock-0pgly-trial1.avi"
trial2 = DATA + r"\2026-02-24\3um-0_5p-4_9pstock-0pgly-trial2.avi"
mu5    = DATA + r"\2026-02-24\5um-20pgly-test-1000burstcount.avi"

# --- Session 6 (2026-02-26) ---
s1b_t3 = DATA + r"\2026-02-26\s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial3.avi"
s1b_t4 = DATA + r"\2026-02-26\s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial4.avi"
s1b_t5 = DATA + r"\2026-02-26\s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial5.avi"

s2a_t1 = DATA + r"\2026-02-26\s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial1.avi"
s2a_t2 = DATA + r"\2026-02-26\s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial2.avi"
s2a_t3 = DATA + r"\2026-02-26\s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial3.avi"

s2b_t1 = DATA + r"\2026-02-26\s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial1.avi"
s2b_t2 = DATA + r"\2026-02-26\s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial2.avi"
s2b_t3 = DATA + r"\2026-02-26\s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial3.avi"

s2c_t1 = DATA + r"\2026-02-26\s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial1.avi"
s2c_t2 = DATA + r"\2026-02-26\s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial2.avi"
s2c_t3 = DATA + r"\2026-02-26\s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial3.avi"

s3_t1  = DATA + r"\2026-02-26\s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial1.avi"
s3_t2  = DATA + r"\2026-02-26\s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial2.avi"
s3_t3  = DATA + r"\2026-02-26\s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial3.avi"

s7_t1  = DATA + r"\2026-02-26\s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial1.avi"
s7_t2  = DATA + r"\2026-02-26\s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial2.avi"
s7_t3  = DATA + r"\2026-02-26\s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial3.avi"

# Acetone samples
s8_t1  = DATA + r"\2026-02-26\s8-3um-0_5p-3ul-water-397ul-ace-100ul-trial1.avi"
s8_t2  = DATA + r"\2026-02-26\s8-3um-0_5p-3ul-water-397ul-ace-100ul-trial2.avi"
s9_t1  = DATA + r"\2026-02-26\s9-3um-0_5p-24_0ul-water-1200ul-ace-800ul-trial1.avi"
s9_t2  = DATA + r"\2026-02-26\s9-3um-0_5p-24_0ul-water-1200ul-ace-800ul-trial2.avi"

# --- JOBS LIST ---
# Each job: (avi_path, bead_diameter_um, solute_percent, solute_type)
#   solute_type: 'glycerol' (default) or 'acetone'
# Add new videos here — already-processed ones are skipped automatically.
JOBS = [
    # Session 5 (Feb 24)
    (trial1, 3.0,  0.0, 'glycerol'),
    (trial2, 3.0,  0.0, 'glycerol'),
    (mu3,    3.0,  0.0, 'glycerol'),
    (mu5,    5.0, 20.0, 'glycerol'),

    # Session 6 (Feb 26) — s1b: 3um in pure water (0% gly)
    (s1b_t3, 3.0,  0.0, 'glycerol'),
    (s1b_t4, 3.0,  0.0, 'glycerol'),
    (s1b_t5, 3.0,  0.0, 'glycerol'),

    # s2a: 1um in 20% glycerol
    (s2a_t1, 1.0, 20.0, 'glycerol'),
    (s2a_t2, 1.0, 20.0, 'glycerol'),
    (s2a_t3, 1.0, 20.0, 'glycerol'),

    # s2b: 3um in 20% glycerol
    (s2b_t1, 3.0, 20.0, 'glycerol'),
    (s2b_t2, 3.0, 20.0, 'glycerol'),
    (s2b_t3, 3.0, 20.0, 'glycerol'),

    # s2c: 1um in 20% glycerol (higher bead concentration)
    (s2c_t1, 1.0, 20.0, 'glycerol'),
    (s2c_t2, 1.0, 20.0, 'glycerol'),
    (s2c_t3, 1.0, 20.0, 'glycerol'),

    # s3: 3um in 20% glycerol
    (s3_t1,  3.0, 20.0, 'glycerol'),
    (s3_t2,  3.0, 20.0, 'glycerol'),
    (s3_t3,  3.0, 20.0, 'glycerol'),

    # s7: 3um in 36% glycerol
    (s7_t1,  3.0, 36.3, 'glycerol'),
    (s7_t2,  3.0, 36.3, 'glycerol'),
    (s7_t3,  3.0, 36.3, 'glycerol'),

    # s8: 3um in 20% acetone (100/(397+100) = 20.1%)
    (s8_t1,  3.0, 20.1, 'acetone'),
    (s8_t2,  3.0, 20.1, 'acetone'),

    # s9: 3um in 40% acetone (800/(1200+800) = 40.0%)
    (s9_t1,  3.0, 40.0, 'acetone'),
    (s9_t2,  3.0, 40.0, 'acetone'),
]

# Set True to reprocess ALL videos (ignores existing results)
FORCE_REPROCESS = True

# --- Shared constants (same for all videos) ---
PIXEL_SIZE = 0.0684           # um/px (68.4 nm/px, 100x oil)
# NOTE: Frame rate is READ from each video file (not hardcoded)
TEMPERATURE_C = 21.0          # Celsius
CHAMBER_DEPTH_UM = 82.5       # Tape spacer chamber depth (um)

# --- Tracking parameters ---
DETECTION_THRESHOLD = 15
GAUSSIAN_BLUR_SIGMA = 1.5
MAX_DISPLACEMENT = 10         # px/frame
MAX_GAP_FRAMES = 3
MIN_TRACK_LENGTH = 10         # frames
MIN_TOTAL_DISPLACEMENT = 3.0  # px

# --- Analysis parameters ---
NUM_BEST_SEGMENTS = 10
MIN_SEGMENT_LENGTH = 10       # frames
MAX_JUMP_PX = 20              # px

print(f'Defined {len(JOBS)} jobs.')
for i, (p, d, g, s) in enumerate(JOBS, 1):
    from pathlib import Path as _P
    print(f'  {i:2d}. {_P(p).name}  ({d} um, {g}% {s})')


# In[2]:


# ============================================================================
# CELL 2 — IMPORTS & FUNCTION DEFINITIONS
# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import shutil
import math
import time
from pathlib import Path
from scipy.optimize import linear_sum_assignment, curve_fit
from scipy.stats import chi2 as chi2_dist
from math import sqrt, pi

k_B = 1.381e-23  # Boltzmann constant (J/K)

# ---------------------------------------------------------------
# Viscosity functions (Cheng 2008 CORRECTED)
# ---------------------------------------------------------------
def get_glycerol_viscosity(glycerol_pct, temp_c):
    """Cheng (2008) CORRECTED formula for glycerol-water mixtures. Returns Pa.s.

    Correct formula:
        eta_m = eta_w^alpha * eta_g^(1-alpha)
        alpha = 1 - cm + (a*b*cm*(1-cm)) / (a*cm + b*(1-cm))
        a = 0.705 - 0.0017*T
        b = (4.9 + 0.036*T) * a^2.5
    """
    T = temp_c
    # Pure water viscosity (mPa.s)
    eta_water = 1.790 * np.exp((-1230 - T) * T / (36100 + 360 * T))
    if glycerol_pct <= 0:
        return eta_water * 1e-3  # Pa.s

    # Pure glycerol viscosity (mPa.s)
    eta_glycerol = 12100.0 * np.exp((-1233 + T) * T / (9900 + 70 * T))

    cm = glycerol_pct / 100.0
    a = 0.705 - 0.0017 * T
    b = (4.9 + 0.036 * T) * a ** 2.5
    alpha = 1.0 - cm + (a * b * cm * (1 - cm)) / (a * cm + b * (1 - cm))

    eta_m = eta_water ** alpha * eta_glycerol ** (1 - alpha)  # mPa.s
    return eta_m * 1e-3  # Pa.s


def get_acetone_viscosity(acetone_vol_pct, temp_c):
    """Acetone-water mixture viscosity (Pa.s) via interpolation.
    Based on Howard & McAllister (1958) data at ~20-25 C.
    """
    T = temp_c
    eta_water = 1.790 * np.exp((-1230 - T) * T / (36100 + 360 * T)) * 1e-3  # Pa.s
    if acetone_vol_pct <= 0:
        return eta_water
    vol_pct = np.array([0, 5, 10, 15, 20, 30, 40, 50, 60, 80, 100])
    eta_mPa = np.array([0.978, 0.94, 0.90, 0.86, 0.82, 0.72, 0.62, 0.52, 0.44, 0.36, 0.32])
    eta = np.interp(acetone_vol_pct, vol_pct, eta_mPa) * 1e-3  # Pa.s
    return eta


def get_viscosity(solute_pct, temp_c, solute_type='glycerol'):
    """Dispatch to correct viscosity function based on solute type."""
    if solute_type == 'acetone':
        return get_acetone_viscosity(solute_pct, temp_c)
    else:
        return get_glycerol_viscosity(solute_pct, temp_c)


# ---------------------------------------------------------------
# Correction factors (Faxen wall, Batchelor concentration)
# ---------------------------------------------------------------
def faxen_correction(bead_radius_m, wall_dist_m):
    """Faxen's Law parallel wall correction. Returns factor <= 1 to multiply D0 by.
    D_parallel = D0 * [1 - 9/16*(R/h) + 1/8*(R/h)^3 - 45/256*(R/h)^4 - 1/16*(R/h)^5]
    """
    x = bead_radius_m / wall_dist_m  # R/h
    return 1 - 9/16 * x + 1/8 * x**3 - 45/256 * x**4 - 1/16 * x**5


# ---------------------------------------------------------------
# Tracking functions (from track_onion_particles.py)
# ---------------------------------------------------------------
def compute_temporal_median(cap, sample_every=10):
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_sampled = []
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    for i in range(0, total_frames, sample_every):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        frames_sampled.append(gray.astype(np.float32))
    if len(frames_sampled) == 0:
        raise RuntimeError('Could not read any frames from video')
    print(f'  Sampled {len(frames_sampled)} frames for background estimation')
    return np.median(np.stack(frames_sampled), axis=0).astype(np.uint8)


def detect_particles(gray_frame, background, threshold, blur_sigma,
                     min_area, max_area):
    ksize = int(blur_sigma * 4) | 1
    blurred = cv2.GaussianBlur(gray_frame, (ksize, ksize), blur_sigma)
    diff = cv2.absdiff(blurred, background)
    _, binary = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    n_labels, labels, stats, centroids_cv = cv2.connectedComponentsWithStats(
        binary, connectivity=8)
    particles = []
    for label_id in range(1, n_labels):
        area = stats[label_id, cv2.CC_STAT_AREA]
        if area < min_area or area > max_area:
            continue
        mask = (labels == label_id)
        weights = diff[mask].astype(np.float64)
        weight_sum = weights.sum()
        if weight_sum > 0:
            ys, xs = np.where(mask)
            cx = np.average(xs.astype(np.float64), weights=weights)
            cy = np.average(ys.astype(np.float64), weights=weights)
        else:
            cx = centroids_cv[label_id, 0]
            cy = centroids_cv[label_id, 1]
        particles.append((cx, cy))
    return particles, binary


def track_all_frames(detections_per_frame, max_disp, max_gap, min_length):
    all_tracks = []
    active_tracks = []
    next_id = 1
    frame_numbers = sorted(detections_per_frame.keys())
    for frame_num in frame_numbers:
        curr_detections = detections_per_frame[frame_num]
        prev_positions = []
        prev_track_indices = []
        prev_gap_sizes = []
        for i, track in enumerate(active_tracks):
            gap = frame_num - track['last_seen_frame']
            if gap <= max_gap + 1:
                pos = track['positions'][track['last_seen_frame']]
                prev_positions.append(pos)
                prev_track_indices.append(i)
                prev_gap_sizes.append(gap)
        effective_max_disps = [max_disp * g for g in prev_gap_sizes]
        if len(prev_positions) > 0 and len(curr_detections) > 0:
            n_prev = len(prev_positions)
            n_curr = len(curr_detections)
            INF = 1e9
            cost = np.full((n_prev, n_curr), INF)
            for i, (px, py) in enumerate(prev_positions):
                for j, (cx, cy) in enumerate(curr_detections):
                    d = np.sqrt((px - cx)**2 + (py - cy)**2)
                    if d <= effective_max_disps[i]:
                        cost[i, j] = d
            row_ind, col_ind = linear_sum_assignment(cost)
            matches = {}
            for r, c in zip(row_ind, col_ind):
                if cost[r, c] < INF:
                    matches[r] = c
            matched_curr = set(matches.values())
            unmatched_curr = [j for j in range(n_curr) if j not in matched_curr]
        else:
            matches = {}
            unmatched_curr = list(range(len(curr_detections)))
        for prev_idx, curr_idx in matches.items():
            track_idx = prev_track_indices[prev_idx]
            track = active_tracks[track_idx]
            gap = frame_num - track['last_seen_frame']
            track['positions'][frame_num] = curr_detections[curr_idx]
            track['flags'][frame_num] = '*' if gap > 1 else ' '
            track['last_seen_frame'] = frame_num
            track['end_frame'] = frame_num
        still_active = []
        for i, track in enumerate(active_tracks):
            if frame_num - track['last_seen_frame'] > max_gap:
                all_tracks.append(track)
            else:
                still_active.append(track)
        active_tracks = still_active
        for curr_idx in unmatched_curr:
            new_track = {
                'id': next_id,
                'positions': {frame_num: curr_detections[curr_idx]},
                'flags': {frame_num: ' '},
                'start_frame': frame_num,
                'end_frame': frame_num,
                'last_seen_frame': frame_num,
            }
            active_tracks.append(new_track)
            next_id += 1
    all_tracks.extend(active_tracks)
    return all_tracks


def clean_tracks(tracks, min_length, min_displacement):
    cleaned = []
    for track in tracks:
        frames = sorted(track['positions'].keys())
        if len(frames) < min_length:
            continue
        first = track['positions'][frames[0]]
        last = track['positions'][frames[-1]]
        net_disp = np.sqrt((last[0] - first[0])**2 + (last[1] - first[1])**2)
        if net_disp < min_displacement:
            continue
        cleaned.append(track)
    for i, track in enumerate(cleaned, 1):
        track['id'] = i
    return cleaned


def write_mtrack2_format(tracks, total_frames, output_path):
    n_tracks = len(tracks)
    with open(output_path, 'w') as f:
        header_parts = ['Frame']
        for i in range(1, n_tracks + 1):
            header_parts.extend([f'X{i}', f'Y{i}', f'Flag{i}'])
        f.write('\t'.join(header_parts) + '\n')
        f.write(f'Tracks 1 to {n_tracks}\n')
        for frame in range(1, total_frames + 1):
            row_parts = [str(frame)]
            for track in tracks:
                if frame in track['positions']:
                    x, y = track['positions'][frame]
                    flag = track['flags'].get(frame, ' ')
                    row_parts.extend([f'{x:.5f}', f'{y:.5f}', flag])
                else:
                    row_parts.extend([' ', ' ', ' '])
            f.write('\t'.join(row_parts) + '\n')
        f.write('\n')
        f.write('Track \tLength\tDistance traveled\tNr of Frames\n')
        for i, track in enumerate(tracks, 1):
            frames = sorted(track['positions'].keys())
            path_length = 0.0
            for j in range(1, len(frames)):
                p1 = track['positions'][frames[j - 1]]
                p2 = track['positions'][frames[j]]
                path_length += np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            start = track['positions'][frames[0]]
            end = track['positions'][frames[-1]]
            distance = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            f.write(f'{i}\t{path_length:.5f}\t{distance:.5f}\t{len(frames)}\n')

# ---------------------------------------------------------------
# Analysis functions (from Diffusion_Analysis_Corrected.ipynb)
# ---------------------------------------------------------------
def load_mtrack2_data(file_path):
    my_data = np.genfromtxt(file_path, delimiter='\t', skip_header=2,
                           skip_footer=1, invalid_raise=False)
    A = np.zeros(my_data.shape[1] // 3 + 1, dtype=int)
    for i in range(my_data.shape[1] // 3 + 1):
        A[i] = 3 * i
    new_data = np.delete(my_data, A, axis=1)
    mask = np.isnan(new_data)
    new_mask = np.zeros(mask.shape)
    for ind, value in enumerate(mask):
        new_mask[ind, :] = ~value * (ind + 1)
    new_mask = new_mask.astype(np.int_)
    for row_index, row in enumerate(new_mask):
        for col_index, item in enumerate(row):
            if item == 0:
                new_mask[row_index][col_index] = new_mask.shape[0] + 5
    for i in range(new_mask.shape[1]):
        new_mask[:, i] = np.sort(new_mask[:, i])
    data = np.empty((mask.shape[0], mask.shape[1]))
    data[:, :] = np.nan
    for i in range(new_mask.shape[0]):
        for j in range(new_mask.shape[1]):
            temp = new_mask[i, j]
            if temp < new_mask.shape[0]:
                data[i, j] = new_data[temp, j]
    return data


def split_tracks_at_jumps(data, min_length, max_jump_px):
    segments = []
    n_particles = data.shape[1] // 2
    segment_id = 0
    for i in range(n_particles):
        x_col = i * 2
        y_col = i * 2 + 1
        x_raw = data[:, x_col]
        y_raw = data[:, y_col]
        valid_mask = ~np.isnan(x_raw) & ~np.isnan(y_raw)
        x_clean = x_raw[valid_mask]
        y_clean = y_raw[valid_mask]
        if len(x_clean) < min_length:
            continue
        dx = np.diff(x_clean)
        dy = np.diff(y_clean)
        steps = np.sqrt(dx**2 + dy**2)
        bad_jump_indices = np.where(steps > max_jump_px)[0]
        if len(bad_jump_indices) == 0:
            segment_id += 1
            segments.append({'x': x_clean, 'y': y_clean, 'id': segment_id,
                             'original_particle': i + 1, 'length': len(x_clean)})
        else:
            split_indices = bad_jump_indices + 1
            x_segments = np.split(x_clean, split_indices)
            y_segments = np.split(y_clean, split_indices)
            for x_seg, y_seg in zip(x_segments, y_segments):
                if len(x_seg) >= min_length:
                    segment_id += 1
                    segments.append({'x': x_seg, 'y': y_seg, 'id': segment_id,
                                     'original_particle': i + 1, 'length': len(x_seg)})
    segments.sort(key=lambda s: s['length'], reverse=True)
    return segments

# ---------------------------------------------------------------
# Fit helpers
# ---------------------------------------------------------------
def gaussian(x, amplitude, mean, std_dev):
    return amplitude * np.exp(-(x - mean)**2 / (2 * std_dev**2))

def compute_chi_squared(observed, expected, errors, n_params):
    valid = errors > 0
    if np.sum(valid) <= n_params:
        return np.nan, np.nan, 0, np.nan
    residuals = (observed[valid] - expected[valid]) / errors[valid]
    chi2 = np.sum(residuals**2)
    dof = np.sum(valid) - n_params
    chi2_red = chi2 / dof if dof > 0 else np.nan
    pval = 1 - chi2_dist.cdf(chi2, dof) if dof > 0 else np.nan
    return chi2, chi2_red, dof, pval

def linear(t, slope, intercept):
    return slope * t + intercept

def power_law(t, K, alpha):
    return K * t**alpha

print('All functions loaded.')

# Quick viscosity sanity check
for _gp in [0, 20, 36.3]:
    _eta = get_glycerol_viscosity(_gp, 21.0) * 1e3
    print(f'  Glycerol {_gp}% at 21C: {_eta:.3f} mPa.s')


# In[ ]:


# ============================================================================
# CELL 3 — MAIN PROCESSING LOOP
# ============================================================================

TEMPERATURE = TEMPERATURE_C + 273.15
NOTEBOOK_DIR = Path(os.getcwd())

n_total = len(JOBS)
n_skipped = 0
n_processed = 0
n_failed = 0
batch_results = []

for job_idx, (avi_path_str, bead_diameter_um, solute_pct, solute_type) in enumerate(JOBS, 1):

    # --- Parse path ---
    avi_path = Path(avi_path_str)
    parts = avi_path.parts
    idx = [i for i, p in enumerate(parts) if p.lower() == 'data']
    if idx:
        date_folder = parts[idx[-1] + 1]
    else:
        date_folder = avi_path.parent.name
    file_stem = avi_path.stem
    FIGURES_DIR = NOTEBOOK_DIR / 'figures' / date_folder / file_stem

    # --- Skip check ---
    summary_file = FIGURES_DIR / 'summary.txt'
    if summary_file.exists() and not FORCE_REPROCESS:
        print(f'\n[{job_idx}/{n_total}] SKIP: {avi_path.name} (already processed)')
        n_skipped += 1
        continue

    solute_label = solute_type.capitalize()  # "Glycerol" or "Acetone"
    print(f'\n{"=" * 70}')
    print(f'[{job_idx}/{n_total}] PROCESSING: {avi_path.name}')
    print(f'  Bead: {bead_diameter_um} um | {solute_label}: {solute_pct}% | Date: {date_folder}')
    print(f'{"=" * 70}')

    # --- Validate file ---
    if not avi_path.exists():
        print(f'  ERROR: File not found! Skipping.')
        n_failed += 1
        continue

    # --- Auto area range from bead size ---
    _bead_radius_px = (bead_diameter_um / 2) / PIXEL_SIZE
    _bead_area_px = math.pi * _bead_radius_px**2
    min_particle_area = max(4, int(_bead_area_px * 0.1))
    max_particle_area = max(200, int(_bead_area_px * 6))

    # --- Viscosity ---
    viscosity = get_viscosity(solute_pct, TEMPERATURE_C, solute_type)
    print(f'  Viscosity: {viscosity*1e3:.3f} mPa.s ({viscosity:.6f} Pa.s)')
    print(f'  Particle area range: {min_particle_area} - {max_particle_area} px^2')

    # --- Create output directory ---
    if FIGURES_DIR.exists():
        shutil.rmtree(FIGURES_DIR)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # ==============================================================
        # STEP 1: TRACKING
        # ==============================================================
        print(f'\n  STEP 1: Tracking...')
        cap = cv2.VideoCapture(str(avi_path))
        if not cap.isOpened():
            raise RuntimeError(f'Cannot open video: {avi_path}')

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Read fps from video file (NOT hardcoded)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 29.0  # fallback for broken metadata
            print(f'  WARNING: Could not read fps, using fallback {fps}')
        dt = 1.0 / fps

        print(f'  Video: {width}x{height}, {total_frames} frames, {fps:.1f} fps, {total_frames/fps:.2f} s')
        print(f'  dt = {dt*1000:.2f} ms/frame')

        t0 = time.time()
        background = compute_temporal_median(cap, sample_every=10)

        detections_per_frame = {}
        first_frame_gray = None
        first_frame_binary = None
        first_frame_particles = None
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for frame_num in range(1, total_frames + 1):
            ret, frame = cap.read()
            if not ret:
                total_frames = frame_num - 1
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
            particles, binary = detect_particles(gray, background, DETECTION_THRESHOLD,
                                             GAUSSIAN_BLUR_SIGMA, min_particle_area,
                                             max_particle_area)
            detections_per_frame[frame_num] = particles
            # Save first frame for mask map
            if frame_num == 1:
                first_frame_gray = gray.copy()
                first_frame_binary = binary.copy()
                first_frame_particles = particles
        cap.release()

        counts = [len(detections_per_frame.get(f, [])) for f in range(1, total_frames + 1)]
        print(f'  Particles/frame: min={min(counts)}, max={max(counts)}, mean={np.mean(counts):.1f}')

        raw_tracks = track_all_frames(detections_per_frame, MAX_DISPLACEMENT, MAX_GAP_FRAMES, 1)
        tracks = clean_tracks(raw_tracks, MIN_TRACK_LENGTH, MIN_TOTAL_DISPLACEMENT)
        print(f'  Tracks: {len(raw_tracks)} raw -> {len(tracks)} valid ({time.time()-t0:.1f} s)')

        if len(tracks) == 0:
            raise RuntimeError('No valid tracks found!')

        track_output = str(FIGURES_DIR / 'trackresults.txt')
        write_mtrack2_format(tracks, total_frames, track_output)

        # --- DETECTION MASK MAP ---
        print(f'  Generating detection mask map...')
        fig_mask, axes_mask = plt.subplots(1, 3, figsize=(18, 6))

        # Panel 1: Raw frame
        axes_mask[0].imshow(first_frame_gray, cmap='gray')
        axes_mask[0].set_title('Raw Frame (frame 1)')
        axes_mask[0].axis('off')

        # Panel 2: Binary mask (what the detector sees)
        axes_mask[1].imshow(first_frame_binary, cmap='gray')
        axes_mask[1].set_title(f'Detection Mask (threshold={DETECTION_THRESHOLD})')
        axes_mask[1].axis('off')

        # Panel 3: Overlay — detected particles circled on raw frame
        overlay = cv2.cvtColor(first_frame_gray, cv2.COLOR_GRAY2RGB)
        r_circle = max(5, int(_bead_radius_px * 1.5))
        for (cx, cy) in first_frame_particles:
            cv2.circle(overlay, (int(cx), int(cy)), r_circle, (0, 255, 0), 2)
            cv2.circle(overlay, (int(cx), int(cy)), 2, (255, 0, 0), -1)
        axes_mask[2].imshow(overlay)
        axes_mask[2].set_title(f'Detected: {len(first_frame_particles)} particles')
        axes_mask[2].axis('off')

        fig_mask.suptitle(f'{avi_path.name} — Detection Mask Map', fontsize=13)
        plt.tight_layout()
        fig_mask.savefig(str(FIGURES_DIR / 'detection_mask.png'), dpi=200, bbox_inches='tight')
        plt.show()

        # ==============================================================
        # STEP 2: LOAD & SEGMENT
        # ==============================================================
        print(f'  STEP 2: Segmenting tracks...')
        data = load_mtrack2_data(track_output)
        segments = split_tracks_at_jumps(data, MIN_SEGMENT_LENGTH, MAX_JUMP_PX)

        if len(segments) == 0:
            raise RuntimeError('No valid segments!')

        n_to_use = min(NUM_BEST_SEGMENTS, len(segments))
        selected = segments[:n_to_use]
        print(f'  Segments: {len(segments)} total, using top {n_to_use}')

        # ==============================================================
        # STEP 3: TRAJECTORY PLOT
        # ==============================================================
        print(f'  STEP 3: Trajectory plot...')
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        colors = plt.cm.tab10(np.linspace(0, 1, n_to_use))

        ax = axes[0]
        for seg, c in zip(selected, colors):
            ax.plot(seg['x'], seg['y'], '-', linewidth=1, color=c, alpha=0.7)
            ax.plot(seg['x'][0], seg['y'][0], 'o', color=c, markersize=4)
            ax.plot(seg['x'][-1], seg['y'][-1], 's', color=c, markersize=4)
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.set_title(f'Top {n_to_use} Trajectories')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        for seg, c in zip(selected, colors):
            x_um = (seg['x'] - seg['x'][0]) * PIXEL_SIZE
            y_um = (seg['y'] - seg['y'][0]) * PIXEL_SIZE
            ax.plot(x_um, y_um, '-o', markersize=1, linewidth=1, color=c, alpha=0.7)
        ax.set_xlabel(r'$\Delta X$ ($\mu$m)')
        ax.set_ylabel(r'$\Delta Y$ ($\mu$m)')
        ax.set_title(f'Displacement from Start ({PIXEL_SIZE*1000:.1f} nm/px)')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        fig.savefig(str(FIGURES_DIR / 'trajectories.png'), dpi=300, bbox_inches='tight')
        plt.show()

        # ==============================================================
        # STEP 4: DISPLACEMENT HISTOGRAM + GAUSSIAN FIT
        # ==============================================================
        print(f'  STEP 4: Displacement analysis...')
        all_dx = []
        all_dy = []
        for seg in selected:
            all_dx.extend(np.diff(seg['x']))
            all_dy.extend(np.diff(seg['y']))

        dx_px = np.array(all_dx)
        dy_px = np.array(all_dy)
        dx_um = dx_px * PIXEL_SIZE
        dy_um = dy_px * PIXEL_SIZE
        n_steps = len(dx_px)

        # METHOD 1: Direct Variance
        var_dx = np.var(dx_px)
        var_dy = np.var(dy_px)
        D_x_direct = var_dx * PIXEL_SIZE**2 / (2 * dt)
        D_y_direct = var_dy * PIXEL_SIZE**2 / (2 * dt)
        D_direct = (D_x_direct + D_y_direct) / 2
        D_direct_err = abs(D_x_direct - D_y_direct) / 2

        # METHOD 2: Gaussian Fit
        nbins = 20
        counts_x, bin_edges_x = np.histogram(dx_um, bins=nbins)
        bin_centers_x = (bin_edges_x[:-1] + bin_edges_x[1:]) / 2
        counts_err_x = np.sqrt(np.maximum(counts_x, 1))
        try:
            popt_x, pcov_x = curve_fit(gaussian, bin_centers_x, counts_x,
                                        p0=[max(counts_x), 0, np.std(dx_um)])
            std_x_fit = abs(popt_x[2])
        except Exception:
            std_x_fit = np.std(dx_um)
            popt_x = [max(counts_x), 0, std_x_fit]

        counts_y, bin_edges_y = np.histogram(dy_um, bins=nbins)
        bin_centers_y = (bin_edges_y[:-1] + bin_edges_y[1:]) / 2
        counts_err_y = np.sqrt(np.maximum(counts_y, 1))
        try:
            popt_y, pcov_y = curve_fit(gaussian, bin_centers_y, counts_y,
                                        p0=[max(counts_y), 0, np.std(dy_um)])
            std_y_fit = abs(popt_y[2])
        except Exception:
            std_y_fit = np.std(dy_um)
            popt_y = [max(counts_y), 0, std_y_fit]

        D_x_fit = std_x_fit**2 / (2 * dt)
        D_y_fit = std_y_fit**2 / (2 * dt)
        D_fit = (D_x_fit + D_y_fit) / 2
        D_fit_err = abs(D_x_fit - D_y_fit) / 2

        # Histogram plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        ax = axes[0]
        ax.bar(bin_centers_x, counts_x, width=bin_edges_x[1]-bin_edges_x[0],
               alpha=0.6, color='steelblue', label='Data')
        x_fine = np.linspace(bin_centers_x[0], bin_centers_x[-1], 200)
        ax.plot(x_fine, gaussian(x_fine, *popt_x), 'r-', linewidth=2,
                label=f'Gaussian fit\n$\\sigma$ = {std_x_fit:.4f} $\\mu$m')
        ax.set_xlabel(r'$\Delta x$ per frame ($\mu$m)')
        ax.set_ylabel('Count')
        ax.set_title(f'X Displacement \u2014 D_x = {D_x_fit:.4f} $\\mu$m$^2$/s')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        ax.bar(bin_centers_y, counts_y, width=bin_edges_y[1]-bin_edges_y[0],
               alpha=0.6, color='darkorange', label='Data')
        y_fine = np.linspace(bin_centers_y[0], bin_centers_y[-1], 200)
        ax.plot(y_fine, gaussian(y_fine, *popt_y), 'r-', linewidth=2,
                label=f'Gaussian fit\n$\\sigma$ = {std_y_fit:.4f} $\\mu$m')
        ax.set_xlabel(r'$\Delta y$ per frame ($\mu$m)')
        ax.set_ylabel('Count')
        ax.set_title(f'Y Displacement \u2014 D_y = {D_y_fit:.4f} $\\mu$m$^2$/s')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        fig.savefig(str(FIGURES_DIR / 'displacement_histogram.png'), dpi=300, bbox_inches='tight')
        plt.show()

        # ==============================================================
        # STEP 5: MSD ANALYSIS + ALPHA EXPONENT
        # ==============================================================
        print(f'  STEP 5: MSD analysis...')
        min_track = min([seg['length'] for seg in selected])
        max_lag = min(min_track // 2, 30)

        all_MSDs = []
        for seg in selected:
            x = seg['x'].copy()
            y = seg['y'].copy()
            MSD_seg = np.zeros(max_lag)
            n_frames = len(x)
            for lag in range(max_lag):
                dx_lag = x[lag+1:] - x[:n_frames-lag-1]
                dy_lag = y[lag+1:] - y[:n_frames-lag-1]
                r_sq = dx_lag**2 + dy_lag**2
                MSD_seg[lag] = np.mean(r_sq) if len(r_sq) > 0 else 0
            all_MSDs.append(MSD_seg)

        all_MSDs = np.array(all_MSDs)
        MSD_px = np.mean(all_MSDs, axis=0)
        MSD_err_px = np.std(all_MSDs, axis=0) / np.sqrt(len(selected))
        MSD_um = MSD_px * PIXEL_SIZE**2
        MSD_err_um = MSD_err_px * PIXEL_SIZE**2
        lag_times = np.arange(max_lag) * dt

        # Linear fit for D
        n_fit = max_lag // 4
        fit_times = lag_times[1:n_fit+1]
        fit_MSD = MSD_um[1:n_fit+1]
        fit_err = MSD_err_um[1:n_fit+1]
        fit_err = np.where(fit_err > 0, fit_err, 1e-10)

        try:
            popt_msd, pcov_msd = curve_fit(linear, fit_times, fit_MSD,
                                            sigma=fit_err, absolute_sigma=True, p0=[1, 0])
            perr_msd = np.sqrt(np.diag(pcov_msd))
            slope = popt_msd[0]
            slope_err = perr_msd[0]
            intercept = popt_msd[1]
        except Exception:
            coeffs = np.polyfit(fit_times, fit_MSD, 1)
            slope = coeffs[0]
            slope_err = 0
            intercept = coeffs[1]

        D_msd = slope / 4
        D_msd_err = slope_err / 4

        # Power-law for alpha
        n_fit_power = max_lag // 2
        pl_t = lag_times[1:n_fit_power+1]
        pl_msd = MSD_um[1:n_fit_power+1]
        pl_err = MSD_err_um[1:n_fit_power+1]
        pl_err = np.where(pl_err > 0, pl_err, 1e-10)

        try:
            popt_pl, pcov_pl = curve_fit(power_law, pl_t, pl_msd,
                                          sigma=pl_err, absolute_sigma=True,
                                          p0=[0.001, 1.0], maxfev=5000)
            perr_pl = np.sqrt(np.diag(pcov_pl))
            K_fit = popt_pl[0]
            alpha_fit = popt_pl[1]
            alpha_err = perr_pl[1]
        except Exception:
            log_t = np.log(pl_t)
            log_msd = np.log(pl_msd)
            coeffs = np.polyfit(log_t, log_msd, 1)
            alpha_fit = coeffs[0]
            K_fit = np.exp(coeffs[1])
            alpha_err = 0

        if alpha_fit > 1.7:
            motion_type = 'BALLISTIC / DIRECTED'
        elif alpha_fit > 1.2:
            motion_type = 'SUPERDIFFUSIVE'
        elif alpha_fit > 0.8:
            motion_type = 'DIFFUSIVE (Brownian)'
        else:
            motion_type = 'SUBDIFFUSIVE (confined)'

        print(f'  D_MSD = {D_msd:.4f} um^2/s, alpha = {alpha_fit:.3f} ({motion_type})')

        # MSD plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        ax = axes[0]
        ax.errorbar(lag_times, MSD_um, yerr=MSD_err_um, fmt='o',
                    markersize=4, capsize=3, alpha=0.6, color='steelblue', label='MSD data')
        fit_line_t = np.linspace(0, lag_times[n_fit], 100)
        ax.plot(fit_line_t, linear(fit_line_t, slope, intercept), 'r-', linewidth=2,
                label=f'Linear fit: D = {D_msd:.4f} $\\pm$ {D_msd_err:.4f} $\\mu$m$^2$/s')
        pl_line_t = np.linspace(dt, lag_times[n_fit_power], 100)
        ax.plot(pl_line_t, power_law(pl_line_t, K_fit, alpha_fit), 'g--', linewidth=2,
                label=f'Power law: $\\alpha$ = {alpha_fit:.2f}')
        ax.set_xlabel('Lag time $\\tau$ (s)', fontsize=12)
        ax.set_ylabel(r'MSD ($\mu$m$^2$)', fontsize=12)
        ax.set_title('MSD \u2014 Linear Scale')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        valid = MSD_um[1:] > 0
        ax.errorbar(lag_times[1:][valid], MSD_um[1:][valid], yerr=MSD_err_um[1:][valid],
                    fmt='o', markersize=4, capsize=3, alpha=0.6, color='steelblue', label='MSD data')
        ref_t = np.logspace(np.log10(dt), np.log10(lag_times[-1]), 50)
        msd_at_1 = MSD_um[1] if MSD_um[1] > 0 else 1e-6
        ax.plot(ref_t, msd_at_1 * (ref_t/dt)**1, 'k:', alpha=0.4, linewidth=1.5,
                label=r'$\alpha=1$ (diffusive)')
        ax.plot(ref_t, msd_at_1 * (ref_t/dt)**2, 'k--', alpha=0.4, linewidth=1.5,
                label=r'$\alpha=2$ (ballistic)')
        ax.plot(pl_line_t, power_law(pl_line_t, K_fit, alpha_fit), 'g-', linewidth=2,
                label=f'Fit: $\\alpha$ = {alpha_fit:.2f} $\\pm$ {alpha_err:.2f}')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Lag time $\\tau$ (s)', fontsize=12)
        ax.set_ylabel(r'MSD ($\mu$m$^2$)', fontsize=12)
        ax.set_title('MSD \u2014 Log-Log Scale')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, which='both')

        plt.tight_layout()
        fig.savefig(str(FIGURES_DIR / 'msd_analysis.png'), dpi=300, bbox_inches='tight')
        plt.show()

        # ==============================================================
        # STEP 6: D COMPARISON (with Faxen wall correction)
        # ==============================================================
        print(f'  STEP 6: Stokes-Einstein comparison...')
        r_m = (bead_diameter_um / 2) * 1e-6
        D_theory = k_B * TEMPERATURE / (6 * pi * viscosity * r_m)
        D_theory_um = D_theory * 1e12

        # Faxen wall correction at chamber midplane
        h_mid = (CHAMBER_DEPTH_UM / 2) * 1e-6
        F_mid = faxen_correction(r_m, h_mid)
        D_theory_faxen = D_theory_um * F_mid

        print(f'  D_theory (S-E base) = {D_theory_um:.4f} um^2/s')
        print(f'  D_theory (+ Faxen)  = {D_theory_faxen:.4f} um^2/s  (F={F_mid:.4f})')
        print(f'  D_direct = {D_direct:.4f}, D_gauss = {D_fit:.4f}, D_msd = {D_msd:.4f}')

        fig, ax = plt.subplots(figsize=(8, 6))
        methods = ['Direct\nVariance', 'Gaussian\nFit', 'MSD\nSlope', 'Stokes-Einstein\n(+Faxen)']
        D_vals = [D_direct, D_fit, D_msd, D_theory_faxen]
        D_errs = [D_direct_err, D_fit_err, D_msd_err, 0]
        bar_colors = ['steelblue', 'darkorange', 'forestgreen', 'crimson']

        bars = ax.bar(methods, D_vals, yerr=D_errs, capsize=5,
                      color=bar_colors, alpha=0.8, edgecolor='black', linewidth=0.5)
        for bar, val in zip(bars, D_vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(D_vals) * 0.02,
                    f'{val:.4f}', ha='center', va='bottom', fontsize=9)
        ax.set_ylabel(r'Diffusion Coefficient $D$ ($\mu$m$^2$/s)', fontsize=12)
        ax.set_title(f'{bead_diameter_um} $\\mu$m beads \u2014 {solute_pct}% {solute_label} \u2014 '
                     f'{PIXEL_SIZE*1000:.1f} nm/px \u2014 {fps:.0f} fps', fontsize=13)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, max(D_vals) * 1.3)

        plt.tight_layout()
        fig.savefig(str(FIGURES_DIR / 'D_comparison.png'), dpi=300, bbox_inches='tight')
        plt.show()

        # ==============================================================
        # STEP 7: SUMMARY
        # ==============================================================
        summary_lines = []
        summary_lines.append('=' * 70)
        summary_lines.append('ANALYSIS SUMMARY')
        summary_lines.append('=' * 70)
        summary_lines.append(f'')
        summary_lines.append(f'Video: {avi_path.name}')
        summary_lines.append(f'Date: {date_folder}')
        summary_lines.append(f'Bead diameter: {bead_diameter_um} um')
        summary_lines.append(f'Solute: {solute_pct}% {solute_label}')
        summary_lines.append(f'Temperature: {TEMPERATURE_C} C ({TEMPERATURE:.2f} K)')
        summary_lines.append(f'Viscosity: {viscosity*1e3:.3f} mPa.s ({viscosity:.6f} Pa.s)')
        summary_lines.append(f'Pixel size: {PIXEL_SIZE} um/px ({PIXEL_SIZE*1000:.1f} nm/px)')
        summary_lines.append(f'Frame rate: {fps:.1f} fps (read from file)')
        summary_lines.append(f'dt: {dt*1000:.2f} ms')
        summary_lines.append(f'')
        summary_lines.append(f'Tracking:')
        summary_lines.append(f'  Total frames: {total_frames}')
        summary_lines.append(f'  Valid tracks: {len(tracks)}')
        summary_lines.append(f'  Segments used: {n_to_use}')
        summary_lines.append(f'  Total displacement steps: {n_steps}')
        summary_lines.append(f'')
        summary_lines.append(f'Diffusion Coefficients (um^2/s):')
        summary_lines.append(f'  Method 1 (Direct Variance): {D_direct:.4f} +/- {D_direct_err:.4f}')
        summary_lines.append(f'  Method 2 (Gaussian Fit):     {D_fit:.4f} +/- {D_fit_err:.4f}')
        summary_lines.append(f'  Method 3 (MSD Slope):        {D_msd:.4f} +/- {D_msd_err:.4f}')
        summary_lines.append(f'')
        summary_lines.append(f'Theory (Stokes-Einstein):')
        summary_lines.append(f'  D_0 (base):      {D_theory_um:.4f} um^2/s')
        summary_lines.append(f'  Faxen factor:     {F_mid:.4f} (midplane, h={CHAMBER_DEPTH_UM/2:.1f} um)')
        summary_lines.append(f'  D_theory (final): {D_theory_faxen:.4f} um^2/s')
        summary_lines.append(f'')
        summary_lines.append(f'Deviations from Theory (S-E + Faxen):')
        for name, D_val in [('Direct Variance', D_direct),
                             ('Gaussian Fit', D_fit),
                             ('MSD Slope', D_msd)]:
            dev = (D_val - D_theory_faxen) / D_theory_faxen * 100
            summary_lines.append(f'  {name}: {dev:+.1f}%')
        summary_lines.append(f'')
        summary_lines.append(f'MSD Exponent:')
        summary_lines.append(f'  alpha = {alpha_fit:.3f} +/- {alpha_err:.3f}')
        summary_lines.append(f'  Classification: {motion_type}')
        summary_lines.append(f'')
        summary_lines.append(f'Figures saved to: {FIGURES_DIR}')
        summary_lines.append('=' * 70)

        summary_text = '\n'.join(summary_lines)
        with open(str(summary_file), 'w') as f:
            f.write(summary_text)

        print(f'  DONE. Saved to: {FIGURES_DIR}')

        # Collect for batch summary
        batch_results.append({
            'video': file_stem,
            'bead_um': bead_diameter_um,
            'solute_pct': solute_pct,
            'solute_type': solute_label,
            'eta_mPas': viscosity * 1e3,
            'fps': fps,
            'n_tracks': len(tracks),
            'n_segs': n_to_use,
            'D_direct': D_direct,
            'D_fit': D_fit,
            'D_msd': D_msd,
            'D_theory': D_theory_um,
            'D_faxen': D_theory_faxen,
            'F_mid': F_mid,
            'alpha': alpha_fit,
        })

        n_processed += 1

    except Exception as e:
        print(f'  FAILED: {e}')
        n_failed += 1

# ======================== BATCH SUMMARY ========================
print(f'\n{"=" * 70}')
print(f'BATCH COMPLETE: {n_processed} processed, {n_skipped} skipped, {n_failed} failed (of {n_total} total)')
print(f'{"=" * 70}')

# ======================== RESULTS TABLE ========================
if batch_results:
    print(f'\n{"=" * 130}')
    print(f'{"BATCH RESULTS -- EXPERIMENT vs THEORY (Stokes-Einstein + Faxen)":^130}')
    print(f'{"=" * 130}')
    print(f'{"Video":<42} {"Bead":>4} {"Solute":>10} {"eta":>8} {"fps":>5} '
          f'{"D_var":>8} {"D_gau":>8} {"D_msd":>8} {"D_SE+F":>8} {"Dev%":>7} {"alpha":>6}')
    print(f'{"":<42} {"(um)":>4} {"":>10} {"mPa.s":>8} {"":>5} '
          f'{"um2/s":>8} {"um2/s":>8} {"um2/s":>8} {"um2/s":>8} {"":>7} {"":>6}')
    print(f'{"-" * 130}')
    for r in batch_results:
        D_avg = np.mean([r['D_direct'], r['D_fit'], r['D_msd']])
        dev = (D_avg - r['D_faxen']) / r['D_faxen'] * 100
        sol = f"{r['solute_pct']:.0f}%{r['solute_type'][:3]}" if r['solute_pct'] > 0 else "Water"
        name = r['video']
        if len(name) > 40:
            name = name[:37] + '...'
        print(f'{name:<42} {r["bead_um"]:>4.1f} {sol:>10} {r["eta_mPas"]:>8.3f} {r["fps"]:>5.0f} '
              f'{r["D_direct"]:>8.4f} {r["D_fit"]:>8.4f} {r["D_msd"]:>8.4f} {r["D_faxen"]:>8.4f} '
              f'{dev:>+7.1f} {r["alpha"]:>6.2f}')
    print(f'{"=" * 130}')


# In[ ]:


# ============================================================================
# CELL 4 — OVERALL TREND PLOTS (across all processed datasets)
# ============================================================================
# Uses batch_results collected in Cell 3

if not batch_results:
    print('No batch results to plot. Run Cell 3 first.')
else:
    import matplotlib.pyplot as plt
    import numpy as np

    # Convert to arrays for easier plotting
    beads = np.array([r['bead_um'] for r in batch_results])
    etas = np.array([r['eta_mPas'] for r in batch_results])
    D_vars = np.array([r['D_direct'] for r in batch_results])
    D_gaus = np.array([r['D_fit'] for r in batch_results])
    D_msds = np.array([r['D_msd'] for r in batch_results])
    D_thys = np.array([r['D_faxen'] for r in batch_results])
    alphas = np.array([r['alpha'] for r in batch_results])
    D_avgs = (D_vars + D_gaus + D_msds) / 3
    solute_types = [r['solute_type'] for r in batch_results]
    solute_pcts = np.array([r['solute_pct'] for r in batch_results])

    # Color by condition
    cond_colors = {}
    cond_list = []
    for r in batch_results:
        sol = f"{r['solute_pct']:.0f}% {r['solute_type']}" if r['solute_pct'] > 0 else "Water"
        cond = f"{r['bead_um']} um, {sol}"
        if cond not in cond_colors:
            cond_colors[cond] = len(cond_colors)
        cond_list.append(cond)
    palette = plt.cm.Set1(np.linspace(0, 1, max(len(cond_colors), 2)))

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # ── Plot 1: D_exp vs D_theory (parity plot) ──
    ax = axes[0, 0]
    for cond, cidx in cond_colors.items():
        mask = [c == cond for c in cond_list]
        ax.scatter(D_thys[mask], D_avgs[mask], color=palette[cidx], s=60,
                   label=cond, edgecolors='black', linewidth=0.5, zorder=3)
    # Parity line
    dmax = max(max(D_avgs), max(D_thys)) * 1.2
    dmin = 0
    ax.plot([dmin, dmax], [dmin, dmax], 'k--', linewidth=1.5, alpha=0.5, label='Perfect agreement')
    ax.set_xlabel(r'$D_{theory}$ (Stokes-Einstein + Faxen) [$\mu$m$^2$/s]', fontsize=11)
    ax.set_ylabel(r'$D_{experiment}$ (avg of 3 methods) [$\mu$m$^2$/s]', fontsize=11)
    ax.set_title('Experiment vs Theory — Parity Plot')
    ax.legend(fontsize=8, loc='upper left')
    ax.set_xlim(dmin, dmax)
    ax.set_ylim(dmin, dmax)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # ── Plot 2: D vs Viscosity ──
    ax = axes[0, 1]
    for cond, cidx in cond_colors.items():
        mask = [c == cond for c in cond_list]
        ax.scatter(etas[mask], D_avgs[mask], color=palette[cidx], s=60,
                   label=cond, edgecolors='black', linewidth=0.5, zorder=3)
        ax.scatter(etas[mask], D_thys[mask], color=palette[cidx], s=30,
                   marker='x', linewidth=1.5, zorder=2)
    # Theory curve for 3um beads
    eta_range = np.linspace(0.5, max(etas) * 1.2, 100)
    r_3um = 1.5e-6
    D_curve = k_B * TEMPERATURE / (6 * pi * eta_range * 1e-3 * r_3um) * 1e12
    ax.plot(eta_range, D_curve, 'k--', alpha=0.4, linewidth=1.5, label='S-E theory (3 um)')
    ax.set_xlabel(r'Viscosity $\eta$ [mPa$\cdot$s]', fontsize=11)
    ax.set_ylabel(r'$D$ [$\mu$m$^2$/s]', fontsize=11)
    ax.set_title(r'$D$ vs Viscosity (circles=exp, x=theory)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # ── Plot 3: D vs Bead Size ──
    ax = axes[1, 0]
    for cond, cidx in cond_colors.items():
        mask = [c == cond for c in cond_list]
        ax.scatter(beads[mask], D_avgs[mask], color=palette[cidx], s=60,
                   label=cond, edgecolors='black', linewidth=0.5, zorder=3)
        ax.scatter(beads[mask], D_thys[mask], color=palette[cidx], s=30,
                   marker='x', linewidth=1.5, zorder=2)
    # Theory curve for water
    bead_range = np.linspace(0.5, 6, 100)
    eta_water = get_glycerol_viscosity(0, TEMPERATURE_C)
    D_bead_curve = k_B * TEMPERATURE / (6 * pi * eta_water * (bead_range/2)*1e-6) * 1e12
    ax.plot(bead_range, D_bead_curve, 'k--', alpha=0.4, linewidth=1.5, label='S-E theory (water)')
    ax.set_xlabel(r'Bead diameter [$\mu$m]', fontsize=11)
    ax.set_ylabel(r'$D$ [$\mu$m$^2$/s]', fontsize=11)
    ax.set_title(r'$D$ vs Bead Size (circles=exp, x=theory)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # ── Plot 4: Alpha exponent distribution ──
    ax = axes[1, 1]
    for cond, cidx in cond_colors.items():
        mask = [c == cond for c in cond_list]
        indices = np.where(mask)[0]
        ax.barh([batch_results[i]['video'][-20:] for i in indices],
                alphas[mask], color=palette[cidx], edgecolor='black', linewidth=0.5,
                label=cond, alpha=0.8)
    ax.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label=r'$\alpha=1$ (Brownian)')
    ax.set_xlabel(r'MSD Exponent $\alpha$', fontsize=11)
    ax.set_title(r'MSD Exponent $\alpha$ — Motion Classification')
    ax.legend(fontsize=7, loc='upper right')
    ax.grid(True, alpha=0.3, axis='x')

    plt.suptitle('Overall Trends Across All Datasets', fontsize=15, fontweight='bold')
    plt.tight_layout()

    # Save to figures root
    trend_dir = NOTEBOOK_DIR / 'figures'
    trend_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(trend_dir / 'overall_trends.png'), dpi=300, bbox_inches='tight')
    plt.show()
    print(f'Saved overall trend plot to: {trend_dir / "overall_trends.png"}')

