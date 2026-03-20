# Lab 3 Session 1: Chaotic Circuits — Op Amp Fundamentals (Part I)

**Date:** (CC date)
**Lab Partner:** Nathan Unruh
**Recorder:** Ahilan Kumaresan

> **SESSION FOCUS:** Introduction to operational amplifiers (op amps) through four subcircuit experiments. These subcircuits (inverting amplifier, integrator, summing amplifier) are the building blocks of the nonlinear "jerk circuit" that will exhibit chaotic behaviour in Part II. Goal is to complete all of Part I today and begin Pre-lab Question 1.

**Repository:** [phys332W-sfu](https://github.com/Ahilan-Bucket/phys332W-sfu/tree/main/Lab3-Chaotic-Circuits)

---

## 1. GOALS

1. Understand the op amp golden rules and verify them experimentally with real circuits
2. Build and test 4 subcircuits: unity-gain inverter, variable-gain inverter, practical integrator, summing amplifier
3. For each subcircuit, predict V_out(t) from V_in(t) using the golden rules, then compare to measured oscilloscope data
4. Complete (or begin) Pre-lab Question 1: derive the ODE for the practical integrator and sketch solutions in three frequency regimes
5. Prepare for Session 2: understand how these subcircuits combine into the jerk circuit (Lab Script Fig. 1a)

---

## 2. APPARATUS

**Equipment** (Lab Script p. 5-6):

| Item | Details | Purpose |
|------|---------|---------|
| Breadboard | Built-in ±15 V and +5 V power supplies | Circuit construction and power |
| Function generator | Keysight 33210A or 33120A | AC input signals (sine, triangle, square) and DC offset |
| Oscilloscope | Siglent SDS2352X-E, 350 MHz, 2 GSa/s | Measure V_in and V_out simultaneously |
| Oscilloscope probes | High-impedance (×1 or ×10) | Monitor voltages without loading circuit |
| Op amps | LF411 (8-pin DIP) — drawers at back of room | Core amplifier element |
| Resistors | 10 kΩ (×4), 20 kΩ, 47 kΩ, 100 kΩ — back of room | Input, feedback, bleed-off resistors |
| Capacitors | 1 nF — back of room | Integrator feedback element |
| Cables/adapters | BNC cables, T-adapters, hook-up wire — back of room | Signal routing and connections |
| DC voltage source | Variable DC power supply, OR Keysight DC Volts mode (Utility > DC on) | Summing amplifier second input |
| Potentiometer | Available at bench | Create variable DC voltage divider |

> **Note:** Make sure oscilloscope probes are set correctly — check ×1 vs ×10 switch. Using ×10 when scope expects ×1 will show 10× too small.

---

## 3. VARIABLES

| Type | Variable | Values / Range | Description |
|------|----------|---------------|-------------|
| Independent | R₂/R₁ ratio | 1, 2, 4.7, 10 | Sets amplifier gain |
| Independent | Input frequency f | 100 Hz to 1 MHz | Tests integrator in different T/R₂C regimes |
| Independent | Input waveform | Triangle, square, sine | Different shapes for different experiments |
| Dependent | V_out(t) | Measured on oscilloscope | Output voltage waveform |
| Dependent | Gain G = V_out/V_in | Measured | Compared to golden rule prediction -R₂/R₁ |
| Dependent | Phase shift | Measured | Should be 180° for inverting configurations |
| Controlled | Power supply | ±15 V | Fixed op amp rails |
| Controlled | Op amp type | LF411 | Same chip for all experiments |

---

## 4. REFERENCES

**Primary Lab Documents:**

1. PHYS 332 Lab Script: "Chaotic Circuit" (PCH, revised Jan 2025) — Part I, pp. 3-7
2. K. Kiers, D. Schmidt, and J. C. Sprott, "Precision measurements of a simple chaotic circuit," *Am. J. Phys.* **72**, 503-509 (2004). (On Canvas)
3. Advanced Physics Laboratory Handout *Electronics Tips*. (On Canvas)

**Supplemental:**

4. P. Horowitz and W. Hill, *The Art of Electronics*, Ch. 4: "Feedback and Operational Amplifiers." (On Canvas)
5. S. H. Strogatz, *Nonlinear Dynamics and Chaos*, 2nd Ed., 2015. Ch. 1 (overview), Ch. 10 (bifurcation). (SFU Library)

---

## 5. BACKGROUND: OP AMP THEORY

*Reference: Lab Script pp. 3-5, Horowitz & Hill Ch. 4*

### 5.1 What Is an Op Amp?

An operational amplifier is a high-gain differential amplifier IC. Key properties (Lab Script p. 3-4):

- **High gain:** ~10^6 (open-loop)
- **High input impedance, low output impedance**
- **Supply:** ±15 V (or ±12 V)
- **Insensitive to temperature and power supply fluctuations**
- **Always used with feedback** in our circuits

The standard symbol is a sideways triangle. Two inputs: V_in,+ (non-inverting) and V_in,- (inverting). One output: V_out.

### 5.2 LF411 Pinout (DIP Package)

*Reference: Lab Script Fig. 2b*

Looking at the chip from above with the half-moon notch on the LEFT:

| Pin | Function |
|-----|----------|
| 1 | BALANCE (leave floating) |
| 2 | Inverting input (V_in,-) |
| 3 | Non-inverting input (V_in,+) |
| 4 | V⁻ → connect to -15 V |
| 5 | BALANCE (leave floating) |
| 6 | Output (V_out) |
| 7 | V⁺ → connect to +15 V |
| 8 | NC (no connection) |

> **Note:** Pins numbered counterclockwise from pin 1 (left of notch). Pin 8 is directly across from pin 1. NC and BALANCE pins are left floating — only 5 pins need connections.

### 5.3 The Op Amp Golden Rules

When used with **negative feedback**, ideal op amp circuits obey two rules (Lab Script p. 4):

1. **The inputs draw no current.** Input impedance is effectively infinite.
2. **The output drives V_in,+ = V_in,-.** The op amp adjusts its output to make the voltage difference between its two inputs zero.

> **CONCLUSION:** These two rules are sufficient to analyze ALL circuits in this lab. Apply Kirchhoff's current law at the inverting input node, using Golden Rule 1 (no current into op amp) and Golden Rule 2 (V_in,- = V_in,+).

**Clipping:** V_out cannot exceed the supply rails (±15 V). If the golden rules would require V_out > 15 V or V_out < -15 V, the output "clips" or "rails."

### 5.4 Example: Voltage Follower

*Reference: Lab Script Fig. 3*

Simplest circuit: V_in connected to pin 3 (non-inverting), pin 2 (inverting) connected directly to pin 6 (output).

By Golden Rule 2: V_in,- = V_in,+ → V_out = V_in.

Gain = 1, no inversion. Purpose: buffer a weak signal source (op amp can source more current than the original source).

---

## 6. PROCEDURE

### 6.1 Breadboard Setup

**Time:** (CC time)

1. Turn on breadboard power supply. Verify ±15 V and +5 V rails with multimeter or oscilloscope.
2. Run +15 V and -15 V along the long power rails of the breadboard. Verify continuity — some breadboards have breaks in the middle of the rail.
3. Insert LF411 chip with the half-moon notch on the LEFT side of the breadboard.
4. Wire power connections:
   - Pin 7 → +15 V rail
   - Pin 4 → -15 V rail
5. For now, wire pin 3 (non-inverting input) to GND.

> **Note:** Op amps are easily destroyed. If your circuit misbehaves, test the op amp by building a simple voltage follower. If V_out does not equal V_in, replace the chip. It's worth retesting with a fresh op amp each week (Lab Script p. 8).

> **[INSERT IMAGE - breadboard power setup photo]**

---

### 6.2 Experiment 1: Unity-Gain Inverting Amplifier

*Reference: Lab Script p. 6, top circuit diagram*

**Circuit:**
- R₁ = 10 kΩ (from V_in to pin 2)
- R₂ = 10 kΩ (from pin 2 to pin 6, feedback)
- Pin 3 → GND

**Expected behaviour:** Gain G = -R₂/R₁ = -(10 kΩ)/(10 kΩ) = **-1**. Output is inverted copy of input (180° phase shift), same amplitude.

**Golden Rule derivation:** By Rule 2, V_in,- = V_in,+ = 0 (pin 3 is grounded). By Rule 1, no current flows into pin 2. So by Kirchhoff at pin 2:

$$I_{in} = \frac{V_{in} - 0}{R_1} = \frac{0 - V_{out}}{R_2} = I_{feedback}$$

$$\Rightarrow V_{out} = -\frac{R_2}{R_1} V_{in}$$

**Procedure:**

1. Build the circuit on the breadboard with R₁ = R₂ = 10 kΩ
2. Record actual resistor values: R₁ = (CC measured) kΩ, R₂ = (CC measured) kΩ
3. Set function generator to **1 kHz triangle wave**, zero DC offset, amplitude ~1 V_pp
4. Use a **T-adapter and BNC cable** to split the function generator signal: one path to oscilloscope Ch1 (V_in), one path to the circuit input
5. Connect oscilloscope Ch2 probe to the circuit output (pin 6)
6. **Measure and record:**

| Parameter | Predicted | Measured |
|-----------|-----------|----------|
| V_in amplitude | (CC) V_pp | (CC) V_pp |
| V_out amplitude | (CC) V_pp | (CC) V_pp |
| Gain G = V_out/V_in | -1.000 | (CC) |
| Phase shift | 180° | (CC) |

7. Try different amplitudes (0.5 V, 2 V, 5 V). At what input amplitude does the output start clipping?

> **[INSERT IMAGE - Exp 1 oscilloscope screenshot: V_in (Ch1) and V_out (Ch2)]**

> **[INSERT IMAGE - Exp 1 circuit photo]**

**Analysis:** Does measured gain agree with -R₂/R₁? Quantify the % error. Is the 180° phase shift clean?

---

### 6.3 Experiment 2: Inverting Amplifier — Variable Gain

*Reference: Lab Script p. 6, second circuit diagram*

**Circuit:** Same as Experiment 1 but with different R₂ values. Keep R₁ = 10 kΩ fixed.

**Predicted gains:** G = -R₂/R₁

**Procedure:**

1. Keep the Experiment 1 circuit. Replace R₂ with different values.
2. For each R₂, use a 1 kHz triangle wave input at ~1 V_pp.
3. Measure V_out/V_in and compare to predicted gain.

<!-- Table 3: Inverting Amplifier Gain Measurements -->

| R₂ (kΩ) | R₂ actual (kΩ) | Predicted G | Measured G | % Error |
|----------|-----------------|-------------|------------|---------|
| 10 | (CC) | -1.00 | (CC) | (CC) |
| 20 | (CC) | -2.00 | (CC) | (CC) |
| 47 | (CC) | -4.70 | (CC) | (CC) |
| 100 | (CC) | -10.0 | (CC) | (CC) |

4. For G = -10 with 1 V_pp input: does the output clip? Reduce input amplitude if needed.
5. Experiment with different op amp types if available — do the golden rules still hold?

> **[INSERT IMAGE - Exp 2 oscilloscope screenshot for one gain setting]**

**Analysis:** Plot measured gain vs R₂/R₁. Should be a straight line with slope -1 through the origin. Does it deviate at high gains?

---

### 6.4 Experiment 3: Practical Integrator

*Reference: Lab Script p. 6, third circuit diagram; Pre-lab Question 1*

**Circuit:**
- R₁ = 10 kΩ (input resistor, from V_in to pin 2)
- C₁ = 1 nF (feedback capacitor, from pin 2 to pin 6)
- R₂ = 100 kΩ (bleed-off resistor, in parallel with C₁, from pin 2 to pin 6)
- Pin 3 → GND

**Key time constant:** R₂C₁ = (100 × 10³ Ω)(1 × 10⁻⁹ F) = **100 µs** → corresponding frequency f = 1/(2π R₂C₁) ≈ **1.6 kHz**

**Why R₂ is needed:** Without R₂, any small DC offset from the function generator or op amp will slowly charge C₁, causing V_out to drift ("rail") to +15 V or -15 V. R₂ provides a DC path that bleeds off this charge.

**Physics:** The output behaviour depends on the ratio of the signal period T to R₂C₁:

- **T ≫ R₂C₁** (f ≪ 1.6 kHz, e.g. **100 Hz**, T = 10 ms): The capacitor has time to fully charge and discharge through R₂ each half-cycle. Output resembles a **simple integral** of the input — for a square wave input, output is **triangular** (sawtooth-like).

- **T ≈ R₂C₁** (f ≈ 1.6 kHz, e.g. **10 kHz**, T = 100 µs): Intermediate behaviour. Output is a mix of integrator and resistive divider characteristics.

- **T ≪ R₂C₁** (f ≫ 1.6 kHz, e.g. **500 kHz**, T = 2 µs): The capacitor barely charges in each half-cycle. C₁ acts almost like an open circuit at these frequencies, so the circuit behaves more like a simple resistive inverting amplifier with gain set by the impedance ratio.

**Procedure:**

1. Build the circuit: R₁ = 10 kΩ, C₁ = 1 nF, R₂ = 100 kΩ (in parallel with C₁)
2. Record actual values: R₁ = (CC), C₁ = (CC), R₂ = (CC)
3. Input: **square wave**, ~1 V_pp, zero DC offset

4. **Low frequency — T ≫ R₂C (integrating regime):**
   - Set f = **100 Hz** (T = 10 ms ≫ 100 µs)
   - Record V_in (Ch1) and V_out (Ch2)
   - Expected: V_out is a **triangular wave** (integral of square wave)

5. **Mid frequency — T ≈ R₂C:**
   - Set f = **10 kHz** (T = 100 µs ≈ R₂C)
   - Record V_in and V_out
   - Expected: intermediate shape — exponential charging/discharging visible

6. **High frequency — T ≪ R₂C:**
   - Set f = **500 kHz** (T = 2 µs ≪ 100 µs)
   - Record V_in and V_out
   - Expected: output is small, mostly determined by capacitive impedance

> **[INSERT IMAGE - Exp 3 oscilloscope: low frequency (100 Hz)]**

> **[INSERT IMAGE - Exp 3 oscilloscope: mid frequency (10 kHz)]**

> **[INSERT IMAGE - Exp 3 oscilloscope: high frequency (500 kHz)]**

7. **DC offset test (without R₂):**
   - Remove R₂ from the circuit (pure integrator)
   - Apply a small DC offset on the function generator
   - Observe: V_out drifts to a rail (±15 V) — this is the problem R₂ prevents
   - Re-insert R₂ and confirm stability returns

**Analysis:** Compare observed waveforms to the analytical solution from Pre-lab Q1. Does the transition between regimes happen near f ≈ 1/(2π R₂C₁)?

---

### 6.5 Experiment 4: Summing Amplifier

*Reference: Lab Script p. 6, bottom circuit diagram*

**Circuit:**
- Two input resistors: R_a = R_b = 10 kΩ (or any equal value)
- Feedback resistor: R_f = R_a = 10 kΩ
- V_in,1 → through R_a → pin 2
- V_in,2 → through R_b → pin 2
- R_f from pin 2 to pin 6
- Pin 3 → GND

**Expected behaviour:** V_out = -(V_in,1 + V_in,2) when R_a = R_b = R_f

**Golden Rule derivation:** V_in,- = V_in,+ = 0 (virtual ground). By Kirchhoff at pin 2:

$$\frac{V_{in,1}}{R_a} + \frac{V_{in,2}}{R_b} + \frac{V_{out}}{R_f} = 0$$

$$V_{out} = -R_f \left(\frac{V_{in,1}}{R_a} + \frac{V_{in,2}}{R_b}\right) = -(V_{in,1} + V_{in,2})$$

**Procedure:**

1. Build the circuit with R_a = R_b = R_f = 10 kΩ
2. Record actual values: R_a = (CC), R_b = (CC), R_f = (CC)
3. **Input 1:** Function generator → 1 kHz sine wave, ~1 V_pp, zero DC offset
4. **Input 2:** DC voltage. Options:
   - Use the variable DC power supply
   - OR use function generator DC Volts mode (Utility > DC on, on Keysight 33210A)
   - OR create a potentiometer voltage divider from the +5 V rail to get a variable 0-5 V DC
5. Set V_in,2 = 0 V DC. Measure V_out — should be inverted copy of V_in,1
6. Increase V_in,2 to +1 V DC. Observe: output waveform shifts DOWN by 1 V (inverted sum)
7. Set V_in,2 = -1 V DC. Observe: output shifts UP by 1 V

<!-- Table 4: Summing Amplifier Measurements -->

| V_in,1 (AC, V_pp) | V_in,2 (DC, V) | V_out predicted | V_out measured |
|-----|------|--------|---------|
| 1.0 | 0.0 | -1.0 V_pp, centered at 0 | (CC) |
| 1.0 | +1.0 | -1.0 V_pp, centered at -1.0 V | (CC) |
| 1.0 | +2.0 | -1.0 V_pp, centered at -2.0 V | (CC) |
| 1.0 | -1.0 | -1.0 V_pp, centered at +1.0 V | (CC) |

> **[INSERT IMAGE - Exp 4 oscilloscope: AC + DC summing]**

**Analysis:** Does the DC offset shift the output by exactly the predicted amount? Does the AC amplitude stay the same regardless of DC offset?

---

## 7. PRE-LAB QUESTION 1

*Due: by the end of Session 1 OR before starting Session 2 (Lab Script p. 7)*

**The practical integrator (Experiment 3) is not exactly an integrator. Analyze it:**

### 7.1 Part (i): Derive the ODE

Derive the differential equation relating V_out(t) to V_in(t) for the practical integrator circuit (R₁, C₁, R₂).

*Hint:* Apply Golden Rules at pin 2. Current through R₁ = current through C₁ + current through R₂.

$$\frac{V_{in}}{R_1} = -C_1 \frac{dV_{out}}{dt} - \frac{V_{out}}{R_2}$$

Rearranging:

$$R_1 C_1 \frac{dV_{out}}{dt} + \frac{R_1}{R_2} V_{out} = -V_{in}$$

(CC — show full derivation here)

### 7.2 Part (ii): Solve for V_out(t)

The ODE is first-order linear. Use integrating factor or Laplace transform.

(CC — show solution)

### 7.3 Part (iii): Sketch Solutions for Three Regimes

For V_in(t) = square wave with period T and zero mean:

- **T ≫ R₂C₁:** output ≈ (CC sketch)
- **T ≈ R₂C₁:** output ≈ (CC sketch)
- **T ≪ R₂C₁:** output ≈ (CC sketch)

*Hint:* In the limit R₂ → ∞ (no bleed-off), the ODE reduces to V_out = -(1/R₁C₁)∫V_in dt — pure integrator. In the limit R₂ → 0, the capacitor is shorted and the circuit is just a resistive divider.

### 7.4 Part (iv): What Problem Does R₂ Prevent?

(CC — answer: prevents DC charge accumulation on C₁ from input offset voltages, which would cause V_out to rail to ±15 V)

---

## 8. ANALYSIS

### 8.1 Golden Rule Verification Summary

<!-- Table 5: Summary of All Experiments -->

| Experiment | Predicted | Measured | Agreement? |
|------------|-----------|----------|------------|
| Exp 1: Unity gain | G = -1.000 | (CC) | (CC) |
| Exp 2: Gain = -2 | G = -2.000 | (CC) | (CC) |
| Exp 2: Gain = -4.7 | G = -4.700 | (CC) | (CC) |
| Exp 2: Gain = -10 | G = -10.00 | (CC) | (CC) |
| Exp 3: Integrator (low f) | Triangular output | (CC) | (CC) |
| Exp 3: Integrator (mid f) | Intermediate | (CC) | (CC) |
| Exp 3: Integrator (high f) | Small output | (CC) | (CC) |
| Exp 4: Sum (DC=0) | Inverted AC | (CC) | (CC) |
| Exp 4: Sum (DC=+1V) | Shifted -1 V | (CC) | (CC) |

### 8.2 Deviations from Ideal Behaviour

(CC — note any discrepancies: finite gain, input offset voltage, slew rate limits at high frequency, etc.)

---

## 9. CONCLUSIONS

(CC — summarize: did the golden rules hold? Which experiment showed the most deviation from ideal? What did you learn about op amp limitations?)

---

## 10. PLAN FOR NEXT SESSION

**Session 2 — Lab Period 2** (Lab Script Suggested Timeline):

1. **Hand in Pre-lab Question 1** (if not completed today)
2. **Build and test the nonlinear element D(x)** — the piecewise-linear function that makes the jerk circuit chaotic (Lab Script p. 7, Fig. 1b)
   - Use 1N4148 or 1N914 diodes
   - R₁ and R₂ in the 10's of kΩ, ratio R₂/R₁ ≈ 6
   - Test with 1 kHz sawtooth ramp input, observe D(x) = -(R₂/R₁)·min(x, 0)
3. **Begin Pre-lab Question 2:** Derive Eqs. 2-6 from Kiers et al. using the full circuit diagram (Lab Script Fig. 1a)

**Data files from today:** (CC — list oscilloscope save files)
