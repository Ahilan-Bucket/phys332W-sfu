#!/usr/bin/env python3
"""
diffusion_calculator.py — Stokes-Einstein Diffusion Coefficient Calculator
==========================================================================
Replicates Nathan's "Diffusion Coefficient Calculator 2026-03-02.xlsx"
with corrected Cheng (2008) viscosity formula.

Calculates theoretical D with:
  - Stokes-Einstein base:        D₀ = k_BT / (6πηr)
  - Faxén wall correction:       D_∥ = D₀ × [1 - 9/16(R/h) + 1/8(R/h)³ - ...]
  - Batchelor concentration:     η_eff = η₀(1 + 2.5φ + 6.2φ²)

Usage:
    from diffusion_calculator import predict_D, print_predictions, predict_all

    # Single prediction
    result = predict_D(bead_um=3.0, viscosity_mPas=1.027, temp_C=21.0)
    print(result)

    # Full matrix (like Nathan's spreadsheet)
    print_predictions(temp_C=21.0)

Author: Ahilan Kumaresan
"""

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

# ─── Constants ───────────────────────────────────────────────────────────
k_B = 1.380649e-23          # Boltzmann constant (J/K), exact CODATA 2018
RHO_PS = 1.05               # Polystyrene density (g/cm³)
STOCK_CONC = 0.005           # Stock bead concentration (0.5% by weight)
CHAMBER_DEPTH_UM = 82.5      # Tape spacer chamber depth (µm)


# ─── Viscosity Functions (CORRECTED) ────────────────────────────────────

def _water_viscosity_mPas(temp_C: float) -> float:
    """Pure water dynamic viscosity in mPa·s. Cheng (2008) Eq. for water."""
    T = temp_C
    return 1.790 * math.exp((-1230 - T) * T / (36100 + 360 * T))


def _glycerol_viscosity_mPas(temp_C: float) -> float:
    """Pure glycerol dynamic viscosity in mPa·s. Cheng (2008)."""
    T = temp_C
    return 12100.0 * math.exp((-1233 + T) * T / (9900 + 70 * T))


def cheng_glycerol_water(glycerol_mass_pct: float, temp_C: float) -> float:
    """
    Glycerol-water mixture viscosity using Cheng (2008) formula.

    CORRECTED implementation:
        η_m = η_w^α × η_g^(1-α)
        α = 1 - c_m + (a·b·c_m·(1-c_m)) / (a·c_m + b·(1-c_m))
        a = 0.705 - 0.0017·T
        b = (4.9 + 0.036·T) · a^2.5

    Parameters:
        glycerol_mass_pct: Glycerol mass fraction as percentage (0-100)
        temp_C: Temperature in °C

    Returns:
        Dynamic viscosity in mPa·s
    """
    eta_w = _water_viscosity_mPas(temp_C)
    if glycerol_mass_pct <= 0:
        return eta_w
    eta_g = _glycerol_viscosity_mPas(temp_C)
    cm = glycerol_mass_pct / 100.0

    a = 0.705 - 0.0017 * temp_C
    b = (4.9 + 0.036 * temp_C) * a ** 2.5
    alpha = 1.0 - cm + (a * b * cm * (1 - cm)) / (a * cm + b * (1 - cm))

    eta_m = eta_w ** alpha * eta_g ** (1 - alpha)
    return eta_m


def acetone_water_viscosity(acetone_vol_pct: float, temp_C: float) -> float:
    """
    Acetone-water mixture viscosity via interpolation.
    Based on Howard & McAllister (1958) data at ~20-25°C.

    Parameters:
        acetone_vol_pct: Acetone volume fraction as percentage (0-100)
        temp_C: Temperature in °C (used for pure water baseline)

    Returns:
        Dynamic viscosity in mPa·s
    """
    if acetone_vol_pct <= 0:
        return _water_viscosity_mPas(temp_C)

    # Interpolation table: (vol%, viscosity in mPa·s at ~21°C)
    vol_pct = np.array([0, 5, 10, 15, 20, 30, 40, 50, 60, 80, 100])
    eta_mPa = np.array([0.978, 0.94, 0.90, 0.86, 0.82, 0.72, 0.62,
                         0.52, 0.44, 0.36, 0.32])

    return float(np.interp(acetone_vol_pct, vol_pct, eta_mPa))


def get_viscosity_mPas(solvent: str, concentration_pct: float,
                       temp_C: float) -> float:
    """
    Get mixture viscosity in mPa·s.

    Parameters:
        solvent: "water", "glycerol", or "acetone"
        concentration_pct: Solute percentage (mass% for glycerol, vol% for acetone)
        temp_C: Temperature in °C

    Returns:
        Dynamic viscosity in mPa·s
    """
    solvent = solvent.lower().strip()
    if solvent == "water":
        return _water_viscosity_mPas(temp_C)
    elif solvent == "glycerol":
        return cheng_glycerol_water(concentration_pct, temp_C)
    elif solvent == "acetone":
        return acetone_water_viscosity(concentration_pct, temp_C)
    else:
        raise ValueError(f"Unknown solvent: {solvent!r}")


# ─── Correction Factors ────────────────────────────────────────────────

def faxen_correction(bead_radius_m: float, wall_dist_m: float) -> float:
    """
    Faxén's Law parallel wall correction for diffusion near a surface.

    D_∥ = D₀ × F(R/h)
    F = 1 - (9/16)(R/h) + (1/8)(R/h)³ - (45/256)(R/h)⁴ - (1/16)(R/h)⁵

    Parameters:
        bead_radius_m: Bead radius R in metres
        wall_dist_m: Distance from bead centre to nearest wall h, in metres

    Returns:
        Correction factor (multiply D₀ by this; always ≤ 1)
    """
    x = bead_radius_m / wall_dist_m  # R/h
    return 1 - 9/16 * x + 1/8 * x**3 - 45/256 * x**4 - 1/16 * x**5


def batchelor_viscosity_ratio(phi: float) -> float:
    """
    Batchelor correction for suspension viscosity.
    η_eff = η₀ × (1 + 2.5φ + 6.2φ²)

    Returns the ratio η_eff/η₀.
    """
    return 1 + 2.5 * phi + 6.2 * phi**2


# ─── Main Calculator ───────────────────────────────────────────────────

@dataclass
class DPrediction:
    """Result from predict_D()."""
    bead_um: float
    solvent: str
    solute_pct: float
    temp_C: float
    temp_K: float
    eta_mPas: float               # Mixture viscosity
    D0_um2s: float                # Base Stokes-Einstein D
    phi: float                    # Volume fraction
    batchelor_ratio: float        # η_eff/η₀
    faxen_mid: float              # Faxén factor at chamber midplane
    faxen_quarter: float          # Faxén factor at quarter-depth
    D_high_um2s: float            # D with min wall correction (midplane)
    D_low_um2s: float             # D with max wall correction (quarter)
    MSD_slope_high: float         # 4×D_high (2D MSD slope)
    MSD_slope_low: float          # 4×D_low

    def __str__(self):
        return (
            f"{self.bead_um} µm beads in {self.solvent} "
            f"({self.solute_pct}%) at {self.temp_C}°C\n"
            f"  η = {self.eta_mPas:.3f} mPa·s\n"
            f"  D₀ (Stokes-Einstein)  = {self.D0_um2s:.4f} µm²/s\n"
            f"  φ = {self.phi:.2e}, Batchelor = {self.batchelor_ratio:.6f}\n"
            f"  Faxén (mid/quarter)   = {self.faxen_mid:.4f} / {self.faxen_quarter:.4f}\n"
            f"  D_final (high–low)    = {self.D_high_um2s:.4f} – {self.D_low_um2s:.4f} µm²/s\n"
            f"  MSD slope (high–low)  = {self.MSD_slope_high:.4f} – {self.MSD_slope_low:.4f} µm²/s"
        )


def predict_D(
    bead_um: float,
    viscosity_mPas: Optional[float] = None,
    solvent: str = "water",
    solute_pct: float = 0.0,
    temp_C: float = 21.0,
    stock_vol_uL: Optional[float] = None,
    total_vol_uL: float = 500.0,
    chamber_depth_um: float = CHAMBER_DEPTH_UM,
) -> DPrediction:
    """
    Predict diffusion coefficient with all corrections.

    Matches Nathan's spreadsheet exactly when using his input values.

    Parameters:
        bead_um:          Bead diameter in µm (e.g. 1.0, 2.0, 3.0, 5.0)
        viscosity_mPas:   Override viscosity (mPa·s). If None, calculated from solvent.
        solvent:          "water", "glycerol", or "acetone"
        solute_pct:       Solute concentration (mass% for glycerol, vol% for acetone)
        temp_C:           Temperature in °C
        stock_vol_uL:     Volume of 0.5% bead stock used (µL). If None, uses Nathan's
                          defaults per bead size.
        total_vol_uL:     Total sample volume (µL)
        chamber_depth_um: Chamber depth (µm)

    Returns:
        DPrediction dataclass with all calculated values
    """
    # Temperature
    T_K = temp_C + 273.15

    # Bead geometry
    d_m = bead_um * 1e-6
    r_m = d_m / 2

    # Viscosity
    if viscosity_mPas is not None:
        eta = viscosity_mPas
    else:
        eta = get_viscosity_mPas(solvent, solute_pct, temp_C)
    eta_Pa = eta * 1e-3

    # Wall distance (centre of chamber)
    h_mid = (chamber_depth_um / 2) * 1e-6      # midplane
    h_quarter = (chamber_depth_um / 4) * 1e-6   # quarter depth (closer to wall)

    # Faxén corrections
    F_mid = faxen_correction(r_m, h_mid)
    F_quarter = faxen_correction(r_m, h_quarter)

    # Volume fraction φ
    # Default stock volumes per bead size (from Nathan's spreadsheet)
    if stock_vol_uL is None:
        if bead_um <= 1.5:
            stock_vol_uL = 1.15   # 1 µm beads: 1.15 µL
        elif bead_um <= 2.5:
            stock_vol_uL = 2.0    # 2 µm beads: 2 µL
        elif bead_um <= 4.0:
            stock_vol_uL = 3.0    # 3 µm beads: 3 µL
        else:
            stock_vol_uL = 10.0   # 5 µm beads: 10 µL

    V_stock_L = stock_vol_uL * 1e-6
    V_total_L = total_vol_uL * 1e-6
    phi = STOCK_CONC * (V_stock_L / V_total_L) / RHO_PS

    # Batchelor correction
    M = batchelor_viscosity_ratio(phi)

    # Stokes-Einstein D₀
    D0_m2s = k_B * T_K / (6 * math.pi * M * eta_Pa * r_m)
    D0_um2s = D0_m2s * 1e12

    # Final D with wall corrections
    D_high = D0_um2s * F_mid
    D_low = D0_um2s * F_quarter

    return DPrediction(
        bead_um=bead_um,
        solvent=solvent if solute_pct > 0 else "water",
        solute_pct=solute_pct,
        temp_C=temp_C,
        temp_K=T_K,
        eta_mPas=eta,
        D0_um2s=D0_um2s,
        phi=phi,
        batchelor_ratio=M,
        faxen_mid=F_mid,
        faxen_quarter=F_quarter,
        D_high_um2s=D_high,
        D_low_um2s=D_low,
        MSD_slope_high=4 * D_high,
        MSD_slope_low=4 * D_low,
    )


# ─── Full Matrix (Nathan's 16-sample table) ────────────────────────────

# Nathan's exact configurations: (bead_um, solvent, solute_pct, eta_mPas_at_19C)
NATHAN_SAMPLES = [
    # Sample, bead_um, solvent, pct, Nathan's eta (mPa·s at 19°C)
    ("S1",  1.0, "acetone",  100,  0.322),
    ("S2",  1.0, "water",      0,  1.027),
    ("S3",  1.0, "glycerol",  20,  1.95),
    ("S4",  1.0, "glycerol",  40,  4.45),
    ("S5",  2.0, "acetone",  100,  0.322),
    ("S6",  2.0, "water",      0,  1.027),
    ("S7",  2.0, "glycerol",  20,  1.95),
    ("S8",  2.0, "glycerol",  40,  4.45),
    ("S9",  3.0, "acetone",  100,  0.322),
    ("S10", 3.0, "water",      0,  1.027),
    ("S11", 3.0, "glycerol",  20,  1.95),
    ("S12", 3.0, "glycerol",  40,  4.45),
    ("S13", 5.0, "acetone",  100,  0.322),
    ("S14", 5.0, "water",      0,  1.027),
    ("S15", 5.0, "glycerol",  20,  1.95),
    ("S16", 5.0, "glycerol",  40,  4.45),
]


def predict_all(temp_C: float = 19.0, use_nathan_viscosities: bool = True):
    """
    Generate predictions for all 16 conditions (Nathan's full matrix).

    Parameters:
        temp_C: Temperature in °C (Nathan uses 19°C)
        use_nathan_viscosities: If True, use Nathan's manually-entered η values.
                                If False, calculate η from Cheng (2008) / interpolation.

    Returns:
        List of (sample_name, DPrediction) tuples
    """
    results = []
    for name, bead, solvent, pct, eta_nathan in NATHAN_SAMPLES:
        eta_override = eta_nathan if use_nathan_viscosities else None
        pred = predict_D(
            bead_um=bead,
            viscosity_mPas=eta_override,
            solvent=solvent,
            solute_pct=pct,
            temp_C=temp_C,
        )
        results.append((name, pred))
    return results


def print_predictions(temp_C: float = 19.0, use_nathan_viscosities: bool = True):
    """Print the full 16-sample prediction table."""
    results = predict_all(temp_C, use_nathan_viscosities)

    src = "Nathan's η" if use_nathan_viscosities else "Cheng (2008)"
    print(f"Diffusion Coefficient Predictions — T = {temp_C}°C, viscosity from {src}")
    print("=" * 110)
    print(f"{'Sample':>6} {'Bead':>5} {'Solvent':>15} {'η (mPa·s)':>10} "
          f"{'D₀':>10} {'Faxén':>7} {'D_high':>10} {'D_low':>10} "
          f"{'MSD_high':>10} {'MSD_low':>10}")
    print(f"{'':>6} {'(µm)':>5} {'':>15} {'':>10} "
          f"{'(µm²/s)':>10} {'(mid)':>7} {'(µm²/s)':>10} {'(µm²/s)':>10} "
          f"{'(µm²/s)':>10} {'(µm²/s)':>10}")
    print("-" * 110)

    for name, p in results:
        solvent_str = f"{p.solute_pct:.0f}% {p.solvent}" if p.solute_pct > 0 else "Water"
        print(f"{name:>6} {p.bead_um:>5.1f} {solvent_str:>15} {p.eta_mPas:>10.3f} "
              f"{p.D0_um2s:>10.4f} {p.faxen_mid:>7.4f} {p.D_high_um2s:>10.4f} "
              f"{p.D_low_um2s:>10.4f} {p.MSD_slope_high:>10.4f} {p.MSD_slope_low:>10.4f}")

    print()


# ─── Convenience: Session 6 actual conditions ──────────────────────────

SESSION_6_SLIDES = [
    # (name, bead_um, solvent, pct, stock_uL, total_uL)
    ("s1b", 3.0, "water",    0.0,  2.5,  600.0),
    ("s2a", 1.0, "glycerol", 20.0, 2.3,  5000.0),
    ("s2b", 3.0, "glycerol", 20.0, 2.3,  5000.0),
    ("s2c", 1.0, "glycerol", 20.0, 11.5, 5000.0),
    ("s3",  3.0, "glycerol", 20.0, 3.0,  500.0),
    ("s7",  3.0, "glycerol", 36.3, 3.8,  500.0),
    ("s9",  3.0, "acetone",  40.0, 24.0, 2000.0),
]


def print_session6_predictions(temp_C: float = 21.0):
    """Print predictions for actual Session 6 slide conditions."""
    print(f"Session 6 Predictions — T = {temp_C}°C, Cheng (2008) corrected viscosity")
    print("=" * 105)
    print(f"{'Slide':>6} {'Bead':>5} {'Solvent':>15} {'η (mPa·s)':>10} "
          f"{'D₀':>10} {'D_high':>10} {'D_low':>10} {'MSD_high':>10} {'φ':>12}")
    print("-" * 105)

    for name, bead, solvent, pct, stock_uL, total_uL in SESSION_6_SLIDES:
        p = predict_D(
            bead_um=bead,
            solvent=solvent,
            solute_pct=pct,
            temp_C=temp_C,
            stock_vol_uL=stock_uL,
            total_vol_uL=total_uL,
        )
        solvent_str = f"{pct:.0f}% {solvent}" if pct > 0 else "Water"
        print(f"{name:>6} {bead:>5.1f} {solvent_str:>15} {p.eta_mPas:>10.3f} "
              f"{p.D0_um2s:>10.4f} {p.D_high_um2s:>10.4f} {p.D_low_um2s:>10.4f} "
              f"{p.MSD_slope_high:>10.4f} {p.phi:>12.2e}")

    print()


# ─── CLI ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 60)
    print("  DIFFUSION COEFFICIENT CALCULATOR")
    print("  Replicates Nathan's Excel + corrected viscosity")
    print("=" * 60)
    print()

    # 1) Nathan's table at 19°C with his viscosity values
    print("─── Nathan's Original Table (19°C, his η values) ───")
    print_predictions(temp_C=19.0, use_nathan_viscosities=True)

    # 2) Same conditions but with corrected Cheng formula
    print("─── Same conditions, Cheng (2008) CORRECTED η (19°C) ───")
    print_predictions(temp_C=19.0, use_nathan_viscosities=False)

    # 3) Session 6 actual conditions at 21°C
    print("─── Session 6 Actual Conditions (21°C) ───")
    print_session6_predictions(temp_C=21.0)

    # 4) Show viscosity comparison
    print("─── Viscosity Comparison: Nathan vs Cheng (2008) CORRECTED ───")
    print(f"{'Condition':>20} {'Nathan η':>12} {'Cheng η':>12} {'Ratio':>8}")
    print("-" * 55)
    for label, pct, solvent, eta_N in [
        ("Water",        0,   "water",    1.027),
        ("20% glycerol", 20,  "glycerol", 1.95),
        ("40% glycerol", 40,  "glycerol", 4.45),
        ("Pure acetone", 100, "acetone",  0.322),
        ("40% acetone",  40,  "acetone",  None),
    ]:
        eta_C = get_viscosity_mPas(solvent, pct, 19.0)
        nstr = f"{eta_N:.3f}" if eta_N else "---"
        rstr = f"{eta_N/eta_C:.2f}x" if eta_N else "---"
        print(f"{label:>20} {nstr:>12} {eta_C:>12.3f} {rstr:>8}")
    print()
