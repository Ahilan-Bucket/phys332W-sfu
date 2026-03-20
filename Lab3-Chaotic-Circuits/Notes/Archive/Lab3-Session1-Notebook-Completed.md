# Lab 3 Session 1: Chaotic Circuits — Op Amp Fundamentals (Part I)

**Date:** 12 Mar 2026
**Lab Partner:** Nathan Unruh
**Recorder:** Ahilan Kumaresan

> **SESSION FOCUS:** Introduction to operational amplifiers (op amps) through four subcircuit experiments. Spent most of the session on Experiment 1 (unity-gain inverter) due to significant troubleshooting of noisy signals and a faulty op amp. Reached Experiment 2 briefly and started thinking about Experiment 3. Experiments 3 and 4 not completed — carry over to Session 2.

**Repository:** [phys332W-sfu](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab3-Chaotic-Circuits)

---

## 1. GOALS

1. Understand the op amp golden rules and verify them experimentally with real circuits
2. Build and test 4 subcircuits: unity-gain inverter, variable-gain inverter, practical integrator, summing amplifier
3. For each subcircuit, predict V_out(t) from V_in(t) using the golden rules, then compare to measured oscilloscope data
4. Complete (or begin) Pre-lab Question 1: derive the ODE for the practical integrator and sketch solutions in three frequency regimes
5. Prepare for Session 2: understand how these subcircuits combine into the jerk circuit (Lab Script Fig. 1a)

**Status:** Goals 1-2 partially completed. Experiment 1 done (with significant debugging). Experiment 2 started. Experiments 3-4 and Pre-lab Q1 deferred to Session 2.

---

## 2. APPARATUS

Equipment (Lab Script p. 5-6):

| Item | Details | Purpose |
|------|---------|---------|
| Breadboard | Built-in +/-15 V and +5 V power supplies | Circuit construction and power |
| Function generator | Keysight 33210A or 33120A | AC input signals (sine, triangle, square) and DC offset |
| Oscilloscope | Siglent SDS2352X-E, 350 MHz, 2 GSa/s | Measure V_in and V_out simultaneously |
| Oscilloscope probes | High-impedance (x1 or x10) | Monitor voltages without loading circuit |
| Op amps | LF411 (8-pin DIP) - drawers at back of room | Core amplifier element |
| Resistors | 10 kOhm (x4), 20 kOhm, 47 kOhm, 100 kOhm - back of room | Input, feedback, bleed-off resistors |
| Capacitors | 1 nF - back of room | Integrator feedback element |
| Cables/adapters | BNC cables, T-adapters, hook-up wire - back of room | Signal routing and connections |

> **Note:** Make sure oscilloscope probes are set correctly - check x1 vs x10 switch. Using x10 when scope expects x1 will show 10x too small.

---

## 3. VARIABLES

| Type | Variable | Values / Range | Description |
|------|----------|---------------|-------------|
| Independent | R2/R1 ratio | 1, 2, 4.7, 10 | Sets amplifier gain |
| Independent | Input frequency f | 100 Hz to 1 MHz | Tests integrator in different T/R2C regimes |
| Independent | Input waveform | Triangle, square, sine | Different shapes for different experiments |
| Dependent | V_out(t) | Measured on oscilloscope | Output voltage waveform |
| Dependent | Gain G = V_out/V_in | Measured | Compared to golden rule prediction -R2/R1 |
| Dependent | Phase shift | Measured | Should be 180 degrees for inverting configurations |
| Controlled | Power supply | +/-15 V | Fixed op amp rails |
| Controlled | Op amp type | LF411 | Same chip for all experiments |

---

## 4. REFERENCES

**Primary Lab Documents:**

1. PHYS 332 Lab Script: "Chaotic Circuit" (PCH, revised Jan 2025) - Part I, pp. 3-7
2. K. Kiers, D. Schmidt, and J. C. Sprott, "Precision measurements of a simple chaotic circuit," Am. J. Phys. 72, 503-509 (2004). (On Canvas)
3. Advanced Physics Laboratory Handout Electronics Tips. (On Canvas)

**Supplemental:**

4. P. Horowitz and W. Hill, The Art of Electronics, Ch. 4: "Feedback and Operational Amplifiers." (On Canvas)
5. S. H. Strogatz, Nonlinear Dynamics and Chaos, 2nd Ed., 2015. Ch. 1 (overview), Ch. 10 (bifurcation). (SFU Library)

---

## 5. BACKGROUND: OP AMP THEORY

Reference: Lab Script pp. 3-5, Horowitz and Hill Ch. 4

### 5.1 What Is an Op Amp?

An operational amplifier is a high-gain differential amplifier IC. Key properties (Lab Script p. 3-4):

- High gain: ~10^6 (open-loop)
- High input impedance, low output impedance
- Supply: +/-15 V (or +/-12 V)
- Insensitive to temperature and power supply fluctuations
- Always used with feedback in our circuits

The standard symbol is a sideways triangle. Two inputs: V_in,+ (non-inverting) and V_in,- (inverting). One output: V_out.

### 5.2 LF411 Pinout (DIP Package)

Reference: Lab Script Fig. 2b

Looking at the chip from above with the half-moon notch on the LEFT:

| Pin | Function |
|-----|----------|
| 1 | BALANCE (leave floating) |
| 2 | Inverting input (V_in,-) |
| 3 | Non-inverting input (V_in,+) |
| 4 | V- -> connect to -15 V |
| 5 | BALANCE (leave floating) |
| 6 | Output (V_out) |
| 7 | V+ -> connect to +15 V |
| 8 | NC (no connection) |

> **Note:** Pins numbered counterclockwise from pin 1 (left of notch). Pin 8 is directly across from pin 1. NC and BALANCE pins are left floating - only 5 pins need connections.

### 5.3 The Op Amp Golden Rules

When used with negative feedback, ideal op amp circuits obey two rules (Lab Script p. 4):

1. **The inputs draw no current.** Input impedance is effectively infinite.
2. **The output drives V_in,+ = V_in,-.** The op amp adjusts its output to make the voltage difference between its two inputs zero.

> **CONCLUSION:** These two rules are sufficient to analyze ALL circuits in this lab. Apply Kirchhoff's current law at the inverting input node, using Golden Rule 1 (no current into op amp) and Golden Rule 2 (V_in,- = V_in,+).

**Clipping:** V_out cannot exceed the supply rails (+/-15 V). If the golden rules would require V_out > 15 V or V_out < -15 V, the output "clips" or "rails."

### 5.4 Example: Voltage Follower

Reference: Lab Script Fig. 3

Simplest circuit: V_in connected to pin 3 (non-inverting), pin 2 (inverting) connected directly to pin 6 (output).

By Golden Rule 2: V_in,- = V_in,+ implies V_out = V_in.

Gain = 1, no inversion. Purpose: buffer a weak signal source (op amp can source more current than the original source).

---

## 6. PRE-LAB PLANNING

**Time:** ~1:28 PM

Before starting experiments, identified some tools for future pre-lab preparation:

- Want to use **TinkerCAD** breadboard simulator for planning circuit layouts before building: https://www.tinkercad.com
- Also plan to explore **LT Spice** for circuit simulation

Initial challenge: figuring out how to identify the channel number (pin mapping) for the corresponding pins on the LF411 op amp on the physical breadboard.

---

## 7. PROCEDURE

### 7.1 Breadboard Setup

1. Turned on breadboard power supply. Verified +/-15 V and +5 V rails.
2. Ran +15 V and -15 V along the long power rails of the breadboard.
3. Inserted LF411 chip with half-moon notch on the LEFT.
4. Wired power connections: Pin 7 to +15 V rail, Pin 4 to -15 V rail.
5. Wired pin 3 (non-inverting input) to GND.

> **[INSERT IMAGE - breadboard power setup photo]**

---

### 7.2 Experiment 1: Unity-Gain Inverting Amplifier

Reference: Lab Script p. 6, top circuit diagram

**Circuit:**
- R1 = 10 kOhm (from V_in to pin 2)
- R2 = 10 kOhm (from pin 2 to pin 6, feedback)
- Pin 3 to GND

**Expected behaviour:** Gain G = -R2/R1 = -(10 kOhm)/(10 kOhm) = -1. Output is inverted copy of input (180 degree phase shift), same amplitude.

**Golden Rule derivation:** By Rule 2, V_in,- = V_in,+ = 0 (pin 3 is grounded). By Rule 1, no current flows into pin 2. So by Kirchhoff at pin 2:

$$I_{in} = \frac{V_{in} - 0}{R_1} = \frac{0 - V_{out}}{R_2} = I_{feedback}$$

$$\Rightarrow V_{out} = -\frac{R_2}{R_1} V_{in}$$

**Procedure:**

1. Built the circuit on the breadboard with R1 = R2 = 10 kOhm
2. Set function generator to 1 kHz triangle wave, zero DC offset, amplitude ~1 Vpp
3. Used T-adapter and BNC cable to split function generator signal: one path to oscilloscope Ch1 (V_in), one path to circuit input
4. Connected oscilloscope Ch2 probe to circuit output (pin 6)

### 7.2.1 Troubleshooting: Noisy/Unstable Signal

**Problem:** The triangle signal used to observe V_in was very unstable - it kept bouncing on the oscilloscope display.

**Debugging steps:**

1. **Tried a new oscilloscope** - did not help
2. **Changed the BNC cable** - did not help
3. **Pressed the Sync BNC connection point on the oscilloscope tighter** - this helped somewhat, indicating a loose connection was part of the issue
4. **Grounded the two oscilloscope probes to the breadboard** - this helped significantly in reducing the noise
5. **Still seeing noise after connecting +V and -V power** - the noisy output persisted
6. **Lab station (TA/instructor) helped identify the root cause:** the op-amp chip itself was faulty

> **Lesson learned:** Op amps are easily destroyed. If the circuit misbehaves after checking all connections, try replacing the op amp first. This is consistent with the lab script warning on p. 8.

**Before connecting +/-V power rails:** V_out was pretty noisy.

> **[INSERT IMAGE - noisy V_out before power connection]**

### 7.2.2 Measurements (After Replacing Op Amp)

After replacing the faulty op amp, the circuit worked. Measurements with 1 kHz triangle wave input:

| Parameter | Predicted | Measured |
|-----------|-----------|----------|
| V_in amplitude (yellow, Ch1) | 1.0 Vpp | 1.0 Vpp |
| V_out amplitude (pink, Ch2) | 1.0 Vpp | 2 Vpp |
| Gain G = V_out/V_in | -1.000 | (not recorded) |
| Phase shift | 180 degrees | (not recorded) |

> **Note:** The measured V_out of 2 Vpp with V_in of 1.0 Vpp gives |G| = 2, which does not match the expected gain of -1 for equal resistors. This needs investigation in Session 2 - possible causes: resistor mismatch, probe attenuation setting (x1 vs x10), or measurement error.

> **[INSERT IMAGE - Exp 1 oscilloscope screenshot: V_in (Ch1, yellow) and V_out (Ch2, pink)]**

> **[INSERT IMAGE - Exp 1 circuit photo]**

---

### 7.3 Experiment 2: Inverting Amplifier - Variable Gain

Reference: Lab Script p. 6, second circuit diagram

**Circuit:** Same as Experiment 1 but with different R2 values. Keep R1 = 10 kOhm fixed.

**Predicted gains:** G = -R2/R1

**Procedure:** Started this experiment but only tested R2 = 10 kOhm (confirmed from color code: Gold-Yellow-Black-Brown = 10 kOhm).

<!-- Table 3: Inverting Amplifier Gain Measurements -->

| R2 (kOhm) | R2 actual (kOhm) | Color Code | Predicted G | Measured G | % Error |
|----------|-----------------|------------|-------------|------------|---------|
| 10 | 10k | Gold-Yellow-Black-Brown | -1.00 | (not completed) | - |
| 20 | - | - | -2.00 | (not completed) | - |
| 47 | - | - | -4.70 | (not completed) | - |
| 100 | - | - | -10.0 | (not completed) | - |

> **Status:** Only the 10 kOhm resistor was identified and tested (same as Exp 1). Higher gain values not tested due to time spent on Exp 1 troubleshooting. Carry over to Session 2.

---

### 7.4 Experiment 3: Practical Integrator (ATTEMPTED - CIRCUIT FAILURE)

Reference: Lab Script p. 6, third circuit diagram; Pre-lab Question 1

**Prediction made before building circuit:**

When V_in is a square wave, predicted that V_out must also be a square wave with a similar 180 degree phase difference.

> **Note for Session 2:** This prediction needs to be revisited. For an integrator, a square wave input should produce a triangular wave output (integral of a constant = linear ramp), not a square wave. The square wave prediction may apply to a simple inverting amplifier but not the integrator. Need to work through Pre-lab Q1 to understand the difference.

### 7.4.1 Circuit Failure - Smoke Incident

**Problem:** While building the integrator circuit, we noticed that at certain points we would not get any V_in reading on the oscilloscope. We attempted several fixes:

1. Cleaned the ends of the resistors
2. Checked the polarity of the capacitor
3. Tried to clean the leads of the parallel resistor with the capacitor by removing it

**Incident:** Within a few seconds of removing the parallel resistor, **smoke came out of the circuit**. We immediately unplugged the system.

**Investigation:**

- Put tape over that part of the breadboard to mark the problem area
- Replaced all resistors and the op amp chip (thinking they could have been damaged)
- Found a wire that had a **black stain** on it - exact cause unclear

**Preliminary hypothesis:** Possible short circuit on the breadboard, or a damaged component creating an unintended current path. The root cause was not definitively identified.

**Action item for Session 2:** Systematically check the breadboard with a DMM (digital multimeter) before building any circuits:
- Test continuity between adjacent rows to check for shorts
- Verify all power rails are intact and not bridged
- Test each component individually before inserting into circuit
- Check for damaged breadboard traces in the affected area

**Status:** Circuit not completed due to smoke incident. Carry over to Session 2 with breadboard verification plan.

---

### 7.5 Experiment 4: Summing Amplifier (NOT COMPLETED)

**Status:** Not reached. Carry over to Session 2.

---

## 8. PRE-LAB QUESTION 1 (NOT COMPLETED)

Due: before starting Session 2.

**Status:** Not started during this session. Must complete before Session 2:
- (i) Derive the ODE relating V_out(t) to V_in(t) for the practical integrator
- (ii) Solve for V_out(t)
- (iii) Plot schematic solutions for T >> R2C, T ~ R2C, T << R2C
- (iv) What problem does R2 prevent?

---

## 9. ANALYSIS

### 9.1 Summary of Completed Work

| Experiment | Status | Key Result |
|------------|--------|------------|
| Exp 1: Unity-gain inverter | Completed (with debugging) | V_in = 1.0 Vpp, V_out = 2 Vpp - gain discrepancy needs investigation |
| Exp 2: Variable gain | Started only | R2 = 10 kOhm identified (color code confirmed), no measurements |
| Exp 3: Integrator | Attempted - smoke incident | Made incorrect prediction; circuit failed with smoke during build |
| Exp 4: Summing amp | Not started | - |
| Pre-lab Q1 | Not started | Due before Session 2 |

### 9.2 Key Issues Encountered

1. **Noisy/unstable oscilloscope signal:** Traced to combination of loose BNC connections and faulty op amp. Solution: ground probes to breadboard and replace op amp.
2. **Gain discrepancy in Exp 1:** Measured |G| ~ 2 instead of expected 1. Possible causes to check in Session 2:
   - Oscilloscope probe attenuation setting (x1 vs x10 mismatch between channels)
   - Actual resistor values differ from nominal
   - Measurement technique (Vpp reading from oscilloscope)
3. **Smoke incident during Exp 3 build:** Circuit produced smoke when removing the parallel resistor from the integrator. Replaced all components, found a blackened wire. Breadboard integrity needs verification with DMM before Session 2.

---

## 10. CONCLUSIONS

Session 1 was primarily a learning/debugging session. Main takeaways:

1. **Op amps fail frequently** - when circuit misbehaves, replace the chip before extensive debugging
2. **Grounding oscilloscope probes to the breadboard** significantly reduces noise
3. **BNC connection quality matters** - push connectors firmly
4. **Breadboard integrity cannot be assumed** - the smoke incident highlights the need to systematically verify the breadboard with a DMM before building circuits
5. Need to complete Pre-lab Q1 before Session 2 to understand integrator behavior (current prediction of square-in/square-out is incorrect for an integrator)

---

## 11. PLAN FOR NEXT SESSION

**Session 2 - Lab Period 2** (Lab Script Suggested Timeline):

1. **Systematically check breadboard with DMM** - verify rows for shorts, test power rails, test components individually before inserting
2. **Hand in Pre-lab Question 1** - must derive integrator ODE and sketch 3 frequency regimes
3. **Resolve Exp 1 gain discrepancy** - check probe attenuation settings, re-measure
4. **Complete Experiments 2, 3, and 4** from Part I
5. **Build and test the nonlinear element D(x)** if time permits (Lab Script p. 7, Fig. 1b)
   - Use 1N4148 or 1N914 diodes
   - R1 and R2 in the 10s of kOhm, ratio R2/R1 ~ 6
   - Test with 1 kHz sawtooth ramp input
5. **Begin Pre-lab Question 2:** Derive Eqs. 2-6 from Kiers et al.

**Tools to explore before next session:**
- TinkerCAD breadboard simulator for planning circuit layouts
- LT Spice for circuit simulation

**Data files from today:** Oscilloscope screenshots saved (insert into .docx)
