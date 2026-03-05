# Auto-generated from Lab2_Analysis_Pipeline.ipynb
# Run with: python _run_pipeline.py
import matplotlib
matplotlib.use('Agg')
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ======================================================================
# CELL 1
# ======================================================================
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

# --- Session 7 (2026-03-03) ---
# Water (0% glycerol)
r1     = DATA + r"\2026-03-03\r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi"
r2_t1  = DATA + r"\2026-03-03\r2-2_1mu-0_5p-4ul-water-498ul-gly-0l-trial1.avi"
r2_t2  = DATA + r"\2026-03-03\r2-2_1mu-0_5p-4ul-water-498ul-gly-0l-trial2.avi"
r3_t1  = DATA + r"\2026-03-03\r3-trial1.avi"
r3_t2  = DATA + r"\2026-03-03\r3-Trial2.avi"
r4_t1  = DATA + r"\2026-03-03\r4-5mu-0_5p-10ul-water-490ul-gly-0-trial1.avi"
r4_t2  = DATA + r"\2026-03-03\r4-5mu-0_5p-10ul-water-490ul-gly-0-trial2.avi"

# 20% glycerol (100 uL gly / 500 uL total)
r5_t1  = DATA + r"\2026-03-03\r5-1mu-0_5p-1_15ul-water-400ul-gly-100ul-trial1.avi"
r6_t1  = DATA + r"\2026-03-03\r6-2_1mu-0_5p-4ul-water-398ul-gly-100l-trial1.avi"
r6_t2  = DATA + r"\2026-03-03\r6-2_1mu-0_5p-4ul-water-398ul-gly-100l-trial2.avi"
r7_t1  = DATA + r"\2026-03-03\r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial1.avi"
r7_t2  = DATA + r"\2026-03-03\r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial2.avi"
r7_t3  = DATA + r"\2026-03-03\r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial3-best.avi"
r8_t1  = DATA + r"\2026-03-03\r8-5mu-0_5p-20ul-water-390ul-gly-100ul-trial1.avi"
r8_t2  = DATA + r"\2026-03-03\r8-5mu-0_5p-20ul-water-390ul-gly-100ul-trial2.avi"
r8_t3  = DATA + r"\2026-03-03\r8-5mu-0_5p-20ul-water-390ul-gly-100ul-trial3.avi"

# 40% glycerol (200 uL gly / 500 uL total)
r10_t1 = DATA + r"\2026-03-03\r10-2_1mu-0_5p-4ul-water-298ul-gly-200ul-trial1.avi"
r10_t2 = DATA + r"\2026-03-03\r10-2_1mu-0_5p-4ul-water-298ul-gly-200ul-trial2.avi"
r11_t1 = DATA + r"\2026-03-03\r11-3mu-0_5p-6ul-water-297ul-gly-200ul-trial1.avi"
r11_t2 = DATA + r"\2026-03-03\r11-3mu-0_5p-6ul-water-297ul-gly-200ul-trial2.avi"
r12_a  = DATA + r"\2026-03-03\r12-5mu-0_5p-10ul-water-290ul-gly-200ul-trial3-best.avi"
r12_b  = DATA + r"\2026-03-03\r12-5mu-0_5p-20ul-water-290ul-gly-200ul-trial2-new-contrast-from-new-focus.avi"
r12_c  = DATA + r"\2026-03-03\r12-5mu-0_5p-20ul-water-290ul-gly-200ul-trial3-best.avi"

# Pure acetone (no water)
r14_t1 = DATA + r"\2026-03-03\r14-2_1mu-0_5p-4ul-acetone-498ul-trial1.avi"
r14_t2 = DATA + r"\2026-03-03\r14-2_1mu-0_5p-4ul-acetone-498ul-trial2.avi"
r15_t1 = DATA + r"\2026-03-03\r15-3mu-0_5p-6ul-acetone-497ul-trial1.avi"
r16_t1 = DATA + r"\2026-03-03\r16-5mu-0_5p-20ul-acetone-490-trial1.avi"
r16_t2 = DATA + r"\2026-03-03\r16-5mu-0_5p-20ul-acetone-490-trial2.avi"
# r16_t3 EXCLUDED — only 9 MB (truncated/corrupt; others are 1.1 GB)
r16_t4 = DATA + r"\2026-03-03\r16-5mu-0_5p-20ul-acetone-490-trial4.avi"

# --- JOBS LIST ---
# Each job: (avi_path, bead_diameter_um, solute_percent, solute_type, temp_c)
#   solute_type: 'glycerol' (default) or 'acetone'
#   temp_c: room temperature for that session (Session 5/6 = 21 C, Session 7 = 19 C)
# Add new videos here — already-processed ones are skipped automatically.
JOBS = [
    # Session 5 (Feb 24) — 21 C
    (trial1, 3.0,  0.0, 'glycerol', 21.0),
    (trial2, 3.0,  0.0, 'glycerol', 21.0),

    # Session 6 (Feb 26) — 21 C
    # s1b: 3um in pure water (0% gly)
    (s1b_t3, 3.0,  0.0, 'glycerol', 21.0),
    (s1b_t4, 3.0,  0.0, 'glycerol', 21.0),
    (s1b_t5, 3.0,  0.0, 'glycerol', 21.0),

    # s2a: 1um in 20% glycerol
    (s2a_t1, 1.0, 20.0, 'glycerol', 21.0),
    (s2a_t2, 1.0, 20.0, 'glycerol', 21.0),
    (s2a_t3, 1.0, 20.0, 'glycerol', 21.0),

    # s2b: 3um in 20% glycerol
    (s2b_t1, 3.0, 20.0, 'glycerol', 21.0),
    (s2b_t2, 3.0, 20.0, 'glycerol', 21.0),
    (s2b_t3, 3.0, 20.0, 'glycerol', 21.0),

    # s2c: 1um in 20% glycerol (higher bead concentration)
    (s2c_t1, 1.0, 20.0, 'glycerol', 21.0),
    (s2c_t2, 1.0, 20.0, 'glycerol', 21.0),
    (s2c_t3, 1.0, 20.0, 'glycerol', 21.0),

    # s3: 3um in 20% glycerol
    (s3_t1,  3.0, 20.0, 'glycerol', 21.0),
    (s3_t2,  3.0, 20.0, 'glycerol', 21.0),
    (s3_t3,  3.0, 20.0, 'glycerol', 21.0),

    # s7: 3um in 36% glycerol
    (s7_t1,  3.0, 36.3, 'glycerol', 21.0),
    (s7_t2,  3.0, 36.3, 'glycerol', 21.0),
    (s7_t3,  3.0, 36.3, 'glycerol', 21.0),

    # s8: 3um in 20% acetone (100/(397+100) = 20.1%)
    (s8_t1,  3.0, 20.1, 'acetone', 21.0),
    (s8_t2,  3.0, 20.1, 'acetone', 21.0),

    # s9: 3um in 40% acetone (800/(1200+800) = 40.0%)
    (s9_t1,  3.0, 40.0, 'acetone', 21.0),
    (s9_t2,  3.0, 40.0, 'acetone', 21.0),

    # =====================================================
    # Session 7 (Mar 3) — 19 C — FULL 4x4 MATRIX
    # =====================================================

    # --- WATER (0% glycerol) ---
    (r1,     1.0,  0.0, 'glycerol', 19.0),   # r1: 1um
    (r2_t1,  2.1,  0.0, 'glycerol', 19.0),   # r2: 2.1um (NEW bead size)
    (r2_t2,  2.1,  0.0, 'glycerol', 19.0),
    (r3_t1,  3.0,  0.0, 'glycerol', 19.0),   # r3: 3um
    (r3_t2,  3.0,  0.0, 'glycerol', 19.0),
    (r4_t1,  5.0,  0.0, 'glycerol', 19.0),   # r4: 5um
    (r4_t2,  5.0,  0.0, 'glycerol', 19.0),

    # --- 20% GLYCEROL (100 uL gly / 500 uL total) ---
    (r5_t1,  1.0, 20.0, 'glycerol', 19.0),   # r5: 1um
    (r6_t1,  2.1, 20.0, 'glycerol', 19.0),   # r6: 2.1um (NEW)
    (r6_t2,  2.1, 20.0, 'glycerol', 19.0),
    (r7_t1,  3.0, 20.0, 'glycerol', 19.0),   # r7: 3um
    (r7_t2,  3.0, 20.0, 'glycerol', 19.0),
    (r7_t3,  3.0, 20.0, 'glycerol', 19.0),   # trial3-best
    (r8_t1,  5.0, 20.0, 'glycerol', 19.0),   # r8: 5um
    (r8_t2,  5.0, 20.0, 'glycerol', 19.0),
    (r8_t3,  5.0, 20.0, 'glycerol', 19.0),

    # --- 40% GLYCEROL (200 uL gly / 500 uL total) ---
    (r10_t1, 2.1, 40.0, 'glycerol', 19.0),   # r10: 2.1um
    (r10_t2, 2.1, 40.0, 'glycerol', 19.0),
    (r11_t1, 3.0, 40.0, 'glycerol', 19.0),   # r11: 3um
    (r11_t2, 3.0, 40.0, 'glycerol', 19.0),
    (r12_a,  5.0, 40.0, 'glycerol', 19.0),   # r12: 5um (10uL stock, best)
    (r12_b,  5.0, 40.0, 'glycerol', 19.0),   # r12: 5um (20uL stock, new focus)
    (r12_c,  5.0, 40.0, 'glycerol', 19.0),   # r12: 5um (20uL stock, best)

    # --- PURE ACETONE (100% acetone, no water) ---
    (r14_t1, 2.1, 100.0, 'acetone', 19.0),   # r14: 2.1um
    (r14_t2, 2.1, 100.0, 'acetone', 19.0),
    (r15_t1, 3.0, 100.0, 'acetone', 19.0),   # r15: 3um (1 trial only — seal failed)
    (r16_t1, 5.0, 100.0, 'acetone', 19.0),   # r16: 5um
    (r16_t2, 5.0, 100.0, 'acetone', 19.0),
    # r16_t3 EXCLUDED — truncated file (9 MB vs 1.1 GB)
    (r16_t4, 5.0, 100.0, 'acetone', 19.0),
]

# --- Pipeline versioning ---
# Bump this whenever analysis logic changes significantly (detection, D calculation,
# noise correction, MSD, etc.).  Each video's readme.txt stores the version it was
# processed with.  If it doesn't match PIPELINE_VERSION, the video is automatically
# reprocessed — no need to set FORCE_REPROCESS.
#
# Version history:
#   1.0  — Original pipeline (no noise correction, 1x3 mask, bins='fd', no Hough)
#   2.0  — Steps 1-12: noise correction, Hough+CC fusion, velocity filter, 3x3 mask,
#           bins='auto', D_gauss fix, combined subplot, per-date trends, interactive tune
#   2.1  — Green/red mask overlay (accepted vs rejected tracks), 1um preset tuning,
#           track ID labels on detection masks, version stamp on all plots
#   2.2  — Two-pass data-driven MAX_DISPLACEMENT (no D_theory dependency),
#           adaptive MAX_GAP_FRAMES for large beads, improved tracking continuity
#   2.3  — Appearance-based tracking: radial intensity profiles for particle identity,
#           appearance similarity in cost matrix + gap closing, centroid correction
#           via local brightness peak (fixes crescent centroid offset)
PIPELINE_VERSION = '2.3'

# Set True to reprocess ALL videos regardless of version (ignores version check)
FORCE_REPROCESS = False

# Set True to enable interactive parameter tuning with sliders (for Jupyter/script)
# When True: pauses before processing each video, shows detection preview with sliders.
# When False: batch mode (default) — no user interaction.
INTERACTIVE_TUNE = False

# --- Shared constants (same for all videos) ---
PIXEL_SIZE = 0.0684           # um/px (68.4 nm/px, 100x oil)
# NOTE: Frame rate is READ from each video file (not hardcoded)
TEMPERATURE_C = 21.0          # Celsius
CHAMBER_DEPTH_UM = 82.5       # Tape spacer chamber depth (um)

# --- Tracking parameters ---
MAX_DISPLACEMENT = 10         # px/frame
MAX_GAP_FRAMES = 3
MIN_TRACK_LENGTH = 10         # frames
MIN_TOTAL_DISPLACEMENT = 3.0  # px
EDGE_MARGIN = 15              # px from frame border to exclude

# --- Appearance-based tracking ---
# Radial intensity profiles capture each particle's circular contrast structure
# (bright center → dark halo → background). Used in tracking cost matrix and
# gap closing to maintain particle identity across frames.
APPEARANCE_WEIGHT = 0.3       # weight in tracking cost (0=off, higher=more weight)
APPEARANCE_WEIGHT_GAP = 0.5   # weight in gap closing (higher for cross-gap matching)
APPEARANCE_N_RINGS = 6        # number of concentric rings in radial profile

# --- Detection presets by bead size ---
# Each bead size gets its own optimized detection parameters.
# Previously there was only ONE rule: threshold=10 if bead<2um, else 15.
# Now each size has: threshold, blur_sigma, close_k_factor (for morphological
# closing kernel), min_fill_ratio, max_aspect_ratio, and area_mult (min, max
# multipliers for expected bead area in pixels).
# NOTE: These are initial estimates — tune empirically against data during
# implementation to ensure the most accurate mask for each bead size.
DETECTION_PRESETS = {
    1.0:  {'threshold': 7,  'blur_sigma': 1.2, 'close_k_factor': 0.8,
           'min_fill': 0.25, 'max_aspect': 3.5, 'area_mult': (0.08, 8.0)},
    2.1:  {'threshold': 12, 'blur_sigma': 1.2, 'close_k_factor': 0.5,
           'min_fill': 0.40, 'max_aspect': 3.0, 'area_mult': (0.10, 6.0)},
    3.0:  {'threshold': 15, 'blur_sigma': 1.5, 'close_k_factor': 0.6,
           'min_fill': 0.40, 'max_aspect': 3.0, 'area_mult': (0.10, 6.0)},
    5.0:  {'threshold': 15, 'blur_sigma': 2.0, 'close_k_factor': 0.7,
           'min_fill': 0.45, 'max_aspect': 2.5, 'area_mult': (0.10, 5.0)},
}
# Default fallback (used if bead size doesn't match a preset key)
DETECTION_DEFAULTS = {'threshold': 15, 'blur_sigma': 1.5, 'close_k_factor': 0.6,
                      'min_fill': 0.40, 'max_aspect': 3.0, 'area_mult': (0.10, 6.0)}

# --- Analysis parameters ---
NUM_BEST_SEGMENTS = 10
MIN_SEGMENT_LENGTH = 10       # frames
MAX_JUMP_PX = 20              # px

print(f'Defined {len(JOBS)} jobs.')
for i, (p, d, g, s, t) in enumerate(JOBS, 1):
    from pathlib import Path as _P
    print(f'  {i:2d}. {_P(p).name}  ({d} um, {g}% {s}, {t}C)')

# ======================================================================
# CELL 2
# ======================================================================
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
import configparser
from datetime import datetime

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
def compute_temporal_median(cap, sample_every=10, percentile=30):
    """Build a background image from a low percentile of sampled frames.
    
    WHY a low percentile instead of median (50th)?
    --------------------------------------------------
    Phase-contrast beads are bright spots.  A bead that barely moves during
    the video sits near the same pixel in every sampled frame.  The *median*
    of those pixels equals the bead's own brightness, so (frame - background)
    = 0 and the bead disappears from the detection mask.
    
    Using a LOW percentile (default 30th) picks the *dimmest* value each
    pixel ever had.  For pixels where a bead sometimes sat, the 30th-pctile
    grabs a frame when the bead was elsewhere (or at its dimmest), producing
    a background darker than the bead -> positive (frame - background) signal
    -> the bead becomes detectable.
    
    Trade-off: lowering the percentile increases background noise, which is
    why we don't go below ~25.  30 is a good balance.
    """
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
    print(f'  Sampled {len(frames_sampled)} frames for background (p={percentile})')
    return np.percentile(np.stack(frames_sampled), percentile, axis=0).astype(np.uint8)


def detect_particles(gray_frame, background, threshold, blur_sigma,
                     min_area, max_area, bead_radius_px=10,
                     edge_margin=0, min_fill_ratio=0.0, max_aspect_ratio=999,
                     close_k_factor=0.6, use_hough=True):
    """Detect particles via background subtraction + CC + Hough circle fusion.

    "Cast a wide net, filter later" — we want to catch as many real beads
    as possible here, and let the velocity filter (post-tracking) remove
    stuck/spurious detections.

    Key design choices (from systematic mask inspection across all videos):

    1. cv2.subtract (positive-only diff) instead of cv2.absdiff:
       Phase-contrast microscopy produces bright bead centres with dark halos.
       subtract() clips negative values to 0, keeping only bright-above-background
       pixels and eliminating dark-ring false detections.

    2. Adaptive morphological closing kernel (proportional to bead size):
       Phase contrast creates a bright centre + a separate bright crescent
       from the halo edge.  A small (3x3) close kernel cannot bridge the gap
       for large beads (5 um ~ 36 px diameter).  Using a kernel proportional
       to bead_radius_px merges the centre and crescent into one blob BEFORE
       connected-component labelling, preventing double detection at the source.

    3. Fill-ratio filter: reject hollow crescents (fill < 0.4 of bounding box).
    4. Aspect-ratio filter: reject elongated artifacts (aspect > 3).
    5. Edge exclusion: reject blobs near frame border (vignetting artifacts).

    6. Hough Circle Transform (supplementary):
       Catches circular shapes the threshold-based CC misses (e.g. low
       contrast beads, dark beads).  Provides more accurate circle centres
       than intensity-weighted CC centroids (which can be biased by crescents).
       Uses HOUGH_GRADIENT_ALT for better accuracy.

    7. Fusion: CC + Hough within bead_radius -> prefer Hough centre.
       Hough-only detections accepted.  CC-only detections kept.

    8. Proximity merge (post-fusion):
       Any two centroids within 1.5x bead diameter are merged,
       keeping the brighter/higher-confidence one.

    Returns:
        particles: list of (cx, cy, r_detected) tuples.
                   r_detected = Hough radius when available, else sqrt(CC_area/pi).
        binary: the thresholded binary mask (for visualization).
    """
    h_frame, w_frame = gray_frame.shape[:2]

    ksize = int(blur_sigma * 4) | 1
    blurred = cv2.GaussianBlur(gray_frame, (ksize, ksize), blur_sigma)

    # --- POSITIVE-ONLY difference ---
    diff = cv2.subtract(blurred, background)

    _, binary = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # --- Adaptive morphological clean-up ---
    # Open (small kernel): remove salt noise without destroying small beads
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_open)

    # Close (bead-proportional kernel): bridge centre-to-crescent gap
    close_k = max(3, int(bead_radius_px * close_k_factor) | 1)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                             (close_k, close_k))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_close)

    n_labels, labels, stats, centroids_cv = cv2.connectedComponentsWithStats(
        binary, connectivity=8)

    # --- Collect CC candidate particles with intensity weights ---
    # Each candidate: (cx, cy, weight_sum, r_estimated)
    cc_candidates = []
    for label_id in range(1, n_labels):
        area = stats[label_id, cv2.CC_STAT_AREA]
        if area < min_area or area > max_area:
            continue

        x_bb = stats[label_id, cv2.CC_STAT_LEFT]
        y_bb = stats[label_id, cv2.CC_STAT_TOP]
        w_bb = stats[label_id, cv2.CC_STAT_WIDTH]
        h_bb = stats[label_id, cv2.CC_STAT_HEIGHT]

        # --- Fill-ratio filter ---
        bbox_area = max(w_bb * h_bb, 1)
        fill_ratio = area / bbox_area
        if fill_ratio < min_fill_ratio:
            continue

        # --- Aspect-ratio filter ---
        aspect = max(w_bb, h_bb) / max(min(w_bb, h_bb), 1)
        if aspect > max_aspect_ratio:
            continue

        # --- Intensity-weighted centroid ---
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
            weight_sum = float(area)

        # --- Edge exclusion ---
        if edge_margin > 0:
            if (cx < edge_margin or cx > w_frame - edge_margin or
                cy < edge_margin or cy > h_frame - edge_margin):
                continue

        # Estimate radius from CC area: A = pi*r^2
        r_est = np.sqrt(area / np.pi)
        cc_candidates.append((cx, cy, weight_sum, r_est))

    # ================================================================
    # HOUGH CIRCLE TRANSFORM (supplementary detector)
    # ================================================================
    hough_circles = []
    if use_hough and bead_radius_px >= 3:
        # Apply Hough on the blurred difference image for best circle detection
        diff_8u = diff.copy()
        # Ensure sufficient contrast for Hough
        if diff_8u.max() > 0:
            min_r = max(2, int(bead_radius_px * 0.5))
            max_r = int(bead_radius_px * 2.5)
            min_dist = max(5, int(bead_radius_px * 2))
            try:
                circles = cv2.HoughCircles(
                    diff_8u, cv2.HOUGH_GRADIENT_ALT,
                    dp=1.5,
                    minDist=min_dist,
                    param1=300,    # Canny upper threshold (GRADIENT_ALT)
                    param2=0.7,    # "perfectness" 0-1 (lower = more circles)
                    minRadius=min_r,
                    maxRadius=max_r)
            except cv2.error:
                circles = None

            if circles is not None:
                for (hx, hy, hr) in circles[0]:
                    # Edge exclusion
                    if edge_margin > 0:
                        if (hx < edge_margin or hx > w_frame - edge_margin or
                            hy < edge_margin or hy > h_frame - edge_margin):
                            continue
                    hough_circles.append((float(hx), float(hy), float(hr)))

    # ================================================================
    # FUSION: CC + Hough
    # ================================================================
    # For each Hough detection, check if a CC candidate is nearby.
    # If yes: prefer Hough centre (more accurate for circles), keep CC weight.
    # If no: accept Hough-only detection.
    # CC-only detections are also kept.

    fuse_dist_sq = (bead_radius_px * 1.5) ** 2
    hough_matched = set()  # indices of Hough circles that matched a CC
    cc_matched = set()     # indices of CC candidates that matched a Hough

    # Build fused list: (cx, cy, weight, r_detected, source)
    fused = []

    for h_idx, (hx, hy, hr) in enumerate(hough_circles):
        best_cc_idx = -1
        best_dist_sq = fuse_dist_sq
        for c_idx, (ccx, ccy, ccw, ccr) in enumerate(cc_candidates):
            if c_idx in cc_matched:
                continue
            dsq = (hx - ccx)**2 + (hy - ccy)**2
            if dsq < best_dist_sq:
                best_dist_sq = dsq
                best_cc_idx = c_idx

        if best_cc_idx >= 0:
            # CC+Hough match: use Hough centre + radius, CC weight
            ccw = cc_candidates[best_cc_idx][2]
            fused.append((hx, hy, ccw, hr, 'fused'))
            hough_matched.add(h_idx)
            cc_matched.add(best_cc_idx)
        else:
            # Hough-only: use diff intensity at circle centre as weight
            ix, iy = int(round(hx)), int(round(hy))
            ix = max(0, min(ix, w_frame - 1))
            iy = max(0, min(iy, h_frame - 1))
            w_hough = float(diff[iy, ix]) * np.pi * hr * hr
            fused.append((hx, hy, w_hough, hr, 'hough'))
            hough_matched.add(h_idx)

    # Add CC-only detections (no matching Hough circle)
    for c_idx, (ccx, ccy, ccw, ccr) in enumerate(cc_candidates):
        if c_idx not in cc_matched:
            fused.append((ccx, ccy, ccw, ccr, 'cc'))

    # ================================================================
    # PROXIMITY MERGE (same as before, but now with radii)
    # ================================================================
    merge_dist_sq = (bead_radius_px * 3.0) ** 2  # 1.5x bead diameter
    fused.sort(key=lambda c: c[2], reverse=True)  # highest weight first
    merged = []
    used = set()
    for i, (cx_i, cy_i, w_i, r_i, src_i) in enumerate(fused):
        if i in used:
            continue
        for j in range(i + 1, len(fused)):
            if j in used:
                continue
            dx = fused[j][0] - cx_i
            dy = fused[j][1] - cy_i
            if dx * dx + dy * dy < merge_dist_sq:
                used.add(j)  # suppress weaker duplicate
        merged.append((cx_i, cy_i, r_i))

    return merged, binary


def track_all_frames(detections_per_frame, max_disp, max_gap, min_length,
                     appearances_per_frame=None, appearance_weight=0.0):
    """Track particles across frames using Hungarian algorithm.

    If appearances_per_frame is provided and appearance_weight > 0, the
    cost matrix combines spatial distance with appearance dissimilarity:

        cost = distance + appearance_weight × (1 - similarity) × max_disp

    This means identical-looking particles are linked preferentially.
    The appearance penalty is in the same units as distance (pixels) so
    the Hungarian algorithm sees a meaningful combined cost.

    Appearance profiles are stored in each track dict under 'appearances'
    so they're available for downstream gap closing.
    """
    all_tracks = []
    active_tracks = []
    next_id = 1
    frame_numbers = sorted(detections_per_frame.keys())

    use_app = (appearances_per_frame is not None and appearance_weight > 0)

    for frame_num in frame_numbers:
        curr_detections = detections_per_frame[frame_num]
        curr_apps = appearances_per_frame.get(frame_num, []) if use_app else []

        prev_positions = []
        prev_track_indices = []
        prev_gap_sizes = []
        prev_apps = []

        for i, track in enumerate(active_tracks):
            gap = frame_num - track['last_seen_frame']
            if gap <= max_gap + 1:
                pos = track['positions'][track['last_seen_frame']]
                prev_positions.append(pos)
                prev_track_indices.append(i)
                prev_gap_sizes.append(gap)
                # Get the most recent appearance for this track
                if use_app and 'appearances' in track:
                    prev_apps.append(
                        track['appearances'].get(track['last_seen_frame']))
                else:
                    prev_apps.append(None)

        # Gap scaling: Brownian displacement ~ sqrt(time), NOT linear.
        effective_max_disps = [max_disp * math.sqrt(g) for g in prev_gap_sizes]

        if len(prev_positions) > 0 and len(curr_detections) > 0:
            n_prev = len(prev_positions)
            n_curr = len(curr_detections)
            INF = 1e9
            cost = np.full((n_prev, n_curr), INF)
            for i, (px, py) in enumerate(prev_positions):
                for j, (cx, cy) in enumerate(curr_detections):
                    d = np.sqrt((px - cx)**2 + (py - cy)**2)
                    if d <= effective_max_disps[i]:
                        c = d
                        # Add appearance penalty (soft preference for same-looking beads)
                        if (use_app and prev_apps[i] is not None and
                                j < len(curr_apps) and curr_apps[j] is not None):
                            sim = appearance_similarity(prev_apps[i], curr_apps[j])
                            c += appearance_weight * (1.0 - sim) * max_disp
                        cost[i, j] = c
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

        # Update matched tracks
        for prev_idx, curr_idx in matches.items():
            track_idx = prev_track_indices[prev_idx]
            track = active_tracks[track_idx]
            gap = frame_num - track['last_seen_frame']
            track['positions'][frame_num] = curr_detections[curr_idx]
            track['flags'][frame_num] = '*' if gap > 1 else ' '
            track['last_seen_frame'] = frame_num
            track['end_frame'] = frame_num
            # Store appearance
            if use_app and curr_idx < len(curr_apps) and curr_apps[curr_idx] is not None:
                if 'appearances' not in track:
                    track['appearances'] = {}
                track['appearances'][frame_num] = curr_apps[curr_idx]

        # Retire tracks that haven't been seen for too long
        still_active = []
        for i, track in enumerate(active_tracks):
            if frame_num - track['last_seen_frame'] > max_gap:
                all_tracks.append(track)
            else:
                still_active.append(track)
        active_tracks = still_active

        # Create new tracks for unmatched detections
        for curr_idx in unmatched_curr:
            new_track = {
                'id': next_id,
                'positions': {frame_num: curr_detections[curr_idx]},
                'flags': {frame_num: ' '},
                'start_frame': frame_num,
                'end_frame': frame_num,
                'last_seen_frame': frame_num,
            }
            if use_app and curr_idx < len(curr_apps) and curr_apps[curr_idx] is not None:
                new_track['appearances'] = {frame_num: curr_apps[curr_idx]}
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


def _gap_merge_pass(tracks_list, max_gap_close, max_dist_px,
                     app_weight=0.0):
    """Single pass of gap-closing merge. Returns (result, any_merge)."""
    tracks_sorted = sorted(tracks_list, key=lambda t: t['start_frame'])
    merged_into = {}
    n = len(tracks_sorted)
    any_merge = False

    for i in range(n):
        if i in merged_into:
            continue
        t_end = tracks_sorted[i]
        end_frame = t_end['end_frame']
        end_pos = t_end['positions'][end_frame]

        # Get end appearance (average of last few frames for robustness)
        end_app = None
        if app_weight > 0 and 'appearances' in t_end:
            end_app = t_end['appearances'].get(end_frame)

        best_j = None
        best_score = float('inf')

        for j in range(i + 1, n):
            if j in merged_into:
                continue
            t_start = tracks_sorted[j]
            start_frame = t_start['start_frame']
            gap = start_frame - end_frame

            if gap < 1:
                continue
            if gap > max_gap_close:
                break

            start_pos = t_start['positions'][start_frame]
            dist = math.sqrt((end_pos[0] - start_pos[0])**2 +
                             (end_pos[1] - start_pos[1])**2)
            effective_max = max_dist_px * math.sqrt(gap)
            if dist > effective_max:
                continue

            # Combined score: spatial + appearance penalty
            score = dist
            if app_weight > 0 and end_app is not None and 'appearances' in t_start:
                start_app = t_start['appearances'].get(start_frame)
                if start_app is not None:
                    sim = appearance_similarity(end_app, start_app)
                    score += app_weight * (1.0 - sim) * max_dist_px

            if score < best_score:
                best_score = score
                best_j = j

        if best_j is not None:
            t_merge = tracks_sorted[best_j]
            for fnum, pos in t_merge['positions'].items():
                tracks_sorted[i]['positions'][fnum] = pos
            for fnum, flag in t_merge['flags'].items():
                tracks_sorted[i]['flags'][fnum] = flag
            # Merge appearances
            if 'appearances' in t_merge:
                if 'appearances' not in tracks_sorted[i]:
                    tracks_sorted[i]['appearances'] = {}
                for fnum, app in t_merge['appearances'].items():
                    tracks_sorted[i]['appearances'][fnum] = app
            tracks_sorted[i]['end_frame'] = t_merge['end_frame']
            tracks_sorted[i]['last_seen_frame'] = t_merge['last_seen_frame']
            merged_into[best_j] = i
            any_merge = True

    result = [t for idx, t in enumerate(tracks_sorted) if idx not in merged_into]
    return result, any_merge


def close_track_gaps(tracks, max_gap_close, max_dist_px, app_weight=0.0):
    """Post-tracking gap closing: merge fragmented tracks of the same bead.

    After initial tracking, the same bead can produce multiple short tracks
    due to detection dropout. This function merges them by:
      1. Sorting tracks by start_frame
      2. For each ended track, looking for later tracks that start
         within max_gap_close frames AND whose start position is within
         max_dist_px of the ended track's last position
      3. If app_weight > 0, also comparing appearance (radial intensity
         profiles) at the gap boundary — similar-looking particles are
         preferred for merging
      4. Merging the best match (lowest combined score) into the earlier track

    Uses multiple passes until convergence (merging creates new endpoints
    that might connect to further fragments).

    Returns: merged tracks (re-numbered IDs).
    """
    if len(tracks) < 2:
        return tracks

    # First pass
    result, _ = _gap_merge_pass(tracks, max_gap_close, max_dist_px, app_weight)

    # Multiple passes until convergence
    for _pass in range(10):
        result, any_merge = _gap_merge_pass(result, max_gap_close,
                                             max_dist_px, app_weight)
        if not any_merge:
            break

    # Re-number IDs
    for i, track in enumerate(result, 1):
        track['id'] = i
        frames = sorted(track['positions'].keys())
        track['start_frame'] = frames[0]
        track['end_frame'] = frames[-1]
        track['last_seen_frame'] = frames[-1]

    return result


# ---------------------------------------------------------------
# Appearance descriptors for particle identity
# ---------------------------------------------------------------
def extract_appearance(gray_frame, cx, cy, bead_radius_px, n_rings=6):
    """Extract radial intensity profile as appearance descriptor.

    Computes average intensity in concentric rings around the detection
    center (from raw grayscale frame, NOT background-subtracted).
    This captures the particle's circular contrast structure:
      - Phase contrast beads: bright centre → dark halo → background
      - Different beads have different absolute intensities
      - Same bead keeps a similar profile across frames

    The profile is normalized (zero-mean, unit-std) for brightness
    invariance: only the SHAPE of the radial curve matters, not the
    overall brightness.

    Args:
        gray_frame: uint8 grayscale frame (raw)
        cx, cy: detection centre (float, sub-pixel)
        bead_radius_px: expected bead radius in pixels
        n_rings: number of concentric rings

    Returns:
        profile: numpy array of length n_rings (normalized), or zeros
    """
    h, w = gray_frame.shape[:2]
    r = max(3.0, float(bead_radius_px))
    max_r = r * 2.5  # capture halo + surrounding background

    pad = int(math.ceil(max_r)) + 1
    y_lo = max(0, int(cy) - pad)
    y_hi = min(h, int(cy) + pad + 1)
    x_lo = max(0, int(cx) - pad)
    x_hi = min(w, int(cx) + pad + 1)

    if y_hi <= y_lo or x_hi <= x_lo:
        return np.zeros(n_rings)

    patch = gray_frame[y_lo:y_hi, x_lo:x_hi].astype(np.float64)

    # Distance from centre for each pixel in patch
    yy = np.arange(y_lo, y_hi, dtype=np.float64) - cy
    xx = np.arange(x_lo, x_hi, dtype=np.float64) - cx
    XX, YY = np.meshgrid(xx, yy)
    dist = np.sqrt(XX**2 + YY**2)

    # Average intensity in each concentric ring
    ring_edges = np.linspace(0, max_r, n_rings + 1)
    profile = np.zeros(n_rings)
    for i in range(n_rings):
        mask = (dist >= ring_edges[i]) & (dist < ring_edges[i + 1])
        if mask.any():
            profile[i] = np.mean(patch[mask])

    # Normalize: zero-mean, unit-std (brightness-invariant)
    std = np.std(profile)
    if std > 1e-8:
        profile = (profile - np.mean(profile)) / std
    else:
        profile[:] = 0.0

    return profile


def appearance_similarity(prof1, prof2):
    """Cosine similarity between two normalized radial profiles.

    Returns value in [0, 1]:
      1.0 = identical profiles (same contrast structure)
      0.5 = uncorrelated (neutral fallback)
      0.0 = opposite profiles

    Since profiles are zero-mean, unit-std, cosine similarity
    equals Pearson correlation.
    """
    if prof1 is None or prof2 is None:
        return 0.5  # neutral when appearance unavailable
    if len(prof1) == 0 or len(prof2) == 0:
        return 0.5
    n1 = np.linalg.norm(prof1)
    n2 = np.linalg.norm(prof2)
    if n1 < 1e-8 or n2 < 1e-8:
        return 0.5
    cos_sim = np.dot(prof1, prof2) / (n1 * n2)
    # Map [-1, 1] → [0, 1]
    return max(0.0, min(1.0, (cos_sim + 1.0) / 2.0))


def correct_centroid_local_peak(gray_frame, cx, cy, bead_radius_px,
                                 background, blur_sigma=2.0):
    """Correct CC centroid by finding local brightness peak.

    Phase contrast microscopy produces crescent-shaped binary masks whose
    centroid is offset from the true bead centre.  The true centre is the
    brightest region in the blurred (frame - background) difference image.

    This function:
      1. Extracts a local patch from the blurred difference image
      2. Finds the peak (brightest pixel) within 1.2× bead radius
      3. Returns the peak position as the corrected centroid

    Only corrects if the peak is within bead_radius of the CC centroid
    (avoids jumping to a completely different feature).
    """
    h, w = gray_frame.shape[:2]
    search_r = max(5, int(bead_radius_px * 1.2))

    y_lo = max(0, int(cy) - search_r)
    y_hi = min(h, int(cy) + search_r + 1)
    x_lo = max(0, int(cx) - search_r)
    x_hi = min(w, int(cx) + search_r + 1)

    if y_hi <= y_lo or x_hi <= x_lo:
        return cx, cy

    # Use the difference image (frame - background), heavily blurred
    # to smooth out crescent artifacts and find the true peak
    patch_frame = gray_frame[y_lo:y_hi, x_lo:x_hi].astype(np.float32)
    patch_bg = background[y_lo:y_hi, x_lo:x_hi].astype(np.float32)
    diff_patch = np.maximum(0, patch_frame - patch_bg)

    # Heavy blur to merge crescent into disc shape
    k = max(3, int(bead_radius_px * 0.8)) | 1
    diff_blurred = cv2.GaussianBlur(diff_patch, (k, k), blur_sigma)

    # Mask: only look within bead_radius of the CC centroid
    yy = np.arange(y_lo, y_hi, dtype=np.float64) - cy
    xx = np.arange(x_lo, x_hi, dtype=np.float64) - cx
    XX, YY = np.meshgrid(xx, yy)
    dist = np.sqrt(XX**2 + YY**2)
    valid_mask = dist <= bead_radius_px * 1.2
    diff_blurred[~valid_mask] = 0

    if diff_blurred.max() < 1:
        return cx, cy

    # Find peak
    peak_y, peak_x = np.unravel_index(diff_blurred.argmax(),
                                        diff_blurred.shape)
    cx_corr = float(x_lo + peak_x)
    cy_corr = float(y_lo + peak_y)

    # Sanity check: don't jump more than bead_radius from original
    jump = math.sqrt((cx_corr - cx)**2 + (cy_corr - cy)**2)
    if jump > bead_radius_px:
        return cx, cy  # too far, keep original

    return cx_corr, cy_corr


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

def gaussian_pdf(x, mean, std_dev):
    """Normalized Gaussian probability density function.
    Use with density=True histograms so the fit area = 1."""
    return (1.0 / (np.sqrt(2 * np.pi) * abs(std_dev))) * np.exp(-(x - mean)**2 / (2 * std_dev**2))

def sigma_clip(arr, sigma=3, max_iter=5):
    """Iterative sigma-clipping. Returns clipped array."""
    a = np.array(arr, dtype=float)
    for _ in range(max_iter):
        mu = np.mean(a)
        sd = np.std(a)
        if sd == 0:
            break
        mask = np.abs(a - mu) < sigma * sd
        if mask.all():
            break
        a = a[mask]
    return a

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


# ---------------------------------------------------------------
# Version watermark on figures
# ---------------------------------------------------------------
def stamp_version(fig):
    """Add a small pipeline version label to the bottom-right of a figure."""
    fig.text(0.99, 0.005, f'v{PIPELINE_VERSION}', fontsize=6, color='gray',
             alpha=0.5, ha='right', va='bottom',
             transform=fig.transFigure)


# Detection preset lookup
# ---------------------------------------------------------------
def get_detection_preset(bead_diameter_um):
    """Get detection parameters for a given bead size.
    Returns a dict with: threshold, blur_sigma, close_k_factor,
    min_fill, max_aspect, area_mult.
    Falls back to nearest key or DETECTION_DEFAULTS.
    """
    if bead_diameter_um in DETECTION_PRESETS:
        return DETECTION_PRESETS[bead_diameter_um].copy()
    # Find nearest preset
    keys = sorted(DETECTION_PRESETS.keys())
    nearest = min(keys, key=lambda k: abs(k - bead_diameter_um))
    print(f'    [preset] No exact match for {bead_diameter_um} um, using {nearest} um preset')
    return DETECTION_PRESETS[nearest].copy()


# ---------------------------------------------------------------
# Metadata functions (readme.txt in figures/ folder)
# ---------------------------------------------------------------
def load_or_create_metadata(figures_dir, avi_path, fps, total_frames,
                            width, height, bead_diameter_um, solute_pct,
                            solute_type, temp_c, pixel_size, preset):
    """Load or create readme.txt metadata file in the figures folder.

    Structure:
      [constants]  — write-once (video properties, never change)
      [detection]  — AUTO by default; switches to MANUAL after interactive tuning
      [volatile]   — overwritten every run (D values, alpha, etc.)

    Returns:
      (config, detection_mode, detection_params)
      - config: configparser object
      - detection_mode: 'AUTO' or 'MANUAL'
      - detection_params: dict of detection parameters to use
    """
    readme_path = figures_dir / 'readme.txt'
    config = configparser.ConfigParser()

    if readme_path.exists():
        config.read(str(readme_path), encoding='utf-8')
        detection_mode = config.get('detection', 'mode', fallback='AUTO')
        print(f'    [metadata] Loaded readme.txt (detection mode: {detection_mode})')

        if detection_mode == 'MANUAL':
            # Override preset with manual values from readme
            detection_params = {
                'threshold': config.getfloat('detection', 'threshold', fallback=preset['threshold']),
                'blur_sigma': config.getfloat('detection', 'blur_sigma', fallback=preset['blur_sigma']),
                'close_k_factor': config.getfloat('detection', 'close_k_factor', fallback=preset['close_k_factor']),
                'min_fill': config.getfloat('detection', 'min_fill_ratio', fallback=preset['min_fill']),
                'max_aspect': config.getfloat('detection', 'max_aspect_ratio', fallback=preset['max_aspect']),
                'area_mult': (config.getfloat('detection', 'area_mult_min', fallback=preset['area_mult'][0]),
                              config.getfloat('detection', 'area_mult_max', fallback=preset['area_mult'][1])),
            }
            return config, 'MANUAL', detection_params
        else:
            return config, 'AUTO', preset

    # --- Create new readme.txt ---
    config['constants'] = {
        'filename': avi_path.name,
        'fps': str(fps),
        'total_frames': str(total_frames),
        'width': str(width),
        'height': str(height),
        'bead_diameter_um': str(bead_diameter_um),
        'solute_pct': str(solute_pct),
        'solute_type': solute_type,
        'temp_c': str(temp_c),
        'pixel_size_um': str(pixel_size),
    }

    config['detection'] = {
        'mode': 'AUTO',
        'threshold': str(preset['threshold']),
        'blur_sigma': str(preset['blur_sigma']),
        'close_k_factor': str(preset['close_k_factor']),
        'min_fill_ratio': str(preset['min_fill']),
        'max_aspect_ratio': str(preset['max_aspect']),
        'area_mult_min': str(preset['area_mult'][0]),
        'area_mult_max': str(preset['area_mult'][1]),
    }

    config['volatile'] = {}  # Will be filled after analysis

    with open(str(readme_path), 'w', encoding='utf-8') as f:
        f.write('# === VIDEO METADATA (readme.txt) ===\n')
        f.write(f'# Generated: {datetime.now().isoformat()}\n')
        f.write('#\n')
        f.write('# [constants] — write-once (video properties from file + JOBS tuple)\n')
        f.write('# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides\n')
        f.write('# [volatile]  — overwritten every pipeline run\n\n')
        config.write(f)

    print(f'    [metadata] Created readme.txt (AUTO mode)')
    return config, 'AUTO', preset


def update_volatile_metadata(figures_dir, D_var, D_gauss, D_msd,
                             alpha, n_tracks, n_segs,
                             max_disp_used=None, max_gap_used=None):
    """Update the [volatile] section of readme.txt after analysis.
    Preserves [constants] and [detection] sections.
    """
    readme_path = figures_dir / 'readme.txt'
    if not readme_path.exists():
        return

    config = configparser.ConfigParser()
    config.read(str(readme_path), encoding='utf-8')

    volatile = {
        'pipeline_version': PIPELINE_VERSION,
        'd_variance': f'{D_var:.6f}',
        'd_gauss': f'{D_gauss:.6f}',
        'd_msd': f'{D_msd:.6f}',
        'alpha': f'{alpha:.4f}',
        'n_tracks': str(n_tracks),
        'n_segs': str(n_segs),
        'last_processed': datetime.now().isoformat(),
    }
    if max_disp_used is not None:
        volatile['max_displacement_px'] = str(max_disp_used)
    if max_gap_used is not None:
        volatile['max_gap_frames'] = str(max_gap_used)
    config['volatile'] = volatile

    with open(str(readme_path), 'w', encoding='utf-8') as f:
        f.write('# === VIDEO METADATA (readme.txt) ===\n')
        f.write(f'# Last updated: {datetime.now().isoformat()}\n')
        f.write('#\n')
        f.write('# [constants] — write-once (video properties from file + JOBS tuple)\n')
        f.write('# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides\n')
        f.write('# [volatile]  — overwritten every pipeline run\n\n')
        config.write(f)


# ---------------------------------------------------------------
# Noise calibration
# ---------------------------------------------------------------
def process_noise_calibration(data_root, figures_root, pixel_size):
    """Process noise calibration videos to measure localization noise floor.

    Noise calibration videos contain stationary features (calibration marks
    on a slide). All measured displacement is localization noise.

    Returns:
      (sigma_noise_um, v_noise_um_s) or (0.0, 0.0) if no calibration data.
    """
    cal_dir = figures_root / 'Calibration'
    cal_file = cal_dir / 'noise_calibration.txt'

    # --- If already processed, load and return ---
    if cal_file.exists():
        config = configparser.ConfigParser()
        config.read(str(cal_file), encoding='utf-8')
        sigma_noise_um = config.getfloat('results', 'sigma_noise_um', fallback=0.0)
        v_noise_um_s = config.getfloat('results', 'v_noise_um_s', fallback=0.0)
        n_displacements = config.getint('results', 'n_displacements', fallback=0)
        print(f'  [noise cal] Loaded from file: sigma={sigma_noise_um:.5f} um, '
              f'v_noise={v_noise_um_s:.3f} um/s ({n_displacements} displacements)')
        return sigma_noise_um, v_noise_um_s

    # --- Find noise calibration videos ---
    data_path = Path(data_root)
    noise_videos = sorted(data_path.rglob('noise-calibration*.avi'))

    if len(noise_videos) == 0:
        print(f'  [noise cal] No noise calibration videos found in {data_root}')
        return 0.0, 0.0

    print(f'  [noise cal] Processing {len(noise_videos)} calibration video(s)...')

    all_displacements_px = []
    all_fps = []

    for vid_path in noise_videos:
        print(f'    Processing: {vid_path.name}')
        cap = cv2.VideoCapture(str(vid_path))
        if not cap.isOpened():
            print(f'      WARNING: Cannot open {vid_path.name}, skipping')
            continue

        vid_fps = cap.get(cv2.CAP_PROP_FPS)
        if vid_fps <= 0:
            vid_fps = 29.0
        all_fps.append(vid_fps)
        vid_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Build background
        background = compute_temporal_median(cap, sample_every=10)

        # Detect and track with permissive settings (these are static marks)
        detections_per_frame = {}
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for frame_num in range(1, vid_total + 1):
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
            # Use permissive detection for calibration marks (no Hough — not beads)
            particles_with_r, _ = detect_particles(
                gray, background, threshold=10, blur_sigma=1.5,
                min_area=4, max_area=5000, bead_radius_px=10,
                edge_margin=15, min_fill_ratio=0.3, max_aspect_ratio=4.0,
                use_hough=False)
            # Strip radius for tracking (only need cx, cy)
            detections_per_frame[frame_num] = [(p[0], p[1]) for p in particles_with_r]
        cap.release()

        counts = [len(detections_per_frame.get(f, [])) for f in range(1, vid_total + 1)]
        print(f'      Frames: {vid_total}, Particles/frame: mean={np.mean(counts):.1f}')

        # Track
        raw_tracks = track_all_frames(detections_per_frame, max_disp=5,
                                       max_gap=3, min_length=1)
        # Keep tracks with at least 10 frames (don't filter by displacement —
        # these are SUPPOSED to be stationary)
        cal_tracks = [t for t in raw_tracks if len(t['positions']) >= 10]

        print(f'      Tracks: {len(raw_tracks)} raw -> {len(cal_tracks)} (>= 10 frames)')

        # Compute frame-to-frame displacements (ALL are noise)
        for track in cal_tracks:
            frames = sorted(track['positions'].keys())
            for i in range(1, len(frames)):
                if frames[i] - frames[i-1] == 1:  # consecutive frames only
                    p1 = track['positions'][frames[i-1]]
                    p2 = track['positions'][frames[i]]
                    all_displacements_px.append(p2[0] - p1[0])  # dx
                    all_displacements_px.append(p2[1] - p1[1])  # dy

    if len(all_displacements_px) < 10:
        print(f'  [noise cal] Too few displacements ({len(all_displacements_px)}), skipping')
        return 0.0, 0.0

    disp_px = np.array(all_displacements_px)
    sigma_noise_px = np.std(disp_px)
    sigma_noise_um = sigma_noise_px * pixel_size

    # Average fps across calibration videos
    avg_fps = np.mean(all_fps)
    avg_dt = 1.0 / avg_fps
    v_noise_um_s = sigma_noise_um / avg_dt

    print(f'  [noise cal] Results: sigma_noise = {sigma_noise_px:.3f} px = {sigma_noise_um:.5f} um')
    print(f'  [noise cal] Noise velocity floor: {v_noise_um_s:.4f} um/s')

    # Save results
    cal_dir.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config['results'] = {
        'sigma_noise_px': f'{sigma_noise_px:.6f}',
        'sigma_noise_um': f'{sigma_noise_um:.6f}',
        'v_noise_um_s': f'{v_noise_um_s:.6f}',
        'n_displacements': str(len(disp_px)),
        'n_videos': str(len(noise_videos)),
        'avg_fps': f'{avg_fps:.1f}',
        'processed': datetime.now().isoformat(),
    }
    with open(str(cal_file), 'w', encoding='utf-8') as f:
        f.write('# === NOISE CALIBRATION RESULTS ===\n')
        f.write(f'# Processed: {datetime.now().isoformat()}\n')
        f.write(f'# Videos: {", ".join(v.name for v in noise_videos)}\n\n')
        config.write(f)

    # Save noise displacement histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    disp_um = disp_px * pixel_size
    ax.hist(disp_um, bins='auto', density=True, alpha=0.7, color='steelblue',
            edgecolor='black', linewidth=0.5)
    x_fit = np.linspace(disp_um.min(), disp_um.max(), 200)
    ax.plot(x_fit, gaussian_pdf(x_fit, 0, sigma_noise_um), 'r-', linewidth=2,
            label=f'Gaussian: $\\sigma$ = {sigma_noise_um:.5f} $\\mu$m\n'
                  f'({sigma_noise_px:.3f} px)')
    ax.set_xlabel(r'Frame-to-frame displacement ($\mu$m)')
    ax.set_ylabel('Probability density')
    ax.set_title(f'Noise Calibration — Localization Noise Floor\n'
                 f'{len(disp_px)} displacements from {len(noise_videos)} videos')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    stamp_version(fig)
    fig.savefig(str(cal_dir / 'noise_histogram.png'), dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f'  [noise cal] Saved to: {cal_dir}')

    return sigma_noise_um, v_noise_um_s


# ---------------------------------------------------------------
# Velocity filter — sigma-clip on track speeds
# ---------------------------------------------------------------
def velocity_filter_tracks(tracks, dt, pixel_size, noise_velocity=0.0):
    """Data-driven velocity filter using sigma-clipping on track median speeds.

    NOT theory-motivated — purely data-driven:
    1. Compute median frame-to-frame speed for each track
    2. Sigma-clip the distribution of median speeds (3σ, 5 iterations)
       → removes stuck tracks (speed ≈ 0) and flow-dragged/mis-linked tracks
    3. Additionally remove any track whose median speed < 2× noise_velocity
       (below localization noise floor — these are definitely not moving)

    Performance note: runs on already-computed track positions, typically
    5-100 tracks × 100-400 positions each. Takes <1ms. If this ever becomes
    a bottleneck with thousands of tracks, compute velocity statistics on
    a random subset of positions per track rather than all positions.

    Args:
        tracks: list of track dicts (from clean_tracks)
        dt: time step in seconds
        pixel_size: um/px conversion
        noise_velocity: noise floor velocity in um/s (from calibration)

    Returns:
        filtered list of tracks, renumbered
    """
    if len(tracks) <= 1:
        return tracks  # Can't filter a single track

    # 1. Compute median speed for each track
    track_speeds = []
    for track in tracks:
        frames = sorted(track['positions'].keys())
        speeds = []
        for i in range(1, len(frames)):
            if frames[i] - frames[i-1] == 1:  # consecutive frames only
                p1 = track['positions'][frames[i-1]]
                p2 = track['positions'][frames[i]]
                dx = (p2[0] - p1[0]) * pixel_size  # um
                dy = (p2[1] - p1[1]) * pixel_size  # um
                speed = np.sqrt(dx**2 + dy**2) / dt  # um/s
                speeds.append(speed)
        median_speed = np.median(speeds) if len(speeds) > 0 else 0.0
        track_speeds.append(median_speed)

    speeds_arr = np.array(track_speeds)

    # 2. Sigma-clip (3σ, 5 iterations)
    clipped = speeds_arr.copy()
    for _ in range(5):
        mu = np.mean(clipped)
        sd = np.std(clipped)
        if sd == 0:
            break
        mask = np.abs(clipped - mu) < 3 * sd
        if mask.all():
            break
        clipped = clipped[mask]

    if len(clipped) == 0:
        return tracks  # All removed — return original

    clip_mean = np.mean(clipped)
    clip_std = np.std(clipped)
    lo = clip_mean - 3 * clip_std
    hi = clip_mean + 3 * clip_std

    # 3. Apply noise floor threshold (conservative)
    # Use 0.5× noise_velocity as the stuck-particle threshold.
    # Rationale: for slow-diffusing particles (high viscosity, large beads),
    # the Brownian speed can be COMPARABLE to the localization noise.
    # Using 2× would filter out real tracks. 0.5× only catches things
    # that are clearly below the noise floor.
    noise_threshold = max(lo, 0.5 * noise_velocity) if noise_velocity > 0 else lo

    # 4. Filter
    filtered = []
    n_stuck = 0
    n_fast = 0
    for track, speed in zip(tracks, speeds_arr):
        if speed < noise_threshold:
            n_stuck += 1
            continue
        if speed > hi:
            n_fast += 1
            continue
        filtered.append(track)

    # Safety check: if filter would remove >80% of tracks, it's too aggressive
    # — skip filtering and warn
    if len(filtered) < max(1, len(tracks) * 0.2):
        print(f'    [velocity filter] WARNING: would remove {len(tracks)-len(filtered)}'
              f'/{len(tracks)} tracks (>80%) — skipping filter')
        print(f'      (noise_floor={noise_threshold:.3f} um/s, upper={hi:.3f} um/s, '
              f'median_speeds={np.median(speeds_arr):.3f} um/s)')
        return tracks

    # Renumber
    for i, track in enumerate(filtered, 1):
        track['id'] = i

    print(f'    [velocity filter] {len(tracks)} -> {len(filtered)} tracks '
          f'(removed {n_stuck} stuck, {n_fast} fast; '
          f'noise_floor={noise_threshold:.3f} um/s, upper={hi:.3f} um/s)')

    return filtered


print('All functions loaded.')

# Quick viscosity sanity check
for _gp in [0, 20, 36.3, 40.0]:
    _eta21 = get_glycerol_viscosity(_gp, 21.0) * 1e3
    _eta19 = get_glycerol_viscosity(_gp, 19.0) * 1e3
    print(f'  Glycerol {_gp}%: 21C={_eta21:.3f}, 19C={_eta19:.3f} mPa.s')
_ace100 = get_acetone_viscosity(100.0, 19.0) * 1e3
print(f'  Pure acetone at 19C: {_ace100:.3f} mPa.s')

# ---------------------------------------------------------------
# Interactive Detection Tuning (Step 12 / Phase 4A)
# ---------------------------------------------------------------
def interactive_tune_detection(avi_path, background, bead_radius_px, preset,
                                figures_dir, bead_diameter_um, pixel_size):
    """Interactive slider-based parameter tuning for particle detection.

    Shows the middle frame with raw/mask/overlay panels.
    Sliders control: threshold, blur_sigma, close_k_factor, min_fill, max_aspect.
    Each slider change re-runs detect_particles() on the preview frame.
    'Save & Continue' writes params to readme.txt as MANUAL mode.
    'Reset to AUTO' restores preset defaults.
    'Skip' continues without saving.

    Works with matplotlib TkAgg backend (scripts) or ipympl (Jupyter).
    """
    import matplotlib
    # Try to use an interactive backend
    try:
        current_backend = matplotlib.get_backend()
        if 'Agg' in current_backend and 'TkAgg' not in current_backend:
            matplotlib.use('TkAgg')
    except Exception:
        pass

    from matplotlib.widgets import Slider, Button

    cap = cv2.VideoCapture(str(avi_path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    mid = total // 2

    # Read the middle frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print('  [tune] Could not read middle frame, skipping tuning.')
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame

    # Expected area range
    expected_area = np.pi * bead_radius_px ** 2

    # Mutable state dict for closures
    state = {
        'threshold': preset['threshold'],
        'blur_sigma': preset['blur_sigma'],
        'close_k_factor': preset['close_k_factor'],
        'min_fill': preset['min_fill'],
        'max_aspect': preset['max_aspect'],
        'action': None,  # 'save', 'reset', or 'skip'
    }

    # Create figure with 3 panels
    fig, (ax_raw, ax_mask, ax_overlay) = plt.subplots(1, 3, figsize=(20, 7))
    plt.subplots_adjust(bottom=0.38)
    fig.suptitle(f'Interactive Tuning: {avi_path.name} (frame {mid})',
                 fontsize=12, fontweight='bold')

    # Initial detection
    area_min = max(1, int(expected_area * preset['area_mult'][0]))
    area_max = int(expected_area * preset['area_mult'][1])

    def update_display(val=None):
        particles, binary = detect_particles(
            gray, background,
            threshold=int(state['threshold']),
            blur_sigma=state['blur_sigma'],
            min_area=area_min, max_area=area_max,
            bead_radius_px=bead_radius_px,
            edge_margin=EDGE_MARGIN,
            min_fill_ratio=state['min_fill'],
            max_aspect_ratio=state['max_aspect'],
            close_k_factor=state['close_k_factor'],
            use_hough=True)

        ax_raw.clear()
        ax_raw.imshow(gray, cmap='gray')
        ax_raw.set_title('Raw Frame')
        ax_raw.axis('off')

        ax_mask.clear()
        ax_mask.imshow(binary, cmap='gray')
        ax_mask.set_title(f'Binary Mask (thr={int(state["threshold"])})')
        ax_mask.axis('off')

        ax_overlay.clear()
        overlay = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        for p in particles:
            cx, cy = p[0], p[1]
            r_det = int(p[2]) if len(p) > 2 else int(bead_radius_px)
            cv2.circle(overlay, (int(cx), int(cy)), max(3, r_det), (0, 255, 0), 2)
            cv2.circle(overlay, (int(cx), int(cy)), 2, (255, 0, 0), -1)
        ax_overlay.imshow(overlay)
        ax_overlay.set_title(f'{len(particles)} particles detected')
        ax_overlay.axis('off')

        fig.canvas.draw_idle()

    # Create sliders
    slider_color = 'lightgoldenrodyellow'
    ax_thr = plt.axes([0.15, 0.28, 0.65, 0.03], facecolor=slider_color)
    ax_blur = plt.axes([0.15, 0.23, 0.65, 0.03], facecolor=slider_color)
    ax_close = plt.axes([0.15, 0.18, 0.65, 0.03], facecolor=slider_color)
    ax_fill = plt.axes([0.15, 0.13, 0.65, 0.03], facecolor=slider_color)
    ax_asp = plt.axes([0.15, 0.08, 0.65, 0.03], facecolor=slider_color)

    s_thr = Slider(ax_thr, 'Threshold', 3, 40, valinit=state['threshold'], valstep=1)
    s_blur = Slider(ax_blur, 'Blur Sigma', 0.3, 5.0, valinit=state['blur_sigma'])
    s_close = Slider(ax_close, 'Close K', 0.1, 2.0, valinit=state['close_k_factor'])
    s_fill = Slider(ax_fill, 'Min Fill', 0.1, 0.8, valinit=state['min_fill'])
    s_asp = Slider(ax_asp, 'Max Aspect', 1.5, 6.0, valinit=state['max_aspect'])

    def on_slider_change(val):
        state['threshold'] = s_thr.val
        state['blur_sigma'] = s_blur.val
        state['close_k_factor'] = s_close.val
        state['min_fill'] = s_fill.val
        state['max_aspect'] = s_asp.val
        update_display()

    s_thr.on_changed(on_slider_change)
    s_blur.on_changed(on_slider_change)
    s_close.on_changed(on_slider_change)
    s_fill.on_changed(on_slider_change)
    s_asp.on_changed(on_slider_change)

    # Create buttons
    ax_save = plt.axes([0.15, 0.01, 0.2, 0.04])
    ax_reset = plt.axes([0.40, 0.01, 0.2, 0.04])
    ax_skip = plt.axes([0.65, 0.01, 0.2, 0.04])

    btn_save = Button(ax_save, 'Save & Continue', color='lightgreen')
    btn_reset = Button(ax_reset, 'Reset to AUTO', color='lightyellow')
    btn_skip = Button(ax_skip, 'Skip (no save)', color='lightsalmon')

    def on_save(event):
        state['action'] = 'save'
        plt.close(fig)

    def on_reset(event):
        state['threshold'] = preset['threshold']
        state['blur_sigma'] = preset['blur_sigma']
        state['close_k_factor'] = preset['close_k_factor']
        state['min_fill'] = preset['min_fill']
        state['max_aspect'] = preset['max_aspect']
        s_thr.set_val(preset['threshold'])
        s_blur.set_val(preset['blur_sigma'])
        s_close.set_val(preset['close_k_factor'])
        s_fill.set_val(preset['min_fill'])
        s_asp.set_val(preset['max_aspect'])
        state['action'] = 'reset'
        plt.close(fig)

    def on_skip(event):
        state['action'] = 'skip'
        plt.close(fig)

    btn_save.on_clicked(on_save)
    btn_reset.on_clicked(on_reset)
    btn_skip.on_clicked(on_skip)

    # Initial display
    update_display()
    plt.show(block=True)

    # Process result
    if state['action'] == 'save':
        # Write MANUAL params to readme.txt
        readme_path = figures_dir / 'readme.txt'
        if readme_path.exists():
            config = configparser.ConfigParser()
            config.read(str(readme_path))
            config.set('detection', 'mode', 'MANUAL')
            config.set('detection', 'threshold', str(int(state['threshold'])))
            config.set('detection', 'blur_sigma', f"{state['blur_sigma']:.2f}")
            config.set('detection', 'close_k_factor', f"{state['close_k_factor']:.2f}")
            config.set('detection', 'min_fill_ratio', f"{state['min_fill']:.2f}")
            config.set('detection', 'max_aspect_ratio', f"{state['max_aspect']:.1f}")
            with open(str(readme_path), 'w', encoding='utf-8') as f:
                f.write('# === VIDEO METADATA (readme.txt) ===\n')
                f.write(f'# Last updated: {datetime.now().isoformat()}\n')
                f.write('#\n')
                f.write('# [constants] — write-once (video properties from file + JOBS tuple)\n')
                f.write('# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides\n')
                f.write('# [volatile]  — overwritten every pipeline run\n\n')
                config.write(f)
            print(f'    [tune] Saved MANUAL params to {readme_path.name}')
        return {
            'threshold': int(state['threshold']),
            'blur_sigma': state['blur_sigma'],
            'close_k_factor': state['close_k_factor'],
            'min_fill': state['min_fill'],
            'max_aspect': state['max_aspect'],
        }
    elif state['action'] == 'reset':
        # Reset readme.txt to AUTO
        readme_path = figures_dir / 'readme.txt'
        if readme_path.exists():
            config = configparser.ConfigParser()
            config.read(str(readme_path))
            config.set('detection', 'mode', 'AUTO')
            config.set('detection', 'threshold', str(preset['threshold']))
            config.set('detection', 'blur_sigma', f"{preset['blur_sigma']:.2f}")
            config.set('detection', 'close_k_factor', f"{preset['close_k_factor']:.2f}")
            config.set('detection', 'min_fill_ratio', f"{preset['min_fill']:.2f}")
            config.set('detection', 'max_aspect_ratio', f"{preset['max_aspect']:.1f}")
            with open(str(readme_path), 'w', encoding='utf-8') as f:
                f.write('# === VIDEO METADATA (readme.txt) ===\n')
                f.write(f'# Last updated: {datetime.now().isoformat()}\n')
                f.write('#\n')
                f.write('# [constants] — write-once (video properties from file + JOBS tuple)\n')
                f.write('# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides\n')
                f.write('# [volatile]  — overwritten every pipeline run\n\n')
                config.write(f)
            print(f'    [tune] Reset to AUTO preset in {readme_path.name}')
        return None
    else:  # skip
        print('    [tune] Skipped — no changes saved.')
        return None


# ======================================================================
# CELL 3
# ======================================================================
# ============================================================================
# CELL 3 — MAIN PROCESSING LOOP
# ============================================================================

NOTEBOOK_DIR = Path(os.getcwd())
FIGURES_ROOT = NOTEBOOK_DIR / 'figures'

# --- NOISE CALIBRATION (run once at pipeline start) ---
print('\n' + '=' * 70)
print('NOISE CALIBRATION')
print('=' * 70)
SIGMA_NOISE_UM, V_NOISE_UM_S = process_noise_calibration(
    DATA, FIGURES_ROOT, PIXEL_SIZE)
print()

n_total = len(JOBS)
n_skipped = 0
n_processed = 0
n_failed = 0
batch_results = []

for job_idx, (avi_path_str, bead_diameter_um, solute_pct, solute_type, job_temp_c) in enumerate(JOBS, 1):

    # Per-job temperature (Session 5/6 = 21 C, Session 7 = 19 C)
    TEMPERATURE_C_JOB = job_temp_c
    TEMPERATURE = TEMPERATURE_C_JOB + 273.15

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

    # --- Skip check (version-aware) ---
    summary_file = FIGURES_DIR / 'summary.txt'
    readme_file = FIGURES_DIR / 'readme.txt'

    if summary_file.exists() and not FORCE_REPROCESS:
        # Check pipeline version in readme.txt
        stored_version = None
        if readme_file.exists():
            _cfg = configparser.ConfigParser()
            try:
                _cfg.read(str(readme_file), encoding='utf-8')
                stored_version = _cfg.get('volatile', 'pipeline_version', fallback=None)
            except Exception:
                pass

        if stored_version == PIPELINE_VERSION:
            print(f'\n[{job_idx}/{n_total}] SKIP: {avi_path.name} (v{stored_version}, up to date)')
            n_skipped += 1
            continue
        else:
            old_v = stored_version or '1.0'
            print(f'\n[{job_idx}/{n_total}] REPROCESSING: {avi_path.name} '
                  f'(v{old_v} -> v{PIPELINE_VERSION})')
            # Fall through to processing

    solute_label = solute_type.capitalize()  # "Glycerol" or "Acetone"
    print(f'\n{"=" * 70}')
    print(f'[{job_idx}/{n_total}] PROCESSING: {avi_path.name}')
    print(f'  Bead: {bead_diameter_um} um | {solute_label}: {solute_pct}% | T={TEMPERATURE_C_JOB}C | Date: {date_folder}')
    print(f'{"=" * 70}')

    # --- Validate file ---
    if not avi_path.exists():
        print(f'  ERROR: File not found! Skipping.')
        n_failed += 1
        continue

    # --- Detection preset for this bead size ---
    _preset = get_detection_preset(bead_diameter_um)
    _bead_radius_px = (bead_diameter_um / 2) / PIXEL_SIZE
    _bead_area_px = math.pi * _bead_radius_px**2
    min_particle_area = max(4, int(_bead_area_px * _preset['area_mult'][0]))
    max_particle_area = max(200, int(_bead_area_px * _preset['area_mult'][1]))
    effective_threshold = _preset['threshold']
    effective_blur_sigma = _preset['blur_sigma']
    effective_close_k_factor = _preset['close_k_factor']
    effective_min_fill = _preset['min_fill']
    effective_max_aspect = _preset['max_aspect']

    # --- Viscosity ---
    viscosity = get_viscosity(solute_pct, TEMPERATURE_C_JOB, solute_type)
    print(f'  Viscosity: {viscosity*1e3:.3f} mPa.s ({viscosity:.6f} Pa.s)')
    print(f'  Particle area range: {min_particle_area} - {max_particle_area} px^2')
    print(f'  Detection preset: threshold={effective_threshold}, blur={effective_blur_sigma}, '
          f'fill>{effective_min_fill}, aspect<{effective_max_aspect}')

    # --- Adaptive tracking parameters (DATA-DRIVEN, two-pass approach) ---
    # We do NOT use D_theory here — instead we use a generous first-pass
    # MAX_DISPLACEMENT, measure actual displacements from the data, then
    # re-track with a tighter, data-tuned value.
    #
    # First-pass heuristic: smaller beads in lower-viscosity solutions
    # move more. We want a generous upper bound to avoid missing links.
    # The velocity filter will clean up any mis-linked tracks afterwards.
    #
    # Generous first-pass values (empirical, NOT theory-based):
    #   - Small beads (<=2 um) in low-viscosity (water/acetone): 30 px
    #   - Small beads in high-viscosity (>20% gly): 20 px
    #   - Large beads (>2 um): 15 px (they move less regardless of medium)
    if bead_diameter_um <= 2.0:
        if solute_pct <= 20.0 or solute_type == 'acetone':
            max_disp_pass1 = 30
        else:
            max_disp_pass1 = 20
    else:
        max_disp_pass1 = 15

    # Adaptive MAX_GAP_FRAMES: allow more gap frames for beads with
    # inconsistent detection. Phase contrast creates artifacts for ALL sizes:
    #   - Large beads (>=5 um): crescent masks vary frame-to-frame
    #   - Small beads (<=2 um): low contrast, faint features, dropout
    #   - Medium beads: most reliable, but still benefit from gap tolerance
    if bead_diameter_um >= 5.0:
        max_gap_adaptive = max(MAX_GAP_FRAMES, 6)
    elif bead_diameter_um <= 2.0:
        # 1-2µm beads have very inconsistent detection in phase contrast
        # (crescent artifacts, low contrast → frequent dropout)
        max_gap_adaptive = max(MAX_GAP_FRAMES, 8)
    elif bead_diameter_um >= 3.0:
        max_gap_adaptive = max(MAX_GAP_FRAMES, 4)
    else:
        max_gap_adaptive = MAX_GAP_FRAMES

    print(f'  First-pass MAX_DISPLACEMENT: {max_disp_pass1} px (will refine from data)')
    print(f'  Adaptive MAX_GAP_FRAMES: {max_gap_adaptive} (global default: {MAX_GAP_FRAMES})')

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

        # --- Load or create metadata (readme.txt) ---
        meta_config, detection_mode, det_params = load_or_create_metadata(
            FIGURES_DIR, avi_path, fps, total_frames, width, height,
            bead_diameter_um, solute_pct, solute_type, TEMPERATURE_C_JOB,
            PIXEL_SIZE, _preset)

        # If MANUAL mode, override effective detection params
        if detection_mode == 'MANUAL':
            effective_threshold = det_params['threshold']
            effective_blur_sigma = det_params['blur_sigma']
            effective_close_k_factor = det_params['close_k_factor']
            effective_min_fill = det_params['min_fill']
            effective_max_aspect = det_params['max_aspect']
            min_particle_area = max(4, int(_bead_area_px * det_params['area_mult'][0]))
            max_particle_area = max(200, int(_bead_area_px * det_params['area_mult'][1]))
            print(f'    Using MANUAL detection params from readme.txt')

        t0 = time.time()
        background = compute_temporal_median(cap, sample_every=10)

        # --- Interactive tuning (if enabled) ---
        if INTERACTIVE_TUNE:
            tune_result = interactive_tune_detection(
                avi_path, background, _bead_radius_px, preset,
                FIGURES_DIR, bead_diameter_um, PIXEL_SIZE)
            if tune_result is not None:
                # Apply tuned params for this run
                effective_threshold = tune_result['threshold']
                effective_blur_sigma = tune_result['blur_sigma']
                effective_close_k_factor = tune_result['close_k_factor']
                effective_min_fill = tune_result['min_fill']
                effective_max_aspect = tune_result['max_aspect']
                print(f'    Using TUNED detection params: thr={effective_threshold}, '
                      f'blur={effective_blur_sigma:.2f}, close_k={effective_close_k_factor:.2f}')

        # --- Frame indices for multi-frame mask (frame 1, mid, last) ---
        mid_frame_num = total_frames // 2
        last_frame_num = total_frames  # last valid frame

        detections_per_frame = {}
        appearances_per_frame = {}  # radial intensity profiles for each detection
        # Storage for 3 key frames (for 3x3 detection mask)
        mask_frames = {}  # {frame_num: (gray, binary, particles)}

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for frame_num in range(1, total_frames + 1):
            ret, frame = cap.read()
            if not ret:
                total_frames = frame_num - 1
                last_frame_num = total_frames
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
            particles_with_r, binary = detect_particles(
                gray, background, effective_threshold,
                effective_blur_sigma, min_particle_area, max_particle_area,
                bead_radius_px=_bead_radius_px,
                edge_margin=EDGE_MARGIN,
                min_fill_ratio=effective_min_fill,
                max_aspect_ratio=effective_max_aspect,
                close_k_factor=effective_close_k_factor)

            # --- Appearance extraction (for identity-based tracking) ---
            # For each detection, extract a radial intensity profile from the
            # raw grayscale frame. This captures the particle's circular contrast
            # structure (bright centre → dark halo → background) regardless of
            # crescent artifacts in the binary mask.
            #
            # NOTE: centroid correction via local brightness peak was tested
            # but caused tracking instability (centroid jitter breaks linking).
            # Kept as a function for future use with better sub-pixel fitting.
            detections_per_frame[frame_num] = [(p[0], p[1]) for p in particles_with_r]
            appearances_per_frame[frame_num] = [
                extract_appearance(gray, p[0], p[1], _bead_radius_px,
                                   APPEARANCE_N_RINGS)
                for p in particles_with_r
            ]
            # Save key frames for multi-frame mask (keep full tuples with r)
            if frame_num == 1 or frame_num == mid_frame_num or frame_num == last_frame_num:
                mask_frames[frame_num] = (gray.copy(), binary.copy(),
                                           particles_with_r)
        cap.release()

        # Update last_frame_num to the actual last frame captured
        if last_frame_num not in mask_frames and total_frames in mask_frames:
            pass  # already captured
        elif total_frames > 0 and total_frames not in mask_frames:
            # Use the last frame we did capture
            last_captured = max(mask_frames.keys())
            if last_captured != 1 and last_captured != mid_frame_num:
                last_frame_num = last_captured

        counts = [len(detections_per_frame.get(f, [])) for f in range(1, total_frames + 1)]
        print(f'  Particles/frame: min={min(counts)}, max={max(counts)}, mean={np.mean(counts):.1f}')

        # === TWO-PASS TRACKING (data-driven MAX_DISPLACEMENT + appearance) ===
        # Pass 1: Track with generous max_disp to capture all real links
        # Appearance weight is used to prefer linking same-looking particles
        raw_tracks_p1 = track_all_frames(
            detections_per_frame, max_disp_pass1, max_gap_adaptive, 1,
            appearances_per_frame=appearances_per_frame,
            appearance_weight=APPEARANCE_WEIGHT)
        tracks_p1 = clean_tracks(raw_tracks_p1, MIN_TRACK_LENGTH, MIN_TOTAL_DISPLACEMENT)
        print(f'  Pass 1: {len(raw_tracks_p1)} raw -> {len(tracks_p1)} valid '
              f'(max_disp={max_disp_pass1}px, app_weight={APPEARANCE_WEIGHT})')

        # Measure actual frame-to-frame displacements from pass-1 tracks
        all_step_sizes = []
        for _t in tracks_p1:
            _frames = sorted(_t['positions'].keys())
            for _i in range(1, len(_frames)):
                if _frames[_i] - _frames[_i-1] == 1:  # consecutive frames only
                    _p1 = _t['positions'][_frames[_i-1]]
                    _p2 = _t['positions'][_frames[_i]]
                    _step = math.sqrt((_p2[0] - _p1[0])**2 + (_p2[1] - _p1[1])**2)
                    all_step_sizes.append(_step)

        if len(all_step_sizes) > 20:
            _steps = np.array(all_step_sizes)
            _median_step = np.median(_steps)
            _mad_step = np.median(np.abs(_steps - _median_step))
            # Robust max: median + 7*MAD (covers extreme tail)
            # MAD ≈ 0.6745*sigma for Gaussian, so 7*MAD ≈ 4.72*sigma
            _data_driven_max = int(math.ceil(_median_step + 7 * _mad_step))

            # NEVER reduce below pass-1 value: if pass-1 gave fragmented tracks,
            # the measured step sizes are biased LOW (large jumps caused the breaks).
            # Reducing max_disp would make fragmentation WORSE.
            max_disp_adaptive = max(max_disp_pass1, _data_driven_max)

            # Check fragmentation: if #tracks >> #particles, data is unreliable
            _mean_particles = np.mean(counts)
            _fragmentation_ratio = len(tracks_p1) / max(1, _mean_particles)
            if _fragmentation_ratio > 2.0:
                print(f'  WARNING: Heavy fragmentation detected ({len(tracks_p1)} tracks '
                      f'for ~{_mean_particles:.0f} particles, ratio={_fragmentation_ratio:.1f}x)')
                print(f'  Step size statistics may be biased low — keeping generous max_disp')

            print(f'  Step sizes: median={_median_step:.2f}px, MAD={_mad_step:.2f}px')
            print(f'  Data-driven MAX_DISP = {_data_driven_max}px (median + 7*MAD)')
            print(f'  Final MAX_DISP = {max_disp_adaptive}px (never below pass-1={max_disp_pass1})')

            # Re-track only if adaptive value increased over pass-1
            if max_disp_adaptive > max_disp_pass1:
                raw_tracks = track_all_frames(
                    detections_per_frame, max_disp_adaptive, max_gap_adaptive, 1,
                    appearances_per_frame=appearances_per_frame,
                    appearance_weight=APPEARANCE_WEIGHT)
                tracks = clean_tracks(raw_tracks, MIN_TRACK_LENGTH, MIN_TOTAL_DISPLACEMENT)
                print(f'  Pass 2: {len(raw_tracks)} raw -> {len(tracks)} valid (max_disp={max_disp_adaptive}px)')
            else:
                raw_tracks = raw_tracks_p1
                tracks = tracks_p1
                print(f'  Pass 2: skipped (pass-1 value {max_disp_pass1}px already sufficient)')
        else:
            # Too few steps to estimate — use pass-1 results
            max_disp_adaptive = max_disp_pass1
            raw_tracks = raw_tracks_p1
            tracks = tracks_p1
            print(f'  Pass 2: skipped (too few steps to estimate, using pass-1)')

        print(f'  After clean: {len(tracks)} tracks ({time.time()-t0:.1f} s)')

        # --- Gap closing: merge fragmented tracks of the same bead ---
        # Same bead can produce multiple track fragments due to detection
        # dropout exceeding MAX_GAP. This step merges them post-hoc.
        # max_gap_close: search window for merging (larger than tracking gap)
        # max_dist_px: spatial threshold for matching (scales with sqrt(gap))
        n_before_merge = len(tracks)
        max_gap_close = max(max_gap_adaptive * 3, 20)  # generous: 3x tracking gap
        tracks = close_track_gaps(tracks, max_gap_close, max_disp_adaptive,
                                   app_weight=APPEARANCE_WEIGHT_GAP)
        n_merged = n_before_merge - len(tracks)
        if n_merged > 0:
            print(f'  Gap closing: {n_before_merge} -> {len(tracks)} tracks '
                  f'({n_merged} fragments merged, gap_window={max_gap_close}, '
                  f'app_weight={APPEARANCE_WEIGHT_GAP})')
        else:
            print(f'  Gap closing: no fragments to merge')

        # --- Velocity filter (sigma-clip on track speeds) ---
        if len(tracks) > 1:
            tracks = velocity_filter_tracks(tracks, dt, PIXEL_SIZE,
                                             noise_velocity=V_NOISE_UM_S)

        if len(tracks) == 0:
            raise RuntimeError('No valid tracks found!')

        track_output = str(FIGURES_DIR / 'trackresults.txt')
        write_mtrack2_format(tracks, total_frames, track_output)

        # --- DETECTION MASK MAP (3x3 grid) ---
        # Rows: Frame 1, Frame mid, Frame last
        # Cols: Raw frame, Binary mask, Overlay (GREEN=accepted, RED=rejected)
        print(f'  Generating 3x3 detection mask map...')

        # Build lookup: which particles are in accepted tracks (after velocity filter)?
        # tracks at this point = FINAL accepted tracks.
        accepted_positions = {}  # {frame_num: [(cx, cy, track_id), ...]}
        for _trk in tracks:
            for _fnum, _pos in _trk['positions'].items():
                if _fnum not in accepted_positions:
                    accepted_positions[_fnum] = []
                accepted_positions[_fnum].append((_pos[0], _pos[1], _trk['id']))

        # Determine which frames to show
        mask_frame_nums = sorted(mask_frames.keys())
        # Ensure we have exactly 3 (frame 1, mid, last)
        if len(mask_frame_nums) < 3:
            # Pad with available frames
            while len(mask_frame_nums) < 3:
                mask_frame_nums.append(mask_frame_nums[-1])
        # Take first, middle, last of available
        show_frames = [mask_frame_nums[0],
                       mask_frame_nums[len(mask_frame_nums)//2],
                       mask_frame_nums[-1]]

        fig_mask, axes_mask = plt.subplots(3, 3, figsize=(18, 18))
        r_circle = max(3, int(_bead_radius_px))
        _match_dist_sq = (_bead_radius_px * 1.5) ** 2

        for row_idx, fnum in enumerate(show_frames):
            gray_f, binary_f, particles_f = mask_frames.get(
                fnum, mask_frames[mask_frame_nums[0]])

            # Col 0: Raw frame
            axes_mask[row_idx, 0].imshow(gray_f, cmap='gray')
            axes_mask[row_idx, 0].set_title(f'Raw Frame {fnum}', fontsize=11)
            axes_mask[row_idx, 0].axis('off')

            # Col 1: Binary mask
            axes_mask[row_idx, 1].imshow(binary_f, cmap='gray')
            axes_mask[row_idx, 1].set_title(f'Mask (thr={effective_threshold})', fontsize=11)
            axes_mask[row_idx, 1].axis('off')

            # Col 2: Overlay — GREEN=in accepted track, RED=rejected/untracked
            overlay = cv2.cvtColor(gray_f, cv2.COLOR_GRAY2RGB)
            _frame_accepted = accepted_positions.get(fnum, [])
            _n_acc = 0
            _n_rej = 0

            for p in particles_f:
                cx, cy = p[0], p[1]
                r_det = int(p[2]) if len(p) > 2 else r_circle

                # Match this detection to an accepted track position
                _matched_tid = None
                for (_tx, _ty, _tid) in _frame_accepted:
                    if (cx - _tx)**2 + (cy - _ty)**2 < _match_dist_sq:
                        _matched_tid = _tid
                        break

                if _matched_tid is not None:
                    # GREEN circle + track ID label with white background
                    cv2.circle(overlay, (int(cx), int(cy)), max(3, r_det), (0, 220, 0), 2)
                    cv2.circle(overlay, (int(cx), int(cy)), 3, (0, 150, 0), -1)
                    _label = f'T{_matched_tid}'
                    _font = cv2.FONT_HERSHEY_SIMPLEX
                    _fscale = 0.55
                    _lx = int(cx) + r_det + 5
                    _ly = int(cy) + 5
                    # White background box for readability
                    (tw, th), _ = cv2.getTextSize(_label, _font, _fscale, 1)
                    cv2.rectangle(overlay, (_lx - 1, _ly - th - 2),
                                  (_lx + tw + 1, _ly + 3), (255, 255, 255), -1)
                    cv2.putText(overlay, _label,
                                (_lx, _ly), _font,
                                _fscale, (0, 160, 0), 1, cv2.LINE_AA)
                    _n_acc += 1
                else:
                    # RED circle (no label — rejected)
                    cv2.circle(overlay, (int(cx), int(cy)), max(3, r_det), (220, 50, 50), 2)
                    cv2.circle(overlay, (int(cx), int(cy)), 2, (180, 30, 30), -1)
                    _n_rej += 1

            axes_mask[row_idx, 2].imshow(overlay)
            axes_mask[row_idx, 2].set_title(
                f'{_n_acc} accepted (green) / {_n_rej} rejected (red)',
                fontsize=10)
            axes_mask[row_idx, 2].axis('off')

        # Row labels
        row_labels = [f'Frame {show_frames[0]}',
                      f'Frame {show_frames[1]} (mid)',
                      f'Frame {show_frames[2]} (last)']
        for row_idx, label in enumerate(row_labels):
            axes_mask[row_idx, 0].set_ylabel(label, fontsize=12, fontweight='bold',
                                              rotation=90, labelpad=10)

        fig_mask.suptitle(
            f'{avi_path.name} — Detection Mask Map\n'
            f'{len(tracks)} accepted tracks after velocity filter',
            fontsize=13, fontweight='bold')
        plt.tight_layout()
        stamp_version(fig_mask)
        fig_mask.savefig(str(FIGURES_DIR / 'detection_mask.png'), dpi=200, bbox_inches='tight')
        plt.close(fig_mask)

        # ==============================================================
        # STEP 2: LOAD & SEGMENT
        # ==============================================================
        print(f'  STEP 2: Segmenting tracks...')
        data = load_mtrack2_data(track_output)
        # Adaptive MAX_JUMP: should be at least max_disp_adaptive so we don't
        # split tracks at legitimate Brownian jumps we just allowed through.
        max_jump_adaptive = max(MAX_JUMP_PX, max_disp_adaptive)
        segments = split_tracks_at_jumps(data, MIN_SEGMENT_LENGTH, max_jump_adaptive)

        if len(segments) == 0:
            raise RuntimeError('No valid segments!')

        # Use ALL qualifying segments — not just top N by length.
        # Selection bias: longest segments come from slowest beads, severely
        # underestimating D. Using all segments gives an unbiased population.
        # NOTE: segments are already filtered by MIN_SEGMENT_LENGTH (10 frames)
        # and split at jumps > max_jump_adaptive px.
        n_to_use = len(segments)
        selected = segments[:n_to_use]
        print(f'  Segments: {len(segments)} total, using all {n_to_use}')

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
        stamp_version(fig)
        fig.savefig(str(FIGURES_DIR / 'trajectories.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

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

        # --- METHOD 1: Direct Variance (with sigma-clipping) ---
        # Tracking artifacts create outlier displacements (e.g. bead-to-bead
        # mis-links).  Iterative 3-sigma clipping removes these before
        # computing variance, so D_variance measures the THERMAL motion,
        # not the tracking noise.
        dx_clipped = sigma_clip(dx_um, sigma=3, max_iter=5)
        dy_clipped = sigma_clip(dy_um, sigma=3, max_iter=5)
        n_clipped = n_steps - len(dx_clipped) + n_steps - len(dy_clipped)
        if n_clipped > 0:
            print(f'    Sigma-clip removed {n_clipped} outlier steps '
                  f'({n_clipped/(2*n_steps)*100:.1f}%)')

        var_dx = np.var(dx_clipped)
        var_dy = np.var(dy_clipped)
        D_x_direct = var_dx / (2 * dt)
        D_y_direct = var_dy / (2 * dt)
        D_direct = (D_x_direct + D_y_direct) / 2

        # --- METHOD 2: Gaussian Fit (density-normalized) ---
        # FIX (3B): Both D_variance and D_gauss now use sigma-clipped data.
        # Previously D_gauss fit the UN-clipped histogram, causing it to
        # differ from D_variance. Now both see the same cleaned data.
        counts_x, bin_edges_x = np.histogram(dx_clipped, bins='auto', density=True)
        bin_centers_x = (bin_edges_x[:-1] + bin_edges_x[1:]) / 2
        try:
            popt_x, pcov_x = curve_fit(gaussian_pdf, bin_centers_x, counts_x,
                                        p0=[0, np.std(dx_clipped)])
            std_x_fit = abs(popt_x[1])
        except Exception:
            std_x_fit = np.std(dx_clipped)
            popt_x = [0, std_x_fit]

        counts_y, bin_edges_y = np.histogram(dy_clipped, bins='auto', density=True)
        bin_centers_y = (bin_edges_y[:-1] + bin_edges_y[1:]) / 2
        try:
            popt_y, pcov_y = curve_fit(gaussian_pdf, bin_centers_y, counts_y,
                                        p0=[0, np.std(dy_clipped)])
            std_y_fit = abs(popt_y[1])
        except Exception:
            std_y_fit = np.std(dy_clipped)
            popt_y = [0, std_y_fit]

        D_x_fit = std_x_fit**2 / (2 * dt)
        D_y_fit = std_y_fit**2 / (2 * dt)
        D_fit = (D_x_fit + D_y_fit) / 2

        # --- NOISE FLOOR CORRECTION (3C) ---
        # Localization noise adds a systematic offset to displacement variance:
        #   var(Δx_measured) = var(Δx_true) + var(Δx_noise)
        #
        # σ_noise (from calibration) = std(displacements of stationary particles)
        #   = std(ε₂ - ε₁) where ε ~ N(0, σ_loc²)
        # So σ_noise² = var(Δx_noise) = 2σ_loc²
        #
        # Correction: var(Δx_true) = var(Δx_measured) - σ_noise²
        # (NOT 2×σ_noise²: σ_noise already captures the displacement noise,
        #  not the per-position noise.)
        #
        # D_msd self-corrects — MSD linear fit absorbs noise into the intercept.
        sigma_noise_sq = SIGMA_NOISE_UM**2
        D_direct_raw = D_direct
        D_fit_raw = D_fit
        if sigma_noise_sq > 0:
            D_x_direct_corr = max(0, (var_dx - sigma_noise_sq) / (2 * dt))
            D_y_direct_corr = max(0, (var_dy - sigma_noise_sq) / (2 * dt))
            D_direct_corr = (D_x_direct_corr + D_y_direct_corr) / 2
            D_x_fit_corr = max(0, (std_x_fit**2 - sigma_noise_sq) / (2 * dt))
            D_y_fit_corr = max(0, (std_y_fit**2 - sigma_noise_sq) / (2 * dt))
            D_fit_corr = (D_x_fit_corr + D_y_fit_corr) / 2

            # Safety: if correction reduces D by more than 50%, the noise floor
            # is comparable to the signal (SNR~1). In this regime the correction
            # is unreliable, so cap the reduction at 50%.
            if D_direct_raw > 0 and D_direct_corr < 0.5 * D_direct_raw:
                D_direct = 0.5 * D_direct_raw
                print(f'    Noise correction CAPPED at 50% for D_var '
                      f'(SNR~1: σ_noise²={sigma_noise_sq:.5f} vs var={var_dx:.5f})')
            else:
                D_direct = D_direct_corr

            if D_fit_raw > 0 and D_fit_corr < 0.5 * D_fit_raw:
                D_fit = 0.5 * D_fit_raw
                print(f'    Noise correction CAPPED at 50% for D_gauss '
                      f'(SNR~1: σ_noise²={sigma_noise_sq:.5f} vs σ_fit²={std_x_fit**2:.5f})')
            else:
                D_fit = D_fit_corr

            print(f'    Noise correction: σ_noise={SIGMA_NOISE_UM:.5f} um, '
                  f'D_var {D_direct_raw:.4f}->{D_direct:.4f}, '
                  f'D_gauss {D_fit_raw:.4f}->{D_fit:.4f}')

        # --- Per-segment D estimates for proper error bars ---
        # Compute D for each segment individually, then take mean +/- SEM.
        # FIX (3B): per-segment D_gauss now uses clipped data (same as D_variance).
        seg_D_var = []
        seg_D_gau = []
        for seg in selected:
            sdx = np.diff(seg['x']) * PIXEL_SIZE
            sdy = np.diff(seg['y']) * PIXEL_SIZE
            if len(sdx) < 5:
                continue
            # Variance method (clipped)
            sdx_c = sigma_clip(sdx, sigma=3, max_iter=3)
            sdy_c = sigma_clip(sdy, sigma=3, max_iter=3)
            seg_var_x = np.var(sdx_c)
            seg_var_y = np.var(sdy_c)
            # With noise correction (capped same way)
            seg_D_x = max(0, (seg_var_x - sigma_noise_sq) / (2 * dt))
            seg_D_y = max(0, (seg_var_y - sigma_noise_sq) / (2 * dt))
            seg_D_uncorr = (np.var(sdx_c) + np.var(sdy_c)) / (4 * dt)
            seg_D_corr = (seg_D_x + seg_D_y) / 2
            # Cap at 50% reduction
            if seg_D_uncorr > 0 and seg_D_corr < 0.5 * seg_D_uncorr:
                seg_D_corr = 0.5 * seg_D_uncorr
            seg_D_var.append(seg_D_corr)
            # Gaussian method (also clipped, also noise-corrected)
            seg_D_gau.append(seg_D_corr)  # Same as D_var since both use clipped var

        if len(seg_D_var) > 1:
            D_direct_err = np.std(seg_D_var) / np.sqrt(len(seg_D_var))
            D_fit_err = np.std(seg_D_gau) / np.sqrt(len(seg_D_gau))
        else:
            D_direct_err = abs(D_direct - D_fit) / 2 if abs(D_direct - D_fit) > 0 else D_direct * 0.1
            D_fit_err = D_direct_err

        # --- Histogram plot ---
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        ax = axes[0]
        bw_x = bin_edges_x[1] - bin_edges_x[0]
        ax.bar(bin_centers_x, counts_x, width=bw_x,
               alpha=0.6, color='steelblue', label='Data (density)')
        x_fine = np.linspace(bin_centers_x[0], bin_centers_x[-1], 200)
        ax.plot(x_fine, gaussian_pdf(x_fine, *popt_x), 'r-', linewidth=2,
                label=f'Gaussian PDF fit\n$\\sigma$ = {std_x_fit:.4f} $\\mu$m')
        ax.set_xlabel(r'$\Delta x$ per frame ($\mu$m)')
        ax.set_ylabel('Probability density')
        ax.set_title(f'X Displacement \u2014 D_x = {D_x_fit:.4f} $\\mu$m$^2$/s')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        bw_y = bin_edges_y[1] - bin_edges_y[0]
        ax.bar(bin_centers_y, counts_y, width=bw_y,
               alpha=0.6, color='darkorange', label='Data (density)')
        y_fine = np.linspace(bin_centers_y[0], bin_centers_y[-1], 200)
        ax.plot(y_fine, gaussian_pdf(y_fine, *popt_y), 'r-', linewidth=2,
                label=f'Gaussian PDF fit\n$\\sigma$ = {std_y_fit:.4f} $\\mu$m')
        ax.set_xlabel(r'$\Delta y$ per frame ($\mu$m)')
        ax.set_ylabel('Probability density')
        ax.set_title(f'Y Displacement \u2014 D_y = {D_y_fit:.4f} $\\mu$m$^2$/s')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        stamp_version(fig)
        fig.savefig(str(FIGURES_DIR / 'displacement_histogram.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

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
        lag_times = (np.arange(max_lag) + 1) * dt  # lag 0 → 1-frame displacement

        # Linear fit for D
        n_fit = max_lag // 4
        fit_times = lag_times[:n_fit]
        fit_MSD = MSD_um[:n_fit]
        fit_err = MSD_err_um[:n_fit]
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
        # Per-segment MSD-slope D for error bar
        seg_D_msd = []
        for seg in selected:
            x = seg['x'].copy()
            y = seg['y'].copy()
            n_f = len(x)
            _ml = min(n_f // 2, max_lag)
            _nf = max(1, _ml // 4)
            _msd_s = np.zeros(_ml)
            for lag in range(_ml):
                dxl = x[lag+1:] - x[:n_f-lag-1]
                dyl = y[lag+1:] - y[:n_f-lag-1]
                _msd_s[lag] = np.mean(dxl**2 + dyl**2) if len(dxl) > 0 else 0
            _msd_um = _msd_s * PIXEL_SIZE**2
            _lt = (np.arange(_ml) + 1) * dt
            if _nf >= 2:
                try:
                    _c = np.polyfit(_lt[:_nf], _msd_um[:_nf], 1)
                    seg_D_msd.append(_c[0] / 4)
                except Exception:
                    pass
        if len(seg_D_msd) > 1:
            D_msd_err = np.std(seg_D_msd) / np.sqrt(len(seg_D_msd))
        else:
            D_msd_err = slope_err / 4

        # Power-law for alpha
        n_fit_power = max_lag // 2
        pl_t = lag_times[:n_fit_power]
        pl_msd = MSD_um[:n_fit_power]
        pl_err = MSD_err_um[:n_fit_power]
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
        fit_line_t = np.linspace(0, lag_times[n_fit-1], 100)
        ax.plot(fit_line_t, linear(fit_line_t, slope, intercept), 'r-', linewidth=2,
                label=f'Linear fit: D = {D_msd:.4f} $\\pm$ {D_msd_err:.4f} $\\mu$m$^2$/s')
        pl_line_t = np.linspace(dt, lag_times[n_fit_power-1], 100)
        ax.plot(pl_line_t, power_law(pl_line_t, K_fit, alpha_fit), 'g--', linewidth=2,
                label=f'Power law: $\\alpha$ = {alpha_fit:.2f}')
        ax.set_xlabel('Lag time $\\tau$ (s)', fontsize=12)
        ax.set_ylabel(r'MSD ($\mu$m$^2$)', fontsize=12)
        ax.set_title('MSD \u2014 Linear Scale')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        valid = MSD_um > 0
        ax.errorbar(lag_times[valid], MSD_um[valid], yerr=MSD_err_um[valid],
                    fmt='o', markersize=4, capsize=3, alpha=0.6, color='steelblue', label='MSD data')
        ref_t = np.logspace(np.log10(dt), np.log10(lag_times[-1]), 50)
        msd_at_1 = MSD_um[0] if MSD_um[0] > 0 else 1e-6
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
        stamp_version(fig)
        fig.savefig(str(FIGURES_DIR / 'msd_analysis.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

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
        stamp_version(fig)
        fig.savefig(str(FIGURES_DIR / 'D_comparison.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

        # ==============================================================
        # STEP 6b: COMBINED SUMMARY FIGURE (2x3 grid)
        # ==============================================================
        # All analysis plots in one figure for quick overview.
        # Layout:
        #   (0,0) Detection mask overlay    (0,1) Trajectories (px)    (0,2) Trajectories (um)
        #   (1,0) Displacement histogram    (1,1) MSD analysis         (1,2) D comparison bars
        print(f'  Generating combined summary figure...')

        # Parse a human-readable title from filename
        _parts = file_stem.replace('-', ' ').replace('_', ' ')
        _suptitle = f'{bead_diameter_um} um beads | {solute_pct}% {solute_label} | {TEMPERATURE_C_JOB}C | {date_folder}'

        fig_comb, axes_comb = plt.subplots(2, 3, figsize=(24, 14))

        # (0,0) Detection overlay — use first frame, GREEN=accepted, RED=rejected
        ax = axes_comb[0, 0]
        f1_key = sorted(mask_frames.keys())[0]
        gray_f, _, particles_f = mask_frames[f1_key]
        overlay_comb = cv2.cvtColor(gray_f, cv2.COLOR_GRAY2RGB)
        _frame_acc_comb = accepted_positions.get(f1_key, [])
        _nacc_c, _nrej_c = 0, 0
        for p in particles_f:
            cx, cy = p[0], p[1]
            r_det = int(p[2]) if len(p) > 2 else r_circle
            _matched_c = None
            for (_tx, _ty, _tid) in _frame_acc_comb:
                if (cx - _tx)**2 + (cy - _ty)**2 < _match_dist_sq:
                    _matched_c = _tid
                    break
            if _matched_c is not None:
                cv2.circle(overlay_comb, (int(cx), int(cy)), max(3, r_det), (0, 220, 0), 2)
                cv2.circle(overlay_comb, (int(cx), int(cy)), 3, (0, 150, 0), -1)
                _label_c = f'T{_matched_c}'
                _font_c = cv2.FONT_HERSHEY_SIMPLEX
                _fscale_c = 0.55
                _lx = int(cx) + r_det + 5
                _ly = int(cy) + 5
                (tw_c, th_c), _ = cv2.getTextSize(_label_c, _font_c, _fscale_c, 1)
                cv2.rectangle(overlay_comb, (_lx - 1, _ly - th_c - 2),
                              (_lx + tw_c + 1, _ly + 3), (255, 255, 255), -1)
                cv2.putText(overlay_comb, _label_c,
                            (_lx, _ly), _font_c,
                            _fscale_c, (0, 160, 0), 1, cv2.LINE_AA)
                _nacc_c += 1
            else:
                cv2.circle(overlay_comb, (int(cx), int(cy)), max(3, r_det), (220, 50, 50), 2)
                cv2.circle(overlay_comb, (int(cx), int(cy)), 2, (180, 30, 30), -1)
                _nrej_c += 1
        ax.imshow(overlay_comb)
        ax.set_title(f'Detection Overlay (frame {f1_key}, {_nacc_c} accepted / {_nrej_c} rejected)')
        ax.axis('off')

        # (0,1) Trajectories (px)
        ax = axes_comb[0, 1]
        colors_comb = plt.cm.tab10(np.linspace(0, 1, n_to_use))
        for seg, c in zip(selected, colors_comb):
            ax.plot(seg['x'], seg['y'], '-', linewidth=1, color=c, alpha=0.7)
            ax.plot(seg['x'][0], seg['y'][0], 'o', color=c, markersize=3)
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.set_title(f'Top {n_to_use} Trajectories (px)')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        # (0,2) Trajectories (um, from origin)
        ax = axes_comb[0, 2]
        for seg, c in zip(selected, colors_comb):
            x_um = (seg['x'] - seg['x'][0]) * PIXEL_SIZE
            y_um = (seg['y'] - seg['y'][0]) * PIXEL_SIZE
            ax.plot(x_um, y_um, '-o', markersize=1, linewidth=1, color=c, alpha=0.7)
        ax.set_xlabel(r'$\Delta X$ ($\mu$m)')
        ax.set_ylabel(r'$\Delta Y$ ($\mu$m)')
        ax.set_title(f'Displacement from Start')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        # (1,0) Displacement histogram (X only, for compactness)
        ax = axes_comb[1, 0]
        bw_x = bin_edges_x[1] - bin_edges_x[0]
        ax.bar(bin_centers_x, counts_x, width=bw_x,
               alpha=0.6, color='steelblue', label='Data')
        x_fine_c = np.linspace(bin_centers_x[0], bin_centers_x[-1], 200)
        ax.plot(x_fine_c, gaussian_pdf(x_fine_c, *popt_x), 'r-', linewidth=2,
                label=f'$\\sigma$={std_x_fit:.4f} $\\mu$m')
        ax.set_xlabel(r'$\Delta x$ per frame ($\mu$m)')
        ax.set_ylabel('Probability density')
        ax.set_title(f'X Displacement Histogram')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # (1,1) MSD analysis
        ax = axes_comb[1, 1]
        ax.errorbar(lag_times, MSD_um, yerr=MSD_err_um, fmt='o',
                    markersize=3, capsize=2, alpha=0.6, color='steelblue')
        fit_line_t = np.linspace(0, lag_times[n_fit-1], 100)
        ax.plot(fit_line_t, linear(fit_line_t, slope, intercept), 'r-', linewidth=2,
                label=f'D={D_msd:.4f} $\\mu$m$^2$/s')
        pl_line_t_c = np.linspace(dt, lag_times[n_fit_power-1], 100)
        ax.plot(pl_line_t_c, power_law(pl_line_t_c, K_fit, alpha_fit), 'g--', linewidth=2,
                label=f'$\\alpha$={alpha_fit:.2f}')
        ax.set_xlabel(r'$\tau$ (s)')
        ax.set_ylabel(r'MSD ($\mu$m$^2$)')
        ax.set_title('MSD Analysis')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # (1,2) D comparison bars
        ax = axes_comb[1, 2]
        methods_short = ['D_var', 'D_gauss', 'D_msd', 'Theory']
        D_vals_c = [D_direct, D_fit, D_msd, D_theory_faxen]
        D_errs_c = [D_direct_err, D_fit_err, D_msd_err, 0]
        bar_colors_c = ['steelblue', 'darkorange', 'forestgreen', 'crimson']
        bars_c = ax.bar(methods_short, D_vals_c, yerr=D_errs_c, capsize=4,
                        color=bar_colors_c, alpha=0.8, edgecolor='black', linewidth=0.5)
        for bar, val in zip(bars_c, D_vals_c):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(D_vals_c)*0.02,
                    f'{val:.4f}', ha='center', va='bottom', fontsize=8)
        ax.set_ylabel(r'$D$ ($\mu$m$^2$/s)')
        ax.set_title('D Comparison')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, max(D_vals_c) * 1.35)

        fig_comb.suptitle(_suptitle, fontsize=14, fontweight='bold')
        plt.tight_layout()
        stamp_version(fig_comb)
        fig_comb.savefig(str(FIGURES_DIR / 'combined_summary.png'), dpi=200, bbox_inches='tight')
        plt.close(fig_comb)

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
        summary_lines.append(f'Temperature: {TEMPERATURE_C_JOB} C ({TEMPERATURE:.2f} K)')
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
        summary_lines.append(f'Diffusion Coefficients (um^2/s) — noise-corrected:')
        summary_lines.append(f'  Method 1 (Direct Variance): {D_direct:.4f} +/- {D_direct_err:.4f}')
        summary_lines.append(f'  Method 2 (Gaussian Fit):     {D_fit:.4f} +/- {D_fit_err:.4f}')
        summary_lines.append(f'  Method 3 (MSD Slope):        {D_msd:.4f} +/- {D_msd_err:.4f}')
        summary_lines.append(f'')
        summary_lines.append(f'Noise Correction:')
        summary_lines.append(f'  sigma_noise: {SIGMA_NOISE_UM:.5f} um ({SIGMA_NOISE_UM/PIXEL_SIZE:.3f} px)')
        summary_lines.append(f'  D_var raw:   {D_direct_raw:.4f} -> corrected: {D_direct:.4f} um^2/s')
        summary_lines.append(f'  D_gauss raw: {D_fit_raw:.4f} -> corrected: {D_fit:.4f} um^2/s')
        summary_lines.append(f'  D_msd:       {D_msd:.4f} (self-correcting via MSD intercept)')
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
        with open(str(summary_file), 'w', encoding='utf-8') as f:
            f.write(summary_text)

        # --- Update volatile metadata in readme.txt ---
        update_volatile_metadata(FIGURES_DIR, D_direct, D_fit, D_msd,
                                 alpha_fit, len(tracks), n_to_use,
                                 max_disp_used=max_disp_adaptive,
                                 max_gap_used=max_gap_adaptive)

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

# ======================================================================
# CELL 4
# ======================================================================
# ============================================================================
# CELL 4 — OVERALL TREND PLOTS (scans ALL output folders)
# ============================================================================
# This cell reads summary.txt from every processed video folder, so the
# trend plots always include ALL data — even videos skipped in this run.

import re
from pathlib import Path

# FIGURES_ROOT already defined at the top of Cell 3

all_results = []
for summary_path in sorted(FIGURES_ROOT.rglob('summary.txt')):
    folder = summary_path.parent
    try:
        txt = summary_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        txt = summary_path.read_text(encoding='latin-1')

    # --- Parse key fields from summary.txt ---
    def _grab(pattern, default=None):
        m = re.search(pattern, txt)
        return m.group(1) if m else default

    video_name = folder.name
    date_str = folder.parent.name  # e.g. '2026-03-03'
    bead_str  = _grab(r'Bead diameter:\s*([\d.]+)')
    solute_str = _grab(r'Solute:\s*([\d.]+)%')
    solute_type = 'acetone' if 'Acetone' in txt else 'glycerol'
    eta_str   = _grab(r'Viscosity:\s*([\d.]+)\s*mPa')
    fps_str   = _grab(r'Frame rate:\s*([\d.]+)')
    d_var_str = _grab(r'Direct Variance\):\s*([\d.eE+-]+)')
    d_gau_str = _grab(r'Gaussian Fit\):\s*([\d.eE+-]+)')
    d_msd_str = _grab(r'MSD Slope\):\s*([\d.eE+-]+)')
    d_the_str = _grab(r'D_theory \(final\):\s*([\d.eE+-]+)')
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
        'video': video_name, 'date': date_str, 'bead': bead,
        'solute_pct': solute_pct, 'solute_type': solute_type,
        'solute_label': solute_label, 'eta': eta, 'fps': fps,
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
    cmap = plt.cm.tab20
    cond_colors = {c: cmap(i / max(len(unique_conditions) - 1, 1))
                   for i, c in enumerate(unique_conditions)}
    cond_labels = {c: f'{c[0]} um, {c[1]}' for c in unique_conditions}

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Overall Trends Across All Datasets (Sessions 5-7)', fontsize=15, weight='bold')

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
    ax.legend(fontsize=6, loc='upper left', ncol=2)

    # ---- (b) D vs viscosity ----
    ax = axes[0, 1]
    for cond in unique_conditions:
        pts = [r for r in all_results if condition_key(r) == cond]
        ax.scatter([r['eta'] for r in pts], [r['d_avg'] for r in pts],
                   color=cond_colors[cond], s=50, label=cond_labels[cond], zorder=3)
    # Theory curve for 3 um beads (use 20 C as average)
    eta_range = np.linspace(0.3, max(r['eta'] for r in all_results) * 1.1, 100)
    T_K = 293.15  # 20 C as representative average
    D_curve = k_B * T_K / (6 * np.pi * (eta_range * 1e-3) * 1.5e-6) * 1e12
    ax.plot(eta_range, D_curve, 'k--', alpha=0.4, label='S-E theory (3 um, 20C)')
    # Theory marker x for each condition
    for cond in unique_conditions:
        pts = [r for r in all_results if condition_key(r) == cond]
        for r in pts:
            ax.scatter(r['eta'], r['d_theory'], marker='x', s=80,
                       color=cond_colors[cond], linewidths=2, zorder=4)
    ax.set_xlabel(r'$\eta$ [mPa$\cdot$s]')
    ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
    ax.set_title(r'D vs Viscosity (circles=exp, x=theory)')
    ax.legend(fontsize=6, ncol=2)

    # ---- (c) D vs bead size ----
    ax = axes[1, 0]
    for cond in unique_conditions:
        pts = [r for r in all_results if condition_key(r) == cond]
        ax.scatter([r['bead'] for r in pts], [r['d_avg'] for r in pts],
                   color=cond_colors[cond], s=50, label=cond_labels[cond], zorder=3)
        for r in pts:
            ax.scatter(r['bead'], r['d_theory'], marker='x', s=80,
                       color=cond_colors[cond], linewidths=2, zorder=4)
    # S-E curve in water at bead sizes (20 C average)
    d_range = np.linspace(0.5, 6, 100)
    eta_water = get_glycerol_viscosity(0, 20.0)
    D_curve_size = k_B * T_K / (6 * np.pi * eta_water * (d_range / 2 * 1e-6)) * 1e12
    ax.plot(d_range, D_curve_size, 'k--', alpha=0.4, label='S-E theory (water, 20C)')
    ax.set_xlabel(r'Bead diameter [$\mu m$]')
    ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
    ax.set_title(r'D vs Bead Size (circles=exp, x=theory)')
    ax.legend(fontsize=6, ncol=2)

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
    stamp_version(fig)
    out_path = FIGURES_ROOT / 'overall_trends.png'
    fig.savefig(str(out_path), dpi=200, bbox_inches='tight')
    plt.close(fig)
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

    # ==================================================================
    # PER-DATE TREND PLOTS (one per session date)
    # ==================================================================
    dates = sorted(set(r['date'] for r in all_results))
    print(f'\nGenerating per-date trend plots for {len(dates)} dates...')

    for date in dates:
        date_results = [r for r in all_results if r['date'] == date]
        if len(date_results) < 2:
            continue

        date_conditions = sorted(set(condition_key(r) for r in date_results))
        date_cond_colors = {c: cmap(i / max(len(date_conditions) - 1, 1))
                            for i, c in enumerate(date_conditions)}

        fig_d, axes_d = plt.subplots(2, 2, figsize=(16, 12))
        fig_d.suptitle(f'Session {date} — Trends ({len(date_results)} videos)',
                       fontsize=15, weight='bold')

        # (a) Parity plot
        ax = axes_d[0, 0]
        for cond in date_conditions:
            pts = [r for r in date_results if condition_key(r) == cond]
            ax.scatter([r['d_theory'] for r in pts], [r['d_avg'] for r in pts],
                       color=date_cond_colors[cond], s=50, label=cond_labels.get(cond, str(cond)), zorder=3)
        lim = max(max(r['d_theory'] for r in date_results),
                  max(r['d_avg'] for r in date_results)) * 1.15
        ax.plot([0, lim], [0, lim], 'k--', alpha=0.3, label='1:1')
        ax.set_xlim(0, lim); ax.set_ylim(0, lim)
        ax.set_xlabel(r'$D_{\mathrm{theory}}$ [$\mu m^2/s$]')
        ax.set_ylabel(r'$D_{\mathrm{exp}}$ [$\mu m^2/s$]')
        ax.set_title('Parity Plot')
        ax.legend(fontsize=6, ncol=2)
        ax.grid(True, alpha=0.3)

        # (b) D vs viscosity
        ax = axes_d[0, 1]
        for cond in date_conditions:
            pts = [r for r in date_results if condition_key(r) == cond]
            ax.scatter([r['eta'] for r in pts], [r['d_avg'] for r in pts],
                       color=date_cond_colors[cond], s=50, label=cond_labels.get(cond, str(cond)), zorder=3)
            for r in pts:
                ax.scatter(r['eta'], r['d_theory'], marker='x', s=60,
                           color=date_cond_colors[cond], linewidths=1.5, zorder=4)
        ax.set_xlabel(r'$\eta$ [mPa$\cdot$s]')
        ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
        ax.set_title('D vs Viscosity')
        ax.legend(fontsize=6, ncol=2)
        ax.grid(True, alpha=0.3)

        # (c) D vs bead size
        ax = axes_d[1, 0]
        for cond in date_conditions:
            pts = [r for r in date_results if condition_key(r) == cond]
            ax.scatter([r['bead'] for r in pts], [r['d_avg'] for r in pts],
                       color=date_cond_colors[cond], s=50, label=cond_labels.get(cond, str(cond)), zorder=3)
            for r in pts:
                ax.scatter(r['bead'], r['d_theory'], marker='x', s=60,
                           color=date_cond_colors[cond], linewidths=1.5, zorder=4)
        ax.set_xlabel(r'Bead diameter [$\mu m$]')
        ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
        ax.set_title('D vs Bead Size')
        ax.legend(fontsize=6, ncol=2)
        ax.grid(True, alpha=0.3)

        # (d) Alpha bars
        ax = axes_d[1, 1]
        d_names = [r['video'][-25:] for r in date_results]
        d_alphas = [r['alpha'] for r in date_results]
        d_colors = [date_cond_colors.get(condition_key(r), 'gray') for r in date_results]
        y_pos = np.arange(len(d_names))
        ax.barh(y_pos, d_alphas, color=d_colors, edgecolor='none', height=0.7)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(d_names, fontsize=6)
        ax.axvline(x=1.0, color='red', linestyle='--', alpha=0.7)
        ax.set_xlabel(r'$\alpha$')
        ax.set_title(r'MSD Exponent $\alpha$')

        plt.tight_layout()
        stamp_version(fig_d)
        date_fig_path = FIGURES_ROOT / date / f'trends_{date}.png'
        fig_d.savefig(str(date_fig_path), dpi=200, bbox_inches='tight')
        plt.close(fig_d)
        print(f'  Saved: {date_fig_path}')

    # ==================================================================
    # LAB-LEVEL TREND PLOTS
    # ==================================================================
    # 1. D vs viscosity at constant bead size (one subplot per bead)
    # 2. D vs bead size at constant viscosity (one subplot per viscosity)
    print(f'\nGenerating lab-level trend plots...')

    bead_sizes = sorted(set(r['bead'] for r in all_results))
    glycerol_results = [r for r in all_results if r['solute_type'] == 'glycerol']

    if len(glycerol_results) >= 2:
        # --- D vs viscosity at constant bead size ---
        n_bead_panels = len(bead_sizes)
        fig_eta, axes_eta = plt.subplots(1, n_bead_panels, figsize=(6 * n_bead_panels, 5))
        if n_bead_panels == 1:
            axes_eta = [axes_eta]
        fig_eta.suptitle('D vs Viscosity at Constant Bead Size (glycerol only)',
                         fontsize=14, weight='bold')

        method_colors = {'D_var': 'steelblue', 'D_gauss': 'darkorange',
                         'D_msd': 'forestgreen', 'Theory': 'crimson'}

        for ax, bead in zip(axes_eta, bead_sizes):
            pts = [r for r in glycerol_results if r['bead'] == bead]
            if len(pts) == 0:
                ax.set_visible(False)
                continue
            etas = [r['eta'] for r in pts]
            ax.scatter(etas, [r['d_var'] for r in pts], c=method_colors['D_var'],
                       s=40, label='D_var', zorder=3, alpha=0.7)
            ax.scatter(etas, [r['d_gau'] for r in pts], c=method_colors['D_gauss'],
                       s=40, label='D_gauss', marker='s', zorder=3, alpha=0.7)
            ax.scatter(etas, [r['d_msd'] for r in pts], c=method_colors['D_msd'],
                       s=40, label='D_msd', marker='^', zorder=3, alpha=0.7)
            ax.scatter(etas, [r['d_theory'] for r in pts], c=method_colors['Theory'],
                       s=60, label='Theory', marker='x', linewidths=2, zorder=4)
            # Theory curve
            _eta_r = np.linspace(min(etas) * 0.8, max(etas) * 1.2, 50)
            _r_m = (bead / 2) * 1e-6
            _D_curve = k_B * 293.15 / (6 * np.pi * (_eta_r * 1e-3) * _r_m) * 1e12
            ax.plot(_eta_r, _D_curve, 'r--', alpha=0.3, linewidth=1.5)
            ax.set_xlabel(r'$\eta$ [mPa$\cdot$s]')
            ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
            ax.set_title(f'{bead} $\\mu$m beads')
            ax.legend(fontsize=7)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        stamp_version(fig_eta)
        fig_eta.savefig(str(FIGURES_ROOT / 'D_vs_viscosity_by_bead.png'),
                        dpi=200, bbox_inches='tight')
        plt.close(fig_eta)
        print(f'  Saved: D_vs_viscosity_by_bead.png')

        # --- D vs bead size at constant viscosity ---
        viscosities = sorted(set(r['solute_label'] for r in glycerol_results))
        n_visc_panels = len(viscosities)
        fig_bead, axes_bead = plt.subplots(1, n_visc_panels,
                                            figsize=(6 * n_visc_panels, 5))
        if n_visc_panels == 1:
            axes_bead = [axes_bead]
        fig_bead.suptitle('D vs Bead Size at Constant Viscosity (glycerol only)',
                          fontsize=14, weight='bold')

        for ax, visc_label in zip(axes_bead, viscosities):
            pts = [r for r in glycerol_results if r['solute_label'] == visc_label]
            if len(pts) == 0:
                ax.set_visible(False)
                continue
            beads_p = [r['bead'] for r in pts]
            ax.scatter(beads_p, [r['d_var'] for r in pts], c=method_colors['D_var'],
                       s=40, label='D_var', zorder=3, alpha=0.7)
            ax.scatter(beads_p, [r['d_gau'] for r in pts], c=method_colors['D_gauss'],
                       s=40, label='D_gauss', marker='s', zorder=3, alpha=0.7)
            ax.scatter(beads_p, [r['d_msd'] for r in pts], c=method_colors['D_msd'],
                       s=40, label='D_msd', marker='^', zorder=3, alpha=0.7)
            ax.scatter(beads_p, [r['d_theory'] for r in pts], c=method_colors['Theory'],
                       s=60, label='Theory', marker='x', linewidths=2, zorder=4)
            # Theory curve
            _d_r = np.linspace(0.5, max(beads_p) * 1.2, 50)
            _eta_avg = np.mean([r['eta'] for r in pts]) * 1e-3  # Pa.s
            _D_curve_b = k_B * 293.15 / (6 * np.pi * _eta_avg * (_d_r / 2 * 1e-6)) * 1e12
            ax.plot(_d_r, _D_curve_b, 'r--', alpha=0.3, linewidth=1.5)
            ax.set_xlabel(r'Bead diameter [$\mu m$]')
            ax.set_ylabel(r'$D$ [$\mu m^2/s$]')
            ax.set_title(f'{visc_label}')
            ax.legend(fontsize=7)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        stamp_version(fig_bead)
        fig_bead.savefig(str(FIGURES_ROOT / 'D_vs_bead_by_viscosity.png'),
                         dpi=200, bbox_inches='tight')
        plt.close(fig_bead)
        print(f'  Saved: D_vs_bead_by_viscosity.png')

