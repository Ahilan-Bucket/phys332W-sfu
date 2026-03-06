# Lab [2] Session [7] — M&M: Continue Data Collection

**Date:** 3 Mar 2026
**Lab Partner:** Nathan Unhrn
**Recorder:** Ahilan Kumaresan

**SESSION FOCUS:** Complete the 4x4 bead diffusion matrix (4 bead sizes x 4 viscosity conditions). This session extends Session 6's dataset with systematic coverage of all bead-size/viscosity combinations, including the 2.1 um beads not tested in Session 6 and a wider viscosity range (0% glycerol through 40% glycerol plus pure acetone). Additionally, a noise baseline was collected from the calibration slide to quantify microscope vibration and tracking uncertainty.

**Repository:** [github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility)

**Google Drive (full AVI dataset):** [drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9](https://drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9?usp=sharing)

> **Note on data storage:** Since 24 Feb 2026 (Session 5 onward), all new AVI files are stored on Google Drive in addition to the lab computer. Only a subset of Session 7 files were copied to the local repository (`Data/2026-03-03/`); the full dataset is available on the shared Google Drive folder above. See Section 16 for the complete file listing with storage locations.

---

## 1. GOALS

1. Spend Initial Moments (10-15 mins) Understanding the Theory of the Calculations
2. Make the Python Calculator (Later)
3. Collect Noise from Calibration Slide video
4. COllect New Data
5. Do Analysis In Lab
6. Reflect and evaluate

**Expanded Session 7 targets:**

- Fill the complete 4x4 matrix: 4 bead sizes (1, 2.1, 3, 5 um) x 4 viscosity conditions (0% glycerol, 20% glycerol, 40% glycerol, pure acetone)
- Add 2.1 um beads (not tested in Sessions 5-6) for a finer bead-size comparison
- Widen glycerol range from 36% (Session 6) to 40% for a cleaner viscosity spread
- Replace acetone-water mixtures (Session 6: 20%, 40%) with pure acetone for maximum viscosity contrast
- Collect 2-3 independent trials per condition for repeatability
- Collect noise baseline videos from calibration slide for systematic error quantification
- Run in-lab analysis between slides to check data quality

---

## 2. APPARATUS

**Standard Equipment (same as Sessions 1-3):**
Refer to Session 1, Section II (pg 2 of lab notebook)

| Item | Description |
|------|-------------|
| Microscope | Olympus BX51 upright bright-field |
| Camera | FLIR BlackFly U3-13Y3M (1440x1080 px) |
| Objectives | 10x, 40x, 100x oil immersion |
| Immersion oil | n = 1.518 |
| Stage micrometer | 1 mm / 100 div (10 um/div) |
| Software | NI Vision Assistant |
| Analysis | Python (Lab2_Analysis_Pipeline.ipynb) |

**Additional Items for Session 7:**

| Item | Source/Location | Purpose |
|------|----------------|---------|
| Glycerol (100%) | Lab bench | Viscosity variable: 20% and 40% solutions |
| Acetone (pure) | Lab technician | Low-viscosity variable: pure acetone solvent |
| 1 um polystyrene beads (0.5% stock) | Lab bench | Smallest bead size |
| 2.1 um polystyrene beads (0.5% stock) | Lab bench | Intermediate bead size (NEW this session) |
| 3 um polystyrene beads (0.5% stock) | Lab bench | Primary bead size |
| 5 um polystyrene beads (0.5% stock) | Lab bench | Largest bead size |
| Micropipettes (2 uL, 20 uL, 200 uL, 1000 uL) | Lab bench | Precise volume measurements |
| Eppendorf tubes | Lab bench | Mixing solutions |
| Glass slides + coverslips | Lab bench | Sample mounting |
| Parafilm spacers | Lab bench | ~100 um thick chamber |
| Nail polish | Lab bench | Seal chamber edges |

---

## 3. VARIABLES

| Type | Variable | Range / Values | Description |
|------|----------|---------------|-------------|
| Independent | Fluid viscosity (eta) | 0.32 - 4.11 mPa.s | Controlled via glycerol (0%, 20%, 40%) and pure acetone |
| Independent | Bead diameter (2r) | 1, 2.1, 3, 5 um | Polystyrene microspheres (rho = 1.05 g/cm^3) |
| Dependent | Diffusion coefficient D | um^2/s | Measured by three methods: variance, Gaussian fit, MSD slope |
| Dependent | MSD(tau) | um^2 | Mean-squared displacement vs lag time |
| Dependent | MSD exponent alpha | dimensionless | Power-law slope on log-log MSD plot |
| Control | Temperature T | 19 C = 292 K | Room temperature --- NOT varied |
| Control | Pixel calibration | 68.4 nm/px | Verified every session at 100x oil (Sessions 1, 3, 4, 6) |
| Control | Bead stock concentration | 0.5% by weight | Standardised across all conditions |
| Control | Chamber type | Parafilm spacer (~100 um) | Consistent with Session 6 |
| Control | Frame rate | 226 fps | Consistent with Session 6 |
| Control | Video length | 120 frames (~0.53 s) | Consistent with Session 6 |

---

## 4. REFERENCES

**Primary Lab Documents:**
1. MM-LabScript-microscopy.pdf (Sec 3.3-3.5)
2. CellMotility-LabScript.pdf
3. Protocol: Microscope Setup --- Olympus BX51
4. Protocol: Making Sample Chambers
5. Protocol: Acquiring Movies with Vision Assistant

**Scientific References:**
6. Cheng (2008) --- empirical formula for glycerol-water viscosity
7. Howard & McAllister (1958) --- acetone-water mixture viscosity data
8. Stokes-Einstein relation: D = k_B T / (6 pi eta r)
9. Faxen's Law --- wall interaction correction for diffusion near boundaries

**Previous Lab Data:**
10. Session 5 data (24 Feb): `Data/2026-02-24/`
11. Session 6 data (26 Feb): `Data/2026-02-26/`
12. Session 5 notebook: `Notes/Lab2-Session5-Notebook.md`
13. Session 6 notebook: `Personal/Lab2-Session6-26Feb2026.md`
14. Analysis pipeline: `Analysis/Lab2_Analysis_Pipeline.ipynb`

---

## 5. MICROSCOPE SETUP VERIFICATION

### 5.1 Kohler Illumination

| Step | Done? |
|------|-------|
| Lamp on, 5 min warm-up | Yes |
| Blank slide, focus at 10x | Yes |
| Field diaphragm edges sharp | Yes |
| Condenser centered | Yes |
| Field diaphragm to just outside FOV | Yes |
| Aperture diaphragm to ~70% NA | Yes |

All steps confirmed.

### 5.2 Calibration Verification (100x)

No new calibration measurement this session. Used established value from Sessions 1, 3, 4, 6.

| Session | Date | Calibration | Status |
|---------|------|-------------|--------|
| Session 1 | 03 Feb 2026 | 68.45 nm/px | REFERENCE |
| Session 3 | 10 Feb 2026 | 68.4 nm/px | CONFIRMED |
| Session 4 | 12 Feb 2026 | 68.7 nm/px | CONFIRMED |
| Session 6 | 26 Feb 2026 | 68.4 nm/px | Retained |
| **Session 7** | **3 Mar 2026** | **68.4 nm/px** | **Retained (no change)** |

---

## 6. BACKGROUND: THEORY REVIEW (10-15 min)

*Spent the initial 10-15 minutes reviewing the theoretical framework before collecting data.*

### 6.1 Viscosity at 19 C

Get Viscority at 19 C (For Glyceol, Water and Acetone)
- From Calculator (Chegg(2008)).
- For acetone use the CHart Figure 1 Session 5

**Reference viscosity values at 19 C (292 K):**

| Fluid | eta (mPa.s) | Source |
|-------|-------------|--------|
| Pure water | ~1.027 | Cheng (2008) |
| 20% glycerol | ~1.76 | Cheng (2008) calculator |
| 40% glycerol | ~4.11 | Cheng (2008) calculator |
| Pure acetone | ~0.33 | Session 5, Figure 1 (Howard & McAllister 1958) |

### 6.2 Concentration Correction (Batchelor Equation)

Use Correctioj use Bachelor Equation:
- Also A Calculator

At our working dilutions (stock fractions of 1-10 uL per 500 uL total), the particle volume fraction phi is very small. The Einstein correction eta = eta_0 * (1 + 2.5*phi) and Batchelor second-order term are negligible. See Session 5, Section 7.5 for the full derivation.

### 6.3 Wall Interaction Correction (Faxen's Laws)

Use Wall Interation COrrection (Faxen's Laws)
To not count the Faxues Effect from vertial and Horzonal Axis, we try to view only the cenetr
We use the Faxues for the depth axis. Becase we do not have a way to know they effect jere.
There is a Range of Values, High and a low.

**Strategy:** We minimise Faxen wall effects in the x-y plane by selecting particles near the centre of the FOV. For the depth (z) axis, we cannot control the bead's vertical position in the chamber, so we apply the Faxen correction as a range:
- **High D estimate:** bead at mid-chamber (h = 50 um, R/h << 1, correction negligible)
- **Low D estimate:** bead near wall (h ~ 5R, correction factor ~ 0.886 for 5 um beads)

See Session 5, Section 7.6 for the full Faxen derivation.

### 6.4 Computing D_theory

Take the Diffusion Constant and Es-Stroke Equation
- Input all the Tempr and other constant and the enw viscoscity

we get the D values
Then multiply the the Faxues law constant on the D values

D Theory.

**Procedure:**
1. Look up eta at 19 C for each fluid condition (Sec 6.1)
2. Compute D_theory = k_B * T / (6 * pi * eta * r) for each bead size
3. Apply Faxen's correction (high/low range) to get D_theory_corrected

---

## 7. NOISE BASELINE COLLECTION

Colected three slides for the noise with the 100x scope with Calibration slide.
While typing, walking and doing other things.
Saved

**Purpose:** Quantify the microscope's intrinsic noise floor --- tracking artifacts from vibrations, electrical noise, and mechanical disturbances --- by recording video of stationary features on the calibration slide under realistic lab conditions.

**Method:** The stage micrometer (calibration slide) was placed under the 100x oil objective. Three videos (120 frames each, 226 fps) were recorded under different ambient conditions:

| File | Condition | Purpose |
|------|-----------|---------|
| `noise-calibration_slide-1.avi` | Normal lab noise (typing, talking) | Baseline noise level |
| `noise-calibration_slide-2.avi` | Walking near microscope | Vibration from footsteps |
| `noise-calibration_slide-3.avi` | Other activities | General disturbance level |

The tracking pipeline will be run on these noise videos to measure apparent D_noise from stationary features. Any D measured from bead samples that is comparable to D_noise is dominated by tracking uncertainty and should not be trusted as a true diffusion measurement.

> **Location:** `Data/2026-03-03/` (all three files stored locally)

---

## 8. SAMPLE PREPARATION

### 8.1 Experimental Design: 4x4 Matrix

This session targets a complete 4x4 matrix of bead size x viscosity:

| | Water (0% gly) | 20% Glycerol | 40% Glycerol | Pure Acetone |
|---|---|---|---|---|
| **1 um** | r1 | r5 | ~~r9~~ SKIP | ~~r13~~ SKIP |
| **2.1 um** | r2 | r6 | r10 | r14 |
| **3 um** | r3 | r7 | r11 | r15 |
| **5 um** | r4 | r8 | r12 | r16 |

Slides are numbered r1-r16 in the order they were prepared and observed. Two slides (r9, r13) were prepared and observed under the microscope but data was NOT recorded --- see Section 8.3.

### 8.2 Solution Preparation

All solutions prepared in Eppendorf tubes. Total volume standardised at ~500 uL per slide (lesson from Session 6: Slides 2b vs 3 showed a 2x D difference between 5 mL and 500 uL preps).

**Stock volumes by bead size (established from Sessions 5-6):**

| Bead Size | Stock Volume (0.5%) | Rationale |
|-----------|-------------------|-----------|
| 1 um | 1.15 uL | High natural number density; needs small stock volume |
| 2.1 um | ~2.5 uL | Intermediate; estimated from concentration scaling |
| 3 um | 3.0 uL | Confirmed in Sessions 5-6 (gives ~10 beads/FOV) |
| 5 um | 10.0 uL | Low number density; needs more stock for trackable count |

**Fluid recipes (500 uL total, excluding stock):**

| Condition | Water (uL) | Glycerol (uL) | Acetone (uL) |
|-----------|-----------|---------------|--------------|
| 0% glycerol | 500 | 0 | 0 |
| 20% glycerol | 400 | 100 | 0 |
| 40% glycerol | 300 | 200 | 0 |
| Pure acetone | 0 | 0 | 500 |

### 8.3 Slide Preparation Table

ROom Temp 19

All slides prepared at room temperature (19 C) using the thick chamber method (parafilm spacer, ~100 um gap), sealed with nail polish.

| Slide | Bead | Solvent | Stock (uL) | Water (uL) | Gly/Ace (uL) | Trials Recorded | Notes |
|-------|------|---------|-----------|-----------|--------------|-----------------|-------|
| r1 | 1 um | Water | 1.15 | 500 | 0 | 1 | Baseline; 1 um difficult to track |
| r2 | 2.1 um | Water | ~2.5 | ~498 | 0 | 2 | Good visibility, NEW bead size |
| r3 | 3 um | Water | ~3.0 | ~497 | 0 | 2 | Standard condition, reliable |
| r4 | 5 um | Water | 10 | 490 | 0 | 2 | Chamber height non-uniform; clumping observed |
| r5 | 1 um | 20% gly | 1.15 | 400 | 100 gly | 2 | 1 um slow in glycerol, hard to resolve |
| r6 | 2.1 um | 20% gly | ~2.5 | ~398 | 100 gly | 2 | NEW bead size in glycerol |
| r7 | 3 um | 20% gly | 3.0 | 397 | 100 gly | 3 | Trial 3 labelled "best" |
| r8 | 5 um | 20% gly | ~10 | ~390 | 100 gly | 3 | Slower beads; needed patience for focusing |
| **r9** | **1 um** | **40% gly** | --- | --- | --- | **0 (SKIPPED)** | **Observed but not recorded; see Sec 8.4** |
| r10 | 2.1 um | 40% gly | ~2.5 | ~298 | 200 gly | 2 | Beads visibly slower in thick glycerol |
| r11 | 3 um | 40% gly | ~3.0 | ~297 | 200 gly | 2 | Moderate track count expected |
| r12 | 5 um | 40% gly | ~10 | ~290 | 200 gly | 3 | Multiple reattempts; see Sec 8.5 |
| **r13** | **1 um** | **Acetone** | --- | --- | --- | **0 (SKIPPED)** | **Observed but not recorded; see Sec 8.4** |
| r14 | 2.1 um | Acetone | ~2.5 | 0 | ~498 ace | 2 | Pure acetone solvent |
| r15 | 3 um | Acetone | ~3.0 | 0 | ~497 ace | 1 | Acetone dissolving nail polish seal |
| r16 | 5 um | Acetone | ~10 | 0 | ~490 ace | 4 | Fast-moving beads; 4 attempts needed |

### 8.4 Slides Not Recorded (r9 and r13)

| Slide | Condition | Reason Not Recorded |
|-------|-----------|-------------------|
| r9 | 1 um, 40% glycerol | SKiping 1mu for now becase its always been harder to record. They keep going out of focus in the chamber and very suspetable to drift and external vibrations. In 40% glycerol (eta ~ 4.11 mPa.s), D_theory for 1 um beads drops to ~0.08 um^2/s --- the particles barely move between frames at 226 fps and are indistinguishable from tracking noise. Combined with the difficulty of resolving 1 um beads near the diffraction limit, this condition was not viable for reliable data. |
| r13 | 1 um, pure acetone | Same fundamental issue as r9 (1 um near diffraction limit, hard to track), compounded by acetone compatibility problems: acetone dissolves the nail polish seal, causing the chamber to leak and introducing flow artifacts. Additionally, pure acetone may soften or alter polystyrene bead surfaces, changing their optical properties. |

> **Decision:** Rather than waste lab time on conditions unlikely to produce usable data, we prioritised collecting multiple reliable trials for 2.1, 3, and 5 um beads across all four viscosity conditions. The 1 um bead size effect can still be assessed from the water (r1) and 20% glycerol (r5) conditions.

### 8.5 Slides Requiring Multiple Attempts

Several slides needed more than the standard 2 trials due to preparation or observation issues:

| Slide | Trials | Issue |
|-------|--------|-------|
| r7 (3 um, 20% gly) | 3 | First two trials had acceptable but not ideal bead counts. Trial 3 achieved the best FOV and was labelled "best" in the filename. |
| r8 (5 um, 20% gly) | 3 | 5 um beads in 20% glycerol are slow-moving and tend to settle near the bottom of the chamber. Multiple trials needed to find a FOV with enough mobile beads in the focal plane. |
| r12 (5 um, 40% gly) | 3 | Glycerol at 40% can have lumps or inhomogeneities where particles get collected and trapped. The thick glycerol also causes more settling of the heavy 5 um beads. Different stock volumes and refocusing were attempted between trials to improve the result. |
| r15 (3 um, acetone) | 1 only | Pure acetone dissolves the nail polish seal. The chamber integrity degraded during observation, introducing drift and flow. Only one usable trial was captured before the seal failed. From now on, acetone slides must be observed and recorded quickly before the seal is compromised. |
| r16 (5 um, acetone) | 4 | Pure acetone has very low viscosity (eta ~ 0.33 mPa.s), so 5 um beads move much faster than in water or glycerol (D_theory ~ 0.27 um^2/s). The fast motion combined with seal degradation (acetone dissolving nail polish) made it hard to capture a good FOV with stable, in-focus particles. Four attempts were needed. |

---

## 9. DATA COLLECTION: WATER SLIDES (0% GLYCEROL)

All videos recorded at 226 fps, 120 frames (0.53 s), 1440x1080 px, 100x oil immersion.

eta_water(19 C) = 1.027 mPa.s

### 9.1 Slide r1 --- 1 um Beads in Pure Water

**Purpose:** Smallest bead in simplest fluid. D_theory = k_B*T / (6*pi*eta*r) = 0.416 um^2/s at 19 C.

**Preparation:** 1.15 uL of 0.5% stock (1 um) + 500 uL water.

**Observation:** 1 um beads are near the diffraction limit at 100x. They appear as small, low-contrast diffraction-limited spots. Only a small number of particles are trackable in each FOV. Consistent with Session 6 experience (Slide 2a gave only 4-7 tracks per trial for 1 um beads).

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | `r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi` | Local + Drive | Low track count expected |

### 9.2 Slide r2 --- 2.1 um Beads in Pure Water

**Purpose:** NEW bead size not tested in Sessions 5-6. Provides an intermediate data point between 1 um and 3 um for the bead-size scaling test. D_theory = 0.198 um^2/s at 19 C.

**Preparation:** ~2.5 uL of 0.5% stock (2.1 um) + ~498 uL water.

**Observation:** 2.1 um beads are clearly visible at 100x, better contrast than 1 um. Good trackability.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r2 trial 1 | Drive | First trial |
| 2 | r2 trial 2 | Drive | Second trial |

### 9.3 Slide r3 --- 3 um Beads in Pure Water

**Purpose:** Primary bead size baseline in water. Direct comparison to Session 6 Slide 1b (same condition). D_theory = 0.139 um^2/s at 19 C.

**Preparation:** ~3 uL of 0.5% stock (3 um) + ~497 uL water.

**Observation:** Good bead count and visibility. Standard condition.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | `r3-trial1.avi` | Local + Drive | Reliable condition |
| 2 | `r3-Trial2.avi` | Local + Drive | Repeat for statistics |

### 9.4 Slide r4 --- 5 um Beads in Pure Water

**Purpose:** Largest bead in water. D_theory = 0.083 um^2/s at 19 C. Tests bead-size scaling at the large end.

**Preparation:** 10 uL of 0.5% stock (5 um) + 490 uL water.

SLide R4 is a little Fishy for me,
- It felt like the height of chamber was not uniform.
- More clumping

**Observation:** The chamber appeared to have non-uniform height, possibly from uneven parafilm spacer placement. More bead clumping was visible than for smaller beads, suggesting insufficient mixing of the stock before pipetting. The larger 5 um beads are more prone to settling and aggregation.

From now on, when we make larger beads like 5mu, ensure more mixing.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | `r4-5mu-0_5p-10ul-water-490ul-gly-0-trial1.avi` | Local + Drive | Chamber height concern |
| 2 | `r4-5mu-0_5p-10ul-water-490ul-gly-0-trial2.avi` | Local + Drive | Same slide, different FOV |

> **Lesson:** For 5 um beads, vortex the stock tube more thoroughly before pipetting. Check chamber uniformity visually before recording.

---

## 10. DATA COLLECTION: 20% GLYCEROL SLIDES

eta_20gly(19 C) ~ 1.76 mPa.s

### 10.1 Slide r5 --- 1 um Beads in 20% Glycerol

**Purpose:** Small bead in moderate viscosity. Same condition as Session 6 Slide 2a (for comparison/repeatability). D_theory = 0.185 um^2/s at 19 C.

**Preparation:** 1.15 uL of 0.5% stock (1 um) + 400 uL water + 100 uL glycerol.

**Observation:** 1 um beads slower than in water (as expected), but still near diffraction limit. Tracking remains challenging.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | `r5-1mu-0_5p-1_15ul-water-400ul-gly-100ul-trial1.avi` | Local + Drive | Low track count likely |
| 2 | r5 trial 2 | Drive | Repeat trial |

### 10.2 Slide r6 --- 2.1 um Beads in 20% Glycerol

**Purpose:** NEW condition. Provides intermediate bead-size data point at moderate viscosity. D_theory = 0.088 um^2/s at 19 C.

**Preparation:** ~2.5 uL of 0.5% stock (2.1 um) + ~398 uL water + 100 uL glycerol.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r6 trial 1 | Drive | New bead size |
| 2 | r6 trial 2 | Drive | Repeat for statistics |

### 10.3 Slide r7 --- 3 um Beads in 20% Glycerol

**Purpose:** Core viscosity condition. Comparable to Session 6 Slides 2b and 3 (same bead/glycerol, standardised 500 uL prep). D_theory = 0.062 um^2/s at 19 C.

**Preparation:** 3 uL of 0.5% stock (3 um) + 397 uL water + 100 uL glycerol.

**Observation:** Three trials collected. Trial 3 achieved the best FOV with good bead count and minimal drift, labelled "best" in the filename.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | `r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial1.avi` | Local + Drive | Acceptable |
| 2 | `r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial2.avi` | Local + Drive | Acceptable |
| 3 | `r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial3-best.avi` | Local + Drive | **Best FOV** |

### 10.4 Slide r8 --- 5 um Beads in 20% Glycerol

**Purpose:** Largest bead in moderate viscosity. This condition failed in Session 6 (Slide 4: beads settled rapidly, too few mobile particles). D_theory = 0.037 um^2/s at 19 C.

**Preparation:** ~10 uL of 0.5% stock (5 um) + ~390 uL water + 100 uL glycerol.

**Observation:** 5 um beads in glycerol are slow. Three trials were needed to find FOVs with enough mobile beads. Beads tend to settle toward the bottom of the thick chamber in glycerol more than in water due to density mismatch at higher viscosity.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r8 trial 1 | Drive | Settling concern |
| 2 | r8 trial 2 | Drive | Better FOV |
| 3 | r8 trial 3 | Drive | Repeat |

---

## 11. DATA COLLECTION: 40% GLYCEROL SLIDES

eta_40gly(19 C) ~ 4.11 mPa.s

> **Note:** This is a higher glycerol concentration than Session 6's maximum of 36%. The 40% condition gives eta ~ 4.11 mPa.s, approximately 4x that of water. Combined with Session 6's 20% condition (eta ~ 1.76 mPa.s) and Session 5's water baseline (eta ~ 1.03 mPa.s), this provides a clean 4x viscosity range.

### 11.1 Slide r9 --- 1 um Beads in 40% Glycerol (SKIPPED)

**NOT RECORDED.** Slide was prepared and placed under the microscope for observation. 1 um beads in 40% glycerol are too slow (D_theory ~ 0.08 um^2/s) and too small to reliably detect and track. They go out of focus easily and their displacements per frame at 226 fps (~0.01 um) are below the tracking noise floor (~0.035-0.070 um). See Section 8.4 for full justification.

### 11.2 Slide r10 --- 2.1 um Beads in 40% Glycerol

**Purpose:** Intermediate bead in high viscosity. D_theory = 0.042 um^2/s at 19 C.

**Preparation:** ~2.5 uL of 0.5% stock (2.1 um) + ~298 uL water + 200 uL glycerol.

**Observation:** Beads visibly slower than in the 20% glycerol condition. The glycerol solution appeared uniform --- no visible lumps or inhomogeneities for 2.1 um beads.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r10 trial 1 | Drive | Beads slow but trackable |
| 2 | r10 trial 2 | Drive | Repeat |

### 11.3 Slide r11 --- 3 um Beads in 40% Glycerol

**Purpose:** Primary bead at high viscosity. D_theory = 0.029 um^2/s at 19 C.

**Preparation:** ~3 uL of 0.5% stock (3 um) + ~297 uL water + 200 uL glycerol.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r11 trial 1 | Drive | Standard condition |
| 2 | r11 trial 2 | Drive | Repeat |

### 11.4 Slide r12 --- 5 um Beads in 40% Glycerol

**Purpose:** Largest bead in highest glycerol. D_theory = 0.017 um^2/s at 19 C. This is the slowest expected diffusion of any condition in the matrix.

**Preparation:** ~10 uL of 0.5% stock (5 um) + ~290 uL water + 200 uL glycerol. Multiple preparations attempted --- see below.

**Observation:** This was the most difficult glycerol condition. The 40% glycerol solution at this concentration sometimes has lumps or inhomogeneities where particles get collected and trapped, artificially reducing the apparent D. The 5 um beads also settle rapidly in the viscous solution. Different stock volumes and refocusing were attempted between trials:

Be more like Image J - Exclude Particles that dont even move at all. They are stuck in Glycerol

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r12 trial 1 | Drive | Initial attempt; some beads stuck |
| 2 | r12 trial 2 | Drive | Adjusted stock or refocused |
| 3 | r12 trial 3 | Drive | Final attempt |

> **Analysis note:** For r12 analysis, stuck particles (zero displacement over entire video) must be excluded from the tracking results. This is analogous to ImageJ's particle filtering --- particles with total displacement below a minimum threshold should be discarded, as they are physically stuck in glycerol lumps, not undergoing Brownian motion.

---

## 12. DATA COLLECTION: PURE ACETONE SLIDES

eta_acetone(19 C) ~ 0.33 mPa.s

> **Note:** Pure acetone has approximately 1/3 the viscosity of water. This is the lowest-viscosity condition in the matrix and gives the highest expected D values. Session 6 used acetone-water mixtures (20%, 40%); Session 7 uses pure acetone for maximum viscosity contrast.

> **WARNING --- Acetone and Nail Polish:** I am growing concern that there might be Nail Polish touching the Scope. Pure acetone dissolves the nail polish seal used to close the chamber edges. This means: (a) the seal degrades during observation, introducing flow and leakage; (b) dissolved nail polish may contaminate the sample and the microscope objective. For future sessions, consider an alternative seal (e.g., vacuum grease, mineral oil) for acetone samples.

### 12.1 Slide r13 --- 1 um Beads in Pure Acetone (SKIPPED)

**NOT RECORDED.** Same fundamental limitations as r9 (1 um near diffraction limit, hard to resolve), compounded by the acetone dissolving the nail polish seal. The rapid seal degradation made it impossible to get a stable observation. See Section 8.4.

### 12.2 Slide r14 --- 2.1 um Beads in Pure Acetone

**Purpose:** Intermediate bead in lowest viscosity. D_theory = 0.57 um^2/s at 19 C --- the highest D of any 2.1 um condition.

**Preparation:** ~2.5 uL of 0.5% stock (2.1 um) + ~498 uL pure acetone.

**Observation:** Beads visibly more active than in any glycerol or water condition. The acetone seal was stable long enough to capture two trials.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r14 trial 1 | Drive | Fast bead motion |
| 2 | r14 trial 2 | Drive | Repeat before seal degrades |

### 12.3 Slide r15 --- 3 um Beads in Pure Acetone

**Purpose:** Primary bead in lowest viscosity. D_theory = 0.40 um^2/s at 19 C.

**Preparation:** ~3 uL of 0.5% stock (3 um) + ~497 uL pure acetone.

**Observation:** Only one trial was captured before the acetone dissolved the nail polish seal. The chamber began leaking during the second attempt, introducing macroscopic flow that would bias any MSD measurement. Further trials were abandoned.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r15 trial 1 | Drive | **Only trial before seal failure** |

> **Lesson:** Acetone slides must be observed and recorded as fast as possible. Prepare the slide, place it on the microscope, find a good FOV, and start recording immediately. Every minute of delay increases the risk of seal degradation.

### 12.4 Slide r16 --- 5 um Beads in Pure Acetone

**Purpose:** Largest bead in lowest viscosity. D_theory = 0.24 um^2/s at 19 C. Despite being the largest bead, the low viscosity of pure acetone makes these beads move fast.

**Preparation:** ~10 uL of 0.5% stock (5 um) + ~490 uL pure acetone.

**Observation:** Four trials were needed. The combination of fast bead motion (acetone viscosity is 1/3 of water) and progressive seal degradation (acetone dissolving nail polish) made it challenging to find a good FOV with stable, in-focus particles before the chamber leaked. Each attempt was a race against the dissolving seal.

| Trial | File | Storage | Notes |
|-------|------|---------|-------|
| 1 | r16 trial 1 | Drive | First attempt |
| 2 | r16 trial 2 | Drive | Better FOV |
| 3 | r16 trial 3 | Drive | Seal starting to degrade |
| 4 | r16 trial 4 | Drive | Final attempt |

---

## 13. IN-LAB OBSERVATIONS (RAW NOTES)

*These are raw observations recorded during the session, preserved verbatim from the lab bench:*

While COntinously Observing.

SLide R4 is a little Fishy for me,
- It felt like the height of chamber was not uniform.
- More clumping

From now on, when we make larger beads like 5mu, ensure more mixing.

I am growing concern that there might be Nail Polish touching the Scope.

SKiping 1mu for now becase its always been harder to record. They keep going out of focus in the chamber and very suspetable to drift and external vibrations.

We might be having an Bin width error with the gaussian.
- Need the Gaussiana nd Variance to match better.

And then Variance match with Slope.

Error Analysis.

Be more like Image J - Exclude Particles that dont even move at all. They are stuck in Glycerol

---

## 14. ANALYSIS NOTES

### 14.1 Gaussian vs Variance Agreement

We might be having an Bin width error with the gaussian.
- Need the Gaussiana nd Variance to match better.

And then Variance match with Slope.

**Issue identified:** The displacement histogram binning affects the Gaussian fit result (D_Gaussian), creating disagreement between D_Gaussian and D_Variance. This was traced to two causes:

1. **Fixed bin count:** Using a fixed number of bins (e.g., `nbins=20`) makes the histogram shape dependent on the number of data points. With few displacements, each bin is noisy and the Gaussian fit is unreliable.

2. **Raw-count vs density-normalized histogram:** Fitting a Gaussian amplitude to raw counts is sensitive to the total number of data points. Fitting a normalized probability density function (PDF) decouples the fit from sample size.

**Fix applied (post-session):** The pipeline was updated to use Freedman-Diaconis automatic binning (`bins='fd'`) with a density-normalized histogram. The Gaussian PDF fit `f(x) = (1/sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2 / (2*sigma^2))` now converges more consistently, and D_Gaussian agrees better with D_Variance. Sigma-clipping (3-sigma, 5 iterations) was also added to remove tracking outliers before computing D_Variance.

### 14.2 Stuck Particle Exclusion

Be more like Image J - Exclude Particles that dont even move at all. They are stuck in Glycerol

**Issue:** In high-viscosity conditions (40% glycerol, especially with 5 um beads), some particles are physically stuck in glycerol lumps or adhered to chamber walls. These particles produce tracks with zero total displacement that bias D downward and alpha toward 0.

**Solution:** The tracking pipeline's `MIN_TOTAL_DISPLACEMENT` parameter (default: 3.0 px) already excludes completely stationary particles. For high-glycerol slides, this threshold may need to be increased to filter out particles that are stuck but show sub-pixel jitter from tracking noise.

### 14.3 Error Analysis Plan

Error Analysis.

**Pending error analysis items:**
1. **Noise floor characterisation:** Run pipeline on the 3 noise calibration videos to measure D_noise from stationary features.
2. **Per-segment D spread:** Compute D for each individual trajectory segment and report the spread (standard error of the mean) as the measurement uncertainty.
3. **Faxen correction range:** Apply wall correction to D_theory for each condition and check whether the corrected prediction bracket overlaps the measured D.
4. **Batchelor correction:** Verify that phi is small enough to neglect the concentration correction (it should be, given our stock volumes).
5. **Systematic vs statistical:** Compare trial-to-trial spread (statistical) to the D >> D_theory offset (systematic) to determine whether the dominant error is random or systematic.

---

## 15. CONCLUSIONS

### 15.1 Summary of Session 7 Data Collection

1. **Matrix completion:** 14 of 16 planned conditions recorded (r9 and r13 skipped --- 1 um beads not viable in 40% glycerol or pure acetone).
2. **Total videos recorded:** ~30 trials across 14 slide conditions (plus 3 noise baselines).
3. **New bead size:** 2.1 um beads tested for the first time (4 conditions: water, 20% gly, 40% gly, acetone).
4. **Extended viscosity range:** 40% glycerol (eta ~ 4.11 mPa.s) replaces Session 6's 36%, and pure acetone (eta ~ 0.33 mPa.s) replaces Session 6's 20%/40% acetone-water mixtures. Total viscosity range: 0.33 to 4.11 mPa.s (~12.5x).
5. **Noise baseline:** 3 calibration slide videos collected for systematic error quantification.

### 15.2 Key Issues Identified

| Issue | Affected Slides | Mitigation |
|-------|----------------|------------|
| 1 um beads near diffraction limit | r1, r5, r9 (skip), r13 (skip) | Only analyse r1 and r5; accept low track counts |
| Acetone dissolves nail polish seal | r13 (skip), r15 (1 trial), r16 (4 attempts) | Record immediately after mounting; consider vacuum grease seal |
| 5 um bead clumping / settling | r4, r8, r12 | Vortex stock more thoroughly; pipette-mix after adding stock |
| Glycerol inhomogeneity (lumps) | r12 | Warm glycerol before mixing; vortex longer; exclude stuck particles |
| Gaussian/Variance D disagreement | All slides | Fixed post-session: Freedman-Diaconis binning + density-normalized PDF + sigma-clipping |
| Non-uniform chamber height | r4 | Check spacer alignment before sealing |

### 15.3 Comparison to Session 6

| Metric | Session 6 | Session 7 |
|--------|-----------|-----------|
| Bead sizes tested | 3 (1, 3, 5 um) | 4 (1, 2.1, 3, 5 um) |
| Viscosity conditions | 5 (0%, 20%, 36% gly, 20%, 40% ace) | 4 (0%, 20%, 40% gly, pure ace) |
| Unique slide conditions | 9 (7 recorded) | 16 (14 recorded) |
| Total trials | 22 | ~30 |
| Noise baseline | No | Yes (3 videos) |
| Known acetone issue | Yes (s8 failed) | Yes (seal degradation understood) |

### 15.4 Combined Dataset Summary (Sessions 5-7)

After Sessions 5-7, the full bead diffusion dataset consists of:

- **Session 5 (24 Feb):** 4 videos --- 3 um in water (3 trials) + 5 um in 20% glycerol (1 trial)
- **Session 6 (26 Feb):** 22 videos --- 7 slide conditions, 20 successfully analysed
- **Session 7 (3 Mar):** ~30 videos --- 14 slide conditions across the 4x4 matrix
- **Total: ~56 videos** across ~20 unique bead/viscosity conditions

This dataset should provide sufficient coverage for the D vs viscosity, D vs bead size, and D vs concentration analyses in the report.

---

## 16. DATA FILES CREATED

### 16.1 Video Files (Session 7: 2026-03-03)

> **Storage note:** Since 24 Feb 2026 (Session 5), all AVI files are uploaded to Google Drive: [drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9](https://drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9?usp=sharing). A subset of Session 7 files were also copied to the local repository (`Data/2026-03-03/`). Files marked "Local + Drive" exist in both locations; files marked "Drive" are only on Google Drive.

**Noise Baseline:**

| # | Filename | Storage | Description |
|---|----------|---------|-------------|
| 1 | `noise-calibration_slide-1.avi` | Local + Drive | Normal lab noise (typing, talking) |
| 2 | `noise-calibration_slide-2.avi` | Local + Drive | Walking near microscope |
| 3 | `noise-calibration_slide-3.avi` | Local + Drive | General disturbance |

**Water Slides (0% Glycerol):**

| # | Filename | Slide | Bead | Storage |
|---|----------|-------|------|---------|
| 4 | `r1-1mu-0_5p-1_15ul-water-500ul-gly-0.avi` | r1 | 1 um | Local + Drive |
| 5 | r2 trial 1 | r2 | 2.1 um | Drive |
| 6 | r2 trial 2 | r2 | 2.1 um | Drive |
| 7 | `r3-trial1.avi` | r3 | 3 um | Local + Drive |
| 8 | `r3-Trial2.avi` | r3 | 3 um | Local + Drive |
| 9 | `r4-5mu-0_5p-10ul-water-490ul-gly-0-trial1.avi` | r4 | 5 um | Local + Drive |
| 10 | `r4-5mu-0_5p-10ul-water-490ul-gly-0-trial2.avi` | r4 | 5 um | Local + Drive |

**20% Glycerol Slides:**

| # | Filename | Slide | Bead | Storage |
|---|----------|-------|------|---------|
| 11 | `r5-1mu-0_5p-1_15ul-water-400ul-gly-100ul-trial1.avi` | r5 | 1 um | Local + Drive |
| 12 | r5 trial 2 | r5 | 1 um | Drive |
| 13 | r6 trial 1 | r6 | 2.1 um | Drive |
| 14 | r6 trial 2 | r6 | 2.1 um | Drive |
| 15 | `r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial1.avi` | r7 | 3 um | Local + Drive |
| 16 | `r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial2.avi` | r7 | 3 um | Local + Drive |
| 17 | `r7-3mu-0_5p-3ul-water-397ul-gly-100ul-trial3-best.avi` | r7 | 3 um | Local + Drive |
| 18 | r8 trial 1 | r8 | 5 um | Drive |
| 19 | r8 trial 2 | r8 | 5 um | Drive |
| 20 | r8 trial 3 | r8 | 5 um | Drive |

**40% Glycerol Slides:**

| # | Filename | Slide | Bead | Storage |
|---|----------|-------|------|---------|
| --- | r9 (SKIPPED) | r9 | 1 um | Not recorded |
| 21 | r10 trial 1 | r10 | 2.1 um | Drive |
| 22 | r10 trial 2 | r10 | 2.1 um | Drive |
| 23 | r11 trial 1 | r11 | 3 um | Drive |
| 24 | r11 trial 2 | r11 | 3 um | Drive |
| 25 | r12 trial 1 | r12 | 5 um | Drive |
| 26 | r12 trial 2 | r12 | 5 um | Drive |
| 27 | r12 trial 3 | r12 | 5 um | Drive |

**Pure Acetone Slides:**

| # | Filename | Slide | Bead | Storage |
|---|----------|-------|------|---------|
| --- | r13 (SKIPPED) | r13 | 1 um | Not recorded |
| 28 | r14 trial 1 | r14 | 2.1 um | Drive |
| 29 | r14 trial 2 | r14 | 2.1 um | Drive |
| 30 | r15 trial 1 | r15 | 3 um | Drive |
| 31 | r16 trial 1 | r16 | 5 um | Drive |
| 32 | r16 trial 2 | r16 | 5 um | Drive |
| 33 | r16 trial 3 | r16 | 5 um | Drive |
| 34 | r16 trial 4 | r16 | 5 um | Drive |

> **Note:** Files marked "Drive" have exact filenames available in the Google Drive folder. Local file copies are in `Data/2026-03-03/`. The naming convention follows: `r{slide}-{bead}mu-0_5p-{stock}ul-water-{water}ul-gly-{gly}ul-trial{n}.avi` for glycerol slides, and similar patterns for acetone slides with `ace` replacing `gly`.

### 16.2 Analysis Output

Analysis figures will be generated in `Analysis/figures/2026-03-03/{video_stem}/` using the updated pipeline (`Analysis/Lab2_Analysis_Pipeline.ipynb`). Each analysed trial folder will contain:
- `trajectories.png` --- trajectory plots (pixel and um)
- `displacement_histogram.png` --- dx/dy histograms with density-normalized Gaussian PDF fit
- `msd_analysis.png` --- MSD vs tau (linear and log-log) with power-law fit
- `D_comparison.png` --- bar chart comparing 3 methods + Stokes-Einstein
- `trackresults.txt` --- MTrack2-format track data
- `summary.txt` --- numerical results summary
