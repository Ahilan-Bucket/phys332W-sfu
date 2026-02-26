# Lab [2] Session [5] — M&M: Short Project Data Collection (Start)

**Date:** 24 Feb 2026
**Lab Partner:** Nathan Unhrn
**Recorder:** Ahilan Kumaresan

> **SESSION FOCUS:** Transition from exploration to report-quality data collection. This session was dedicated to establishing the theory and sample preparation protocols for the quantitative bead diffusion project, running qualitative test batches to check feasibility, and resolving concentration and frame-rate issues before committing to full data collection in Session 6.

**Repository:** [github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility)

---

## 1. GOALS

1. Agree on the viscosity model for predicting η at each glycerol/alcohol concentration (Refutas method — confirmed with Nathan).
2. Calculate expected D values for all bead sizes across the three viscosity conditions.
3. Calculate expected bead counts per field of view for each bead size at 0.5% stock — identify whether dilution is needed.
4. Prepare and test a qualitative sample (5 µm beads + 20% glycerol) to verify that beads are visible and trackable before committing to full data collection.
5. Investigate concentration effects for 3 µm beads in water — find the right stock dilution.
6. Save at least one usable trial dataset as a proof-of-concept for analysis.
7. Finalize the data collection plan for Session 6.

---

## 2. APPARATUS

**Standard Equipment (same as Sessions 1–3):**
Refer to Session 1, Section II (pg 2 of lab notebook)

**Additional Items for Session 5:**

| Item | Source/Location | Purpose |
|------|----------------|---------|
| Glycerol (educational grade) | Lab bench | Prepare high-viscosity fluid mixtures |
| Acetone *(not yet available)* | Lab technician ordering | Low-viscosity fluid (thinner than water) |
| 1 µm beads (0.5% stock) | Lab bench | Smallest bead size tested |
| 2.1 µm beads (0.5% stock) | Lab bench | Intermediate bead size |
| 3 µm beads (0.5% stock) | Lab bench | Primary bead size for this session |
| 5 µm beads (0.5% stock) | Lab bench | Largest bead size tested |
| Analytical balance | Lab bench | Weigh glycerol by mass (not volume) |

> **Note:** Acetone was not available this session — the lab technician confirmed it will be ordered for Session 6. The low-viscosity condition will use water as the baseline for now, with alcohol/acetone to be added in Session 6.

---

## 3. VARIABLES

| Type | Variable | Range / Values | Description |
|------|----------|---------------|-------------|
| Independent | Fluid viscosity (η) | ~1.03, ~1.50, ~2.05 mPa·s | Controlled via glycerol mass fraction (0%, ~12%, ~23%) |
| Independent | Bead diameter (2r) | 1, 2.1, 3, 5 µm | Polystyrene microspheres (ρ = 1.05 g/cm³) |
| Dependent | Diffusion coefficient D | µm²/s | Measured by three methods: variance, Gaussian fit, MSD slope |
| Dependent | MSD(τ) | µm² | Mean-squared displacement vs lag time |
| Dependent | MSD exponent α | dimensionless | Power-law slope on log–log MSD plot |
| Control | Temperature T | 19°C = 292 K | Room temperature — NOT varied |
| Control | Pixel calibration | 68.7 nm/px | Verified every session at 100× oil |
| Control | Bead stock concentration | 0.5% by weight | Standardised across all conditions |
| Control | Chamber depth | 80 µm | Tape spacer — measured this session |
| Control | Frame rate | 30 fps (beads) | Consistent across trials unless noted |

> **Note:** Temperature is a known variable in the Stokes-Einstein equation (D ∝ T) but is NOT being varied in this experiment — it is impossible to control lab room temperature systematically. Temperature will be recorded at each run and used for theoretical D calculations, but not as an independent variable.

---

## 4. REFERENCES

**Primary Lab Documents:**
1. MM-LabScript-microscopy.pdf (Sec 3.3–3.5)
2. CellMotility-LabScript.pdf
3. Protocol: Microscope Setup — Olympus BX51
4. Protocol: Making Sample Chambers
5. Protocol: Tracking Particles (MTrack2)
6. Protocol: Acquiring Movies with Vision Assistant

**Scientific References:**

7. Cheng, N.S. (2008). "Formula for the viscosity of a glycerol-water mixture." *Industrial & Engineering Chemistry Research*, 47(9), 3285–3288. — viscosity values at different concentrations

8. Refutas method (ASTM D341) — viscosity blending index for predicting mixture viscosity

9. Einstein, A. (1905). "On the movement of small particles suspended in stationary liquids." — Stokes-Einstein derivation

10. Hughes & Hase, *Measurements and Uncertainties* (Ch 2.9, 5–8) — uncertainty propagation

**Previous Lab Data:**

11. Sessions 1–2 corrected analysis: `Analysis/Diffusion_Analysis_Corrected.ipynb`

12. Session 4 onion streaming (D_eff, α = 1.66): `Data/12-Feb/`

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

No quantitative calibration measurement was taken this session. Instead, we performed a **visual check**: with the stage micrometer slide under the 100× objective, we observed approximately **8 lines** in the field of view — consistent with the previously measured value of 68.7 nm/px from Session 4. No discrepancy was detected, and no re-measurement was needed.

> **CONCLUSION:** Calibration confirmed as **68.7 nm/px** (Session 4 value retained). No new calibration file created this session.

---

## 7. BACKGROUND: VISCOSITY MODEL AND SAMPLE PLANNING

*Time: ~2:00 PM*

Before collecting any data, Nathan and I work through the theory to calculate exactly what we expect to see and what sample preparation will give good results. This section records that work.

### 7.1 Viscosity Model: The Refutas Method

To predict the viscosity of glycerol-water mixtures at arbitrary concentrations, we use the **Refutas blending index** (ASTM D341 standard). This is more accurate than simple linear interpolation across concentrations.

**Step 1 — Convert kinematic viscosity ν (in cSt) to Refutas Blending Number (RBN):**

RBN = 14.534 × ln(ln(ν + 0.8)) + 10.975

**Step 2 — Blend by mass fraction:**

RBN_mix = w₁ × RBN₁ + w₂ × RBN₂

where w₁, w₂ are the mass fractions of each component.

**Step 3 — Invert to get mixture kinematic viscosity:**

ν_mix = exp(exp((RBN_mix − 10.975) / 14.534)) − 0.8

**Step 4 — Convert to dynamic viscosity:**

η = ρ_mix × ν_mix

For our purposes (low to moderate glycerol %, near room temperature), we cross-check these values against published Cheng (2008) tables for glycerol-water viscosity. Both methods agree well below 30% glycerol.

> **Update — Nathan's Prelab (24 Feb 2026):** Nathan subsequently found that the Refutas method requires density variables that fluctuate with temperature, making it error-prone in practice. He switched to the **Exponential Power-Form Model (Cheng, 2008)** computed via an online viscosity calculator. His VBN derivation and blending equations are shown below:
>
> **[📷 INSERT IMAGE — Nathan's Notebook, p.1: VBN formula and viscosity blending equations]**
> *Source file: `Notes/Lab2-Session5-Notebook-NathansNotebook-Must-Merege-to-session5-markwdown.pdf`, Page 1 (top-left)*

**Viscosity Reference Charts (from Nathan's Notebook):**

The following charts were used to look up η for water, glycerol, and acetone at room temperature (19°C) and to verify theoretical predictions:

> **[📷 INSERT IMAGE — Nathan's Notebook, p.1: Acetone viscosity vs temperature — theoretical model η_a = A·e^(−E_a/RT)]**
> *Source: Page 1, right column top*

> **[📷 INSERT IMAGE — Nathan's Notebook, p.1: Water kinematic viscosity vs temperature — Cheng (2008) and Kestin & Moszynski (1987) datasets + tabulated values]**
> *Source: Page 1, right column middle*

> **[📷 INSERT IMAGE — Nathan's Notebook, p.2: Glycerol dynamic viscosity vs temperature — Miner & Dalton data, 99.5% glycerol]**
> *Source: Page 2, right column top*

> **[📷 INSERT IMAGE — Nathan's Notebook, p.2: Table V — Viscosity of Aqueous Glycerol Solutions at multiple temperatures and concentrations]**
> *Source: Page 2, right column bottom*

### 7.2 Choosing the Glycerol Concentration Range

**Initial plan (0–10% glycerol):** Only a ~26% change in η — tight, and hard to distinguish from experimental uncertainty.

*Calculation:* From Cheng (2008) tables, η_water(19°C) ≈ 1.027 mPa·s and η at 10% glycerol (19°C) ≈ 1.30 mPa·s. Fractional change = (1.30 − 1.027)/1.027 ≈ 0.27 = **~26%**. Given that our MSD-derived D typically carries ±10–15% uncertainty, a 26% signal is only ~2σ — marginal for drawing a convincing D vs η trend.

**Revised plan (0–23% glycerol):** Gives a 2× range in viscosity (η from ~1.03 to ~2.05 mPa·s), which means a 2× range in measured D. Much more convincing for a D vs η plot.

Room temperature today: **19°C = 292 K**. η_water at 19°C ≈ 1.027 mPa·s (Cheng 2008).

**Chosen viscosity conditions:**

| Sample | Glycerol mass % | η (mPa·s) at ~20°C | Preparation |
|--------|----------------|---------------------|-------------|
| Pure water | 0% | ~1.03 | Direct from tap |
| Mid-glycerol | ~12% | ~1.50 | 120 mg glycerol + 880 µL water |
| High-glycerol | ~23% | ~2.05 | 230 mg glycerol + 770 µL water |

> **Protocol note — always weigh glycerol by mass, not volume.** Glycerol is extremely viscous and clings to pipette walls; volume pipetting introduces large errors. Tare a Jar and put small tube inside it, add glycerol by mass (Used a small scalple to take small portions of GLyecerol and add it) on the analytical balance, then add water by pipette.

**Nathan's Revised Concentration Targets (Cheng 2008 Calculator):**

After using the Cheng (2008) online calculator, Nathan revised the glycerol concentrations to achieve a wider viscosity spread (up to 4× rather than 2×). His two glycerol conditions target η = 2.0532 mPa·s and η = 4.1064 mPa·s — the corresponding mass fractions are shown in his notebook:

> **[📷 INSERT IMAGE — Nathan's Notebook, p.1: Cheng (2008) calculator results — glycerol mass fractions for G1 and G2 targets]**
> *Source: Page 1, left column — "From calculator:" section*

> **Note on discrepancy:** Nathan's G2 condition uses ~36% glycerol (η ≈ 4.11 mPa·s), which is more ambitious than our originally planned ~23% (η ≈ 2.05 mPa·s). This doubles the viscosity range. The Session 6 prep should follow Nathan's calculator-confirmed percentages; the table above reflects the original plan and will be updated before Session 6.

**Nathan's Dilution Calculations per Bead Size (corrected for 82.5 µm chamber depth):**

Nathan reworked the bead count calculations using the corrected chamber depth of 82.5 µm. His full derivation for 5 µm, 3 µm, and 1 µm beads (including mass per bead, number density, and dilution factors) is shown in his notebook:

> **[📷 INSERT IMAGE — Nathan's Notebook, p.1: Dilution calculations — 5 µm, 3 µm, and 1 µm beads with 82.5 µm chamber depth correction]**
> *Source: Page 1, left column — "Dilution calculation with glycerol..." sections*

> **Key conclusion from Nathan's calculations:** For 3 µm beads targeting 10 beads/FOV with 82.5 µm depth, the required dilution is approximately **20.4× of 0.5% stock (4.90%)** — consistent with the 4.9% dilution found experimentally in Section 10 below.

### 7.3 Predicted D Values — Stokes-Einstein at T = 292 K

$$D = \frac{k_B T}{6\pi\eta r}, \quad k_BT = 1.381\times10^{-23} \times 292 = 4.03\times10^{-21}\ \text{J}$$

| Bead diameter | Radius r | η = 1.03 mPa·s (0%) | η = 1.50 mPa·s (~12%) | η = 2.05 mPa·s (~23%) |
|--------------|---------|----------------------|------------------------|------------------------|
| 1 µm | 0.50 µm | **0.416 µm²/s** | 0.286 µm²/s | 0.209 µm²/s |
| 2.1 µm | 1.05 µm | **0.198 µm²/s** | 0.136 µm²/s | 0.100 µm²/s |
| 3 µm | 1.50 µm | **0.139 µm²/s** | 0.095 µm²/s | 0.070 µm²/s |
| 5 µm | 2.50 µm | **0.083 µm²/s** | 0.057 µm²/s | 0.042 µm²/s |

This gives a clean ~10× range in D across all conditions (0.416 down to 0.042 µm²/s) — an excellent spread for testing Stokes-Einstein scaling with both η and r.

> **Key observation for the report:** The viscosity range (0–23% glycerol) changes D by ~2×. The bead size range (1–5 µm) changes D by ~5×. Together, the full matrix spans nearly a 10× range — a rigorous test of the D ∝ 1/(η·r) prediction.

### 7.4 Expected Bead Count per Field of View

Before collecting data we need to know: at 0.5% by weight stock, how many beads will we see in the FOV? Too few → poor statistics; too many → overlapping tracks.

**FOV at 100× (calibrated):**

- Sensor: 1440 × 1080 px at 68.7 nm/px
- FOV = (1440 × 0.0687 µm) × (1080 × 0.0687 µm) = **98.9 µm × 74.2 µm = 7338 µm²**

*(Note: the effective imaging area used for tracking is typically the central ~50% = ~3669 µm², but the full FOV is used here for the count estimate.)*

**Number density at 0.5% by weight stock:**

For a sphere of radius r and density ρ_PS = 1.05 g/cm³, the mass of one bead is:

m_bead = ρ_PS × (4/3)π r³

Number of beads per gram of suspension:

N/g = 0.005 / m_bead

Number density (beads/µm³):

n = (N/g) / (V_water/m_water) = 0.005 / [ρ_PS × (4/3)π r³ × (0.995/ρ_water)]

Calculated for each bead size at 0.5% stock:

| Bead diameter | r (µm) | n (beads/µm³) | N_FOV (1 µm depth) | N_FOV (80 µm depth) |
|--------------|--------|----------------|---------------------|----------------------|
| 1 µm | 0.50 | 9.14 × 10⁻³ | ~67 | **too many** |
| 2.1 µm | 1.05 | 0.98 × 10⁻³ | ~7 | ~580 (too many) |
| 3 µm | 1.50 | 0.34 × 10⁻³ | ~2.5 | ~200 |
| 5 µm | 2.50 | 0.073 × 10⁻³ | ~0.5 | ~40 |

> **Key finding:** At 0.5% stock, 1 µm and 2.1 µm beads are far too concentrated for the full 80 µm chamber. Even 3 µm beads fill the FOV at full stock. We need to **dilute** the 0.5% stock before use. The 5 µm beads at 0.5% give approximately 40 beads in the full chamber depth — workable.

We will need to determine the correct dilution factor experimentally by test imaging, which is the purpose of Procedures B and C below.

### 7.5 Concentration Effects on Suspension Viscosity (Nathan's Prelab)

At higher bead concentrations, the beads themselves increase the effective viscosity of the suspension beyond that of the pure fluid — reducing the measured D relative to the Stokes-Einstein prediction for pure water or glycerol. Nathan's prelab covers two models for this effect:

**Einstein's Viscosity Equation (dilute suspension):**

$$\eta = \eta_0\,(1 + 2.5\phi)$$

where $\eta_0$ is the pure-fluid viscosity and $\phi$ is the particle volume fraction. For higher concentrations, the **Batchelor equation** adds a second-order term:

$$\eta = \eta_0\,(1 + 2.5\phi + 6.2\phi^2)$$

The volume fraction is:

$$\phi = \frac{V_\text{bead} \cdot n_\text{bead}}{V_\text{solution}}$$

> **[📷 INSERT IMAGE — Nathan's Notebook, p.2: Einstein viscosity equation and Batchelor equation with φ definition]**
> *Source: Page 2, left column — "Einstines Viscosity Equation (for suspension)" section*

**Practical implication for our experiment:** At our working dilution (~4.9% of 0.5% stock), φ is very small and the Einstein correction is negligible. However, this is theoretical support for why **Trail 1** (sparse, ~10 beads) should yield a purer Brownian D than **Trail 2** (dense, ~20–40 beads) — the denser region has a higher φ, increasing effective η and potentially biasing D downward (complementing the Fickian drift argument in Section 10.5).

> **Concentration should be chosen where particles do not clump or fuse** so that fused-particle radius effects can be ignored (Nathan's note).

### 7.6 Wall Interactions — Faxén's Law (Nathan's Prelab)

When a bead diffuses close to the chamber wall, hydrodynamic drag increases due to fluid shearing between the bead surface and the wall. This reduces the apparent diffusion coefficient. The correction is given by **Faxén's Law** for parallel diffusion:

$$D_\parallel = D_0 \cdot \left[1 - \frac{9}{16}\left(\frac{R}{h}\right) + \frac{1}{8}\left(\frac{R}{h}\right)^3 - \frac{45}{256}\left(\frac{R}{h}\right)^4 - \frac{1}{16}\left(\frac{R}{h}\right)^5 \cdots\right]$$

where $R$ is the bead radius and $h$ is the distance from the bead centre to the nearest wall.

> **[📷 INSERT IMAGE — Nathan's Notebook, p.2: Faxén's Law equation and wall interaction analysis]**
> *Source: Page 2, left column — "Wall Interactions: Use Faxén's Laws" section*

**Estimated wall correction for our setup:**

- Chamber depth: ~82.5 µm (tape spacer)
- Largest bead: 5 µm (R = 2.5 µm)
- Nathan's calculation: for a 5 µm bead with its centre ~5 radii from the wall ($h = 5R = 12.5\ \mu\text{m}$, so $R/h = 0.2$), $D_\parallel \approx D_0 \times (1 - 0.114) = 0.886\,D_0$

→ **~11% reduction in D** at this moderate proximity. At truly maximum proximity ($R/h \to 1$, bead touching the wall) the series does not converge and the correction is far larger. For 1 µm and 3 µm beads the correction is much smaller ($R/h \ll 1$ for beads in mid-chamber).

**Practical implication:** During MSD analysis in Session 6, beads that hug the chamber floor or ceiling should be excluded or flagged — they will show anomalously low D. Tracks analysed from the mid-chamber plane (the in-focus plane) are largely unaffected by the wall correction.

---

## 8. PROCEDURE A: SAMPLE PREPARATION

*Time: ~2:30 PM*

### 8.1 Glycerol Solution Preparation

**Protocol — 20% glycerol test batch (qualitative first test):**

1. Tare a clean 1.5 mL microcentrifuge tube on the analytical balance
2. Add **200 mg glycerol** directly from stock bottle (by mass — do not pipette)
3. Add **800 µL deionised water** by pipette — mix thoroughly by vortexing
4. Result: 20% glycerol by mass (η ≈ 1.76 mPa·s at 20°C — intermediate)
5. Add **50 µL of 0.5% bead stock** to **950 µL of the glycerol solution**
6. Mix gently — do not vortex beads (creates bubbles)
7. Final bead concentration: **~0.025% by weight** (50 µL stock into 1000 µL total = 5% of the 0.5% stock; a 20× dilution)

> **Why 20% for the first test?** We chose 20% glycerol (rather than the final 23%) as a qualitative check — it is viscous enough to clearly slow bead diffusion relative to water, making the effect easy to see by eye. The exact viscosity does not matter for this qualitative batch.

> **Note:** No separate file was saved for the glycerol solution preparation itself. The video of beads in this solution is recorded in Section 9 below.

### 8.2 Slide Preparation (Thick Chamber)

Refer to **Protocol: Making Sample Chambers** (MM-LabScript-microscopy.pdf, Section 2.4) for the full step-by-step procedure.


> **Chamber depth Reconsiderations:** We found online the tape spacer used in our chambers today. Height = **80 µm**. This is important for calculating the observation volume and predicted bead counts. Previous sessions used this same tape but the depth had not been explicitly measured until today.

---

## 9. PROCEDURE B: QUALITATIVE TEST — 5 µm BEADS IN 20% GLYCEROL

*Time: ~2:45 PM*

Purpose: Verify that 5 µm beads are visible and countable in a glycerol-water mixture before committing to full data collection.

### 9.1 Acquisition Settings — First Attempt

| Setting | Target | Actual |
|---------|--------|--------|
| Objective | 100× oil | 100× oil |
| Frame rate | 200 fps | **66.019 fps** |
| Burst count | 1000 frames | 1000 frames |
| Result | — | Too fast for slow beads; lowered to 1 fps |

> **Observation:** No visible difference was apparent in the 1000-frame burst at 66 fps — the beads appeared nearly stationary between frames, confirming that this frame rate far exceeds what is needed for slowly diffusing 5 µm beads in glycerol.

> **Note on frame rate:** NI Vision Assistant capped acquisition at 66.019 fps even when 200 fps was requested — likely limited by USB transfer bandwidth for the FLIR BlackFly at 1440×1080. For slow-diffusing 5 µm beads in glycerol (D ≈ 0.05–0.08 µm²/s), a high frame rate captures many steps but each step is tiny (~0.01–0.02 µm per frame at 66 fps) — harder to detect above noise. We reverted to **1 fps** for this sample, consistent with previous sessions.

### 9.2 Observations

| Feature | Observation |
|---------|-------------|
| Beads visible? | Yes — small, high-contrast spheres |
| Count in FOV | 2–3 particles total |
| In focus | ~2 beads clearly in focus |
| Out of focus | ~2 beads visible but blurred (deeper in chamber) |
| Clumping | Some — 1 aggregate observed |
| Motility | Slow Brownian jitter visible — qualitatively slower than water |

**Comparison to predicted count:**

Predicted n for 5 µm at 0.5% stock: 7.25 × 10⁻⁵ beads/µm³

N_FOV (80 µm chamber) = 7.25 × 10⁻⁵ × 7338 × 80 ≈ **42 beads**

Observed only 2–3 in focus. Initial hypothesis for the discrepancy: **gravitational settling** — 5 µm polystyrene beads are larger and denser than 1 µm beads and more susceptible to sedimentation toward the chamber floor, depleting the mid-chamber imaging plane. This was tested by returning the sample tube to the rack and inspecting the solution: the suspension was **well mixed with no visible settling layer**. Settling was therefore **ruled out**.

The correct explanation is **focal depth**: at 100× oil immersion, the depth of field is approximately 1–2 µm — only a thin optical slice of the 80 µm chamber is in sharp focus at any given z-position. The camera captures only beads within that narrow plane.

Revised estimate using 2 µm focal depth:

N_FOV (2 µm depth) = 7.25 × 10⁻⁵ × 7338 × 2 ≈ **~1 bead**

Observed 2–3 in focus → **broadly consistent** when accounting for focal depth and some local concentration variation.

> **CONCLUSION:** 5 µm beads at 0.5% stock in 20% glycerol are visible and trackable, though count is low. For quantitative data collection, we should use **undiluted 0.5% stock** and select regions where beads are in focus. Viability: **Good — proceed to Session 6.**

---

## 10. PROCEDURE C: CONCENTRATION INVESTIGATION — 3 µm BEADS IN WATER

*Time: ~3:30 PM*

Purpose: Find the correct dilution of 3 µm bead stock to give ~10–20 beads per FOV for tracking.

### 10.1 Test 1 — High Stock Concentration (80% of 0.5% Stock)

**Sample:** ~80% of 0.5% stock → effectively ~0.4% by weight 3 µm beads in pure water.

**Observation:** The entire FOV was packed with beads — approximately **200 beads** visible. Beads were so close together that tracking was impossible; many were touching or overlapping.

**Frame rate:** 30 fps (set via Vision Assistant)

**File saved:** `Data/24-Feb/3um-0_5p-0pgky-test-1brustcount.avi`

> **Conclusion:** 0.4–0.5% stock is far too concentrated for 3 µm beads. Need significant dilution.

### 10.2 Test 2 — Diluted Stock (4.9% of 0.5% Stock, 0% Glycerol)

**Sample:** 4.9% of 0.5% stock → effectively ~0.024% by weight 3 µm beads in pure water.

Preparation: 4.9 µL of 0.5% stock + 95.1 µL water → 100 µL total at 4.9% dilution.

**Observation:** ~10 beads visible in a selected region of the slide. Concentration was still uneven across the slide (beads tend to accumulate at chamber edges), but a central region with ~10 beads was identified and used for acquisition.

**Frame rate:** 30 fps

**File saved:** `Data/24-Feb/3um-0_5p-4_9pstock-0pGly-trail1.avi`

> **CONCLUSION:** 4.9% of 0.5% stock gives approximately 10 beads in a well-chosen FOV region — a trackable density. Some concentration variation across the slide is normal. **For Session 6, we will use this dilution factor as the starting point for 3 µm beads.**

### 10.3 Summary of Concentration Findings

| Bead size | Recommended stock dilution | Expected beads in FOV | Notes |
|-----------|---------------------------|----------------------|-------|
| 1 µm | ~1:50 dilution of 0.5% stock | ~10–20 | High natural density; needs large dilution |
| 3 µm | ~5% of 0.5% stock (1:20) | ~10 | Confirmed today |
| 5 µm | Undiluted 0.5% stock | ~2–4 in focus | Gravity settling negligible; focal depth limits count |

### 10.4 Trail 2 — Dense Region of Same Slide

**Purpose:** Collect a second acquisition from a visibly denser region of the same non-uniform slide to enable a direct experimental test of the concentration uniformity hypothesis (see Section 10.5).

**Method:** Without preparing a new slide, the stage was translated to a region of the same chamber that showed a clearly higher bead density. All acquisition settings were identical to Trail 1: 30 fps, 4.9% of 0.5% stock, 0% glycerol.

**Approximate bead count in FOV:** Visibly higher than Trail 1 — estimated 20–40 beads in the selected region.

**File saved:** `Data/24-Feb/3um-0_5p-4_9pstock-0pGly-trail2.avi`

### 10.5 Discussion: Concentration Uniformity Hypothesis

The non-uniform bead distribution observed in the 4.9% diluted sample prompted a scientific disagreement about whether it is valid to collect Brownian motion data from a non-homogeneous slide by simply selecting a region with the desired density.

**Nathan's position:** A region of the non-uniform slide containing ~10 beads in the FOV is physically equivalent to a true uniform sample at that concentration. In a perfectly uniform sample of the same bulk density, any chosen FOV would also show approximately 10 beads per field. Since Brownian motion of each particle is governed by its immediate neighbours — and at these separations inter-particle forces are negligible — the local dynamics should be identical. The macroscopic distribution of beads across the rest of the chamber is irrelevant to the physics within the FOV.

**Ahilan's counter-argument:** The local bead density may be the same, but the *time evolution* of the particle positions is not equivalent. In the non-uniform slide, a macroscopic concentration gradient exists across the chamber. This gradient drives **Fickian drift**: a net diffusive flux $J = -D\,\nabla c$ directed from the dense region toward the sparse region. Every bead in a high-concentration zone has a statistical bias toward the low-concentration side, superimposed on its random Brownian jitter. In a true uniform sample, the gradient is zero and there is no net flux. The observed trajectories in the dense region are therefore systematically biased — yielding an apparent D that conflates true Brownian diffusion with directed concentration-driven drift. The underlying physics of the two situations is distinct, and the non-uniform sample cannot be treated as an exact substitute for a uniform one.

**Experimental test:** Rather than resolving this theoretically, we opted to test it empirically. Trail 1 (sparse region, ~10 beads) and Trail 2 (dense region, ~20–40 beads) were collected from the same slide under identical acquisition conditions. If Nathan is correct, MSD analysis of both trails should yield the same diffusion coefficient D. If the Fickian drift effect is significant, D from the Trail 2 dense region should be systematically higher than D from Trail 1.

> **Prediction (Ahilan):** D(Trail 2) > D(Trail 1) — net drift toward the low-concentration end of the chamber inflates the apparent MSD slope.
> **Prediction (Nathan):** D(Trail 1) ≈ D(Trail 2) — local Brownian physics is independent of the macroscopic concentration gradient.

### 10.6 Preliminary Analysis (Pending)

*MSD analysis of Trail 1 and Trail 2 will be performed during the inter-session period before Session 6, using the corrected diffusion analysis pipeline (`Analysis/Diffusion_Analysis_Corrected.ipynb`). The measured D values from both trails will be compared, and the result of the hypothesis test will be recorded here and incorporated into the Session 6 notebook.*

---

## 11. CONCLUSIONS

### 11.1 Summary of Session 5 Findings

1. **Calibration:** 68.7 nm/px confirmed. Consistent with all previous sessions.

2. **Viscosity model:** Refutas method (ASTM D341) agreed on for report. Cross-checked against Cheng (2008) published tables. Three glycerol concentrations chosen: 0%, ~12%, ~23% (giving η = 1.03, 1.50, 2.05 mPa·s at 19°C).

3. **Predicted D values:** Calculated for all four bead sizes across all three viscosity conditions. Full 2D matrix spans ~10× range in D — sufficient to test Stokes-Einstein scaling with both η and r.

4. **Chamber depth measured:** Tape spacer = **80 µm**. Used to correct bead count predictions.

5. **Concentration issue resolved for 3 µm beads:** 0.5% stock is ~20× too concentrated. 4.9% of stock gives ~10 beads in a trackable FOV region.

6. **5 µm beads in 20% glycerol:** 2–3 beads visible and in focus — workable for tracking. Will use undiluted 0.5% stock in Session 6.

7. **Frame rate:** NI Vision Assistant caps at ~66 fps (not 200 fps as intended) at full resolution. For slow-diffusing beads at 30 fps, each frame captures meaningful displacement. Confirmed 30 fps as the working frame rate for 3 µm and 5 µm beads.

8. **Concentration uniformity hypothesis test:** The 4.9% diluted sample was not uniformly distributed. A debate between Nathan (non-uniform region ≡ uniform sample locally) and Ahilan (Fickian drift from concentration gradient biases trajectories) was resolved by collecting Trail 1 (sparse region) and Trail 2 (dense region) for empirical comparison. Analysis pending.

### 11.2 Comparison to Pre-Lab Predictions

| Prediction | Actual | Status |
|------------|--------|--------|
| 5 µm beads: ~40 in FOV (80 µm chamber) | ~2–3 in focus | Expected — focal depth limits imaging to ~1–2 µm of 80 µm chamber (settling ruled out) |
| 3 µm beads at 0.5% stock: ~200 in FOV | ~200 confirmed | CORRECT |
| 3 µm at 4.9% stock: ~10 in FOV | ~10 confirmed | CORRECT |
| D_predicted (1 µm, water): 0.416 µm²/s | Not yet tested | Session 6 |
| Camera frame rate: 200 fps | 66 fps max | Hardware limit — use 30 fps instead |

---

## 12. PLAN FOR SESSION 6

**Session 6 is the primary data collection session for the report.**

### 12.1 Data Collection Matrix

**Our original 9-set matrix (3 per variable):**

| Variable tested | Condition 1 | Condition 2 | Condition 3 |
|----------------|-------------|-------------|-------------|
| **Viscosity** (1 µm bead) | 0% glycerol | ~12% glycerol | ~23% glycerol |
| **Bead size** (0% glycerol) | 1 µm | 3 µm | 5 µm |
| **Concentration check** (3 µm, 0% glycerol) | ~5% stock | ~10% stock | ~20% stock |

For each condition: ideally 2 trials. Start with 1 trial each, run a quick MSD check in Python to confirm quality before running the second trial.

---

**Nathan's Revised 7-Slide Plan (from his prelab):**

Nathan restructured the collection plan into 7 explicit slides, using his Cheng (2008) calculator values (20% and 36% glycerol) and including explicit concentration variation slides. His full target-slides table and dilution factor table are shown below:

> **[📷 INSERT IMAGE — Nathan's Notebook, p.2: Target slides table (7 slides × mix/visc/bead/conc) and dilution factors table]**
> *Source: Page 2, left column — "Target slides:" and "Dilution factors:" tables*

| Slide | Glycerol (%) | Bead Size | Target Beads/FOV | Purpose |
|-------|-------------|-----------|-----------------|---------|
| 1 | 0% | 3 µm | 10 | Bead size baseline (water) |
| 2 | 20% | 1 µm | 10 | Viscosity + size: 1 µm |
| 3 | 20% | 3 µm | 10 | Viscosity main: 3 µm |
| 4 | 20% | 5 µm | 10 | Viscosity + size: 5 µm |
| 5 | 20% | 3 µm | 5 | Concentration low |
| 6 | 20% | 3 µm | 20 | Concentration high |
| 7 | 36% | 3 µm | 10 | Viscosity high: 3 µm |

> **Note on plan reconciliation:** Nathan's plan uses 20% and 36% glycerol (η ≈ 2.05 and 4.11 mPa·s) rather than our original ~12% and ~23%. The 36% condition gives a 4× viscosity range — broader and more compelling for the D vs η plot. **Before Session 6, Nathan and Ahilan should agree on the final glycerol percentages and confirm dilution factors for slides 2–7.**

> Dilution factors from Nathan's prelab: Slide 1 confirmed at 4.90% of 0.5% stock (20.4× dilution). Slides 2–7 calculations are in Nathan's notebook — see image above.

### 12.2 Sample Preparation Protocol for Session 6

**Glycerol solutions (prepare at start of session):**
- 0%: pure deionised water
- ~12%: 120 mg glycerol + 880 µL water (by mass on analytical balance)
- ~23%: 230 mg glycerol + 770 µL water (by mass)

**Bead dilutions:**
- 1 µm: ~1% of 0.5% stock in the target fluid
- 3 µm: ~5% of 0.5% stock in the target fluid
- 5 µm: undiluted 0.5% stock

**Frame rates:**
- 1 µm beads: 30 fps (fast diffusion, need short time steps)
- 3 µm beads: 30 fps
- 5 µm beads: 1–5 fps (slow diffusion, don't need high time resolution)

**Duration:** 120–240 frames per video (4–8 seconds at 30 fps)

### 12.3 Qualitative Project — Yeast (Session 6)

If time allows after bead data collection:
1. Prepare plain yeast slide (yeast in water — Brownian baseline, α ≈ 1)
2. Prepare yeast + sugar gradient slide (deposit a small amount of glucose at one end of the chamber, add yeast)
3. Observe whether yeast trajectories show directional bias toward the sugar
4. Compare trajectory plots and MSD exponents (α) between the two conditions

### 12.4 Items to Confirm Before Session 6

- [ ] Acetone available from lab technician? (low-viscosity condition)
- [ ] Nathan's mathematical model of D vs η, r, and concentration ready
- [ ] Python MSD analysis notebook ready to run on the day
- [ ] Yeast culture fresh (ask TA to prepare)

---

## 13. POST-LAB REFLECTIONS

**Goal Review:**

| Goal | Status |
|------|--------|
| 1. Agree on viscosity model (Refutas method) | DONE |
| 2. Calculate expected D values for all conditions | DONE — full table recorded in Sec. 7.3 |
| 3. Calculate expected bead counts per FOV | DONE — table in Sec. 7.4 |
| 4. Qualitative test batch (5 µm + 20% glycerol) | DONE — 2–3 beads visible, workable |
| 5. Concentration investigation for 3 µm beads | DONE — 4.9% stock gives ~10 beads |
| 6. Save at least one trial dataset | DONE — Trail 1 and Trail 2 collected (see Sec. 10.4–10.6) |
| 7. Finalise plan for Session 6 | DONE — full matrix and protocols in Sec. 12 |

**What worked well:**
- Starting with a qualitative test batch before committing to full data collection was the right call — it revealed the concentration problem before wasting lab time on unusable data.
- The Refutas method + Cheng (2008) tables give consistent predictions — we now have theoretical D values for every condition we plan to test.
- Measuring the tape spacer depth (80 µm) resolved the apparent discrepancy between our bead count predictions and observations.

**What didn't work and surprises:**
- The camera frame rate capped at 66 fps rather than 200 fps — NI Vision Assistant is bandwidth-limited at full 1440×1080 resolution. For slow beads this is fine (30 fps is sufficient); for future fast-bead work, consider reducing resolution.
- 0.5% stock at full concentration for 3 µm beads gave ~200 beads in FOV — completely unusable. This was predictable from the calculation, but seeing it experimentally confirmed the theory.
- Glycerol is harder to work with than anticipated. It is extremely viscous — it clings to pipette walls and drips slowly. Weighing by mass on the balance (rather than pipetting by volume) is essential for accuracy.

**What I would do differently:**
- Prepare all glycerol solutions at the start of the session, before even touching the microscope — they need several minutes of mixing.
- Have the Python analysis notebook open and ready on the lab computer to check MSD quality in real time.
- Bring the concentration calculation table to the lab on paper (not just in the notebook) so it's easy to reference during sample prep.

**Inter-lab period work (between Sessions 4 and 5):**
- Reviewed Cheng (2008) paper for glycerol-water viscosity data at low concentrations
- Nathan prepared the Refutas viscosity blending model and expected D value calculations
- Drafted the 9-dataset collection matrix (3 per variable)
- Reviewed Python MSD analysis pipeline from Session 1–2 analysis

---

## 14. DATA FILES CREATED

All files in: `Lab2-Microscopy-and-Motility/Data/24-Feb/`

| Category | Filename | Description |
|----------|----------|-------------|
| 5 µm test | `5um-0_5p-20pGly-qual-test.avi` | 5 µm beads in 20% glycerol, 1 fps, qualitative test |
| 3 µm burst test | `3um-0_5p-0pgky-test-1brustcount.avi` | 80% of 0.5% stock, 30 fps — too concentrated (~200 beads) |
| 3 µm Trail 1 | `3um-0_5p-4_9pstock-0pGly-trail1.avi` | 4.9% stock, sparse region, 30 fps — ~10 beads, usable |
| 3 µm Trail 2 | `3um-0_5p-4_9pstock-0pGly-trail2.avi` | 4.9% stock, dense region, 30 fps — ~20–40 beads (uniformity test) |

**Analysis notebooks:**
- `Analysis/Diffusion_Analysis_Corrected.ipynb` — to be updated with Session 5 trial data
- `Analysis/track_onion_particles.py` — adapted for bead tracking pipeline



SUS ERROR? 

Notebook fact-check — 2 errors corrected:

Section	Error	Fix
8.1	"Final bead concentration: ~0.5% by weight"	Corrected to ~0.025% — 50 µL into 1000 µL = 5% of stock = 0.025% actual bead concentration (was 20× too high)
7.6	"at maximum wall proximity" gives 11% reduction	Corrected — 11% corresponds to R/h = 0.2 (bead centre 5 radii from wall, h = 12.5 µm), not maximum proximity. True maximum would give a far larger correction.