# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:45:38.920990
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = r16-5mu-0_5p-20ul-acetone-490-trial1.avi
fps = 29.0
total_frames = 240
width = 1440
height = 1080
bead_diameter_um = 5.0
solute_pct = 100.0
solute_type = acetone
temp_c = 19.0
pixel_size_um = 0.0684

[detection]
mode = AUTO
threshold = 15
blur_sigma = 2.0
close_k_factor = 0.7
min_fill_ratio = 0.45
max_aspect_ratio = 2.5
area_mult_min = 0.1
area_mult_max = 5.0

[volatile]
pipeline_version = 2.3
d_variance = 0.103650
d_gauss = 0.026308
d_msd = 0.034140
alpha = 0.3616
n_tracks = 4
n_segs = 4
last_processed = 2026-03-05T13:45:38.919992
max_displacement_px = 15
max_gap_frames = 6

