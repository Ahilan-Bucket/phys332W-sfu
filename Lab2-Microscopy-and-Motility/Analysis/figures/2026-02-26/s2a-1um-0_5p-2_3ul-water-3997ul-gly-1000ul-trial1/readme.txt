# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:16:03.292355
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial1.avi
fps = 29.0
total_frames = 240
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
d_variance = 0.173236
d_gauss = 0.130521
d_msd = 0.244053
alpha = 0.9984
n_tracks = 4
n_segs = 4
last_processed = 2026-03-05T13:16:03.292355
max_displacement_px = 30
max_gap_frames = 8

