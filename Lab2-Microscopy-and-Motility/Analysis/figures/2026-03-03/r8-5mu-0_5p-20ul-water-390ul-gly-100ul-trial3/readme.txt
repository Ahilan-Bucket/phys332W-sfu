# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:35:09.058730
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = r8-5mu-0_5p-20ul-water-390ul-gly-100ul-trial3.avi
fps = 29.0
total_frames = 240
width = 1440
height = 1080
bead_diameter_um = 5.0
solute_pct = 20.0
solute_type = glycerol
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
d_variance = 0.115344
d_gauss = 0.046737
d_msd = 0.074297
alpha = 0.7185
n_tracks = 2
n_segs = 2
last_processed = 2026-03-05T13:35:09.057706
max_displacement_px = 15
max_gap_frames = 6

