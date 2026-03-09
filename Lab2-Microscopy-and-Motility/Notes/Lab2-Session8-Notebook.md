# Lab [2] Session [8] --- M&M: Tracker Analysis, Code Corrections and Final Data Processing

**Date:** 5 Mar 2026
**Lab Partner:** Nathan Unhrn
**Recorder:** Ahilan Kumaresan

**SESSION FOCUS:** Nathan completed manual particle tracking for all Session 6 and 7 videos using ImageJ/Tracker, producing .txt position files. Ahilan built and debugged the automated analysis pipeline (`from_text_analysis.ipynb`, v1.3) to process all tracker data with physically correct models: MSD forced through origin, consistent sigma-clipping, dual-wall Faxen correction, Einstein viscosity correction, and calibration-slide noise subtraction. This session produced the final quantitative results for the bead diffusion project.

**Repository:** [github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility)

**Google Drive (full AVI dataset):** [drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9](https://drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9?usp=sharing)

---

## 1. GOALS

1. Nathan: Complete manual particle tracking for all Session 6 and 7 AVI files using ImageJ/Tracker
2. Nathan: Track calibration slide videos to establish camera noise baseline
3. Ahilan: Build and debug the tracker analysis pipeline (`from_text_analysis.ipynb`)
4. Review Nathan's theoretical Diffusion Coefficient formulas (Faxen corrections, Einstein viscosity)
5. Fix physics bugs in the MSD analysis (force fit through origin, consistent sigma-clipping)
6. Run the complete pipeline on all 49+ tracker datasets
7. Produce presentation-quality figures for each dataset and lab-level trend plots

**Expanded Session 8 targets:**

- Process all tracker .txt files from both Session 6 (s-prefix: s1b, s2a, s2b, s2c, s3, s7, s8, s9) and Session 7 (r-prefix: r1 through r16)
- Implement calibration noise subtraction using average D_noise from two calibration slide profiles
- Implement dual-wall Faxen correction: theory range from quarter-plane (D_wall) to midplane (D_mid)
- Implement Einstein viscosity correction: eta_eff = eta_0 * (1 + 2.5*phi + 6.2*phi^2) for finite bead concentration
- Produce trend plots: D vs viscosity at constant bead size, D vs bead size at constant viscosity, parity plot (D_exp vs D_theory), MSD exponent distribution
- Export batch_results.csv with all 49 datasets for the formal report

---

## 2. APPARATUS

**Standard Equipment (same as Sessions 1--7):**
Refer to Session 1, Section II (pg 2 of lab notebook)

| Item | Description |
|------|-------------|
| Microscope | Olympus BX51 upright bright-field |
| Camera | FLIR BlackFly U3-13Y3M (1440x1080 px) |
| Objectives | 10x, 40x, 100x oil immersion |
| Immersion oil | n = 1.518 |
| Stage micrometer | 1 mm / 100 div (10 um/div) |
| Software | NI Vision Assistant (video acquisition), ImageJ/Tracker (particle tracking) |
| Analysis | Python (`Analysis/from_text_analysis.ipynb`, Pipeline v1.3) |

**Software for Session 8:**

| Tool | Version | Purpose |
|------|---------|---------|
| ImageJ Tracker plugin | --- | Manual multi-particle tracking on AVI files (Nathan) |
| Python 3.12 | 3.12 | Analysis pipeline |
| NumPy, SciPy, Matplotlib | --- | Computation and plotting |
| Jupyter Notebook | --- | Interactive analysis environment |

---

## 3. VARIABLES

Same experimental variables as Session 7. No new data was collected at the microscope in this session --- all work was post-processing of Session 6 and 7 recordings.

| Type | Variable | Range / Values | Description |
|------|----------|---------------|-------------|
| Independent | Fluid viscosity (eta) | 0.32 -- 4.11 mPa.s | Glycerol (0%, 20%, 36--41%) and acetone (20%, 40%, 100%) |
| Independent | Bead diameter (2r) | 1, 2.1, 3, 5 um | Polystyrene microspheres (rho = 1.05 g/cm^3) |
| Dependent | Diffusion coefficient D | um^2/s | Three methods: Direct Variance, Gaussian Fit, MSD Slope |
| Dependent | MSD exponent alpha | dimensionless | Power-law fit: MSD ~ tau^alpha |
| Control | Temperature T | 21 C = 294 K | Room temperature, not varied |
| Control | Pixel calibration | 68.4 nm/px | Established in Sessions 1, 3, 4, 6 |
| Control | Frame rate | 29 fps | Camera frame rate for tracker data |

---

## 4. REFERENCES

**Primary Lab Documents:**
1. MM-LabScript-microscopy.pdf (Sec 3.3--3.5)
2. CellMotility-LabScript.pdf
3. Diffusion Coefficient formulas.pdf (Nathan's theoretical model, in `Data/2026-03-05/`)

**Scientific References:**
4. Cheng (2008) --- empirical formula for glycerol-water viscosity
5. Howard & McAllister (1958) --- acetone-water mixture viscosity data
6. Stokes-Einstein relation: D_0 = k_B T / (6 pi eta r)
7. Faxen's law (dual-wall): F = 1 - (9/16)*s + (1/8)*s^3, where s = a/h + a/(L-h)
8. Batchelor (1977) --- Einstein viscosity correction: eta_eff = eta_0 * (1 + 2.5*phi + 6.2*phi^2)

**Data Sources:**
9. Session 6 videos: `Data/2026-02-26/` (s-prefix slides)
10. Session 7 videos: `Data/2026-03-03/` (r-prefix slides)
11. Session 7 notebook: `Notes/Lab2-Session7-Notebook.md`
12. Session 6 notebook: `Notes/Lab2-Session6-26Feb2026.md`
13. Analysis pipeline: `Analysis/from_text_analysis.ipynb` (v1.3)

---

## 5. NATHAN'S PARTICLE TRACKING

### 5.1 Tracking Method

Nathan used the ImageJ Tracker plugin to manually identify and follow bead positions frame-by-frame in each AVI video. For each video:
1. Open AVI in ImageJ
2. Use the Tracker plugin to mark bead centres in each frame
3. Export position data as .txt (comma- or tab-delimited, with columns: frame, x, y, mass, size, etc.)

The Tracker approach gives more accurate position data than the automated MTrack2 method used in earlier sessions because:
- Human operator can distinguish real beads from dirt, out-of-focus particles, and stuck beads
- Can handle crossing trajectories that confuse automated linkers
- Can reject bad frames (drift, vibration) in real time

### 5.2 Calibration Slide Tracking

Two calibration videos were tracked to establish the camera noise baseline. These are videos of immobilised beads on a glass calibration slide --- any measured "motion" is purely camera vibration and tracking imprecision.

| File | Description | D_noise (um^2/s) |
|------|-------------|-------------------|
| `noise-calibration_slide-1-tracker.txt` | Calibration slide, profile 1 | 0.0147 |
| `noise-calibration_slide-3-tracker.txt` | Calibration slide, profile 3 | 0.0213 |
| **Average** | | **0.0180** |

D_noise = 0.0180 um^2/s is subtracted from all measured D values. This is a significant correction for slow-moving beads (e.g., 5 um in 40% glycerol where D_theory ~ 0.023) but negligible for fast beads (e.g., 1 um in water where D ~ 0.44).

### 5.3 Tracked Datasets

Nathan tracked 49 data files from Session 6 (s-prefix) and Session 7 (r-prefix) videos. Some videos were omitted due to quality issues (see Session 7 notebook, Section 8.4 for skip justifications).

**Session 7 tracker exports (r-prefix):**

| Slide | Bead | Solute | Trials | Files |
|-------|------|--------|--------|-------|
| r1 | 1 um | Water | 1 | r1-1mu-...-tracker.txt |
| r2 | 2.1 um | Water | 1 | r2-2_1mu-...-tracker.txt |
| r3 | 3 um | Water | 2 | r3-trial1-tracker.txt, r3-trial2-tracker.txt |
| r4 | 5 um | Water | 2 | r4-trial1-tracker.txt, r4-trial2-tracker.txt |
| r5 | 1 um | 20% Gly | 2 | r5-trial1-tracker.txt, r5-trial2-tracker.txt |
| r6 | 2.1 um | 20% Gly | 2 | r6-trial1-tracker.txt, r6-trial2-tracker.txt |
| r7 | 3 um | 20% Gly | 3 | r7-trial1,2,3-tracker.txt |
| r8 | 5 um | 20% Gly | 3 | r8-trial1,2,3-tracker.txt |
| r10 | 2.1 um | 40% Gly | 2 | r10-trial1,2-tracker.txt |
| r11 | 3 um | 40% Gly | 2 | r11-trial1,2-tracker.txt |
| r12 | 5 um | 40% Gly | 4 | r12-trial2,3 (10ul and 20ul stock) |
| r14 | 2.1 um | 100% Ace | 2 | r14-trial1,2-tracker.txt |
| r15 | 3 um | 100% Ace | 1 | r15-trial1-tracker.txt |
| r16 | 5 um | 100% Ace | 3 | r16-trial1,2,4-tracker.txt |

> **Skipped:** r9 (1 um / 40% Gly --- below noise floor), r13 (1 um / Acetone --- below noise floor + seal failure). See Session 7, Section 8.4.

**Session 6 tracker exports (s-prefix):**

| Slide | Bead | Solute | Trials | Files |
|-------|------|--------|--------|-------|
| s1b | 3 um | Water | 3 | s1b-trial3,4,5-tracker.txt |
| s2a | 1 um | 20% Gly | 2 | s2a-trial2,3-tracker.txt |
| s2b | 3 um | 20% Gly | 3 | s2b-trial1,2,3-tracker.txt |
| s2c | 1 um | 20% Gly | 3 | s2c-trial1,2,3-tracker.txt |
| s3 | 3 um | 20% Gly | 2 | s3-trial1,2-tracker.txt |
| s7 | 3 um | 36% Gly | 3 | s7-trial1,2,3-tracker.txt |
| s8 | 3 um | 20% Ace | 2 | s8-trial1,2-tracker.txt |
| s9 | 3 um | 40% Ace | 1 | s9-trial1-tracker.txt |

---

## 6. THEORY REVIEW AND CODE CORRECTIONS

### 6.1 Nathan's Theoretical Formulas

Nathan compiled a reference document (`Diffusion Coefficient formulas.pdf`) with the complete theoretical framework:

**Stokes-Einstein:** D_0 = k_B T / (6 pi eta r)

**Viscosity models:**
- Glycerol-water: Cheng (2008) empirical formula
- Acetone-water: Howard & McAllister (1958) data
- Einstein correction for finite bead concentration: eta_eff = eta_0 (1 + 2.5 phi + 6.2 phi^2), where phi = volume fraction of beads

**Faxen wall correction (dual-wall):**
- s = a/h + a/(L - h), where a = bead radius, h = height from bottom wall, L = chamber depth
- F = 1 - (9/16) s + (1/8) s^3
- D_corrected = F * D_0
- Evaluated at two heights: midplane h = L/2 (upper bound) and quarter-plane h = L/4 (lower bound)
- For L = 82.5 um, 1 um beads: F_mid = 0.986, F_wall = 0.969

### 6.2 MSD Fit Through Origin

**Problem:** The original code used `MSD = slope*t + intercept` with a free intercept parameter. This produced a non-physical offset at tau = 0 (MSD should be exactly zero when no time has passed).

**Fix:** Changed to `MSD = 4*D*tau` forced through the origin. Camera jitter is handled separately via the calibration slide noise subtraction (D_noise = 0.018 um^2/s), not by fitting an intercept.

The 25% fit range is retained: only the first 25% of lag times are used for the linear fit. This avoids the noisy tail where statistical sampling is poor (few independent pairs at long lag times).

### 6.3 Consistent Sigma-Clipping

**Problem:** The variance method applied sigma-clipping to displacements (removing outliers before computing D_variance), but MSD was computed on raw positions. This created a systematic disagreement: D_variance < D_MSD because the MSD included outlier jumps that the variance method rejected.

**Fix:** Apply sigma-clipping to displacements BEFORE computing MSD. For each segment, identify outlier frames (where |dx| or |dy| exceeds 3-sigma), remove those frames, then split the remaining contiguous frames into clean sub-segments. Compute MSD only on clean sub-segments.

After this fix, D_variance and D_MSD agree within error bars for most datasets.

### 6.4 Calibration Noise Subtraction

All measured D values are corrected by subtracting the average noise floor:

D_corrected = max(0, D_raw - D_noise)

where D_noise = 0.0180 um^2/s from the calibration slide average (Section 5.2). Values that fall below the noise floor are clamped to zero.

---

## 7. PIPELINE ARCHITECTURE (v1.3)

The analysis pipeline is implemented in `Analysis/from_text_analysis.ipynb` (23 cells, 11 code + 12 markdown), generated by `Analysis/_build_notebook_v12.py`.

### 7.1 Processing Steps (per dataset)

1. **Parse filename** --- extract bead size, solute %, type, slide prefix, trial number, stock/total volumes
2. **Load position data** --- auto-detect Tracker vs MTrack2 format, parse multi-particle trajectories
3. **Segment tracks** --- split trajectories at large jumps (> 1.5 um/frame) into contiguous segments
4. **Compute theory** --- Stokes-Einstein + dual-wall Faxen + Einstein viscosity correction
5. **Displacement analysis** --- sigma-clipped dx/dy variance and Gaussian PDF fit for D_variance and D_gauss
6. **MSD analysis** --- sigma-clipped sub-segments, origin-forced linear fit for D_MSD, power-law fit for alpha
7. **Noise subtraction** --- subtract D_noise = 0.018 from all three D values (clamp >= 0)
8. **Generate plots** --- trajectories, displacement histograms, MSD (linear + log-log), D comparison bar chart, combined 2x3 summary
9. **Write outputs** --- summary.txt, trackresults.txt, readme.txt metadata, PNG + PDF (presentation mode)

### 7.2 Plot Features

- **D comparison chart:** Three bars (Variance, Gaussian, MSD) with error bars from per-segment spread. Theory shown as shaded band [D_wall, D_mid] with labelled midplane and quarter-plane boundaries. Noise floor shown as dotted grey line.
- **MSD plot:** Linear and log-log panels. Fit line passes through origin, labelled "MSD = 4*D*tau". Power-law alpha exponent annotated.
- **Trend plots:** D vs viscosity at constant bead size (4 panels), D vs bead size at constant viscosity (5 panels), parity plot (D_exp vs D_theory by method), MSD exponent distribution.

---

## 8. RESULTS SUMMARY

### 8.1 Overall Statistics

- **49 datasets** processed (34 from Session 7, 15 from Session 6)
- **0 failures** --- all tracker files loaded and analysed successfully
- **D_noise = 0.018 um^2/s** subtracted from all measurements
- **8 datasets at noise floor** (D corrected to ~0): all 5 um or 3 um beads in high-viscosity glycerol

### 8.2 Key Results by Condition (Tracker Data Only)

| Condition | N | D_var (um^2/s) | D_theory (um^2/s) | Deviation |
|-----------|---|---------------|-------------------|-----------|
| 1.0 um, Water | 1 | 0.407 | 0.440 | -7.5% |
| 1.0 um, 20% Gly | 7 | 0.234 | 0.254 | -8.0% |
| 2.1 um, 20% Gly | 2 | 0.123 | 0.121 | +1.7% |
| 3.0 um, 20% Gly | 8 | 0.058 | 0.085 | -31.1% |
| 2.1 um, 100% Ace | 2 | 0.316 | 0.641 | -50.7% |
| 3.0 um, 100% Ace | 1 | 0.196 | 0.449 | -56.2% |
| 5.0 um, 100% Ace | 3 | 0.064 | 0.269 | -76.4% |
| 5.0 um, 41% Gly | 4 | 0.000 | 0.023 | at noise floor |

### 8.3 Observations

**Best agreement with theory:**
- 1 um beads in water and 20% glycerol: D within 8% of Stokes-Einstein + Faxen prediction. This is excellent for a student lab with manual tracking at 29 fps.
- 2.1 um beads in 20% glycerol: D within 2% of theory --- essentially perfect.

**Systematic frame-rate averaging:**
- All measured D values are below theory (D_exp < D_theory), consistent with the camera integrating bead motion over the 34 ms exposure time. This effect is well-documented in the literature.
- Larger beads show more deviation because their slower dynamics give lower signal-to-noise ratio for displacement measurements.
- The deviation increases with viscosity as bead displacements approach the noise floor.

**Anomalous acetone datasets:**
- 3 um beads in 20% and 40% acetone (s8, s9) show D essentially at zero, despite theory predicting D ~ 0.18--0.23 um^2/s. This is likely a sample preparation issue: acetone dissolves nail polish sealant, contaminating the sample chamber and potentially causing beads to stick to the glass surface.
- Pure acetone (100%) datasets for 2.1 and 3 um beads gave reasonable results (D ~ 50--56% below theory), consistent with other conditions.

**Noise floor datasets:**
- 5 um beads in 41% glycerol: all 4 trials at or below D_noise. The theoretical D ~ 0.023 um^2/s is barely above the noise floor (0.018 um^2/s), making reliable measurement impossible at this frame rate.
- 3 um beads in 36--40% glycerol: similar noise-limited behaviour.

### 8.4 MSD Exponent Distribution

The MSD exponent alpha ranges from 0.20 to 1.44 across all datasets:
- Most datasets show alpha ~ 0.8--1.0, consistent with normal Brownian diffusion (alpha = 1) with slight sub-diffusive character from wall interactions and frame-rate effects.
- Sub-diffusive (alpha < 0.9): 25 datasets --- likely due to confinement effects near chamber walls and tracking noise at low displacements.
- Normal diffusion (0.9 <= alpha <= 1.1): 14 datasets --- best-quality measurements.
- Super-diffusive (alpha > 1.1): 10 datasets --- some genuine convective drift in the chamber, or statistical fluctuation in small datasets.

---

## 9. CODE REVIEW NOTES

*These are in-lab notes from the session, preserved for the record.*

### MSD Fix
The fitting line was only for the start of the points, not for the entire dataset.
- From theory, the first data point must be at zero. Our plot had an offset.
- Solution: force the fit through the origin with MSD = 4*D*tau (no intercept).
- Camera jitter is handled by the calibration noise subtraction, not by fitting an intercept.

### Error Bars
- Explored both inter-segment spread (standard deviation across segments) and the difference between methods.
- Final choice: per-segment D estimates for error bars, with all three methods shown side-by-side.

### Fit Range (25%)
- Only fitting the first 25% of lag times is correct. Fitting 100% would include the noisy tail where few independent displacement pairs contribute, biasing D toward zero.

### Nathan's Tracker Approach
- At 2:39 PM, started building the new code for Tracker data format.
- The Tracker plugin exports comma/tab-delimited .txt files with columns: frame, x, y, mass, size, etc.
- Multi-particle files have a `#multi:N` header; single-particle files start with a header row containing "mass".
- Auto-detection logic in `detect_format()` handles both.

---

## 10. IN-LAB DISCUSSION: THEORY VS EXPERIMENT

Nathan and I discussed why our measured D values are systematically below theory:

1. **Frame-rate averaging** (dominant effect): The camera records each frame over ~34 ms. During that time, the bead moves. The recorded position is an average over the exposure, not an instantaneous snapshot. This "blurs" the trajectory and reduces apparent displacements, lowering D_measured. A higher frame rate (hundreds of fps over shorter videos) would reduce this effect.

2. **Wall proximity**: Beads near the chamber walls experience increased drag (Faxen correction). We account for this with the dual-wall correction at midplane and quarter-plane heights, but the actual bead height distribution may include particles closer to the walls than assumed.

3. **Glycerol inhomogeneity**: At higher glycerol concentrations (36--41%), the solution may have micro-scale viscosity gradients, especially if mixing was incomplete. This could trap beads or create local regions of higher viscosity.

4. **Acetone seal degradation**: Pure acetone dissolves nail polish sealant, introducing drift, leakage, and potential surface contamination. This explains the anomalously low D for 20% and 40% acetone mixtures where the beads may have become stuck.

Despite these limitations, our data clearly shows the predicted trends:
- D decreases with increasing viscosity (1/eta dependence)
- D decreases with increasing bead size (1/d dependence)
- All three measurement methods (Variance, Gaussian, MSD) agree within error bars

These trends are the central result of our quantitative project.

---

## 11. TASKS COMPLETED THIS SESSION

| Task | Status | Notes |
|------|--------|-------|
| Nathan: Track all Session 6 videos | Done | 15 tracker files (s-prefix) |
| Nathan: Track all Session 7 videos | Done | 34 tracker files (r-prefix) |
| Nathan: Track calibration slides | Done | 2 calibration files |
| Ahilan: Build tracker pipeline v1.3 | Done | from_text_analysis.ipynb |
| Ahilan: Fix MSD through origin | Done | MSD = 4*D*tau |
| Ahilan: Fix sigma-clipping consistency | Done | Applied before MSD |
| Ahilan: Add dual-wall Faxen | Done | D_mid and D_wall |
| Ahilan: Add noise subtraction | Done | D_noise = 0.018 |
| Ahilan: Presentation-ready figures | Done | PNG + PDF outputs |
| Ahilan: Trend plots | Done | D vs eta, D vs bead, parity, alpha |

---

## 12. OUTPUT FILES

### 12.1 Pipeline Outputs

All outputs saved to `Analysis/figures/2026-03-05/{dataset_stem}/`:

Per-dataset outputs:
- `trajectories-{prefix}-trial{N}.png` --- bead trajectory plots
- `displacement_histogram-{prefix}-trial{N}.png` --- dx/dy histograms with Gaussian fit
- `msd_analysis-{prefix}-trial{N}.png` --- MSD vs tau (linear + log-log)
- `D_comparison-{prefix}-trial{N}.png` --- bar chart: 3 methods + theory band + noise floor
- `combined_summary-{prefix}-trial{N}.png` --- 2x3 grid summary
- `summary.txt` --- numerical results
- `trackresults.txt` --- processed track data
- `readme.txt` --- pipeline metadata and version

Lab-level outputs in `Analysis/figures/`:
- `batch_results.csv` --- all 49 datasets, all D values, theory, alpha
- `overall_trends.png` --- 2x2: parity, D vs eta, D vs bead, alpha distribution
- `D_vs_viscosity_by_bead.png` --- D vs eta at constant bead size (4 panels)
- `D_vs_bead_by_viscosity.png` --- D vs bead at constant viscosity (5 panels)
- `2026-03-05/trends_2026-03-05.png` --- per-session grouped bar chart

### 12.2 Tracker Input Files

All tracker .txt files are in `Data/2026-03-05/`. Total: 51 files (49 data + 2 calibration).

---

## 13. REFLECTION

This session was primarily a data processing and code debugging session rather than a data collection session. The transition from automated MTrack2 tracking to Nathan's manual Tracker approach significantly improved data quality --- the tracker pipeline consistently produces D values within 8--50% of theory for well-behaved conditions, compared to the old video pipeline which often gave > 90% deviations.

The main limitation of our experiment is the camera frame rate (29 fps). At 34 ms per frame, fast-moving beads (especially small beads in low-viscosity fluids) have their displacements averaged down. For future work, recording at the camera's maximum frame rate (~226 fps) over a shorter duration would reduce this systematic error.

The acetone experiments highlighted an important practical lesson: sample chamber sealing must be compatible with the solvent. Nail polish dissolves in acetone, compromising the chamber integrity. For acetone samples, vacuum grease or mineral oil should be used as a sealant.

Despite the systematic underestimation of D, the data clearly demonstrates the Stokes-Einstein prediction: diffusion coefficient scales as 1/(viscosity * bead_diameter). This is the core physics result of our bead diffusion project.

---
