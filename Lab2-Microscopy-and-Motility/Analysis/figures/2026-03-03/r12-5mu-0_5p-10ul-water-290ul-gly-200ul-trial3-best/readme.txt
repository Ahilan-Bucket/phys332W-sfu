# === VIDEO METADATA (readme.txt) ===
# Last updated: 2026-03-05T13:39:14.280163
#
# [constants] — write-once (video properties from file + JOBS tuple)
# [detection] — AUTO = use preset; MANUAL = interactive tuning overrides
# [volatile]  — overwritten every pipeline run

[constants]
filename = r12-5mu-0_5p-10ul-water-290ul-gly-200ul-trial3-best.avi
fps = 29.0
total_frames = 240
width = 1440
height = 1080
bead_diameter_um = 5.0
solute_pct = 40.0
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
d_variance = 0.025732
d_gauss = 0.013682
d_msd = 0.086711
alpha = 0.8445
n_tracks = 9
n_segs = 5
last_processed = 2026-03-05T13:39:14.279164
max_displacement_px = 15
max_gap_frames = 6

