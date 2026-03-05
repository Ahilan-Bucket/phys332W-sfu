# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:16:35.247889
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial2.avi
fps = 29.0
total_frames = 120
width = 1440
height = 1080
bead_diameter_um = 1.0
solute_pct = 20.0
solute_type = glycerol
temp_c = 21.0
pixel_size_um = 0.0684

[detection]
mode = AUTO
threshold = 7
blur_sigma = 1.2
close_k_factor = 0.8
min_fill_ratio = 0.25
max_aspect_ratio = 3.5
area_mult_min = 0.08
area_mult_max = 8.0

[volatile]
pipeline_version = 2.3
d_variance = 0.246475
d_gauss = 0.226858
d_msd = 0.530231
alpha = 0.7264
n_tracks = 6
n_segs = 4
last_processed = 2026-03-05T13:16:35.246890
max_displacement_px = 30
max_gap_frames = 8

