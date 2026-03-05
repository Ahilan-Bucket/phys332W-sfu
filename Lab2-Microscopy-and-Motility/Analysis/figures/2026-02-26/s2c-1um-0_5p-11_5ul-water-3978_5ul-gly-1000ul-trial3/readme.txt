# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:20:09.179895
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial3.avi
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
d_variance = 0.091843
d_gauss = 0.032835
d_msd = 0.302539
alpha = 0.5379
n_tracks = 11
n_segs = 12
last_processed = 2026-03-05T13:20:09.178896
max_displacement_px = 30
max_gap_frames = 8

