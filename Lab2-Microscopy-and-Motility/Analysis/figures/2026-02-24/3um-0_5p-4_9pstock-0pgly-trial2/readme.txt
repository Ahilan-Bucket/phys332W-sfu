# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:13:53.609404
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = 3um-0_5p-4_9pstock-0pgly-trial2.avi
fps = 30.0
total_frames = 240
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
d_variance = 0.048298
d_gauss = 0.000117
d_msd = 0.140926
alpha = 0.3946
n_tracks = 65
n_segs = 63
last_processed = 2026-03-05T13:13:53.608404
max_displacement_px = 15
max_gap_frames = 4

