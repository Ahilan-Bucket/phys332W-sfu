# Lab [2] Session [8] — M&M: Final Data Collection and Understanding where we are at

**Date:** 3 Mar 2026
**Lab Partner:** Nathan Unhrn
**Recorder:** Ahilan Kumaresan

**SESSION FOCUS:** 

**Repository:** [github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab2-Microscopy-and-Motility)

**Google Drive (full AVI dataset):** [drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9](https://drive.google.com/drive/folders/1YohMY9cfBztTLWQlAUtM3DVpDo0R6Tf9?usp=sharing)


---

## 1. GOALS
1. Final Explorations for the Lab
2. Work on the Figures Assignment for Next Assignment
3. Work on making all tracker Data
4. Work on Notebook completion and Executive Submission
5. Correct the Code for the new Tracker Data. Much more Accurate. 



**Expanded Session 8 targets:**


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

**Additional Items for Session 8:**

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

---

## 6. BACKGROUND: THEORY REVIEW (10-15 min)

*Spent the initial 10-15 minutes reviewing the theoretical framework before collecting data.*

### Measure Room Temperature and the temperature of a water on the Microscope, saw no big difference

### 6.3 Wall Interaction Correction (Faxen's Laws)
Nathan was saying how the Faxen Law's Calcualtion actually has an error

---

### Code review and things to change:

MSD
The fitting line is only for the start of the points for some reason, not fot the entire Data points. 
- From theory we msut have the first Data point on Zero. In our plot we for soem reaosn have some offset
To solve this issue I am not sure if we neeed to take the intercept and force it to zero? 
The current MSD fit uses MSD = slope*t + intercept (free intercept), which produces a non-physical offset at τ=0. This will be changed to MSD = slope*t (forced through origin)?? Is that ok?

Error Bars
- Explore if I want to do both error bars and also take up the model that is closest to one of the methods. 


- We are only plotting the 25% of Data, why? If you tried to fit 100% of your data, your $D$ value would likely be wrong because the "tail" of your graph—which is just random noise—would tilt the slope of your fit line. By cutting it off at 25%, you ensure that the math is driven by the most "certain" data you have.

- I am working on making the figures more accurate with the right labels, titles , and accurate scales for professional presentation (Done)


### Nathan wanted to do a Tracker Approach, were working on that to see how that worlks and see if we have bettter accurate Data. 

- 2:39 Pm 
So currnelty making a new code that can do the analysis from these new Tarcker Data. 




In Lab TO do list:
1. Input the "D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Data\2026-03-05\Diffusion Coefficient formulas.pdf" to get the new formulas. Use this as the basis for therotial values. 

- With this, and maybe error propogation? , and the differece between our most accurate model and thoerical, models for the error from Fauxen and others, use this for error bars


3. Lab Notebook - Finish the Results today, Analysis. With all Requiments

2. Make final Code with ("Presentation Argument for the Presentationa plots") and get the final Code for the Pipeline. Use this for Neat Figures


4. Make the formal Report. 



---



