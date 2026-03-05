"""Apply detection fixes to the pipeline notebook.
Run once, then delete this file.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

NB_PATH = r'D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Analysis\Lab2_Analysis_Pipeline.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Helper to get cell source as string
def get_src(idx):
    s = nb['cells'][idx]['source']
    return ''.join(s) if isinstance(s, list) else s

def set_src(idx, s):
    nb['cells'][idx]['source'] = s

# =====================================================================
# FIX 1 — Cell 2: compute_temporal_median → percentile-based background
# =====================================================================
cell2 = get_src(2)

old_bg = (
    'def compute_temporal_median(cap, sample_every=10):\n'
    '    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))\n'
    '    frames_sampled = []\n'
    '    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)\n'
    '    for i in range(0, total_frames, sample_every):\n'
    '        cap.set(cv2.CAP_PROP_POS_FRAMES, i)\n'
    '        ret, frame = cap.read()\n'
    '        if not ret:\n'
    '            break\n'
    '        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame\n'
    '        frames_sampled.append(gray.astype(np.float32))\n'
    '    if len(frames_sampled) == 0:\n'
    "        raise RuntimeError('Could not read any frames from video')\n"
    "    print(f'  Sampled {len(frames_sampled)} frames for background estimation')\n"
    '    return np.median(np.stack(frames_sampled), axis=0).astype(np.uint8)'
)

new_bg = (
    'def compute_temporal_median(cap, sample_every=10, percentile=30):\n'
    '    """Build a background image from a low percentile of sampled frames.\n'
    '    \n'
    '    WHY a low percentile instead of median (50th)?\n'
    '    --------------------------------------------------\n'
    '    Phase-contrast beads are bright spots.  A bead that barely moves during\n'
    '    the video sits near the same pixel in every sampled frame.  The *median*\n'
    '    of those pixels equals the bead\'s own brightness, so (frame - background)\n'
    '    = 0 and the bead disappears from the detection mask.\n'
    '    \n'
    '    Using a LOW percentile (default 30th) picks the *dimmest* value each\n'
    '    pixel ever had.  For pixels where a bead sometimes sat, the 30th-pctile\n'
    '    grabs a frame when the bead was elsewhere (or at its dimmest), producing\n'
    '    a background darker than the bead -> positive (frame - background) signal\n'
    '    -> the bead becomes detectable.\n'
    '    \n'
    '    Trade-off: lowering the percentile increases background noise, which is\n'
    '    why we don\'t go below ~25.  30 is a good balance.\n'
    '    """\n'
    '    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))\n'
    '    frames_sampled = []\n'
    '    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)\n'
    '    for i in range(0, total_frames, sample_every):\n'
    '        cap.set(cv2.CAP_PROP_POS_FRAMES, i)\n'
    '        ret, frame = cap.read()\n'
    '        if not ret:\n'
    '            break\n'
    '        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame\n'
    '        frames_sampled.append(gray.astype(np.float32))\n'
    '    if len(frames_sampled) == 0:\n'
    "        raise RuntimeError('Could not read any frames from video')\n"
    "    print(f'  Sampled {len(frames_sampled)} frames for background (p={percentile})')\n"
    '    return np.percentile(np.stack(frames_sampled), percentile, axis=0).astype(np.uint8)'
)

if old_bg in cell2:
    cell2 = cell2.replace(old_bg, new_bg)
    print('FIX 1: compute_temporal_median -> percentile-based (p=30)')
else:
    print('ERROR: Could not find compute_temporal_median')

# =====================================================================
# FIX 2 — Cell 2: detect_particles → adaptive kernel + proximity merge
# =====================================================================

# Find the function boundaries
lines = cell2.split('\n')
start = None
end = None
for i, line in enumerate(lines):
    if line.startswith('def detect_particles('):
        start = i
    if start is not None and i > start and line.startswith('def '):
        end = i
        break

if start is not None and end is not None:
    # Replace the entire function
    new_func_lines = [
        'def detect_particles(gray_frame, background, threshold, blur_sigma,',
        '                     min_area, max_area, bead_radius_px=10,',
        '                     edge_margin=0, min_fill_ratio=0.0, max_aspect_ratio=999):',
        '    """Detect bright particles via background subtraction + connected components.',
        '    ',
        '    Key design choices (from systematic mask inspection across all videos):',
        '    ',
        '    1. cv2.subtract (positive-only diff) instead of cv2.absdiff:',
        '       Phase-contrast microscopy produces bright bead centres with dark halos.',
        '       subtract() clips negative values to 0, keeping only bright-above-background',
        '       pixels and eliminating dark-ring false detections.',
        '    ',
        '    2. Adaptive morphological closing kernel (proportional to bead size):',
        '       Phase contrast creates a bright centre + a separate bright crescent',
        '       from the halo edge.  A small (3x3) close kernel cannot bridge the gap',
        '       for large beads (5 um ~ 36 px diameter).  Using a kernel proportional',
        '       to bead_radius_px merges the centre and crescent into one blob BEFORE',
        '       connected-component labelling, preventing double detection at the source.',
        '    ',
        '    3. Fill-ratio filter: reject hollow crescents (fill < 0.4 of bounding box).',
        '    4. Aspect-ratio filter: reject elongated artifacts (aspect > 3).',
        '    5. Edge exclusion: reject blobs near frame border (vignetting artifacts).',
        '    ',
        '    6. Proximity merge (post-detection):',
        '       Even after morphological closing, two blobs from the same bead can',
        '       survive.  Any two centroids within 1.5x bead diameter are merged,',
        '       keeping the brighter one.',
        '    """',
        '    h_frame, w_frame = gray_frame.shape[:2]',
        '',
        '    ksize = int(blur_sigma * 4) | 1',
        '    blurred = cv2.GaussianBlur(gray_frame, (ksize, ksize), blur_sigma)',
        '',
        '    # --- POSITIVE-ONLY difference ---',
        '    diff = cv2.subtract(blurred, background)',
        '',
        '    _, binary = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)',
        '',
        '    # --- Adaptive morphological clean-up ---',
        '    # Open (small kernel): remove salt noise without destroying small beads',
        '    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))',
        '    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_open)',
        '    ',
        '    # Close (bead-proportional kernel): bridge centre-to-crescent gap',
        '    # 3 um beads (~22 px diam) -> close_k ~ 7',
        '    # 5 um beads (~37 px diam) -> close_k ~ 11',
        '    # 1 um beads  (~7 px diam) -> close_k ~ 3',
        '    close_k = max(3, int(bead_radius_px * 0.6) | 1)',
        '    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,',
        '                                             (close_k, close_k))',
        '    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_close)',
        '',
        '    n_labels, labels, stats, centroids_cv = cv2.connectedComponentsWithStats(',
        '        binary, connectivity=8)',
        '',
        '    # --- Collect candidate particles with intensity weights ---',
        '    candidates = []  # (cx, cy, weight_sum)',
        '    for label_id in range(1, n_labels):',
        '        area = stats[label_id, cv2.CC_STAT_AREA]',
        '        if area < min_area or area > max_area:',
        '            continue',
        '',
        '        x_bb = stats[label_id, cv2.CC_STAT_LEFT]',
        '        y_bb = stats[label_id, cv2.CC_STAT_TOP]',
        '        w_bb = stats[label_id, cv2.CC_STAT_WIDTH]',
        '        h_bb = stats[label_id, cv2.CC_STAT_HEIGHT]',
        '',
        '        # --- Fill-ratio filter ---',
        '        bbox_area = max(w_bb * h_bb, 1)',
        '        fill_ratio = area / bbox_area',
        '        if fill_ratio < min_fill_ratio:',
        '            continue',
        '',
        '        # --- Aspect-ratio filter ---',
        '        aspect = max(w_bb, h_bb) / max(min(w_bb, h_bb), 1)',
        '        if aspect > max_aspect_ratio:',
        '            continue',
        '',
        '        # --- Intensity-weighted centroid ---',
        '        mask = (labels == label_id)',
        '        weights = diff[mask].astype(np.float64)',
        '        weight_sum = weights.sum()',
        '        if weight_sum > 0:',
        '            ys, xs = np.where(mask)',
        '            cx = np.average(xs.astype(np.float64), weights=weights)',
        '            cy = np.average(ys.astype(np.float64), weights=weights)',
        '        else:',
        '            cx = centroids_cv[label_id, 0]',
        '            cy = centroids_cv[label_id, 1]',
        '            weight_sum = float(area)',
        '',
        '        # --- Edge exclusion ---',
        '        if edge_margin > 0:',
        '            if (cx < edge_margin or cx > w_frame - edge_margin or',
        '                cy < edge_margin or cy > h_frame - edge_margin):',
        '                continue',
        '',
        '        candidates.append((cx, cy, weight_sum))',
        '',
        '    # --- Proximity merge ---',
        '    # Phase-contrast can split one bead into two blobs (bright centre +',
        '    # bright crescent).  Merge centroids within 1.5x bead diameter.',
        '    merge_dist_sq = (bead_radius_px * 3.0) ** 2  # (1.5 * diam)^2',
        '    candidates.sort(key=lambda c: c[2], reverse=True)  # brightest first',
        '    merged = []',
        '    used = set()',
        '    for i, (cx_i, cy_i, w_i) in enumerate(candidates):',
        '        if i in used:',
        '            continue',
        '        for j in range(i + 1, len(candidates)):',
        '            if j in used:',
        '                continue',
        '            dx = candidates[j][0] - cx_i',
        '            dy = candidates[j][1] - cy_i',
        '            if dx * dx + dy * dy < merge_dist_sq:',
        '                used.add(j)  # suppress weaker duplicate',
        '        merged.append((cx_i, cy_i))',
        '',
        '    return merged, binary',
        '',
        '',
    ]

    before = lines[:start]
    after = lines[end:]
    cell2 = '\n'.join(before + new_func_lines + after)
    print(f'FIX 2: detect_particles replaced (lines {start}-{end}) with adaptive kernel + proximity merge')
else:
    print(f'ERROR: Could not find detect_particles boundaries: start={start}, end={end}')

set_src(2, cell2)

# =====================================================================
# FIX 3 — Cell 3: Pass bead_radius_px to detect_particles
# =====================================================================
cell3 = get_src(3)

old_call = (
    '            particles, binary = detect_particles(\n'
    '                gray, background, effective_threshold,\n'
    '                GAUSSIAN_BLUR_SIGMA, min_particle_area, max_particle_area,\n'
    '                edge_margin=EDGE_MARGIN,\n'
    '                min_fill_ratio=MIN_FILL_RATIO,\n'
    '                max_aspect_ratio=MAX_ASPECT_RATIO)'
)

new_call = (
    '            particles, binary = detect_particles(\n'
    '                gray, background, effective_threshold,\n'
    '                GAUSSIAN_BLUR_SIGMA, min_particle_area, max_particle_area,\n'
    '                bead_radius_px=_bead_radius_px,\n'
    '                edge_margin=EDGE_MARGIN,\n'
    '                min_fill_ratio=MIN_FILL_RATIO,\n'
    '                max_aspect_ratio=MAX_ASPECT_RATIO)'
)

if old_call in cell3:
    cell3 = cell3.replace(old_call, new_call)
    print('FIX 3: Added bead_radius_px to detect_particles call in Cell 3')
else:
    print('ERROR: Could not find detect_particles call in Cell 3')

set_src(3, cell3)

# =====================================================================
# FIX 4 — Cell 1: Set FORCE_REPROCESS = True for full rerun
# =====================================================================
cell1 = get_src(1)
cell1 = cell1.replace('FORCE_REPROCESS = False', 'FORCE_REPROCESS = True')
print('FIX 4: FORCE_REPROCESS = True')
set_src(1, cell1)

# Save
with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('\nAll fixes applied and saved.')
