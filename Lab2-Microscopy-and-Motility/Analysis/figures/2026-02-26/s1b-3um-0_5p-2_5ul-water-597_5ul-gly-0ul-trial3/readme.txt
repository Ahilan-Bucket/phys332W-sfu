# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:14:21.722473
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial3.avi
fps = 29.0
total_frames = 120
width = 1440
height = 1080
bead_diameter_um = 3.0
solute_pct = 0.0
solute_type = glycerol
temp_c = 21.0
pixel_size_um = 0.0684

[detection]
mode = AUTO
threshold = 15
blur_sigma = 1.5
close_k_factor = 0.6
min_fill_ratio = 0.4
max_aspect_ratio = 3.0
area_mult_min = 0.1
area_mult_max = 6.0

[volatile]
pipeline_version = 2.3
d_variance = 0.053465
d_gauss = 0.038852
d_msd = 0.042236
alpha = 0.2393
n_tracks = 10
n_segs = 10
last_processed = 2026-03-05T13:14:21.722473
max_displacement_px = 15
max_gap_frames = 4

