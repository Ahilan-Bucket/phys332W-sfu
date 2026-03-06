# Lab [2] Session [4] — M&M: Short Project Exploration

**Date:** 12 Feb 2026
**Lab Partner:** Nathan Unhrn
**Recorder:** Ahilan Kumaresan

> **NOTICE:** E. coli HCB1274 culture is still NOT available. This session focuses on exploring 2–3 candidate projects to decide what to commit to for Sessions 5–6.


**Repository:** [github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility)

---

## 1. GOALS

1. Verify calibration (should match ~68 nm/px)
2. Check incubated pond water for motile organisms (3 days since collection)
3. If motile organisms found: capture video and attempt tracking with MTrack2
4. Explore onion cell streaming as candidate project
5. Explore bead diffusion under corrected calibration
6. Select primary project for Sessions 5–6
7. Capture preliminary data for selected project
8. Document all observations to justify selection

---

## 2. APPARATUS

**Standard Equipment (same as Sessions 1–3):**
Refer to Session 1, Section II (pg 2 of lab notebook)

| Item | Description |
|------|-------------|
| Microscope | Olympus BX51 upright bright-field |
| Camera | FLIR BlackFly U3-13Y3M (1440×1080 px) |
| Objectives | 10×, 40×, 100× oil immersion |
| Immersion oil | n = 1.518 |
| Stage micrometer | 1 mm / 100 div (10 µm/div) |
| Software | NI Vision Assistant |
| Analysis | ImageJ/Fiji + MTrack2, Python |

**Additional Items for Session 4:**

| Item | Source/Location | Purpose |
|------|----------------|---------|
| Incubated pond water | Lab bench (jar) | Motile organism search |
| Onion | Ask TA | Intracellular streaming |
| Tweezers | Lab bench | Peel onion membrane |
| 1 µm beads | Lab bench | Diffusion comparison |
| 5 µm beads | Lab bench | Diffusion comparison |
| Glass slides | Lab bench | Sample mounting |
| Coverslips (#1) | Lab bench | 22×22 mm |
| Parafilm spacers | Lab bench | ~100 µm chambers |
| Nail polish | Lab bench | Seal chambers |

---

## 3. VARIABLES

| Type | Variable | Description |
|------|----------|-------------|
| Independent | Sample type | Pond water / onion / beads |
| Independent | Incubation time | 3 days for pond water |
| Independent | Chamber type | With/without spacer |
| Dependent | Organism density | Cells per FOV |
| Dependent | Cell size (µm) | From images |
| Dependent | Motion type | Swimming / streaming / Brownian |
| Dependent | Swimming velocity | µm/s |
| Dependent | D_eff | Effective diffusion coeff. |
| Dependent | MSD(τ) | Mean-squared displacement |
| Dependent | α (MSD exp.) | MSD ~ τ^α |
| Control | Temperature | ~22°C (room temp) |
| Control | Objective | 100× oil immersion |
| Control | Pixel size | 68.4 nm/px (calibrated) |
| Control | Frame rate | 1 fps |

---

## 4. REFERENCES

**Primary Lab Documents:**
1. MM-LabScript-microscopy.pdf (Sec 3.3–3.5, pp. 9–11)
2. CellMotility-LabScript.pdf (cell motion background)
3. Protocol: Microscope Setup — Olympus BX51
4. Protocol: Making Sample Chambers
5. Protocol: Tracking Particles (MTrack2)
6. Protocol: Acquiring Movies with Vision Assistant

**Scientific References:**
7. UCB Advanced Lab BMC — intracellular movement
8. Banks & Fradin — anomalous diffusion in polymers
9. Freshwater organism identification guides

**Previous Lab Data:**
10. Session 1–2 Diffusion Analysis: Diffusion_Analysis.ipynb
11. Session 3: Pond water collection (Data/10-Feb/)

**Textbooks:**
12. Hughes & Hase, *Measurements and Uncertainties* (Ch 2.9, 5–8)

---

## 5. MICROSCOPE SETUP VERIFICATION

*(Must do every session)*

Ref: Protocol: Microscope Setup — OLYMPUS BX51

Time: ~1:30 PM

### 5.1 Köhler Illumination

| Step | Done? |
|------|-------|
| Lamp on, 5 min warm-up | Yes |
| Blank slide, focus at 10× | Yes |
| Field diaphragm edges sharp | Yes |
| Condenser centered | Yes |
| Field diaphragm to just outside FOV | Yes |
| Aperture diaphragm to ~70% NA | Yes |

All steps confirmed.

### 5.2 Calibration Verification (100×)

File: Data/12-Feb/calibration-100x-feb-12.tif

Stage micrometer measurement:
- Number of lines: 9
- Physical distance: 9 × 10 µm = 90 µm
- Pixel count: 1310 px
- Pixel size = 90 µm / 1310 px = 90 000 nm / 1310 px = **68.7 nm/px**

> **CONCLUSION:** Calibration is 68.7 nm/px. This MATCHES Sessions 1 and 3.

| Session | Calibration | Match? |
|---------|-------------|--------|
| Session 1 | 68.45 nm/px | REF |
| Session 3 | 68.4 nm/px | YES |
| Today | 68.7 nm/px | YES |

---

## 6. CALIBRATION ERROR HISTORY

### 6.1 Calibration Across All Sessions

| Session | Date | Calibration | Status |
|---------|------|-------------|--------|
| Session 1 | 03 Feb 2026 | 68.45 nm/px | REFERENCE |
| Session 2 | 05 Feb 2026 | 345 nm/px | ERROR — WRONG |
| Session 3 | 10 Feb 2026 | 68.4 nm/px | CONFIRMED |
| Session 4 | 12 Feb 2026 | 68.7 nm/px | CONFIRMED (condenser adjusted) |

> **IMPORTANT:** Session 2 calibration (345 nm/px = 0.345 µm/px) was WRONG. The correct value is 68.4 nm/px = 0.0684 µm/px. All Session 2 diffusion coefficients were inflated by a factor of ~25 because D scales as (pixel size)². Today's value is slightly different (68.7 nm/px) because we adjusted the condenser lens for sharper contrast.


**Note:** There appears to be an additional ~2× digital zoom applied by the camera/screen software. This would affect the effective pixel calibration if not accounted for. Further investigation is needed — check the FLIR BlackFly camera settings and NI Vision Assistant zoom level to determine whether the stage micrometer image already includes this zoom factor (in which case our calibration is correct as-is) or whether an additional correction is required.

Action today: Verified calibration matches ~68 nm/px. Using same 100× objective — consistent.

File saved as: Data/12-Feb/calibration-100x-feb-12.tif

Note: When placing the onion epithelial cells on top of the tape and the glass coverslip, we had difficulty getting enough volume to place the immersion oil on top. We performed a recalibration with the calibration slide and coverslip to confirm the value still held.

### 6.2 Impact on Previous Results

Session 2 diffusion analysis used 0.345 µm/px. Correcting to 0.0684 µm/px reduces all D values by a factor of (0.345/0.0684)² = 25.4×.

Corrected values:

| Bead (µm) | D_MSD (Sess 2) | D_corrected | D_theory |
|-----------|----------------|-------------|----------|
| 1.0 | 12.88 µm²/s | 0.507 µm²/s | 0.4414 |
| 5.0 | 3.75 µm²/s | 0.148 µm²/s | 0.0883 |

> **CONCLUSION:** 68.7 nm/px confirmed. Session 2 D values were off due to calibration error. The 1 µm corrected D is within ~15% of Stokes–Einstein theory. The 5 µm corrected D is still ~68% high — likely due to drift or noise at the longer diffusion timescale.

The calibration pixel count was 1310 px. Our value today is slightly different from Sessions 1 and 3 because we adjusted the condenser lens slightly for sharper contrast. This is a small systematic shift (~0.4%), well within the uncertainty of the stage micrometer measurement.

---

## 7. PROCEDURE A: POND WATER INCUBATION CHECK

Pond water collected 10 Feb 2026 from bottom of SFU campus pond by technician Selvesta. Stored sealed at ~22°C on lab bench. Days incubated: 3 (10 Feb → 12 Feb).

### 7.1 Visual Inspection (Before Microscope)

*(For procedure refer to Session 3, Pond Water Collection — see pg 8 of Session 3 notebook)*

Time: ~1:15 PM

We predicted that after 3 days of incubation:
- Water may show slight green tinge (algae growth at ~22°C)

However, the water was darker and had less visible debris. We also collected a new swamp sample, which showed much better images. We developed an improved collection technique: take the nozzle of the pipette, approach the larger masses and chunks, and draw from that region. For the new jar sample, we let the water wash over a piece of glass submerged in the pond and let grass sit in the water to attract organisms.

| Property | Session 3 (10 Feb) | Session 4 (today) |
|----------|-------------------|-------------------|
| Water colour | Largely clear | Darker |
| Cloudiness | Can see through | Same |
| Visible debris | Large particles | Lesser |
| Green tinge (algae?) | Not noted | None |
| Smell | Not noted | Same |
| Sediment at bottom | Present | None |

Summary: The original incubated sample did not show increased organisms as predicted. However, a freshly collected sample using the improved technique showed more organisms, though motility remained limited.

### 7.2 Microscope Observation of Incubated Water

Time: ~1:20 PM

Sample preparation: Wet mount WITHOUT spacer (thin mount), confirmed best for pond water in Session 3.

Objective: Start at 40× overview, then 100× detail.

100× Detailed Observations:

| Finding | Result |
|---------|--------|
| Organism density vs Session 3 | Higher — incubation increased population |
| Unknown 1 (55–58 µm, air bubble?) | Still present |
| Any NEW organism types | Yes — globular cell with possible villi |
| New  MOTILE organisms found? | Minimal motility in new sample |
| Motile cells per FOV | ~1–2 slow-moving |

### 7.3 New Organism Identification

**New Organism 3:**
- File: Data/12-Feb/unknown-3.avi
- Objective: 100×

[PASTE IMAGE: Image 1 — Unknown organism 3 from incubated SFU pond water at 100×.]

**New Organism 4:**
- File: Data/12-Feb/unknown4.avi
- Size: ~20 × ~15 µm
- Motion: Yes (minimal)
- Shape: Globular, spherical
- Possible ID: Unknown — appears to have villi-like structures for propulsion
- Single-celled organism with a clear outer wall, inner wall, and visible cell organelles.

[PASTE IMAGE: Image 2 — Unknown organism 4 at 100×.]

> **CONCLUSION:** Our prediction was wrong — the incubated water did not show a significant increase in organisms. However, the freshly collected sample using the improved technique yielded more organisms, suggesting that collection method matters more than incubation time for this source.

Viability as a short project: **Unlikely** — insufficient motile cells for systematic tracking.

---

## 8. PROCEDURE B: ONION CELL EXPLORATION

*(Priority #2 — Estimated time: ~30 min)*

Time: 2:04 PM

### 8.1 Background: Intracellular Streaming

Cytoplasmic streaming (cyclosis) is the directed flow of cytoplasm inside plant cells. In onion epidermal cells:

Ref: MM-LabScript Sec 3.5; UCB Advanced Lab BMC (background)

- Organelles are carried along actin filaments by myosin motor proteins
- Streaming is directional — it follows cell geometry and converges on the nucleus
- Typical literature speed: 1–10 µm/s (slower than bacterial swimming)
- This is ACTIVE transport, not passive diffusion
- MSD exponent: α ≈ 2 (ballistic) along the streaming direction

Key question: How does intracellular transport differ from Brownian diffusion and free swimming?

### 8.2 Onion Preparation

Membrane quality: Good (some folding, but usable regions found)

1. Cut onion in half
2. Separate an inner layer (scale leaf)
3. Carefully peel thin transparent membrane (epidermis)
4. Place membrane flat on glass slide
5. Add a drop of water, lower coverslip gently at an angle
6. Observe at 40× first, then 100×

### 8.3 Observations at 50× and 100×

Time: ~2:10 PM

**50× observations:**
- Cell walls visible: Yes
- Cell shape: Rectangular
- Estimated cell size: 110 px × 904 px (≈ 7.5 µm × 62 µm at 68.7 nm/px)
- Streaming visible: Yes

**100× observations (with oil):**

[PASTE IMAGE: Image 4 — Onion epidermis cells at 100× showing small granules of transport material.]

| Feature | Observation |
|---------|-------------|
| Cell wall clarity | Very clear |
| Cytoplasm appearance | Transparent — may need stain for detail |
| Organelles visible | None at this magnification without stain |
| Streaming direction | Yes — along the cell wall |
| Streaming speed | Fast (qualitative) |
| Granules/particles | Yes — small, moving granules visible |
| Nucleus visible | Not yet (visible in Recording 2 below) |

### 8.4 Video Capture of Cytoplasmic Streaming

Recorded at 1 fps (not 10 fps as originally planned — 1 fps gave better signal for slow-moving granules).

**Recording 1 (Onion streaming):**

| Setting | Value |
|---------|-------|
| Filename | Data/12-Feb/onion-stream-01.avi |
| Objective | 100× |
| Frame rate | 1 fps |
| Number of frames | 120 |
| Duration | 120 seconds |
| Notes | Nice image but slightly out of focus. Might be hard to track. |

**Recording 2:**

| Setting | Value |
|---------|-------|
| Filename | Data/12-Feb/onion2-stream.avi |
| Frame rate | 1 fps |
| Number of frames | 240 |
| Duration | 240 seconds |
| Notes | **We are seeing the nucleus! Lots of material is going towards it!!** |

### 8.5 Quick Velocity Estimate

Pick a visible granule and measure its displacement over N frames:

**Granule 1:** Distance: 44 px over 240 frames at 1 fps
- v = (44 px) × (0.0684 µm/px) / (240 s) = **0.0125 µm/s**

**Granule 2 (from onion2-stream.avi):** Distance: 50 px over 240 frames at 1 fps
- v = (50 px) × (0.0684 µm/px) / (240 s) = **0.0143 µm/s**

Expected from literature: 1–10 µm/s. Our values are lower — likely because we tracked slow-moving granules rather than the fastest ones, and the 1 fps capture rate limits our ability to resolve rapid displacements.

> **CONCLUSION:** Onion cell streaming clearly observed. Estimated speed: 0.013–0.014 µm/s (manual). Viability as project: **Strong.**

### 8.6 Stained Onion Observations

We stained the onion epidermis with Crystal Violet. The images improved dramatically — the nucleus and cell structures became clearly visible.

[PASTE IMAGE: Onion cells stained with Crystal Violet at 10×. This clearly shows the rod-like rectangular cell shapes, distinct from the round bacterial or pond water cells observed earlier.]

This observation supports our streaming data: much of the granule movement was directed toward the nucleus, and some movement occurred along the cell walls. The staining pattern reflects this — more dye is absorbed and concentrated near the nucleus, consistent with active intracellular transport directing material there. This provides independent visual evidence of the directed transport we measured quantitatively.

[PASTE IMAGE: Onion cells stained with Crystal Violet at 50×, showing the nucleus and cell wall structure clearly.]

Saved stained images at 10× (onion-stained-10x.tif) and 50× (onion-stained-50x.tif).

---

## 9. POST-LAB ANALYSIS

### 9.1 Qualitative Motion Comparison

| System | Motion Type | Speed | Direction |
|--------|------------|-------|-----------|
| 1 µm beads (Sess 1) | Brownian | ~0 net | Random |
| 5 µm beads (Sess 2) | Brownian | ~0 net | Random |
| Yeast (Sess 3) | Brownian only | ~0 net | Random |
| Pond organisms (today) | Minimal motility | Slow | Random |
| Onion streaming | Directed + random | 0.013–0.023 µm/s | Along cell wall → nucleus |

The progression from passive Brownian systems (beads, yeast) to the directed transport observed in onion cells illustrates the fundamental difference between thermal fluctuations and active, motor-driven motion.

### 9.2 Trajectory Analysis (Post-Lab Automated Tracking)

We encountered difficulties with ImageJ's MTrack2 plugin for tracking onion granules — the low contrast and slow motion made automatic detection unreliable. To overcome this, we adapted our existing Session 1–2 diffusion analysis notebook (Diffusion_Analysis.ipynb) by building a new tracking front-end on top of it. The modified pipeline (track_onion_particles.py + Onion_Cell_Analysis.ipynb) uses background subtraction to enhance granule contrast, applies flexible detection thresholds suited to the onion data, and then feeds the cleaned trajectories into the same MSD framework we used for bead analysis.

For the full tracking code, refer to: `Analysis/track_onion_particles.py`
For the complete analysis notebook: `Analysis/Onion_Cell_Analysis.ipynb`

[PASTE IMAGE: Figure 1 — 2D trajectories of onion granules from onion2-stream.avi (onion_trajectories.png)]

Note the directionality: many of the particle trajectories converge toward the centre of the field of view. That central region corresponds to the nucleus, which is consistent with our real-time observation during Recording 2 ("We are seeing the nucleus! Lots of material is going towards it!!"). This convergent pattern is a hallmark of cytoplasmic streaming — motor proteins on actin filaments actively shuttle organelles and vesicles toward the nucleus.

Motion appears: Mixed (directed + random components)
Trajectory shape: Curved paths following cell wall geometry
Comparison to Session 2 bead trajectories: Onion shows directed paths vs random bead walks

### 9.3 MSD Analysis

Mean-squared displacement analysis was performed on the top 20 longest track segments from onion2-stream.avi. The MSD is defined as:

MSD(τ) = ⟨[r(t + τ) − r(t)]²⟩

For the general power-law model MSD = K τ^α:
- Pure Brownian diffusion: α = 1.0 (random walk)
- Ballistic (fully directed): α = 2.0 (straight line)
- Superdiffusive: 1 < α < 2 (directed + random)

[PASTE IMAGE: Figure 2 — MSD log–log plot showing power-law fit with α = 1.66 (onion_msd_analysis.png)]

The log–log MSD plot shows a clear linear trend with slope α = 1.662 ± 0.052. This places the onion granule motion firmly in the **superdiffusive** regime — between pure diffusion and ballistic transport. The physical interpretation is straightforward: the granules are being actively carried along actin filaments (directed component, pushing α toward 2) while simultaneously experiencing random thermal fluctuations (diffusive component, pulling α toward 1). The resulting α ≈ 1.66 reflects this superposition.

### 9.4 Velocity Estimates

| Method | System | Mean velocity (µm/s) | Notes |
|--------|--------|---------------------|-------|
| Manual | Onion granule 1 | 0.0125 | 44 px / 240 s |
| Manual | Onion granule 2 | 0.0143 | 50 px / 240 s |
| Automated | Onion (top 20 tracks) | 0.0228 ± 0.0071 | Mean from tracking |
| Automated | Onion (median) | 0.0177 | Less sensitive to outliers |
| Literature | E. coli | ~20 | Reference |
| Literature | Chlamydomonas | ~100 | Reference |

The automated tracking yields higher speeds than the manual estimates because it captures a wider range of granules, including faster-moving ones that are harder to follow by eye. Both methods are consistent: streaming speeds are on the order of 0.01–0.02 µm/s, well below free-swimming organisms but clearly above zero-net-drift Brownian motion.

### 9.5 MSD Framework and Physical Constants

MSD(τ) = ⟨[r(t + τ) − r(t)]²⟩
- 2D Pure diffusion: MSD = 4Dτ (α = 1)
- Ballistic: MSD = v²τ² (α = 2)
- General: MSD = Kτ^α

Stokes–Einstein (passive diffusion):
D = k_BT / (6πηr)
- T = 295.15 K (room temp)
- η ≈ 0.001 Pa·s (water at ~22°C)

For 10 µm organism: D_passive = 0.044 µm²/s
For 1 µm bead: D_passive = 0.441 µm²/s
If self-propelled: D_eff = v²τ_r / 2 >> D_passive

### 9.6 Onion Cell Quantitative Results Summary

Analysis performed using custom Python tracking (track_onion_particles.py) on onion2-stream.avi (240 frames, 1 fps, 68.7 nm/px calibration). Full analysis: Onion_Cell_Analysis.ipynb in Analysis/ folder.

**Manual Velocity Estimates (from lab):**
- Granule 1: 44 px over 240 frames → v = 0.0125 µm/s
- Granule 2 (onion2-stream): 50 px over 240 frames → v = 0.0143 µm/s

**Automated Tracking Results:**

| Parameter | Value | Uncertainty |
|-----------|-------|-------------|
| Particles detected | 1246 | — |
| Valid track segments | 1099 | — |
| Top segments analysed | 20 | — |
| Mean speed | 0.0228 µm/s | ± 0.0071 µm/s |
| Median speed | 0.0177 µm/s | — |
| MSD exponent (α) | 1.662 | ± 0.052 |
| D_eff (effective) | 0.000623 µm²/s | ± 0.000038 µm²/s |
| Directionality ratio | 0.540 | ± 0.229 |

[PASTE IMAGE: Figure A — Onion cell particle trajectories (onion_trajectories.png)]
[PASTE IMAGE: Figure B — Displacement statistics (onion_displacement_stats.png)]
[PASTE IMAGE: Figure C — MSD analysis log–log plot (onion_msd_analysis.png)]

> **CONCLUSION:** MSD power-law α = 1.66 ± 0.05 indicates **superdiffusive** motion. This lies between pure diffusion (α = 1) and ballistic transport (α = 2), consistent with directed cytoplasmic streaming superimposed on random thermal fluctuations.

Comparison to physical models:
- Pure Brownian diffusion: α = 1.0 (random walk)
- Pure ballistic (directed): α = 2.0 (straight line)
- **Our result: α = 1.66 → superdiffusive (directed + random)**

Key insight: The nucleus observation ("Lots of material is going towards it!!") is consistent with α > 1 — active transport along the cytoskeleton. The Crystal Violet staining results (more dye near nucleus) provide independent support: active transport concentrates materials at the nucleus.

---

## 10. PROJECT SELECTION DECISION

Based on today's explorations, select project for Sessions 5–6.

**Decision Matrix:**

| Criterion (weight) | Pond Water | Onion Cells | Bead Diff. |
|---------------------|-----------|-------------|------------|
| Motile cells found? (30%) | 2 | N/A | N/A |
| Data quality (25%) | 2 | 3 | 4 |
| Scientific interest (20%) | 2 | 4 | 3 |
| Feasibility Sess 5–6 (15%) | 1 | 3 | 4 |
| Comparison to beads (10%) | 2 | 3 | 4 |
| **TOTAL SCORE** | **9** | **13** | **15** |

Rating: 1 = Poor, 2 = Fair, 3 = Good, 4 = Excellent

**SELECTED PROJECT: Bead Diffusion (varied viscosities and sizes)**

**Justification:**
1. Bead diffusion offers the most systematic comparison to Stokes–Einstein theory.
2. We can vary viscosity (glycerol solutions) and bead size (1 µm, 5 µm) for multiple independent checks.
3. The corrected calibration (68.7 nm/px) should resolve the 20–40× discrepancy from Session 2.

**Additional data needed in Sessions 5–6:**
1. Multiple bead sizes (1 µm and 5 µm) with corrected calibration
2. Varied viscosity solutions (water, 10% glycerol, 25% glycerol)
3. Temperature-controlled measurements for Stokes–Einstein verification

---

## 11. CONCLUSIONS

### 11.1 Summary of Session 4 Findings

1. **Calibration:** 68.7 nm/px — MATCHES Sessions 1 (68.45) and 3 (68.4). The slight difference is due to a minor condenser adjustment for improved contrast.

2. **Pond water incubation (3 days):**
   - Organism density increased relative to Session 3
   - New organisms found: globular cell with possible villi (Unknown 4)
   - Motility: Limited — only 1–2 slow-moving cells per FOV
   - Viability as project: **Unlikely**

3. **Onion cell streaming:**
   - Streaming clearly observed at 50× and 100×
   - Manual speed: 0.013–0.014 µm/s; Automated mean: 0.023 µm/s
   - MSD exponent α = 1.66 ± 0.05 (superdiffusive)
   - Crystal Violet staining revealed nucleus and confirmed directed transport
   - Viability as project: **Strong**

4. **Bead diffusion (corrected):**
   - NOT tested this session — prioritised onion streaming
   - Corrected Session 2 values within ~15% of theory (1 µm beads)

5. **Project selected:** Bead Diffusion (varied viscosities and sizes)

> **CONCLUSION:** Session 4 accomplished calibration verification (68.7 nm/px), discovered onion cell superdiffusive streaming (α = 1.66), and selected bead diffusion as the project for Sessions 5–6.

### 11.2 Comparison of Motion Types

| System | D or D_eff | Motion | α |
|--------|-----------|--------|-------|
| 1 µm beads | 0.44 µm²/s | Brownian | ~1 |
| 5 µm beads | 0.09 µm²/s | Brownian | ~1 |
| Yeast | Non-motile | Brownian | ~1 |
| Pond organisms | N/A | Minimal | ~1 |
| Onion streaming | 0.000623 µm²/s | Directed + random | 1.66 |

---

## 12. PLAN FOR SESSIONS 5–6

Selected project: Bead Diffusion (varied viscosities and sizes)

**Session 5 plan:**
- Time 0–30 min: Prepare glycerol solutions (10%, 25%, 50%), calibrate
- Time 30–90 min: Record 1 µm beads in water and each glycerol concentration
- Time 90–120 min: Record 5 µm beads in water, begin tracking

**Session 6 plan:**
- Time 0–60 min: Complete remaining bead size/viscosity combinations
- Time 60–90 min: Run analysis pipeline on all data
- Time 90–120 min: Yeast cell observation for population study

**Data needed:**
- Number of videos: 8–12 (2 bead sizes × 4 viscosities)
- Duration per video: 120–240 frames at 1 fps
- Organisms/cells to track: 20+ beads per video
- Analysis to complete: MSD, D vs viscosity, Stokes–Einstein comparison

**Deliverables for final submission:**
- [ ] 2D trajectory plots
- [ ] Displacement histograms with Gaussian fits
- [ ] MSD vs τ plots (linear and log–log)
- [ ] Velocity distribution
- [ ] Comparison table (project vs beads vs theory)
- [ ] Error analysis with uncertainties
- [ ] Final conclusions

---

## 13. POST-LAB REFLECTIONS

**Goal Review:**

| Goal | Status |
|------|--------|
| 1. Verify calibration (~68 nm/px) | DONE — 68.7 nm/px |
| 2. Check pond water for motile organisms | DONE — found organisms, limited motility |
| 3. If motile: capture video and track | NOT DONE — prioritised onion streaming |
| 4. Explore onion cell streaming | DONE — streaming observed, α = 1.66 |
| 5. Explore bead diffusion (corrected) | NOT DONE — prioritised onion streaming |
| 6. Select project for Sessions 5–6 | DONE — Bead diffusion selected |
| 7. Capture preliminary data | DONE — onion streaming data captured |
| 8. Document observations | DONE — all observations recorded |

**Future Plans:**
For Sessions 5–6 we will pursue bead diffusion analysis with varied viscosity (glycerol solutions) and bead sizes (1 µm, 5 µm). We verified with the TA that we do not need a full matrix of all combinations — one or two controlled parameters that systematically influence D are sufficient. We also plan to study yeast cells for population modelling and cellular motion analysis.

**What worked well:**
- Onion cell preparation gave excellent streaming visibility at 100×.
- Crystal Violet staining dramatically improved nucleus visibility and provided independent evidence of directed transport.
- The adapted tracking pipeline (modified from our diffusion notebook) handled the low-contrast onion data effectively.

**What didn't work and surprises:**
- Pond water organisms showed minimal motility despite 3 days of incubation — this was unexpected.
- Condenser adjustment slightly changed calibration (68.4 → 68.7 nm/px), a reminder that optical alignment affects pixel calibration.
- ImageJ MTrack2 struggled with the onion granule data; custom Python tracking was necessary.

**What I would do differently:**
- Start with onion cells earlier — it was the most productive experiment of the day.
- Try different stains (iodine, methylene blue) for comparison alongside Crystal Violet.
- Record at higher frame rate (5–10 fps) to better resolve fast granule motion.

**Inter-lab period work (between Sessions 3 and 4):**
- Corrected calibration analysis (identified Session 2 error, re-ran diffusion analysis)
- Background research on onion cell cytoplasmic streaming
- Session 4 planning and predicted notebook preparation

---

## 14. DATA FILES CREATED

All files in: Lab2-Microscopy-and-Motility/Data/12-Feb/

| Category | Filename | Description |
|----------|----------|-------------|
| Calibration | calibration-100x-feb-12.tif | Stage micrometer (9 lines) |
| Calibration | calibration-100x-feb-12-2.tif | Second measurement |
| Onion | onion-stream-01.avi | 120 fr, 1 fps, slightly OOF |
| Onion | onion2-stream.avi | 240 fr, 1 fps, nucleus visible! |
| Onion stained | onion-stained-10x.tif | Crystal violet, 10× |
| Onion stained | onion-stained-50x.tif | Crystal violet, 50× |
| Unknown cells | unknown-3.avi | Pond water organism |
| Unknown cells | unknown4.avi | Globular, possible villi |
| Unknown cells | unknown5.avi | Pond water organism |
| Track data | onion2-trackresults.txt | 1490 particle tracks |
| Diagnostics | diagnostics/ | Background subtraction frames |

**Analysis notebooks:**
- Analysis/Onion_Cell_Analysis.ipynb — Full onion streaming analysis
- Analysis/Diffusion_Analysis_Corrected.ipynb — Bead diffusion with correct pixel size
- Analysis/track_onion_particles.py — Custom particle tracking script
