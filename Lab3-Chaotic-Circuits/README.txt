Lab 3: Chaotic Circuits
====================================

PHYS 332W Advanced Physics Laboratory
Simon Fraser University, Spring 2026

Project: Op Amp Circuits, Jerk Equation, and Deterministic Chaos
Duration: Sessions 1-8 (Mar-Apr 2026)

Collaborators:
  - Ahilan Kumaresan (Recorder)
  - Nathan Unruh (Lab Partner)

Instructor: PHYS 332W Teaching Team
Lab Location: SFU Physics Teaching Lab

====================================
PROJECT DESCRIPTION
====================================

This experiment builds a nonlinear electronic circuit (the "jerk circuit")
from op amp subcircuits and investigates the transition from periodic to
chaotic behaviour. The primary goals are:

1. Build and test 4 op amp subcircuits: inverting amplifier, variable-gain
   amplifier, practical integrator, summing amplifier
2. Verify golden rules of op amps experimentally
3. Build the piecewise-linear nonlinear element D(x) using 1N4148 diodes
4. Assemble the full jerk circuit (3 integrators + summing amp + D(x))
5. Derive the governing jerk ODE: x''' = -Ax'' - x' + D(x) - alpha
6. Vary bifurcation parameter A = R/R_v to observe:
   stable -> periodic -> period-doubling -> chaos
7. Capture time series, phase portraits, bifurcation diagrams, power spectra
8. Compare measured dynamics to numerical simulation of the jerk ODE

====================================
KEY RESULTS (Sessions 1-3)
====================================

Part I (Op Amp Subcircuits):
  - All 4 experiments completed across Sessions 1-2
  - Unity-gain inverter: |G| confirmed (probe attenuation resolved)
  - Variable gain: |G| matches -R2/R1 at 10k and 100k Ohm
  - Practical integrator: 3 frequency regimes verified (Pre-lab Q1)
  - Summing amplifier: tested, unexpected result needs investigation

D(x) Nonlinear Element:
  - Built with 2x 1N4148 diodes, R1 ~ 2 kOhm, R2 ~ 12 kOhm
  - XY mode confirms piecewise-linear: D(x) = -(R2/R1) min(x, 0)
  - Slope ~ -6 for x < 0, flat for x > 0

Jerk Circuit (Session 3):
  - Section 1 (D(x) + first integrator) built and tested
  - Beating pattern observed at 1 kHz -- two close frequencies interfering
  - Full circuit layout planned on TinkerCAD
  - Pre-lab Q2 derivation of jerk equation completed

Pre-lab Status:
  - Q1: Completed and handed in (integrator ODE + 3 regimes)
  - Q2: Derivation written (jerk equation from circuit, due Period 4)
  - Q3: Not started (numerical simulation, due before Period 4)

====================================
DIRECTORY STRUCTURE
====================================

Lab3-Chaotic-Circuits/
|
|-- README.txt                  This file
|
|-- Analysis/                   Analysis scripts and outputs
|   |-- Session3/
|   |   |-- Session3-Dx-Plots.ipynb         D(x) + Section 1 plotting notebook
|   |   |-- Session3-Dx-Plots-executed.ipynb Executed version with outputs
|   |-- figures/
|   |   |-- Session3/                       Session 3 figure outputs
|   |   |   |-- Dx-Nonlinear-Test_Zoom-Out_CH1-Vin_CH2-Vout_100us-div.png
|   |   |   |-- Dx-Nonlinear-Test_Zoom-In_CH1-Vin_CH2-Vout_0.1us-div.png
|   |   |   |-- Section1-Integrator_Error-vs-Retake_CH1-Vin_CH2-Vout_Comparison.png
|   |   |-- 2026-03-19/                     Date-stamped copies
|
|-- Data/                       Raw experimental data
|   |-- Session-3/              Session 3 (19 Mar 2026)
|   |   |-- Test-D_x-Zoom-in-SDS00002.csv   D(x) zoom-in (1,400 pts, 0.1 us/div)
|   |   |-- Test-D_x-Zoom-out-SDS00003.csv  D(x) full view (1.4M pts, 100 us/div)
|   |   |-- Section1-Error-SDS00001.csv     Section 1 error trace (CH2 at 5 mV/div)
|   |   |-- Section1-SDS00004.csv           Section 1 retake (CH2 at 200 mV/div)
|   |   |-- SDS00001.png                    Oscilloscope screenshot (Section 1)
|   |   |-- SDS00002.png                    Oscilloscope screenshot (D(x) zoom-in)
|   |   |-- SDS00003.png                    Oscilloscope screenshot (D(x) zoom-out)
|
|-- Drafts/                     Old submissions and scans
|
|-- Notes/                      Session notebooks and images
|   |-- Lab3-Sessions1-2-Final.md           Sessions 1-2 combined notebook (current)
|   |-- Lab3-Session3-Notebook.md           Session 3 notebook (current)
|   |-- Archive/                            Superseded .md files
|   |   |-- Lab3-Session1-Notebook.md
|   |   |-- Lab3-Session1-Notebook-Completed.md
|   |   |-- Lab3-Session2-Notebook.md
|   |-- Images/
|   |   |-- Session1/                       Session 1 photos (6 images)
|   |   |-- Session2/                       Session 2 photos (12 images)
|   |   |-- Session3/                       Session 3 photos (5 images)
|   |   |-- Prelab-Q1-T-much-greater-tau.png   Pre-lab Q1 computed plot
|   |   |-- Prelab-Q1-T-approx-tau.png         Pre-lab Q1 computed plot
|   |   |-- Prelab-Q1-T-much-less-tau.png      Pre-lab Q1 computed plot
|   |   |-- generate_prelab_q1_plots.py        Script that generated Q1 plots
|   |-- References/
|   |   |-- Chaotic Circuit-labScript.pdf
|   |   |-- kiers-schmidt-sprott_ajp04.pdf
|   |   |-- Op Amps (Horowitz and Hill, Ch 4).pdf
|   |   |-- SigLent-oscilloscope.pdf

====================================
COMPONENT VALUES
====================================

Op Amp Subcircuits (Part I):
  R1 = 10 kOhm (input resistor, all experiments)
  R2 = 10, 20, 47, 100 kOhm (variable gain)
  C1 = 1 nF (integrator feedback capacitor)
  R2_bleed = 100 kOhm (integrator bleed-off, parallel with C1)
  tau = R2_bleed * C1 = 100 us
  Op amp: LF411 (8-pin DIP), powered at +/-15 V

D(x) Nonlinear Element:
  R1 ~ 2 kOhm, R2 ~ 12 kOhm (gain R2/R1 ~ 6)
  Diodes: 2x 1N4148 in antiparallel

Jerk Circuit (Part II):
  R = 10 kOhm, C = 1 nF (all integrators)
  Rb = 100 kOhm (bleed-off, each integrator)
  R_v = decade box (bifurcation control, A = R/R_v)
  IMPORTANT: 1 nF capacitors (NOT 1 uF from Kiers et al.)

====================================
REQUIREMENTS
====================================

Software:
  - Python 3.12
  - Jupyter Lab or Notebook
  - NumPy, Pandas, Matplotlib (scientific Python)
  - TinkerCAD (circuit planning)

Hardware:
  - Breadboard with built-in +/-15 V and +5 V power supplies
  - Keysight 33210A function generator
  - Siglent SDS2352X-E oscilloscope (350 MHz, 2 GSa/s)
  - LF411 op amps (DIP-8)
  - 1N4148 signal diodes
  - Decade resistor box
  - Anatek regulated DC power supply
  - USB cable (oscilloscope to laptop data transfer)

