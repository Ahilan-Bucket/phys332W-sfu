# Lab [2] Session [6] — M&M: Short Project Data Collection (Start)

**Date:** 26 Feb 2026
**Lab Partner:** Nathan Unhrn
**Recorder:** Ahilan Kumaresan

**SESSION FOCUS:**
- Observation
- Reason
- Conclusion
- Error

**Repository:** [github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility)

---

## 1. GOALS

1. Execute Nathan's 7-slide data collection plan from Session 5 (Sec 12.1 of Session 5 notebook)
2. Collect multiple trials per slide for the three variables under investigation:
   - **Viscosity** (glycerol concentration: 0%, 20%, 36%)
   - **Bead size** (1 um, 3 um, 5 um)
   - **Concentration** (varying stock dilutions)
3. Attempt acetone-water mixtures as a low-viscosity condition (if acetone available)
4. Analyse our data and get an overall trend for D vs each variable
5. Discuss the analysis to think about what worked and plan the data collection for the next lab
6. Plan a rough lab report outline: What is our narrative? What data do we discuss? What does our trend show overall?
   - Our report must describe what we did throughout this lab AND what we additionally investigated in our project(s)
   - We will be investigating: **How does bead size, concentration, and viscosity affect bead movement?**

---

## 2. APPARATUS

**Standard Equipment (same as Sessions 1–3):**
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

**Additional Items for Session 6:**

| Item | Source/Location | Purpose |
|------|----------------|---------|
| Glycerol (100%) | Lab bench | Viscosity variable: 20% and 36% solutions |
| Acetone | Lab technician | Low-viscosity variable: 20% and 40% solutions |
| 1 um polystyrene beads (0.5% stock) | Lab bench | Bead size variable |
| 3 um polystyrene beads (0.5% stock) | Lab bench | Primary bead size (most conditions) |
| 5 um polystyrene beads (0.5% stock) | Lab bench | Bead size variable (large) |
| Micropipettes (2 uL, 20 uL, 200 uL, 1000 uL) | Lab bench | Precise volume measurements |
| Eppendorf tubes | Lab bench | Mixing solutions |
| Glass slides | Lab bench | Sample mounting |
| Coverslips (#1, 22x22 mm) | Lab bench | Sample cover |
| Parafilm spacers | Lab bench | ~100 um thick chamber |
| Nail polish | Lab bench | Seal chamber edges |

---

## 3. VARIABLES

| Type | Variable | Description |
|------|----------|-------------|
| Independent | Glycerol concentration | 0%, 20%, 36% (vol/vol) |
| Independent | Acetone concentration | 0%, ~20%, ~40% (vol/vol) |
| Independent | Bead diameter | 1 um, 3 um, 5 um |
| Independent | Bead concentration | Varying stock fraction (0.5% to ~5x stock) |
| Dependent | D (diffusion coefficient) | um^2/s, three methods |
| Dependent | alpha (MSD exponent) | MSD ~ tau^alpha |
| Dependent | Particles per FOV | Tracking quality metric |
| Dependent | Number of valid tracks | From pipeline output |
| Control | Temperature | ~21 C (room temp) |
| Control | Objective | 100x oil immersion |
| Control | Pixel size | 68.4 nm/px (calibrated Sessions 1, 3, 4) |
| Control | Frame rate | 226 fps |
| Control | Video length | 120 frames (~0.53 s) |
| Control | Chamber type | Parafilm spacer (~100 um) |

---

## 4. REFERENCES

**Primary Lab Documents:**
1. MM-LabScript-microscopy.pdf (Sec 3.3-3.5, pp. 9-11)
2. CellMotility-LabScript.pdf (cell motion background)
3. Protocol: Microscope Setup --- Olympus BX51
4. Protocol: Making Sample Chambers
5. Protocol: Acquiring Movies with Vision Assistant

**Scientific References:**
6. Cheng (2008) --- empirical formula for glycerol-water viscosity
7. Howard & McAllister (1958) --- acetone-water mixture viscosity data
8. Stokes-Einstein relation: D = k_B T / (6 pi eta r)

**Previous Lab Data:**
9. Session 5 data (24 Feb): `Data/2026-02-24/`
10. Session 5 analysis: `Analysis/figures/2026-02-24/`
11. Session 5 notebook: Lab2-Session5-Notebook-v4.docx (Sec 12: full 7-slide plan)
12. Sessions 1-2 corrected analysis: `Analysis/Diffusion_Analysis_Corrected.ipynb`
13. Session 4 onion streaming (D_eff, alpha = 1.66): `Data/12-Feb/`

**Analysis Pipeline:**
14. `Analysis/Lab2_Analysis_Pipeline.ipynb` --- batch processing notebook (particle tracking, MSD, Stokes-Einstein comparison)

---

## 5. MICROSCOPE SETUP VERIFICATION

*(Must do every session)*

Ref: Protocol: Microscope Setup --- OLYMPUS BX51

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

No new calibration file created this session. Used established value from Sessions 1, 3, 4.

| Session | Date | Calibration | Status |
|---------|------|-------------|--------|
| Session 1 | 03 Feb 2026 | 68.45 nm/px | REFERENCE |
| Session 3 | 10 Feb 2026 | 68.4 nm/px | CONFIRMED |
| Session 4 | 12 Feb 2026 | 68.7 nm/px | CONFIRMED |
| **Session 6** | **26 Feb 2026** | **68.4 nm/px** | **Retained (no change)** |

> **CONCLUSION:** Calibration confirmed as 68.4 nm/px (Session 4 value retained). No new calibration file created this session.

---

## 6. PRE-LAB PLAN SUMMARY (FROM SESSION 5)

Refer to Session 5 notebook, Sections VII-XII for the full background and planning.

### 6.1 Central Research Question

**How does Brownian motion differ from directed motion? How do viscosity, bead size, and concentration affect Brownian motion?**

### 6.2 Nathan's 7-Slide Plan

Nathan restructured our original 9-set matrix into 7 explicit slides using his Cheng (2008) calculator (see Session 5 notebook, Sec 12.1):

| Slide | Glycerol (%) | Bead Size | Target Beads/FOV | Purpose |
|-------|-------------|-----------|-------------------|---------|
| 1 | 0% | 3 um | 10 | Baseline (pure water) |
| 2 | 20% | 1 um | 10 | Viscosity + size: small bead |
| 3 | 20% | 3 um | 10 | Viscosity main |
| 4 | 20% | 5 um | 10 | Viscosity + size: large bead |
| 5 | 20% | 3 um | 5 | Concentration low |
| 6 | 20% | 3 um | 20 | Concentration high |
| 7 | 36% | 3 um | 10 | Viscosity high |

### 6.3 Predicted D Values (Stokes-Einstein, T = 294 K)

| Condition | eta (Pa.s) | D_theory (um^2/s) |
|-----------|-----------|-------------------|
| 3 um, 0% glycerol | 0.000981 | 0.147 |
| 1 um, 20% glycerol | 0.00434 | 0.099 |
| 3 um, 20% glycerol | 0.00434 | 0.033 |
| 5 um, 20% glycerol | 0.00434 | 0.020 |
| 3 um, 36% glycerol | 0.01471 | 0.010 |
| 3 um, 20% acetone | 0.000819 | 0.176 |
| 3 um, 40% acetone | 0.000620 | 0.232 |

Key prediction: D should **decrease** with increasing glycerol (higher viscosity) and **increase** with increasing acetone (lower viscosity).

---

## 7. SAMPLE PREPARATION

### 7.1 Glycerol Solution Preparation

All solutions prepared at the start of the session in Eppendorf tubes. Glycerol was pipetted by volume (100% glycerol stock). Acetone was added later in the session after confirming availability with the lab technician.

### 7.2 Slide Preparation Table

All slides used the thick chamber method (parafilm spacer, ~100 um gap) sealed with nail polish.

| Slide | Solute (%) | Bead Size | Water (uL) | Stock (uL) | Glycerol/Acetone (uL) | Target Beads/FOV | Notes |
|-------|-----------|-----------|-----------|-----------|----------------------|------------------|-------|
| 1 | 0% gly | 3 um | 97.55 | 2.45 | 0 | 10 | First attempt; discarded |
| **1b** | **0% gly** | **3 um** | **597.5** | **2.5** | **0** | **10** | **Larger volume for uniformity** |
| 1c | 0% gly | 3 um | 497.5 | 2.5 | 0 | --- | Alternate dilution; not recorded |
| **2a** | **20% gly** | **1 um** | **3997.7** | **2.3** | **1000** | **10** | **Size variable: small bead** |
| **2b** | **20% gly** | **3 um** | **3997.7** | **2.3** | **1000** | **---** | **Size variable: medium bead** |
| **2c** | **20% gly** | **1 um** | **3978.5** | **11.5** | **1000** | **---** | **Higher bead concentration** |
| **3** | **20% gly** | **3 um** | **396.9** | **3.0** | **100** | **10** | **Smaller total volume** |
| 4 | 20% gly | 5 um | 80 (stock) | 20 (gly) | --- | 10 | 5 um beads; not recorded (see 7.3) |
| 5 | 20% gly | 3 um | 398.5 | 1.5 | 100 | 5 | Low concentration; not recorded |
| 6 | 20% gly | 3 um | 393.8 | 6.2 | 100 | 20 | High concentration; not recorded |
| **7** | **36% gly** | **3 um** | **316.2** | **3.8** | **180** | **10** | **High viscosity condition** |
| **8** | **~20% ace** | **3 um** | **397** | **3.0** | **100 (ace)** | **---** | **Acetone: low-visc condition** |
| **9** | **~40% ace** | **3 um** | **1200** | **24.0** | **800 (ace)** | **---** | **Acetone: very low viscosity** |

Bold rows = data successfully recorded. Non-bold rows = prepared but not recorded or discarded.

### 7.3 Slides Not Recorded

| Slide | Reason |
|-------|--------|
| 1 | Initial attempt at pure water; volume too small for uniform mixing. Remade as Slide 1b with larger volume. |
| 1c | Alternate dilution factor tested; concentration not satisfactory. |
| 4 | 5 um beads settled rapidly in 20% glycerol; too few mobile particles detected in FOV. Deprioritised in favour of more glycerol/acetone trials. |
| 5 | Low concentration slide (5 beads/FOV target) --- insufficient particles detected for tracking. Time allocated to acetone trials instead. |
| 6 | High concentration slide (20 beads/FOV target) --- particles overlapped and tracking was unreliable. Time allocated to acetone trials instead. |

> **NOTE:** Slides 4, 5, 6 addressed the concentration and 5 um bead conditions. These were deprioritised during the session in favour of acetone-water data, which was not part of the original plan but became available when the technician confirmed acetone supply. We plan to revisit these conditions in Session 7 with improved preparation.

---

## 8. DATA COLLECTION: GLYCEROL SLIDES

All videos recorded at 226 fps, 120 frames (0.53 s), 1440x1080 px, 100x oil immersion.

### 8.1 Slide 1b --- 3 um Beads in Pure Water (0% Glycerol)

**Purpose:** Baseline condition --- no solute, standard 3 um beads.

**Preparation:** 597.5 uL water + 2.5 uL of 0.5% stock (3 um). Larger volume than Slide 1 for better uniformity.

**Observation:** CC OBSERVATION — Describe what was seen on the slide. How many beads per FOV? Were they moving visibly? Any clumping?

| Trial | File | Notes |
|-------|------|-------|
| 3 | `Data/2026-02-26/s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial3.avi` | CC |
| 4 | `Data/2026-02-26/s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial4.avi` | CC |
| 5 | `Data/2026-02-26/s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial5.avi` | CC |

> **Note:** Trials labelled 3-5 because the first two attempts (trials 1-2) were from Slide 1/1c which were discarded.

### 8.2 Slide 2a --- 1 um Beads in 20% Glycerol

**Purpose:** Small bead in moderate viscosity. Tests bead size effect at fixed glycerol.

**Preparation:** 3997.7 uL water + 2.3 uL of 0.5% stock (1 um) + 1000 uL glycerol. Large total volume (5 mL) to ensure uniform mixing at 20% glycerol.

**Observation:** CC OBSERVATION — 1 um beads are near the resolution limit at 100x. Were they visible? Did they appear as diffraction-limited spots? How many per FOV?

[CC PASTE IMAGE: BMP snapshot of Slide 2a field of view]

| Trial | File | Notes |
|-------|------|-------|
| 1 | `Data/2026-02-26/s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial1.avi` | Also captured BMP snapshot |
| 2 | `Data/2026-02-26/s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial2.avi` | CC |
| 3 | `Data/2026-02-26/s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial3.avi` | CC |

BMP snapshot: `Data/2026-02-26/S2a-1um-0_5p-2_3uL-water-3997uL-Gly-1000uL-Trial1.bmp`

### 8.3 Slide 2b --- 3 um Beads in 20% Glycerol

**Purpose:** Medium bead in moderate viscosity. Same solution as 2a but with 3 um beads. Direct comparison with Slide 2a (size effect) and Slide 3 (volume effect).

**Preparation:** 3997.7 uL water + 2.3 uL of 0.5% stock (3 um) + 1000 uL glycerol.

**Observation:** CC OBSERVATION — Describe what was seen. How did bead motion compare visually to Slide 2a (1 um)?

| Trial | File | Notes |
|-------|------|-------|
| 1 | `Data/2026-02-26/s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial1.avi` | CC |
| 2 | `Data/2026-02-26/s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial2.avi` | CC |
| 3 | `Data/2026-02-26/s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial3.avi` | CC |

### 8.4 Slide 2c --- 1 um Beads in 20% Glycerol (Higher Concentration)

**Purpose:** Same as Slide 2a but with ~5x more bead stock. Tests whether higher bead concentration changes the measured D or produces crowding effects.

**Preparation:** 3978.5 uL water + 11.5 uL of 0.5% stock (1 um) + 1000 uL glycerol.

**Observation:** CC OBSERVATION — Were there more beads per FOV? Any clumping or crowding visible?

| Trial | File | Notes |
|-------|------|-------|
| 1 | `Data/2026-02-26/s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial1.avi` | CC |
| 2 | `Data/2026-02-26/s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial2.avi` | CC |
| 3 | `Data/2026-02-26/s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial3.avi` | CC |

### 8.5 Slide 3 --- 3 um Beads in 20% Glycerol (Small Volume)

**Purpose:** Same glycerol % as Slide 2b but prepared with a smaller total volume (500 uL vs 5 mL). Tests whether preparation volume affects uniformity and measured D.

**Preparation:** 396.9 uL water + 3.0 uL of 0.5% stock (3 um) + 100 uL glycerol.

**Observation:** CC OBSERVATION — Compare bead density and behaviour to Slide 2b. Any visible difference?

| Trial | File | Notes |
|-------|------|-------|
| 1 | `Data/2026-02-26/s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial1.avi` | CC |
| 2 | `Data/2026-02-26/s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial2.avi` | CC |
| 3 | `Data/2026-02-26/s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial3.avi` | CC |

### 8.6 Slide 7 --- 3 um Beads in 36% Glycerol

**Purpose:** High viscosity condition. Glycerol at 36% gives eta ~ 14.7 mPa.s (15x water). Should show significantly reduced D compared to 20% glycerol.

**Preparation:** 316.2 uL water + 3.8 uL of 0.5% stock (3 um) + 180 uL glycerol. Glycerol fraction: 180/496 = 36.3%.

**Observation:** CC OBSERVATION — Were beads visibly slower? Could you see reduced Brownian motion compared to 20% glycerol slides?

| Trial | File | Notes |
|-------|------|-------|
| 1 | `Data/2026-02-26/s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial1.avi` | CC |
| 2 | `Data/2026-02-26/s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial2.avi` | CC |
| 3 | `Data/2026-02-26/s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial3.avi` | CC |

---

## 9. DATA COLLECTION: ACETONE SLIDES

After completing the glycerol slides, the lab technician confirmed acetone was available. Acetone-water mixtures have **lower viscosity** than pure water (eta_acetone ~ 0.32 mPa.s at 21 C), providing the opposite end of the viscosity spectrum from glycerol.

### 9.1 Acetone-Water Viscosity

Unlike glycerol (which increases viscosity monotonically), acetone-water mixtures show non-ideal behaviour: the mixture viscosity decreases with increasing acetone fraction.

| Acetone vol% | eta (mPa.s) | Relative to water |
|-------------|-------------|-------------------|
| 0% | 0.978 | 1.00x |
| 20% | 0.82 | 0.84x |
| 40% | 0.62 | 0.63x |
| 100% | 0.32 | 0.33x |

Source: Howard & McAllister (1958), interpolated at 21 C.

### 9.2 Slide 8 --- 3 um Beads in ~20% Acetone

**Purpose:** Low-viscosity condition. Acetone at ~20% gives eta ~ 0.82 mPa.s (slightly less than water).

**Preparation:** 397 uL water + 3.0 uL of 0.5% stock (3 um) + 100 uL acetone. Acetone fraction: 100/500 = 20.0%.

**Observation:** CC OBSERVATION — Did the acetone affect bead visibility? Any bubbles or evaporation issues? Bead count?

| Trial | File | Notes |
|-------|------|-------|
| 1 | `Data/2026-02-26/s8-3um-0_5p-3ul-water-397ul-ace-100ul-trial1.avi` | Very few particles detected |
| 2 | `Data/2026-02-26/s8-3um-0_5p-3ul-water-397ul-ace-100ul-trial2.avi` | Very few particles detected |

> **WARNING:** Both Slide 8 trials had extremely low particle counts (mean 0.1 and 0.6 particles/frame). The pipeline found 0 valid tracks (trial 1) and 1 valid track with no usable segments (trial 2). **These trials are not usable for analysis.** Possible cause: acetone may have affected bead surface properties or caused beads to stick to surfaces. The low concentration (3 uL stock in 500 uL) may also be a factor.

### 9.3 Slide 9 --- 3 um Beads in ~40% Acetone

**Purpose:** Very low viscosity condition. Acetone at 40% gives eta ~ 0.62 mPa.s (63% of water). Higher bead stock volume used to avoid the particle count issue from Slide 8.

**Preparation:** 1200 uL water + 24.0 uL of 0.5% stock (3 um) + 800 uL acetone. Acetone fraction: 800/2000 = 40.0%.

**Observation:** CC OBSERVATION — Much higher particle count than Slide 8 due to 8x more stock. Describe bead motion --- faster than water baseline?

| Trial | File | Notes |
|-------|------|-------|
| 1 | `Data/2026-02-26/s9-3um-0_5p-24_0ul-water-1200ul-ace-800ul-trial1.avi` | 31 valid tracks |
| 2 | `Data/2026-02-26/s9-3um-0_5p-24_0ul-water-1200ul-ace-800ul-trial2.avi` | 36 valid tracks |

> **Note:** Slide 9 used a much larger stock volume (24 uL vs 3 uL for Slide 8) and worked well. For future acetone slides, use at least 10-20 uL stock per 500 uL total volume.

---

## 10. PRELIMINARY ANALYSIS

All videos processed using `Analysis/Lab2_Analysis_Pipeline.ipynb` (batch mode, 226 fps, 68.4 nm/px, 21 C).

### 10.1 Pipeline Output Summary

| Slide | Bead | Solute | Trials Recorded | Trials Analysed | Status |
|-------|------|--------|----------------|-----------------|--------|
| 1b | 3 um | 0% gly | 3 | 3 | OK |
| 2a | 1 um | 20% gly | 3 | 3 | OK |
| 2b | 3 um | 20% gly | 3 | 3 | OK |
| 2c | 1 um | 20% gly (high conc) | 3 | 3 | OK |
| 3 | 3 um | 20% gly | 3 | 3 | OK |
| 7 | 3 um | 36% gly | 3 | 3 | OK |
| 8 | 3 um | 20% ace | 2 | 0 | FAILED --- too few particles |
| 9 | 3 um | 40% ace | 2 | 2 | OK |
| **Total** | | | **22** | **20** | |

### 10.2 Results by Slide Group

All analysis figures saved in `Analysis/figures/2026-02-26/{video_stem}/`. Pipeline parameters: 226 fps, 68.4 nm/px, T = 21 C, top-10 segments per video.

#### Slide 1b --- 3 um, 0% Glycerol (Baseline)

eta = 0.000981 Pa.s | D_theory = 0.147 um^2/s

| Trial | Tracks | D_Direct | D_Gaussian | D_MSD | alpha |
|-------|--------|----------|-----------|-------|-------|
| 3 | 53 | 2.907 | 0.916 | 2.188 | 0.505 |
| 4 | 44 | 2.719 | 0.711 | 1.865 | 0.662 |
| 5 | 9 | 4.896 | 3.025 | 4.675 | 0.530 |
| **Avg** | **35** | **3.507** | **1.551** | **2.909** | **0.566** |

> Trial 5 has only 9 tracks (poor statistics) and inflates the averages. Excluding trial 5: D_Gaussian = 0.81, D_MSD = 2.03, alpha = 0.58. All three methods give D >> D_theory. Deviations from Stokes-Einstein: +525% (Gaussian, trial 3) to +3242% (Direct, trial 5).

[CC PASTE IMAGE: Trajectories and D_comparison from s1b trial 3 or trial 4 (best track count)]

#### Slide 2a --- 1 um, 20% Glycerol

eta = 0.00434 Pa.s | D_theory = 0.099 um^2/s

| Trial | Tracks | D_Direct | D_Gaussian | D_MSD | alpha |
|-------|--------|----------|-----------|-------|-------|
| 1 | 4 | 2.737 | 2.862 | 3.210 | 0.471 |
| 2 | 7 | 2.924 | 2.381 | 4.063 | 0.535 |
| 3 | 7 | 2.307 | 1.186 | 2.322 | 0.591 |
| **Avg** | **6** | **2.656** | **2.143** | **3.198** | **0.532** |

> Very low track counts (4-7 per trial). 1 um beads are near the diffraction limit and hard to detect. All D values are 10-40x higher than theory. The Gaussian method does not converge to theory here as it does for larger beads --- likely because the displacement distribution is dominated by tracking noise rather than true Brownian steps.

#### Slide 2b --- 3 um, 20% Glycerol (Large Volume Prep)

eta = 0.00434 Pa.s | D_theory = 0.033 um^2/s

| Trial | Tracks | D_Direct | D_Gaussian | D_MSD | alpha |
|-------|--------|----------|-----------|-------|-------|
| 1 | 11 | 2.848 | 1.039 | 2.224 | 0.228 |
| 2 | 9 | 4.763 | 2.034 | 6.039 | 0.468 |
| 3 | 6 | 1.781 | 0.451 | 1.043 | 0.233 |
| **Avg** | **9** | **3.131** | **1.175** | **3.102** | **0.310** |

> Trial 2 is an outlier (D_MSD = 6.04, deviation +18 136%). Low track counts (6-11). Alpha is very low (0.23-0.47), indicating strongly confined motion. Large spread across trials suggests high sensitivity to which field of view was captured.

#### Slide 2c --- 1 um, 20% Glycerol (5x Higher Bead Concentration)

eta = 0.00434 Pa.s | D_theory = 0.099 um^2/s

| Trial | Tracks | D_Direct | D_Gaussian | D_MSD | alpha |
|-------|--------|----------|-----------|-------|-------|
| 1 | 6 | 2.043 | 1.749 | 2.702 | 0.701 |
| 2 | 12 | 1.586 | 1.096 | 1.509 | 0.643 |
| 3 | 8 | 1.534 | 1.107 | 1.421 | 0.577 |
| **Avg** | **9** | **1.721** | **1.317** | **1.877** | **0.640** |

> Higher bead concentration (5x stock vs Slide 2a) produces more consistent results across trials and slightly lower D values. Compare to Slide 2a (D_Gaussian = 2.14): the 5x concentration gives D_Gaussian = 1.32, a ~38% reduction. This could indicate crowding effects or simply better statistics from more trackable particles.

#### Slide 3 --- 3 um, 20% Glycerol (Small Volume Prep)

eta = 0.00434 Pa.s | D_theory = 0.033 um^2/s

| Trial | Tracks | D_Direct | D_Gaussian | D_MSD | alpha |
|-------|--------|----------|-----------|-------|-------|
| 1 | 16 | 1.431 | 0.425 | 1.102 | 0.608 |
| 2 | 16 | 1.210 | 0.440 | 0.573 | 0.392 |
| 3 | 11 | 2.233 | 0.799 | 1.760 | 0.283 |
| **Avg** | **14** | **1.625** | **0.555** | **1.145** | **0.428** |

> More tracks (11-16) and lower D values than Slide 2b (same bead/glycerol but 10x smaller prep volume). D_Gaussian averages 0.56 vs 1.18 for Slide 2b. The smaller prep volume (500 uL vs 5 mL) may have produced a more concentrated bead suspension despite the same nominal dilution, or the glycerol may have mixed less uniformly.

#### Slide 7 --- 3 um, 36% Glycerol (High Viscosity)

eta = 0.01471 Pa.s | D_theory = 0.010 um^2/s

| Trial | Tracks | D_Direct | D_Gaussian | D_MSD | alpha |
|-------|--------|----------|-----------|-------|-------|
| 1 | 15 | 1.127 | 0.280 | 1.084 | 0.753 |
| 2 | 21 | 1.744 | 0.577 | 1.136 | 0.619 |
| 3 | 20 | 2.045 | 0.614 | 1.070 | 0.456 |
| **Avg** | **19** | **1.639** | **0.490** | **1.097** | **0.609** |

> Highest glycerol condition. D_Gaussian = 0.49, which is the lowest of all 3 um glycerol slides (consistent with higher viscosity suppressing diffusion). However, the D_MSD values (~1.1) barely differ from Slide 3 or Slide 2b, suggesting the MSD method saturates at a noise floor. Track counts are good (15-21). Deviations from theory are extreme (+2 800% to +20 800%) because D_theory is only 0.010 um^2/s.

[CC PASTE IMAGE: Trajectories and D_comparison from s7 trial 2 (best track count)]

#### Slide 8 --- 3 um, ~20% Acetone (FAILED)

eta = 0.000819 Pa.s | D_theory = 0.176 um^2/s

| Trial | Tracks | Status |
|-------|--------|--------|
| 1 | 0 | FAILED --- 0.1 particles/frame, no valid tracks |
| 2 | 1 | FAILED --- 0.6 particles/frame, 1 track, no usable segments |

> Both trials unusable. Mean particles per frame < 1. Likely cause: 3 uL stock in 500 uL total was too dilute, and/or acetone at 20% altered bead surface properties causing adhesion to glass.

#### Slide 9 --- 3 um, 40% Acetone

eta = 0.000620 Pa.s | D_theory = 0.232 um^2/s

| Trial | Tracks | D_Direct | D_Gaussian | D_MSD | alpha |
|-------|--------|----------|-----------|-------|-------|
| 1 | 31 | 2.470 | 0.557 | 1.892 | 0.624 |
| 2 | 36 | 2.818 | 1.013 | 2.195 | 0.522 |
| **Avg** | **34** | **2.644** | **0.785** | **2.044** | **0.573** |

> Highest track counts of any Session 6 slide (31-36), thanks to 24 uL stock in 2 mL total. Theory D (0.232) is higher than any glycerol condition, and measured D_Gaussian (0.79) is also higher than the glycerol slides, consistent with lower viscosity. Deviations from theory: +140% (Gaussian, trial 1) to +1 116% (Direct, trial 2) --- **the smallest deviations of any Session 6 slide group**, suggesting the acetone condition is closest to ideal Brownian behaviour.

[CC PASTE IMAGE: Trajectories and D_comparison from s9 trial 2 (highest track count)]

### 10.3 Summary Table --- All Slide Averages

| Slide | Bead | Solute | eta (mPa.s) | D_theory | D_Gauss avg | D_MSD avg | alpha avg | Tracks avg |
|-------|------|--------|------------|----------|------------|----------|----------|-----------|
| 1b | 3 um | 0% gly | 0.981 | 0.147 | 1.551 | 2.909 | 0.57 | 35 |
| 2a | 1 um | 20% gly | 4.338 | 0.099 | 2.143 | 3.198 | 0.53 | 6 |
| 2b | 3 um | 20% gly | 4.338 | 0.033 | 1.175 | 3.102 | 0.31 | 9 |
| 2c | 1 um | 20% gly* | 4.338 | 0.099 | 1.317 | 1.877 | 0.64 | 9 |
| 3 | 3 um | 20% gly | 4.338 | 0.033 | 0.555 | 1.145 | 0.43 | 14 |
| 7 | 3 um | 36% gly | 14.71 | 0.010 | 0.490 | 1.097 | 0.61 | 19 |
| 8 | 3 um | 20% ace | 0.819 | 0.176 | --- | --- | --- | 0 |
| 9 | 3 um | 40% ace | 0.620 | 0.232 | 0.785 | 2.044 | 0.57 | 34 |

*Slide 2c = higher bead concentration (5x stock)

### 10.4 Trend Analysis

#### Trend 1: D vs Glycerol Concentration (3 um beads)

Stokes-Einstein predicts D should drop by 4.4x from 0% to 20% glycerol and by 15x from 0% to 36%.

| Condition | D_theory | D_Gauss | Ratio to 0% (theory) | Ratio to 0% (measured) |
|-----------|----------|---------|----------------------|----------------------|
| 0% gly (s1b) | 0.147 | 1.551 | 1.00x | 1.00x |
| 20% gly (s3) | 0.033 | 0.555 | 0.22x | 0.36x |
| 36% gly (s7) | 0.010 | 0.490 | 0.068x | 0.32x |

**Verdict: Qualitatively correct but quantitatively weak.** D does decrease from 0% to 20% to 36% glycerol, but the measured ratio (1.00 : 0.36 : 0.32) is much flatter than theory (1.00 : 0.22 : 0.07). The measured D values compress toward a floor of ~0.5 um^2/s regardless of viscosity, suggesting a **systematic noise floor** dominates at high viscosity.

#### Trend 2: Acetone vs Water (3 um beads)

Acetone at 40% should give D = 0.232 um^2/s (1.6x higher than water).

| Condition | D_theory | D_Gauss | Relative to water |
|-----------|----------|---------|-------------------|
| 0% (water, s1b) | 0.147 | 1.551 | 1.00x |
| 40% acetone (s9) | 0.232 | 0.785 | 0.51x |

**Verdict: Wrong direction.** Theory predicts acetone should give *higher* D than water, but measured D_Gaussian is *lower* (0.79 vs 1.55). However, the s1b average is inflated by trial 5 (only 9 tracks). Excluding trial 5: s1b D_Gauss = 0.81, making acetone (0.79) essentially the same as water. The systematic noise floor likely masks the true viscosity effect at this end of the range.

#### Trend 3: Bead Size Effect (1 um vs 3 um at 20% glycerol)

Stokes-Einstein predicts D(1 um)/D(3 um) = 3.0.

| Bead | D_theory | D_Gauss | Tracks |
|------|----------|---------|--------|
| 1 um (s2a) | 0.099 | 2.143 | 6 |
| 3 um (s2b) | 0.033 | 1.175 | 9 |
| **Ratio (1/3 um)** | **3.0** | **1.8** | |

**Verdict: Right direction, compressed ratio.** Smaller beads show higher D as expected. The measured ratio of 1.8 is lower than the theoretical 3.0, again suggesting a noise floor that compresses the dynamic range. The very low track count for 1 um beads (4-7 per trial) makes these values unreliable.

#### Trend 4: Concentration Effect (1 um beads at 20% glycerol)

Stokes-Einstein does not predict a concentration dependence for dilute suspensions.

| Slide | Stock used | D_Gauss | Tracks |
|-------|-----------|---------|--------|
| 2a (low conc) | 2.3 uL | 2.143 | 6 |
| 2c (5x conc) | 11.5 uL | 1.317 | 9 |

**Verdict: Higher concentration gives lower D (38% reduction).** This is not predicted by Stokes-Einstein for dilute suspensions. Possible explanations: (a) hydrodynamic interactions between neighbouring beads, (b) the higher track count at 5x concentration provides better statistics and reduces outlier inflation, (c) crowding increases effective viscosity. This is a genuinely interesting finding for the report.

#### Trend 5: Preparation Volume Effect (3 um, 20% glycerol)

Slides 2b (5 mL prep) and 3 (500 uL prep) have identical nominal composition.

| Slide | Prep volume | D_Gauss | Tracks |
|-------|------------|---------|--------|
| 2b (5 mL) | 5000 uL | 1.175 | 9 |
| 3 (500 uL) | 500 uL | 0.555 | 14 |

**Verdict: 2x difference for the same recipe.** The smaller volume prep gives lower D and more tracks. Possible causes: glycerol mixing is more complete in smaller volumes, or the bead concentration is effectively higher in the smaller-volume prep (3.0 uL stock in 500 uL vs 2.3 uL in 5000 uL = 6x more concentrated).

#### Trend 6: Universal Subdiffusion (alpha < 1)

All 20 analysed trials show alpha < 1 (range 0.19 to 0.75). No sample reaches alpha = 1 (ideal Brownian).

| Slide | alpha avg | Classification |
|-------|----------|---------------|
| 1b | 0.57 | Subdiffusive |
| 2a | 0.53 | Subdiffusive |
| 2b | 0.31 | Subdiffusive (strongly confined) |
| 2c | 0.64 | Subdiffusive |
| 3 | 0.43 | Subdiffusive |
| 7 | 0.61 | Subdiffusive |
| 9 | 0.57 | Subdiffusive |

**Verdict: Systematic artefact, not real physics.** All conditions --- including pure water where no confinement is expected --- show alpha ~ 0.3-0.7. This is almost certainly caused by the **short video duration** (120 frames / 226 fps = 0.53 s). At short timescales, the MSD curve flattens because: (a) the particle cannot diffuse far enough to show the linear MSD regime, (b) tracking noise adds a constant offset to MSD at all lags, which creates an apparent plateau. Session 5's mu3 video (2737 tracks, much longer recording) gave alpha = 0.70, closer to 1.0 but still subdiffusive, supporting the short-video hypothesis.

### 10.5 Systematic Error Discussion

**Why are all D values 5-200x above Stokes-Einstein theory?**

Three dominant error sources, in order of likely magnitude:

1. **Tracking noise floor.** The connected-component centroid has a localization uncertainty of ~0.5-1 pixel (~35-70 nm). At 226 fps (dt = 4.4 ms), even 0.5 px of noise per frame creates an apparent D_noise = (0.5 * 0.0684)^2 / (2 * 0.0044) = 0.13 um^2/s --- comparable to the theoretical D values. This noise adds in quadrature to the real D, inflating all measurements.

2. **Short video duration.** Only 120 frames limits the number of independent displacement measurements (~100 per track, but most tracks are shorter). The MSD curve has only ~10-30 lag points before statistical noise dominates, making fits unreliable. The linear fit window (max_lag/4) uses only 2-7 points.

3. **Vibration and drift.** The microscope stage may have sub-micron vibrations over the 0.53 s recording window. Unlike random tracking noise, drift adds a systematic velocity component that inflates the MSD slope. This would affect all trials equally.

**Why does the Gaussian fit give the lowest D?**

The Gaussian fit to the displacement histogram is less sensitive to outlier jumps than the Direct Variance or MSD methods. Large single-frame displacements (from mis-tracking or vibration) inflate the variance and MSD but are down-weighted in the Gaussian fit because they fall in the tails. This makes D_Gaussian the most robust estimator, though it is still systematically high.

---

## 11. CONCLUSIONS

### 11.1 Summary of Session 6 Data Collection

1. **Slides completed:** 7 of 9 planned conditions recorded (missing: 5 um in 20% glycerol, concentration low/high)
2. **Bonus data:** 2 acetone conditions attempted (Slide 8 at 20% failed, Slide 9 at 40% succeeded)
3. **Total usable trials:** 20 out of 22 recorded (Slide 8 trials 1-2 both failed)
4. **Acetone lesson:** 3 uL stock in 500 uL total is too dilute for acetone slides; 24 uL in 2 mL worked reliably
5. **Best data quality:** Slide 9 (acetone, 31-36 tracks) and Slide 7 (36% glycerol, 15-21 tracks)
6. **Worst data quality:** Slide 2a (1 um beads, only 4-7 tracks per trial)

### 11.2 Comparison to Session 5

Session 5 (24 Feb) recorded 4 videos: 3 um in water (3 trials) and 5 um in 20% glycerol (1 trial). Session 6 expands this to 22 videos across 7 slide conditions plus acetone.

The best Session 5 result was the mu3 video (3 um, 0% glycerol, high burst count): D_Gaussian = 0.261 um^2/s, alpha = 0.70, with 2737 valid tracks. This gives the closest agreement with Stokes-Einstein theory (+78% deviation). Session 6 uses shorter videos (120 frames at 226 fps vs 1000+ frames) which limits track length but allows more trials.

### 11.3 Key Issues Identified

1. **All D values systematically above theory (5-200x).** The dominant cause is tracking noise: centroid localization uncertainty of ~0.5-1 px creates an apparent diffusion floor of ~0.1-0.5 um^2/s that adds to all measurements. This noise floor is comparable to or larger than the theoretical D for most conditions.

2. **All alpha values subdiffusive (0.19-0.75).** This is a video-length artefact, not real confinement. At 120 frames (0.53 s), the MSD has too few lag points to resolve the linear regime. Session 5's longer mu3 video (thousands of frames) gave alpha = 0.70 with the same beads in water.

3. **Gaussian fit is the most reliable D estimator.** D_Gaussian is consistently lower than D_Direct and D_MSD because it down-weights outlier displacements from mis-tracking. For the report, we should primarily use D_Gaussian for comparisons.

4. **Qualitative trends are correct; quantitative agreement is poor.** D decreases from 0% to 20% to 36% glycerol (correct direction). D is higher for 1 um than 3 um beads (correct). But the measured ratios are compressed compared to Stokes-Einstein predictions because the noise floor dominates.

5. **Preparation volume affects results.** Slides 2b and 3 (identical composition, 10x different prep volume) give D_Gauss of 1.18 vs 0.56 --- a factor of 2. This must be controlled in Session 7 by standardising prep volume.

6. **1 um beads are unreliable at 100x.** Track counts of 4-7 per trial are insufficient for reliable statistics. The beads are near the diffraction limit and produce weak contrast against the background.

7. **Acetone compatibility.** 40% acetone works well for tracking (highest track counts of any Session 6 slide). 20% acetone failed completely (particle adhesion or insufficient stock). The Slide 9 recipe (24 uL stock in 2 mL total) should be the template for all future acetone preparations.

---

## 12. PLAN FOR SESSION 7

Session 7 is the second data collection session and focuses on **repeatability and gap-filling**.

### 12.1 Key Change: Repeatability Over Variety

Rather than taking multiple different trials from the same slide (different fields of view), we want to **prepare the same solutions 2-3 times independently** and see repeatability between preparations. This tests whether slide-to-slide variation is a significant source of error.

### 12.2 Priority Data to Collect

| Priority | Condition | Reason |
|----------|-----------|--------|
| **1** | **Longer videos (500+ frames) for 3 um in 0%, 20%, 36% gly** | **Fix alpha < 1 problem; longer MSD range; reduce noise floor** |
| 2 | 3 um, 0% gly (independent repeat x2) | Baseline repeatability --- compare to s1b |
| 3 | 3 um, 20% gly (independent repeat x2) | Core viscosity condition repeatability |
| 4 | 3 um, 40% acetone (independent repeat x2) | Acetone repeatability --- compare to s9 |
| 5 | 5 um, 20% gly | Gap: missing from Session 6 (Slide 4 failed) |
| 6 | 3 um, 20% acetone (higher stock, 20+ uL) | Gap: Slide 8 failed, need retry |
| 7 | 1 um, 0% gly | Gap: bead size comparison in water |
| 8 | 5 um, 0% gly | Gap: bead size comparison in water |

### 12.3 Preparation Notes for Session 7

- **CRITICAL: Longer videos.** The single most impactful change is increasing the recording duration. Current: 120 frames at 226 fps = 0.53 s. Options: (a) 500 frames at 226 fps = 2.2 s, or (b) 240 frames at 30 fps = 8 s. Option (b) gives 16x more temporal range for MSD and should push alpha toward 1.0.
- **Standardise prep volume.** Session 6 showed a 2x D difference between 5 mL and 500 uL preps (Slides 2b vs 3). Use 500 uL total for all slides in Session 7 to eliminate this variable.
- **Acetone slides:** Use at least 20 uL stock per 500 uL total (Slide 9 recipe template)
- **5 um beads:** May need lower frame rate (1-5 fps) and longer recording; these beads are slow in glycerol
- **Chamber sealing:** Acetone may dissolve nail polish; check seal integrity after preparation
- **Run quick MSD check** between trials (in the notebook) to confirm data quality before making more slides
- **Independent preparations:** For repeatability, make a fresh solution in a new Eppendorf each time rather than using the same solution for all trials

### 12.4 Lab Report Outline (Rough)

CC REPORT OUTLINE --- Discuss with Nathan. Key sections:
1. Introduction: Brownian motion, Stokes-Einstein, project motivation
2. Theory: D = k_B T / (6 pi eta r), MSD ~ 4Dt, alpha exponent
3. Methods: Microscope setup, sample prep, tracking pipeline
4. Results: D vs viscosity, D vs bead size, D vs concentration, acetone comparison
5. Discussion: Deviations from theory, subdiffusive alpha, error sources
6. Conclusion: What affects Brownian motion and how

---

## 13. POST-LAB REFLECTIONS

CC POST-LAB REFLECTIONS --- Fill in after session. Consider:
- What went well today?
- What would you do differently?
- Were the 226 fps / 120 frame settings appropriate?
- Did the thick chamber work for all solutions?
- How did the acetone slides compare to glycerol in ease of preparation?
- Any concerns about evaporation (especially acetone)?

---

## 14. DATA FILES CREATED

### 14.1 Video Files (Session 6: 2026-02-26)

All files in `Lab2-Microscopy-and-Motility/Data/2026-02-26/`:

| # | Filename | Slide | Bead | Solute |
|---|----------|-------|------|--------|
| 1 | `s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial3.avi` | 1b | 3 um | 0% gly |
| 2 | `s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial4.avi` | 1b | 3 um | 0% gly |
| 3 | `s1b-3um-0_5p-2_5ul-water-597_5ul-gly-0ul-trial5.avi` | 1b | 3 um | 0% gly |
| 4 | `s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial1.avi` | 2a | 1 um | 20% gly |
| 5 | `s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial2.avi` | 2a | 1 um | 20% gly |
| 6 | `s2a-1um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial3.avi` | 2a | 1 um | 20% gly |
| 7 | `s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial1.avi` | 2b | 3 um | 20% gly |
| 8 | `s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial2.avi` | 2b | 3 um | 20% gly |
| 9 | `s2b-3um-0_5p-2_3ul-water-3997ul-gly-1000ul-trial3.avi` | 2b | 3 um | 20% gly |
| 10 | `s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial1.avi` | 2c | 1 um | 20% gly |
| 11 | `s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial2.avi` | 2c | 1 um | 20% gly |
| 12 | `s2c-1um-0_5p-11_5ul-water-3978_5ul-gly-1000ul-trial3.avi` | 2c | 1 um | 20% gly |
| 13 | `s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial1.avi` | 3 | 3 um | 20% gly |
| 14 | `s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial2.avi` | 3 | 3 um | 20% gly |
| 15 | `s3-3um-0_5p-3ul-water-396ul-gly-100ul-trial3.avi` | 3 | 3 um | 20% gly |
| 16 | `s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial1.avi` | 7 | 3 um | 36% gly |
| 17 | `s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial2.avi` | 7 | 3 um | 36% gly |
| 18 | `s7-3um-0_5p-3_8ul-water-316_2ul-gly-180ul-trial3.avi` | 7 | 3 um | 36% gly |
| 19 | `s8-3um-0_5p-3ul-water-397ul-ace-100ul-trial1.avi` | 8 | 3 um | 20% ace |
| 20 | `s8-3um-0_5p-3ul-water-397ul-ace-100ul-trial2.avi` | 8 | 3 um | 20% ace |
| 21 | `s9-3um-0_5p-24_0ul-water-1200ul-ace-800ul-trial1.avi` | 9 | 3 um | 40% ace |
| 22 | `s9-3um-0_5p-24_0ul-water-1200ul-ace-800ul-trial2.avi` | 9 | 3 um | 40% ace |

### 14.2 Image Files

| Filename | Description |
|----------|-------------|
| `S2a-1um-0_5p-2_3uL-water-3997uL-Gly-1000uL-Trial1.bmp` | Snapshot of Slide 2a FOV |

### 14.3 Analysis Output

All analysis figures in `Analysis/figures/2026-02-26/{video_stem}/`:

Each successfully analysed trial folder contains:
- `trajectories.png` --- top-N trajectory plots (pixel and um)
- `displacement_histogram.png` --- dx/dy histograms with Gaussian fit
- `msd_analysis.png` --- MSD vs tau (linear and log-log) with power-law fit
- `D_comparison.png` --- bar chart comparing 3 methods + Stokes-Einstein
- `trackresults.txt` --- MTrack2-format track data
- `summary.txt` --- numerical results summary

### 14.4 Analysis Notebooks

| Notebook | Description |
|----------|-------------|
| `Analysis/Lab2_Analysis_Pipeline.ipynb` | Batch processing pipeline (26 jobs: 4 Session 5 + 22 Session 6) |
