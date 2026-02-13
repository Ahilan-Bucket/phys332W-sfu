#!/usr/bin/env python3
"""
track_onion_particles.py
Automated particle tracking for onion cell intracellular streaming.
Outputs MTrack2-compatible tab-separated text file for use with
Diffusion_Analysis_Corrected.ipynb.

Usage: python track_onion_particles.py
"""

import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment
import os
import sys
import time

# =============================================================================
# USER-CONFIGURABLE PARAMETERS
# =============================================================================

# Input / Output
INPUT_VIDEO = '../Data/12-Feb/onion2.avi'
OUTPUT_FILE = '../Data/12-Feb/onion2-trackresults.txt'
DIAGNOSTICS_DIR = '../Data/12-Feb/diagnostics'

# Background estimation
BG_SAMPLE_EVERY = 10          # Sample every Nth frame for temporal median

# Detection parameters
GAUSSIAN_BLUR_SIGMA = 1.5    # Gaussian blur sigma for noise reduction
DETECTION_THRESHOLD = 15      # Intensity threshold above background (0-255)
MIN_PARTICLE_AREA = 4         # Minimum connected component area (px^2)
MAX_PARTICLE_AREA = 200       # Maximum connected component area (px^2)

# Tracking parameters
MAX_DISPLACEMENT = 10         # Maximum linking distance (px/frame)
MAX_GAP_FRAMES = 3            # Allow gap-closing up to N frames
MIN_TRACK_LENGTH = 10         # Minimum track length to keep (frames)
MIN_TOTAL_DISPLACEMENT = 3.0  # Minimum net displacement to keep (px)

# Diagnostic output
DIAGNOSTIC_MODE = True        # Save annotated frames for visual verification
DIAGNOSTIC_FRAMES = [1, 2, 3, 4, 5]  # Which frames to save diagnostics for


# =============================================================================
# BACKGROUND ESTIMATION
# =============================================================================

def compute_temporal_median(cap, sample_every=BG_SAMPLE_EVERY):
    """
    Compute per-pixel temporal median from sampled frames.
    Static structures (cell walls, vacuoles) become the background;
    moving particles are suppressed by the median.
    """
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_sampled = []

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    for i in range(0, total_frames, sample_every):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        frames_sampled.append(gray.astype(np.float32))

    if len(frames_sampled) == 0:
        raise RuntimeError("Could not read any frames from video")

    print(f"  Sampled {len(frames_sampled)} frames for background estimation")
    background = np.median(np.stack(frames_sampled), axis=0).astype(np.uint8)
    return background


# =============================================================================
# PARTICLE DETECTION
# =============================================================================

def detect_particles(gray_frame, background, threshold=DETECTION_THRESHOLD,
                     blur_sigma=GAUSSIAN_BLUR_SIGMA, min_area=MIN_PARTICLE_AREA,
                     max_area=MAX_PARTICLE_AREA):
    """
    Detect particles in a single frame by background subtraction + thresholding.

    Returns:
        list of (x, y) centroid positions (sub-pixel, float)
        binary mask (for diagnostics)
    """
    # Gaussian blur for noise reduction
    ksize = int(blur_sigma * 4) | 1  # ensure odd kernel size
    blurred = cv2.GaussianBlur(gray_frame, (ksize, ksize), blur_sigma)

    # Background subtraction (absolute difference)
    diff = cv2.absdiff(blurred, background)

    # Fixed threshold
    _, binary = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Connected component analysis
    n_labels, labels, stats, centroids_cv = cv2.connectedComponentsWithStats(
        binary, connectivity=8
    )

    # Filter by area and compute intensity-weighted centroids
    particles = []
    for label_id in range(1, n_labels):  # skip background (label 0)
        area = stats[label_id, cv2.CC_STAT_AREA]
        if area < min_area or area > max_area:
            continue

        # Intensity-weighted centroid for sub-pixel accuracy
        mask = (labels == label_id)
        weights = diff[mask].astype(np.float64)
        weight_sum = weights.sum()

        if weight_sum > 0:
            ys, xs = np.where(mask)
            cx = np.average(xs.astype(np.float64), weights=weights)
            cy = np.average(ys.astype(np.float64), weights=weights)
        else:
            # Fallback to geometric centroid
            cx = centroids_cv[label_id, 0]
            cy = centroids_cv[label_id, 1]

        particles.append((cx, cy))

    return particles, binary


# =============================================================================
# FRAME-TO-FRAME LINKING (HUNGARIAN ALGORITHM)
# =============================================================================

def link_particles(prev_positions, curr_positions, max_disp):
    """
    Link particles between consecutive frames using the Hungarian algorithm.

    Returns:
        matches: dict {prev_idx: curr_idx}
        unmatched_curr: list of curr_idx with no match
        unmatched_prev: list of prev_idx with no match
    """
    n_prev = len(prev_positions)
    n_curr = len(curr_positions)

    if n_prev == 0:
        return {}, list(range(n_curr)), []
    if n_curr == 0:
        return {}, [], list(range(n_prev))

    # Build cost matrix
    INF = 1e9
    cost = np.full((n_prev, n_curr), INF)
    for i, (px, py) in enumerate(prev_positions):
        for j, (cx, cy) in enumerate(curr_positions):
            d = np.sqrt((px - cx)**2 + (py - cy)**2)
            if d <= max_disp:
                cost[i, j] = d

    row_ind, col_ind = linear_sum_assignment(cost)

    matches = {}
    for r, c in zip(row_ind, col_ind):
        if cost[r, c] < INF:
            matches[r] = c

    matched_curr = set(matches.values())
    matched_prev = set(matches.keys())
    unmatched_curr = [j for j in range(n_curr) if j not in matched_curr]
    unmatched_prev = [i for i in range(n_prev) if i not in matched_prev]

    return matches, unmatched_curr, unmatched_prev


# =============================================================================
# MAIN TRACKING LOOP
# =============================================================================

def track_all_frames(detections_per_frame, max_disp, max_gap, min_length):
    """
    Link detections across all frames into tracks.

    Args:
        detections_per_frame: dict {frame_number: [(x, y), ...]}
        max_disp: maximum displacement per frame (px)
        max_gap: maximum gap to attempt re-linking (frames)
        min_length: minimum track length to keep

    Returns:
        list of track dicts with keys: id, positions, flags, start_frame, end_frame
    """
    all_tracks = []
    active_tracks = []  # tracks that could still be extended
    next_id = 1

    frame_numbers = sorted(detections_per_frame.keys())

    for frame_num in frame_numbers:
        curr_detections = detections_per_frame[frame_num]

        # Collect last known positions from active tracks
        prev_positions = []
        prev_track_indices = []
        prev_gap_sizes = []

        for i, track in enumerate(active_tracks):
            gap = frame_num - track['last_seen_frame']
            if gap <= max_gap + 1:
                pos = track['positions'][track['last_seen_frame']]
                prev_positions.append(pos)
                prev_track_indices.append(i)
                prev_gap_sizes.append(gap)

        # Scale max displacement by gap size for gap-closing
        effective_max_disps = [max_disp * g for g in prev_gap_sizes]

        # For Hungarian, use the maximum of all effective displacements as gate
        # but check individual constraints after
        if len(prev_positions) > 0 and len(curr_detections) > 0:
            n_prev = len(prev_positions)
            n_curr = len(curr_detections)
            INF = 1e9
            cost = np.full((n_prev, n_curr), INF)

            for i, (px, py) in enumerate(prev_positions):
                for j, (cx, cy) in enumerate(curr_detections):
                    d = np.sqrt((px - cx)**2 + (py - cy)**2)
                    if d <= effective_max_disps[i]:
                        cost[i, j] = d

            row_ind, col_ind = linear_sum_assignment(cost)

            matches = {}
            for r, c in zip(row_ind, col_ind):
                if cost[r, c] < INF:
                    matches[r] = c

            matched_curr = set(matches.values())
            unmatched_curr = [j for j in range(n_curr) if j not in matched_curr]
        else:
            matches = {}
            unmatched_curr = list(range(len(curr_detections)))

        # Update matched tracks
        matched_track_set = set()
        for prev_idx, curr_idx in matches.items():
            track_idx = prev_track_indices[prev_idx]
            track = active_tracks[track_idx]
            gap = frame_num - track['last_seen_frame']

            track['positions'][frame_num] = curr_detections[curr_idx]
            # Flag gap-closed frames
            if gap > 1:
                track['flags'][frame_num] = '*'
            else:
                track['flags'][frame_num] = ' '
            track['last_seen_frame'] = frame_num
            track['end_frame'] = frame_num
            matched_track_set.add(track_idx)

        # Move expired tracks to finished list
        still_active = []
        for i, track in enumerate(active_tracks):
            if frame_num - track['last_seen_frame'] > max_gap:
                all_tracks.append(track)
            else:
                still_active.append(track)
        active_tracks = still_active

        # Start new tracks for unmatched detections
        for curr_idx in unmatched_curr:
            new_track = {
                'id': next_id,
                'positions': {frame_num: curr_detections[curr_idx]},
                'flags': {frame_num: ' '},
                'start_frame': frame_num,
                'end_frame': frame_num,
                'last_seen_frame': frame_num,
            }
            active_tracks.append(new_track)
            next_id += 1

    # Finalize remaining active tracks
    all_tracks.extend(active_tracks)

    return all_tracks


# =============================================================================
# TRACK CLEANING
# =============================================================================

def clean_tracks(tracks, min_length=MIN_TRACK_LENGTH,
                 min_displacement=MIN_TOTAL_DISPLACEMENT):
    """
    Remove spurious tracks:
    - Too short (< min_length frames)
    - Stationary (net displacement < min_displacement px)
    """
    cleaned = []
    for track in tracks:
        frames = sorted(track['positions'].keys())
        if len(frames) < min_length:
            continue

        # Net displacement (start to end)
        first = track['positions'][frames[0]]
        last = track['positions'][frames[-1]]
        net_disp = np.sqrt((last[0] - first[0])**2 + (last[1] - first[1])**2)

        if net_disp < min_displacement:
            continue

        cleaned.append(track)

    # Re-number tracks sequentially
    for i, track in enumerate(cleaned, 1):
        track['id'] = i

    return cleaned


# =============================================================================
# MTRACK2 OUTPUT WRITER
# =============================================================================

def write_mtrack2_format(tracks, total_frames, output_path):
    """
    Write tracks in MTrack2-compatible tab-separated format.

    Format:
      Line 1: Frame  X1  Y1  Flag1  X2  Y2  Flag2  ...
      Line 2: Tracks 1 to N
      Lines 3+: frame_num  x1  y1  flag1  x2  y2  flag2  ...
      Blank line
      Footer: Track  Length  Distance traveled  Nr of Frames
    """
    n_tracks = len(tracks)

    with open(output_path, 'w') as f:
        # Header line 1
        header_parts = ['Frame']
        for i in range(1, n_tracks + 1):
            header_parts.extend([f'X{i}', f'Y{i}', f'Flag{i}'])
        f.write('\t'.join(header_parts) + '\n')

        # Header line 2
        f.write(f'Tracks 1 to {n_tracks}\n')

        # Data rows (1-based frame numbers)
        for frame in range(1, total_frames + 1):
            row_parts = [str(frame)]
            for track in tracks:
                if frame in track['positions']:
                    x, y = track['positions'][frame]
                    flag = track['flags'].get(frame, ' ')
                    row_parts.extend([f'{x:.5f}', f'{y:.5f}', flag])
                else:
                    row_parts.extend([' ', ' ', ' '])
            f.write('\t'.join(row_parts) + '\n')

        # Blank line
        f.write('\n')

        # Footer summary
        f.write('Track \tLength\tDistance traveled\tNr of Frames\n')
        for i, track in enumerate(tracks, 1):
            frames = sorted(track['positions'].keys())
            n_frames = len(frames)

            # Total path length (sum of step distances)
            path_length = 0.0
            for j in range(1, len(frames)):
                p1 = track['positions'][frames[j - 1]]
                p2 = track['positions'][frames[j]]
                path_length += np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

            # Net distance (start to end)
            start = track['positions'][frames[0]]
            end = track['positions'][frames[-1]]
            distance = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

            f.write(f'{i}\t{path_length:.5f}\t{distance:.5f}\t{n_frames}\n')


# =============================================================================
# DIAGNOSTIC OUTPUT
# =============================================================================

def save_diagnostics(frame_num, gray_frame, background, binary_mask,
                     particles, diagnostics_dir):
    """Save annotated diagnostic images for visual verification."""
    os.makedirs(diagnostics_dir, exist_ok=True)

    # Background-subtracted difference
    diff = cv2.absdiff(gray_frame, background)

    # Annotated frame with detected centroids
    annotated = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
    for (cx, cy) in particles:
        cv2.circle(annotated, (int(round(cx)), int(round(cy))), 4, (0, 0, 255), 1)
        cv2.circle(annotated, (int(round(cx)), int(round(cy))), 1, (0, 255, 0), -1)

    cv2.putText(annotated, f'Frame {frame_num}: {len(particles)} particles',
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imwrite(os.path.join(diagnostics_dir, f'frame_{frame_num:04d}_annotated.png'),
                annotated)
    cv2.imwrite(os.path.join(diagnostics_dir, f'frame_{frame_num:04d}_diff.png'),
                diff)
    cv2.imwrite(os.path.join(diagnostics_dir, f'frame_{frame_num:04d}_binary.png'),
                binary_mask)

    if frame_num == DIAGNOSTIC_FRAMES[0]:
        cv2.imwrite(os.path.join(diagnostics_dir, 'background_median.png'),
                    background)


# =============================================================================
# MAIN
# =============================================================================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, INPUT_VIDEO)
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    diag_dir = os.path.join(script_dir, DIAGNOSTICS_DIR)

    print("=" * 60)
    print("ONION CELL PARTICLE TRACKING")
    print("=" * 60)

    # --- 1. Open video ---
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {input_path}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"\nVideo: {input_path}")
    print(f"  Resolution: {width} x {height}")
    print(f"  Total frames: {total_frames}")
    print(f"  FPS: {fps}")
    print(f"  Duration: {total_frames / fps:.2f} s" if fps > 0 else "  FPS: unknown")

    print(f"\nParameters:")
    print(f"  Detection threshold: {DETECTION_THRESHOLD}")
    print(f"  Max displacement: {MAX_DISPLACEMENT} px/frame")
    print(f"  Max gap frames: {MAX_GAP_FRAMES}")
    print(f"  Min track length: {MIN_TRACK_LENGTH} frames")
    print(f"  Particle area range: {MIN_PARTICLE_AREA}-{MAX_PARTICLE_AREA} px^2")

    # --- 2. Compute temporal median background ---
    print(f"\nComputing temporal median background...")
    t0 = time.time()
    background = compute_temporal_median(cap, BG_SAMPLE_EVERY)
    print(f"  Done in {time.time() - t0:.1f} s")

    # --- 3. Detect particles in each frame ---
    print(f"\nDetecting particles in {total_frames} frames...")
    t0 = time.time()
    detections_per_frame = {}
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    for frame_num in range(1, total_frames + 1):
        ret, frame = cap.read()
        if not ret:
            print(f"  Warning: could not read frame {frame_num}, stopping at {frame_num - 1}")
            total_frames = frame_num - 1
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        particles, binary = detect_particles(gray, background)
        detections_per_frame[frame_num] = particles

        # Diagnostic output
        if DIAGNOSTIC_MODE and frame_num in DIAGNOSTIC_FRAMES:
            save_diagnostics(frame_num, gray, background, binary, particles, diag_dir)

        if frame_num % 200 == 0 or frame_num == 1:
            print(f"  Frame {frame_num}/{total_frames}: {len(particles)} particles detected")

    cap.release()
    elapsed = time.time() - t0
    print(f"  Detection complete in {elapsed:.1f} s ({total_frames / elapsed:.0f} fps)")

    # Detection statistics
    counts = [len(detections_per_frame.get(f, [])) for f in range(1, total_frames + 1)]
    print(f"  Particles per frame: min={min(counts)}, max={max(counts)}, "
          f"mean={np.mean(counts):.1f}, median={np.median(counts):.0f}")

    # --- 4. Link particles into tracks ---
    print(f"\nLinking particles into tracks...")
    t0 = time.time()
    raw_tracks = track_all_frames(detections_per_frame, MAX_DISPLACEMENT,
                                  MAX_GAP_FRAMES, 1)
    print(f"  Raw tracks found: {len(raw_tracks)}")
    print(f"  Linking complete in {time.time() - t0:.1f} s")

    # --- 5. Clean tracks ---
    print(f"\nCleaning tracks...")
    tracks = clean_tracks(raw_tracks, MIN_TRACK_LENGTH, MIN_TOTAL_DISPLACEMENT)
    print(f"  Valid tracks after cleaning: {len(tracks)}")

    if len(tracks) == 0:
        print("\nWARNING: No valid tracks found! Try adjusting parameters:")
        print("  - Lower DETECTION_THRESHOLD (currently {})".format(DETECTION_THRESHOLD))
        print("  - Lower MIN_TRACK_LENGTH (currently {})".format(MIN_TRACK_LENGTH))
        print("  - Increase MAX_DISPLACEMENT (currently {})".format(MAX_DISPLACEMENT))
        sys.exit(1)

    # Track statistics
    lengths = [len(t['positions']) for t in tracks]
    net_disps = []
    mean_step_sizes = []
    for t in tracks:
        frames = sorted(t['positions'].keys())
        first = t['positions'][frames[0]]
        last = t['positions'][frames[-1]]
        net_disps.append(np.sqrt((last[0] - first[0])**2 + (last[1] - first[1])**2))
        steps = []
        for j in range(1, len(frames)):
            p1 = t['positions'][frames[j - 1]]
            p2 = t['positions'][frames[j]]
            steps.append(np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2))
        if steps:
            mean_step_sizes.append(np.mean(steps))

    print(f"\n  Track length (frames): min={min(lengths)}, max={max(lengths)}, "
          f"mean={np.mean(lengths):.1f}")
    print(f"  Net displacement (px): min={min(net_disps):.1f}, "
          f"max={max(net_disps):.1f}, mean={np.mean(net_disps):.1f}")
    if mean_step_sizes:
        print(f"  Mean step size (px/frame): min={min(mean_step_sizes):.2f}, "
              f"max={max(mean_step_sizes):.2f}, mean={np.mean(mean_step_sizes):.2f}")

    # --- 6. Write output ---
    print(f"\nWriting MTrack2-format output to:")
    print(f"  {output_path}")
    write_mtrack2_format(tracks, total_frames, output_path)

    # Verify the output is readable
    print(f"\nVerifying output format...")
    try:
        test_data = np.genfromtxt(output_path, delimiter='\t', skip_header=2,
                                  skip_footer=1, invalid_raise=False)
        print(f"  np.genfromtxt loaded successfully: shape = {test_data.shape}")
        expected_cols = 1 + 3 * len(tracks)  # Frame + (X, Y, Flag) * N
        print(f"  Expected columns: {expected_cols}, got: {test_data.shape[1]}")
        if test_data.shape[1] == expected_cols:
            print(f"  FORMAT CHECK: PASSED")
        else:
            print(f"  FORMAT CHECK: WARNING - column count mismatch")
    except Exception as e:
        print(f"  FORMAT CHECK: FAILED - {e}")

    print(f"\n{'=' * 60}")
    print(f"TRACKING COMPLETE")
    print(f"  {len(tracks)} tracks written to {os.path.basename(output_path)}")
    print(f"  Total frames: {total_frames}")
    if DIAGNOSTIC_MODE:
        print(f"  Diagnostic images saved to: {diag_dir}")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
