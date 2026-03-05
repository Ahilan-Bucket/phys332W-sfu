# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:42:24.617002
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = r14-2_1mu-0_5p-4ul-acetone-498ul-trial1.avi
fps = 29.0
total_frames = 241
width = 1440
height = 1080
bead_diameter_um = 2.1
solute_pct = 100.0
solute_type = acetone
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
d_variance = 0.291078
d_gauss = 0.292727
d_msd = 0.315179
alpha = 0.9359
n_tracks = 11
n_segs = 11
last_processed = 2026-03-05T13:42:24.615586
max_displacement_px = 15
max_gap_frames = 3

