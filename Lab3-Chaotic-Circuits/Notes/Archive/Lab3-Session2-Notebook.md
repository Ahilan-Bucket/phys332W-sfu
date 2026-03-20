# Lab 3 Session 2: Pre-Lab Work + Complete Part I + Begin Nonlinear Element

## PRE-LAB QUESTION 1 (TO HAND IN)

*Reference: Lab Script p. 7*

The practical integrator circuit (Exp 3) is not exactly an integrator. Analyze it:

### Part (i): Derive the ODE

Circuit: R1 = 10 kOhm (input), C1 = 1 nF (feedback capacitor), R2 = 100 kOhm (bleed-off, parallel with C1). Pin 3 to GND.

Apply Golden Rules at pin 2 (inverting input). By Rule 2: V_in,- = V_in,+ = 0 (virtual ground). By Rule 1: no current into pin 2.

Kirchhoff's current law at pin 2:

Current through R1 + Current through C1 + Current through R2 = 0

$$\frac{V_{in}}{R_1} + C_1 \frac{dV_{out}}{dt} + \frac{V_{out}}{R_2} = 0$$

Rearranging to standard first-order linear ODE form:

$$R_1 C_1 \frac{dV_{out}}{dt} + \frac{R_1}{R_2} V_{out} = -V_{in}$$

Or equivalently:

$$\frac{dV_{out}}{dt} + \frac{1}{R_2 C_1} V_{out} = -\frac{V_{in}}{R_1 C_1}$$

**Time constant:** tau = R2 * C1 = (100 kOhm)(1 nF) = 100 us

(CC - show full derivation with circuit diagram here)

### Part (ii): Solve for V_out(t)

This is a first-order linear ODE. Using integrating factor mu = exp(t / R2C1):

$$V_{out}(t) = e^{-t/\tau} \left[ V_{out}(0) - \frac{1}{R_1 C_1} \int_0^t V_{in}(t') e^{t'/\tau} dt' \right]$$

where tau = R2 * C1 = 100 us.

The "twist" compared to a pure integrator: the exponential decay factor exp(-t/tau) means the output is not a simple integral. It is a weighted integral with exponential memory loss.

(CC - show full solution steps)

### Part (iii): Schematic Solutions for Square Wave Input

For V_in(t) = square wave with period T and zero mean (amplitude +/-V0):

**Case 1: T >> R2C (low frequency, e.g. f = 100 Hz, T = 10 ms >> 100 us)**

- Each half-cycle is much longer than tau
- Output has time to reach steady state within each half-cycle
- V_out approaches -V_in * (R2/R1) during each half-period (acts like inverting amplifier at DC)
- But with exponential transitions between levels
- Output looks like a rounded square wave, inverted
- This is the regime where the circuit is MOST like a simple integral - the output is approximately triangular (linear ramps)

(CC - sketch: triangular wave output, inverted)

**Case 2: T ~ R2C (mid frequency, e.g. f = 10 kHz, T = 100 us ~ tau)**

- Half-cycle duration comparable to tau
- Output shows clear exponential charging/discharging curves
- Neither fully integrated nor fully passed through
- Intermediate sawtooth-like shape with exponential curvature

(CC - sketch: exponential charge/discharge curves)

**Case 3: T << R2C (high frequency, e.g. f = 500 kHz, T = 2 us << 100 us)**

- Each half-cycle is much shorter than tau
- Capacitor barely charges during each half-cycle
- Output amplitude is small
- Circuit behaves more like a pure integrator (no time for R2 to matter)
- Output is approximately triangular but with very small amplitude: V_out ~ V_in * T/(4 R1 C1)

(CC - sketch: small-amplitude triangular output)

**Which case is most like a simple integral?** Case 3 (T << R2C), because R2 has no time to drain the capacitor. The output is the integral of the input, but with very small amplitude.

### Part (iv): What Problem Does R2 Prevent?

R2 prevents DC charge accumulation on C1. Without R2:
- Any small DC offset from the function generator or op amp input offset voltage will slowly charge C1
- With no discharge path, V_out drifts steadily toward +15 V or -15 V (rails)
- The op amp saturates ("rails") and the circuit becomes useless

R2 provides a resistive path that bleeds off accumulated charge with time constant tau = R2*C1 = 100 us, preventing this drift.

---

## Inter-Lab Work: Breadboard Verification Plan

Rough plan on how we could verify the breadboard is safe after the Session 1 smoke incident:

### Breadboard Verification Procedure (DMM)

Before building any circuits, systematically check the breadboard:

1. **Power rails:** Set DMM to DC voltage. Turn on breadboard power. Measure:
   - +15 V rail: should read +15.0 V (+/- 0.5 V) relative to GND
   - -15 V rail: should read -15.0 V (+/- 0.5 V) relative to GND
   - +5 V rail: should read +5.0 V (+/- 0.2 V) relative to GND
   - Check both ends of each rail (some boards have breaks in the middle)

2. **Continuity within rows:** Set DMM to continuity/beep mode. With power OFF:
   - Test that holes in the same row (5-hole groups) are connected
   - Test that adjacent rows are NOT connected (no shorts between rows)
   - Focus especially on the area where the smoke incident occurred (taped section)

3. **Check for shorts near incident area:**
   - Test continuity between the +15 V and -15 V rails (should be OPEN)
   - Test continuity between +15 V and GND (should be OPEN)
   - Test continuity between -15 V and GND (should be OPEN)
   - If any of these beep, there is a short - do NOT use that area

4. **Test components individually before inserting:**
   - New LF411: test with voltage follower circuit before using in experiments
   - Resistors: measure actual resistance with DMM and record values
   - Capacitor: check for shorts (should read open circuit on DMM resistance mode)

**Record all DMM readings:** (CC - fill in during lab)

| Test | Expected | Measured | Pass? |
|------|----------|----------|-------|
| +15 V rail (left end) | +15.0 V | (CC) | (CC) |
| +15 V rail (right end) | +15.0 V | (CC) | (CC) |
| -15 V rail (left end) | -15.0 V | (CC) | (CC) |
| -15 V rail (right end) | -15.0 V | (CC) | (CC) |
| +5 V rail | +5.0 V | (CC) | (CC) |
| Rail-to-rail short (+15 to -15) | Open | (CC) | (CC) |
| Rail-to-GND short (+15 to GND) | Open | (CC) | (CC) |
| Rail-to-GND short (-15 to GND) | Open | (CC) | (CC) |
| Incident area row continuity | Connected within row | (CC) | (CC) |
| Incident area cross-row | Open between rows | (CC) | (CC) |

---
---

# Lab 3 Session 2: Complete Part I + Begin Nonlinear Element

**Date:** (CC date)
**Lab Partner:** Nathan Unruh
**Recorder:** Ahilan Kumaresan

> **SESSION FOCUS:** Heavy carry-over from Session 1. First priority: systematically verify breadboard with DMM after last session's smoke incident. Then complete remaining Part I experiments (Exps 2, 3, 4), resolve Exp 1 gain discrepancy, and hand in Pre-lab Q1. If time permits, begin building the nonlinear element D(x) for Part II.

**Repository:** [phys332W-sfu](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab3-Chaotic-Circuits)

---

## 1. GOALS

1. Verify breadboard integrity with DMM - check for shorts, damaged traces, and component health before building any circuits
2. Hand in Pre-lab Question 1 (practical integrator ODE derivation)
3. Resolve Experiment 1 gain discrepancy (measured |G| = 2, expected |G| = 1 - likely probe attenuation x1/x10 mismatch)
4. Complete Experiments 2, 3, and 4 from Part I
5. If time permits: build and test nonlinear element D(x) (Lab Script p. 7, Part II step 1)

---

## 2. APPARATUS

Same as Session 1 (see Session 1, Section 2). Additional items this session:

| Item | Details | Purpose |
|------|---------|---------|
| Digital multimeter (DMM) | Available at bench | Breadboard verification - continuity, voltage, resistance checks |
| Fresh LF411 op amps | Drawers at back of room | Replace potentially damaged chips from Session 1 |
| 1N4148 or 1N914 diodes | Back of room | For nonlinear element D(x) if we reach Part II |
| Decade resistor box | Manual stepping | For Part II: variable R_v control parameter |

---

## 3. CARRY-OVER FROM SESSION 1

### 3.1 Issues to Resolve

| Issue | Priority | Plan |
|-------|----------|------|
| Smoke incident - breadboard damage | HIGH | DMM verification before any circuit building |
| Exp 1 gain discrepancy (|G|=2 not 1) | HIGH | Check probe attenuation settings (x1 vs x10) |
| Exp 2 incomplete | MEDIUM | Complete variable gain measurements |
| Exp 3 not built | MEDIUM | Build integrator after breadboard verification |
| Exp 4 not reached | MEDIUM | Build summing amplifier |
| Pre-lab Q1 not started | HIGH | Must hand in before starting Part II |

---

## 4. PROCEDURE

### 4.1 Breadboard Verification (FIRST PRIORITY)

Refer to the Inter-Lab Work section above for the full DMM verification plan.

**Time:** (CC time)

Follow the DMM verification procedure above. Record all measurements in the table.

**Decision point:** If the incident area has shorts or damage, avoid that area entirely and use a different section of the breadboard.

(CC - record results and decision)

---

### 4.2 Resolve Experiment 1 Gain Discrepancy

**Time:** (CC time)

Quick verification of parameters:

- Check oscilloscope probe attenuation setting (x1 vs x10) - this is the most likely cause of measuring |G| = 2 instead of |G| = 1
- Verify both probes are set to the same attenuation
- Re-measure V_in and V_out with correct probe settings
- Record corrected gain: (CC)

---

### 4.3 Experiment 2: Inverting Amplifier - Variable Gain (COMPLETE)

*Reference: Lab Script p. 6, second circuit diagram*

Same circuit as Exp 1, but vary R2. Keep R1 = 10 kOhm fixed. Use 1 kHz triangle wave, ~1 Vpp.

**Measure actual resistor values with DMM before inserting:**

| R2 nominal (kOhm) | R2 actual (kOhm) | Color Code | Predicted G = -R2/R1 | Measured G | % Error |
|----------|-----------------|------------|-------------|------------|---------|
| 10 | (CC) | (CC) | (CC) | (CC) | (CC) |
| 20 | (CC) | (CC) | (CC) | (CC) | (CC) |
| 47 | (CC) | (CC) | (CC) | (CC) | (CC) |
| 100 | (CC) | (CC) | (CC) | (CC) | (CC) |

For G = -10 with 1 Vpp input: expected V_out = 10 Vpp. Does it clip at +/-15 V rails? If so, reduce input amplitude.

> [INSERT IMAGE - Exp 2 oscilloscope screenshot for one gain setting]

---

### 4.4 Experiment 3: Practical Integrator (COMPLETE)

*Reference: Lab Script p. 6, third circuit diagram; Pre-lab Question 1*

**Circuit:**
- R1 = 10 kOhm (input resistor, from V_in to pin 2)
- C1 = 1 nF (feedback capacitor, from pin 2 to pin 6)
- R2 = 100 kOhm (bleed-off resistor, in parallel with C1, from pin 2 to pin 6)
- Pin 3 to GND

**Measure actual component values with DMM:**
- R1 actual = (CC) kOhm
- R2 actual = (CC) kOhm
- C1 = 1 nF (cannot easily measure with standard DMM - use nominal value)

**Key time constant:** tau = R2 * C1 = (100 kOhm)(1 nF) = 100 us, corresponding frequency f = 1/(2*pi*tau) ~ 1.6 kHz

**Procedure:**

Input: square wave, ~1 Vpp, zero DC offset.

1. **Low frequency (T >> tau, integrating regime):**
   - Set f = 100 Hz (T = 10 ms >> 100 us)
   - Expected: V_out is approximately triangular (integral of square wave)
   - Record V_in (Ch1) and V_out (Ch2)

2. **Mid frequency (T ~ tau):**
   - Set f = 10 kHz (T = 100 us ~ tau)
   - Expected: intermediate shape with visible exponential charging/discharging
   - Record V_in and V_out

3. **High frequency (T << tau):**
   - Set f = 500 kHz (T = 2 us << 100 us)
   - Expected: small-amplitude output, nearly triangular (pure integrator regime)
   - Record V_in and V_out

> [INSERT IMAGE - Exp 3: low frequency (100 Hz)]

> [INSERT IMAGE - Exp 3: mid frequency (10 kHz)]

> [INSERT IMAGE - Exp 3: high frequency (500 kHz)]

4. **DC offset test (optional, if time):**
   - Remove R2 from the circuit (pure integrator, only C1 in feedback)
   - Apply a small DC offset on the function generator
   - Observe: V_out drifts to a rail (+/-15 V) - this is what R2 prevents
   - Re-insert R2, confirm stability returns

**Compare to Pre-lab Q1 predictions:** Do the observed waveforms match the three cases derived analytically?

---

### 4.5 Experiment 4: Summing Amplifier (COMPLETE)

*Reference: Lab Script p. 6, bottom circuit diagram*

**Circuit:**
- R_a = R_b = R_f = 10 kOhm (two input resistors + one feedback resistor, all equal)
- V_in,1 through R_a to pin 2
- V_in,2 through R_b to pin 2
- R_f from pin 2 to pin 6 (feedback)
- Pin 3 to GND

**Expected:** V_out = -(V_in,1 + V_in,2) when all resistors are equal.

**Golden Rule derivation:** V_in,- = V_in,+ = 0 (virtual ground). KCL at pin 2:

$$\frac{V_{in,1}}{R_a} + \frac{V_{in,2}}{R_b} + \frac{V_{out}}{R_f} = 0$$

$$V_{out} = -R_f \left(\frac{V_{in,1}}{R_a} + \frac{V_{in,2}}{R_b}\right) = -(V_{in,1} + V_{in,2})$$

**Procedure:**

1. Build the circuit. Measure actual resistor values: R_a = (CC), R_b = (CC), R_f = (CC)
2. Input 1: function generator, 1 kHz sine wave, ~1 Vpp, zero DC offset
3. Input 2: DC voltage (variable DC supply, or Keysight DC Volts mode, or potentiometer from +5 V rail)
4. Measure V_out with different DC offsets:

| V_in,1 (AC, Vpp) | V_in,2 (DC, V) | V_out predicted | V_out measured |
|-----|------|--------|---------|
| 1.0 | 0.0 | -1.0 Vpp, centered at 0 | (CC) |
| 1.0 | +1.0 | -1.0 Vpp, centered at -1.0 V | (CC) |
| 1.0 | +2.0 | -1.0 Vpp, centered at -2.0 V | (CC) |
| 1.0 | -1.0 | -1.0 Vpp, centered at +1.0 V | (CC) |

> [INSERT IMAGE - Exp 4: AC + DC summing]

**Verify:** AC amplitude stays the same regardless of DC offset. Only the DC level of the output shifts.

---

### 4.6 Begin Part II: Nonlinear Element D(x) (IF TIME PERMITS)

*Reference: Lab Script p. 7, Part II step 1-2; Fig. 1b*

**Circuit (Lab Script Fig. 1b):**
- Two diodes (1N4148 or 1N914) in antiparallel configuration
- R1 and R2 in the 10s of kOhm range, with ratio R2/R1 ~ 6
- This implements D(x) = -(R2/R1) * min(x, 0)

**How D(x) works:**
- When V_in > 0: diodes are reverse-biased (approximately), so D(x) ~ 0
- When V_in < 0: diodes conduct, and the circuit acts as an inverting amplifier with gain -R2/R1
- Result: piecewise-linear function - zero for positive input, linear with slope -R2/R1 for negative input

**Testing procedure (Lab Script p. 8, step 2):**

1. Build D(x) circuit with R1 ~ 10 kOhm, R2 ~ 60 kOhm (so R2/R1 ~ 6)
2. Input: 1 kHz sawtooth ramp from function generator (ramp goes from negative to positive)
3. Display both V_in (Ch1) and V_out (Ch2) on oscilloscope
4. Set oscilloscope to XY mode to see D(x) vs x directly (I-V curve)
5. Expected: flat at ~0 for positive x, linear with slope ~-6 for negative x

> [INSERT IMAGE - D(x) test: sawtooth input, time domain]

> [INSERT IMAGE - D(x) test: XY mode showing piecewise-linear I-V curve]

**Measured values:**
- R1 actual = (CC) kOhm
- R2 actual = (CC) kOhm
- R2/R1 ratio = (CC)
- Slope of D(x) for x < 0: (CC) (should be ~ -R2/R1)

---

## 5. ANALYSIS

### 5.1 Part I Summary

| Experiment | Status | Key Result |
|------------|--------|------------|
| Breadboard verification | (CC) | (CC) |
| Exp 1 revisit (gain fix) | (CC) | (CC) |
| Exp 2: Variable gain | (CC) | (CC) |
| Exp 3: Integrator | (CC) | (CC) |
| Exp 4: Summing amp | (CC) | (CC) |
| Pre-lab Q1 | Handed in | ODE derived, 3 regimes sketched |

### 5.2 Golden Rule Verification

For all experiments, compare predicted vs measured gain. Quantify agreement.

(CC - fill in after experiments) (Highlight in purple if CC needs to fill later)

---

## 6. CONCLUSIONS

(CC - summarize Session 2 results)

---

## 7. PLAN FOR NEXT SESSION

**Session 3 - Lab Period 3** (Lab Script Suggested Timeline):

1. **Build the full jerk circuit** (Lab Script Fig. 1a) - three cascaded inverting integrators + summing amplifier + nonlinear element D(x)
2. **Observe chaos** - vary R_v to find period doubling, bifurcation, and chaotic regimes
3. Build and test each integrator separately first (with 500 kOhm temporary feedback resistor for stability - Lab Script p. 8, step 4)
4. Use 1 nF capacitors (not 1 uF from Kiers et al.) - this speeds up the circuit by 1000x
5. Begin Pre-lab Question 2: derive Eqs. 2-6 from Kiers et al. for the full circuit (due Lab Period 4)

**Data files from today:** (CC - list oscilloscope save files)
