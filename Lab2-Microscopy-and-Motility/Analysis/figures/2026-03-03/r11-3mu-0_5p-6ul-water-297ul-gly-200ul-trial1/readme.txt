# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:37:27.709429
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = r11-3mu-0_5p-6ul-water-297ul-gly-200ul-trial1.avi
fps = 29.0
total_frames = 240
width = 1440
height = 1080
bead_diameter_um = 3.0
solute_pct = 40.0
solute_type = glycerol
temp_c = 19.0
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
d_variance = 0.037239
d_gauss = 0.000236
d_msd = 0.174388
alpha = 0.2693
n_tracks = 9
n_segs = 7
last_processed = 2026-03-05T13:37:27.708410
max_displacement_px = 15
max_gap_frames = 4

