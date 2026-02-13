Lab 2: Microscopy and Cell Motility
====================================

PHYS 332W Advanced Physics Laboratory
Simon Fraser University, Spring 2026

Project: Brownian Motion, Diffusion Analysis, and Cell Motility
Duration: Sessions 1-6 (Feb 2026)

Collaborators:
  - Ahilan Kumaresan (Recorder, Sessions 1-4)
  - Nathan Unhrn (Lab Partner)

Instructor: PHYS 332W Teaching Team
Lab Location: SFU Physics Teaching Lab

====================================
PROJECT DESCRIPTION
====================================

This experiment investigates the physics of microscopic motion using
bright-field microscopy. The primary goals are:

1. Calibrate the microscope camera and establish pixel-to-physical
   unit conversion (nm/px)
2. Measure Brownian motion of polystyrene beads (1 um and 5 um)
3. Extract diffusion coefficients from particle tracking data using
   three methods: variance, Gaussian fitting, and MSD analysis
4. Compare measured D to Stokes-Einstein prediction
5. Observe and characterize biological cell motion (yeast, HT1080,
   pond water organisms, onion cell streaming)
6. Distinguish Brownian diffusion from active/directed transport
7. Select and execute a short project on cell motility

====================================
KEY RESULTS
====================================

Calibration:
  Session 1 (03 Feb): 68.45 nm/px (100x oil immersion) -- REFERENCE
  Session 2 (05 Feb): 345 nm/px -- ERROR (wrong calibration procedure)
  Session 3 (10 Feb): 68.4 nm/px -- CONFIRMED (matches Session 1)
  Session 4 (12 Feb): 68.7 nm/px -- CONFIRMED (condenser adjusted)

Diffusion Coefficients (CORRECTED at 68.4 nm/px):
  1.0 um beads: D = 0.507 +/- 0.008 um^2/s (theory: 0.441 um^2/s)
  5.0 um beads: D = 0.148 +/- 0.006 um^2/s (theory: 0.088 um^2/s)

  The Session 2 analysis used the WRONG pixel size (345 nm/px = 5.04x
  too large). Since D scales as pixel_size^2, all D values were
  inflated by 25.4x. The corrected analysis (Diffusion_Analysis_Corrected.ipynb)
  shows agreement within 15% for 1 um beads.

Onion Cell Streaming (Session 4):
  MSD exponent alpha = 1.662 +/- 0.052 (superdiffusive)
  Mean streaming speed = 0.023 +/- 0.007 um/s
  D_eff = 0.000623 +/- 0.000038 um^2/s
  Directed cytoplasmic transport along actin filaments + random fluctuations.

Selected Short Project (Sessions 5-6):
  Bead Diffusion -- varied viscosities (glycerol) and bead sizes (1, 5 um)
  to systematically verify Stokes-Einstein relation.

====================================
DIRECTORY STRUCTURE
====================================

Lab2-Microscopy-and-Motility/
|
|-- README.txt              This file
|
|-- Analysis/               Analysis scripts and outputs
|   |-- Diffusion_Analysis.ipynb           Original analysis (WRONG pixel size)
|   |-- Diffusion_Analysis_Corrected.ipynb Corrected analysis (68.4 nm/px)
|   |-- brownian_motion_analysis.ipynb     Alternative analysis script
|   |-- MTrack2Loader-fixed.ipynb          Track data loading/processing
|   |-- Onion_Cell_Analysis.ipynb          Onion streaming MSD analysis
|   |-- track_onion_particles.py           Custom Python particle tracker
|   |-- trackresults.txt                   Raw MTrack2 tracking data
|   |-- figures/                           Exported publication-quality figures
|
|-- Data/                   Raw experimental data
|   |-- 2026-02-03/         Session 1 (calibration + 1 um beads)
|   |-- 2026-02-05/         Session 2 (recalibration + 1 um & 5 um beads)
|   |-- 10-Feb/             Session 3 (live cells, pond water, yeast, HT1080)
|   |-- 12-Feb/             Session 4 (onion streaming, pond water incubation)
|
|-- Drafts/                 Submission documents and old drafts
|   |-- Lab2-Submission-Brief-Sessions1-2.tex   Week 1-2 submission (LaTeX)
|   |-- Lab2-Submission-Brief-Sessions3-4.tex   Week 3-4 submission (LaTeX)
|   |-- W2-Submission-Brief-Sessions1-2.pdf     Rendered submission PDF
|   |-- W3-Submission-Brief-Sessions3-4.pdf     Rendered submission PDF
|   |-- Lab2-Session3-Notebook-Scan.pdf         Session 3 handwritten scan
|   |-- Prelab-Lab2.pdf                         Pre-lab questions
|
|-- Notes/                  Photos, sketches, references
|   |-- Lab2-Session3-Notebook.md           Session 3 notebook (markdown)
|   |-- Lab2-Session4-Notebook.md           Session 4 notebook (markdown)
|   |-- microscope-setup-photo-03Feb.png    Lab setup photo
|   |-- References/                         Protocol PDFs and lab scripts
|
|-- Lab2-Sessions1-2-Notebook-Scan.pdf  Sessions 1-2 full notebook scan
|-- Lab2-Session1-Notebook-Scan.pdf     Session 1 notebook scan

====================================
CALIBRATION NOTE
====================================

The pixel calibration is CRITICAL for this experiment.

CORRECT value: 68.4-68.7 nm/px (0.0684 um/px) at 100x oil immersion.
Measured using a stage micrometer with 10 um divisions (0.01 mm/line).
Confirmed independently in Sessions 1 (68.45), 3 (68.4), and 4 (68.7 nm/px).

Session 2 incorrectly used 345 nm/px (0.345 um/px), which was a
5.04x error. Since D = <dx^2> * pixel_size^2 / (2*dt), D scales
as pixel_size^2. This inflated ALL diffusion coefficients by
(345/68.4)^2 = 25.4x, explaining the 20-40x discrepancy with
Stokes-Einstein theory reported in the original analysis.

====================================
REQUIREMENTS
====================================

Software:
  - Python 3.12
  - Jupyter Lab or Notebook
  - NumPy, SciPy, Matplotlib (standard scientific Python)
  - ImageJ/Fiji with MTrack2 plugin (for particle tracking)
  - NI Vision Assistant (for image/video acquisition)

Hardware:
  - Olympus BX51 upright microscope
  - FLIR BlackFly U3-13Y3M camera (1440 x 1080 px)
  - 10x, 40x, 100x oil immersion objectives
  - Stage micrometer (1 mm / 100 divisions)

====================================
WORKFLOW NOTES (for future sessions)
====================================

Notebook Generation Pipeline:
  1. Write lab content in markdown (.md) -- one file per session
  2. Use generate_notebook_v2.py (PageWriter) to render into .docx
     with floating OOXML textboxes over ruled-line backgrounds
  3. Custom font "Ahilan 2" embedded for handwritten appearance
  4. Edit on iPad: paste images into placeholders, fill in CC markers
  5. Use insert_session4.py to merge sessions into single .docx
  6. Use add_toc.py to insert Table of Contents pages
  7. Submission brief: write .tex, compile to PDF

Key Lessons Learned:
  - NEVER regenerate the full .docx after images are pasted -- this
    destroys image relationships. Instead, surgically edit the XML
    or use insert_session4.py to replace only one session's textboxes.
  - PageWriter appends textboxes to the END of the doc body; must
    move them to the correct position if inserting mid-document.
  - Session boundary detection: search for "Session [N]" title text
    in textboxes, NOT keyword matching (keywords can appear in
    multiple sessions and cause wrong boundary detection).
  - Calibration verification takes 5 minutes -- do it EVERY session.
  - For pond water: collection technique matters more than incubation
    time. Draw from near visible masses/chunks for best results.
  - Crystal Violet staining dramatically improves nucleus visibility
    in onion cells.
  - ImageJ MTrack2 struggles with low-contrast biological data;
    custom Python tracking (track_onion_particles.py) was necessary.
  - Record at higher frame rate (5-10 fps) for fast granule motion.
  - When saving .docx with python-docx, always read from the
    CORRECT source file. Reading from a locked/open file can silently
    drop image relationships (file shrinks from 17 MB to 9 MB).
  - Keep intermediate .docx versions (-base, -v2, -v3) until the
    final is verified, then delete them.
  - TOC page insertion shifts ALL page numbers; recalculate after
    adding TOC pages.

====================================

Last updated: 2026-02-12
