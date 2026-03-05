# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:35:51.374445
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = r10-2_1mu-0_5p-4ul-water-298ul-gly-200ul-trial1.avi
fps = 29.0
total_frames = 240
width = 1440
height = 1080
bead_diameter_um = 2.1
solute_pct = 40.0
solute_type = glycerol
temp_c = 19.0
pixel_size_um = 0.0684

[detection]
mode = AUTO
threshold = 12
blur_sigma = 1.2
close_k_factor = 0.5
min_fill_ratio = 0.4
max_aspect_ratio = 3.0
area_mult_min = 0.1
area_mult_max = 6.0

[volatile]
pipeline_version = 2.3
d_variance = 0.072736
d_gauss = 0.050743
d_msd = 0.059488
alpha = 0.5514
n_tracks = 2
n_segs = 2
last_processed = 2026-03-05T13:35:51.373444
max_displacement_px = 15
max_gap_frames = 3

