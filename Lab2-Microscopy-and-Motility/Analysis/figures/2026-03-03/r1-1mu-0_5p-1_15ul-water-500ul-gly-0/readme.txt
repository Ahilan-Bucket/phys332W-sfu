# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-04T20:52:40.591353
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi
fps = 29.0
total_frames = 240
width = 1440
height = 1080
bead_diameter_um = 1.0
solute_pct = 0.0
solute_type = glycerol
temp_c = 19.0
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
d_variance = 0.251530
d_gauss = 0.090840
d_msd = 0.949875
alpha = 0.6277
n_tracks = 78
n_segs = 93
last_processed = 2026-03-04T20:52:40.590354
max_displacement_px = 30
max_gap_frames = 8

