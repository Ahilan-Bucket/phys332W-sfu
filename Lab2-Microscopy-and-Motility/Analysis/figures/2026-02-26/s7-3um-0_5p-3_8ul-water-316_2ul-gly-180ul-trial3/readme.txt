# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:22:31.132983
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial3.avi
fps = 29.0
total_frames = 120
width = 1440
height = 1080
bead_diameter_um = 3.0
solute_pct = 36.3
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
d_variance = 0.044684
d_gauss = 0.000485
d_msd = 0.252192
alpha = 0.8052
n_tracks = 3
n_segs = 3
last_processed = 2026-03-05T13:22:31.131993
max_displacement_px = 15
max_gap_frames = 4

