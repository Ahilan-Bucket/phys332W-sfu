# Brownian Motion Diffusion Analysis - February 5, 2026

## Experiment Overview

This dataset contains particle tracking results from microscopy videos of polystyrene beads undergoing Brownian motion in water. Two bead sizes (1 um and 5 um) were analyzed to verify the Stokes-Einstein relation for diffusion.

## Data Files

| File | Bead Size | Particles Tracked | Description |
|------|-----------|-------------------|-------------|
| `1mu-21c-1isto224w-0_5p-trackresults.txt` | 1.0 um | 75 | Primary 1um bead data |
| `5mu-21c-1isto6_5w-0_5p-trackresults.txt` | 5.0 um | 17 | Primary 5um bead data |
| `1mu-0_5p_225x-Results.txt` | 1.0 um | 39 | Alternative 1um data |

## Experimental Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Temperature** | 21.0 C (294.15 K) | Room temperature |
| **Frame Rate** | 226 fps | High-speed camera |
| **Time Step (dt)** | 4.42 ms | 1/226 s between frames |
| **Pixel Size** | 0.0684 um/px (68.4 nm) | **CORRECTED** — originally recorded as 345 nm/px (see Calibration Note) |
| **Viscosity** | 0.0009764 Pa.s | Water at 21C |
| **Bead Diameters** | 1.0 um, 5.0 um | Polystyrene microspheres |

---

## Theoretical Predictions (Stokes-Einstein)

The diffusion coefficient is predicted by:

$$D = \frac{k_B T}{6 \pi \eta r}$$

### Expected Values

| Bead Size | Radius | D_theory (um^2/s) |
|-----------|--------|-------------------|
| 1.0 um | 0.5 um | **0.441** |
| 5.0 um | 2.5 um | **0.088** |

**Expected Ratio:** D(1um) / D(5um) = 5.0

---

# KEY OBSERVATIONS AND RESULTS

## Summary of Measured Diffusion Coefficients

### Diffusion Coefficients

| Bead | Method 1 (Variance) | Method 2 (Gauss Fit) | Method 3 (MSD) | Theory |
|------|---------------------|---------------------|----------------|--------|
| **1.0 um** | 8.71 um^2/s | 8.91 um^2/s | 12.99 um^2/s | 0.441 um^2/s |
| **5.0 um** | 2.73 um^2/s | 2.06 um^2/s | 3.69 um^2/s | 0.088 um^2/s |

### Key Ratios

| Ratio | Measured | Expected |
|-------|----------|----------|
| D(1um)/D(5um) | **3.5** | 5.0 |
| D_exp/D_theory (1um) | **~20-30x** | 1.0 |
| D_exp/D_theory (5um) | **~23-42x** | 1.0 |

---

## 1. Are Displacements Gaussian Distributed?

**Theory predicts:** Frame-to-frame displacements should be Gaussian with variance = 2D*dt

**Observations:**

| Bead Size | std_x (px) | std_y (px) | Gaussian Fit std_x | Gaussian Fit std_y |
|-----------|-----------|-----------|-------------------|-------------------|
| 1.0 um | 0.807 | 0.803 | 0.812 | 0.815 |
| 5.0 um | 0.438 | 0.463 | 0.362 | 0.419 |

**Analysis:**
- [x] **Shape:** Histograms are approximately bell-shaped (Gaussian)
- [x] **Symmetry:** Distributions are symmetric around zero (after drift correction)
- [x] **Consistency:** Direct calculation and Gaussian fit give similar sigma values for 1um beads
- [ ] **5um beads:** Some discrepancy between direct and fit methods suggests possible outliers

**Conclusion:** Displacements appear Gaussian-distributed, consistent with Brownian motion. The 1um beads show better agreement between methods than 5um beads.

---

## 2. Direct Variance vs Gaussian Fit

**1 um Beads:**
| Method | sigma_x (px) | sigma_y (px) | D (um^2/s) |
|--------|-------------|-------------|------------|
| Direct Calculation | 0.807 | 0.803 | 8.71 |
| Gaussian Fit | 0.812 | 0.815 | 8.91 |

**Agreement:** Excellent - methods differ by only 2%

**5 um Beads:**
| Method | sigma_x (px) | sigma_y (px) | D (um^2/s) |
|--------|-------------|-------------|------------|
| Direct Calculation | 0.438 | 0.463 | 2.73 |
| Gaussian Fit | 0.362 | 0.419 | 2.06 |

**Agreement:** Fair - methods differ by ~25%

**Discussion:**
- The larger discrepancy for 5um beads suggests possible outliers or non-Gaussian tails
- Direct variance is more sensitive to outliers than Gaussian fit
- The Gaussian fit may be more reliable when there are tracking errors

---

## 3. Comparison with Stokes-Einstein Theory

### MAJOR FINDING: D_experimental >> D_theory (20-40x higher)

| Bead Size | D_experiment (MSD) | D_theory | Ratio |
|-----------|-------------------|----------|-------|
| 1.0 um | 12.99 um^2/s | 0.441 um^2/s | **29.4x** |
| 5.0 um | 3.69 um^2/s | 0.088 um^2/s | **41.8x** |

**This large discrepancy requires explanation. Possible causes:**

### CONFIRMED: Pixel Calibration Error
- D scales as (pixel_size)^2
- Session 2 used 0.345 um/px — **5.04× too large**. Correct value: 0.0684 um/px
- Confirmed in Sessions 1 (68.45 nm/px), 3 (68.4 nm/px), and 4 (68.7 nm/px)
- Corrected D (1 um beads) = 0.507 um²/s — within ~15% of theory (0.441)
- See `Analysis/Diffusion_Analysis_Corrected.ipynb` for corrected analysis

### Other Possible Causes:
1. **Tracking errors** - false matches between particles inflating apparent motion
2. **Convection/drift** - sample not fully equilibrated, thermal gradients
3. **Particle aggregation** - clusters behaving as smaller effective particles
4. **Wrong magnification** - objective or tube lens different than assumed

### What is NOT likely the cause:
- Temperature error (would need T > 6000K to explain 20x)
- Viscosity error (water would need to be 20x less viscous)
- Wrong bead size (would need sub-100nm beads)

---

## 4. MSD Analysis: Linearity and Time Scales

**MSD Results:**

| Bead Size | Slope (um^2/s) | Intercept (um^2) | D from slope |
|-----------|---------------|------------------|--------------|
| 1.0 um | 51.96 | -0.082 | 12.99 um^2/s |
| 5.0 um | 14.76 | -0.011 | 3.69 um^2/s |

**Observations:**
- [x] MSD is linear at short lag times (consistent with free diffusion)
- [ ] Negative intercept is unphysical (should be positive from localization error)
- [x] Slope gives D values consistent with variance methods (same order of magnitude)

**Discussion:**
- The linear MSD confirms diffusive behavior (not confined or directed motion)
- The negative intercept suggests possible systematic error in data processing
- MSD method gives highest D values, possibly more sensitive to tracking errors at longer lags

---

## 5. Comparison Between Bead Sizes

**Key test:** D should scale as 1/r (inversely with radius)

**Expected ratio:** D(1um) / D(5um) = 5.0

**Measured ratios:**
| Method | D(1um)/D(5um) | Expected |
|--------|--------------|----------|
| Variance | 3.19 | 5.0 |
| Gaussian Fit | 4.32 | 5.0 |
| MSD | 3.52 | 5.0 |

**Analysis:**
- Measured ratio (~3.2-4.3) is **lower than expected (5.0)**
- This suggests the 5um beads have proportionally more apparent motion than expected
- Possible causes:
  - 5um beads tracked less accurately (larger apparent motion from tracking noise)
  - Bead sizes not exactly 1.0 and 5.0 um
  - Different hydrodynamic effects near surfaces

**Positive finding:** The ratio is in the right direction (1um moves more than 5um), confirming size-dependent diffusion even if absolute values are off.

---

## 6. Measurement Noise Correction

The refined equation accounting for localization error (sigma^2) and exposure time (t_c):

$$\langle \Delta x^2 \rangle = 2\sigma^2 + 2D(\Delta t - \frac{1}{3}t_c)$$

**Estimation of localization error:**
- Typical sub-pixel fitting accuracy: ~0.1 pixel
- sigma^2 ~ (0.1 px)^2 = 0.01 px^2
- Contribution to variance: 2*sigma^2 ~ 0.02 px^2
- Measured variance: ~0.65 px^2 (for 1um beads)
- **Conclusion:** Localization error is ~3% of signal - NOT significant

**Camera exposure correction:**
- If t_c << dt (typical for 226 fps), correction factor is negligible
- This does NOT explain the 20-40x discrepancy

---

## Conclusions

### 1. Is Brownian motion observed?
**YES** - Displacement histograms are Gaussian, MSD is linear, and smaller beads diffuse faster than larger beads.

### 2. Does Stokes-Einstein hold?
**INCONCLUSIVE** - Measured D values are 20-40x higher than theory. This is most likely due to **pixel calibration error** rather than a failure of Stokes-Einstein.

### 3. Is the size dependence correct?
**PARTIALLY** - D(1um)/D(5um) ratio is ~3.5 instead of expected 5.0. The trend is correct (smaller beads diffuse faster), but quantitative agreement is lacking.

### 4. Main sources of error:
1. **Pixel calibration** - Most likely cause of systematic 20-40x offset
2. **Tracking quality** - May explain variance in D(1um)/D(5um) ratio
3. **Sample preparation** - Possible convection or aggregation

---

## Recommendations

1. **Verify pixel calibration** - Re-measure using stage micrometer images in calibration-feb5-*.tif
2. **Check for convection** - Let sample equilibrate longer, seal slide edges
3. **Improve tracking** - Use stricter parameters to reduce false matches
4. **Repeat measurements** - Collect more data to improve statistics

---

## Calibration Files

| File | Description |
|------|-------------|
| `calibration-feb5-100x.tif` | Stage micrometer at 100x magnification |
| `calibration-feb5-50x.tif` | Stage micrometer at 50x magnification |

## Analysis Notebook

```
../Analysis/Diffusion_Analysis.ipynb
```

## References

1. Einstein, A. (1905). "On the Movement of Small Particles Suspended in Stationary Liquids Required by the Molecular-Kinetic Theory of Heat"
2. Perrin, J. (1909). Brownian Movement and Molecular Reality
3. Berg, H.C. (1993). Random Walks in Biology. Princeton University Press.

---
*Data collected: February 5, 2026*
*Analysis completed: February 6, 2026*
*PHYS 332W - Advanced Physics Lab, SFU*
