"""
Generate three publication-quality plots of a practical integrator circuit response
to a zero-mean square wave input, one for each frequency regime.

ODE: R1*C1*(dV_out/dt) + (R1/R2)*V_out = -V_in
Rewritten: tau*(dV_out/dt) + V_out = -(R2/R1)*V_in   where tau = R2*C1

Piecewise solution (V_in constant each half-period):
    V_out(t) = V_ss + (V_0 - V_ss) * exp(-t / tau)
    where V_ss = -(R2/R1)*V_in

Component values: R1 = 10 kOhm, R2 = 1 MOhm, C1 = 100 nF
tau = R2*C1 = 100 us (as stated in problem), gain = R2/R1 = 100
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'lines.linewidth': 1.8,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.linestyle': '-',
    'grid.linewidth': 0.5,
})

# Circuit parameters
R1 = 10e3       # 10 kOhm
R2 = 1e6        # 1 MOhm
C1 = 100e-9     # 100 nF
tau = 100e-6    # 100 us (R2*C1, as stated)
gain = R2 / R1  # 100
V0 = 1.0        # square wave amplitude

OUT_DIR = r"D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab3-Chaotic-Circuits\Notes\Images"


def solve_integrator(T_us, n_periods=5, pts_per_half=2000):
    """
    Solve the practical integrator ODE piecewise for a square wave of period T.
    Returns time (us), V_in, V_out arrays.
    """
    T = T_us * 1e-6
    half_T = T / 2.0

    # Find steady-state initial condition by iterating many periods
    V_curr = 0.0
    for i in range(200):
        V_in_val = V0 if (i % 2 == 0) else -V0
        V_ss = -gain * V_in_val
        V_curr = V_ss + (V_curr - V_ss) * np.exp(-half_T / tau)

    # Generate waveform
    t_all, v_in_all, v_out_all = [], [], []
    n_halves = 2 * n_periods

    for i in range(n_halves):
        V_in_val = V0 if (i % 2 == 0) else -V0
        V_ss = -gain * V_in_val
        t_local = np.linspace(0, half_T, pts_per_half, endpoint=False)
        v_out_local = V_ss + (V_curr - V_ss) * np.exp(-t_local / tau)

        t_all.append(t_local + i * half_T)
        v_in_all.append(np.full_like(t_local, V_in_val))
        v_out_all.append(v_out_local)

        V_curr = V_ss + (V_curr - V_ss) * np.exp(-half_T / tau)

    t = np.concatenate(t_all) * 1e6  # to us
    v_in = np.concatenate(v_in_all)
    v_out = np.concatenate(v_out_all)
    return t, v_in, v_out


def make_plot(T_us, title, filename):
    t, v_in, v_out = solve_integrator(T_us, n_periods=5)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 4.5), sharex=True,
                                    gridspec_kw={'height_ratios': [1, 2], 'hspace': 0.08})

    # Top: V_in
    ax1.plot(t, v_in, 'k-', linewidth=1.2, label=r'$V_{\mathrm{in}}(t)$')
    ax1.set_ylabel(r'$V_{\mathrm{in}}$ (V)')
    vin_margin = V0 * 0.3
    ax1.set_ylim(-V0 - vin_margin, V0 + vin_margin)
    ax1.legend(loc='upper right', framealpha=0.9)
    ax1.set_title(title)
    ax1.tick_params(labelbottom=False)

    # Bottom: V_out
    ax2.plot(t, v_out, 'C0-', linewidth=1.8, label=r'$V_{\mathrm{out}}(t)$')
    ax2.set_xlabel(r'Time ($\mu$s)')
    ax2.set_ylabel(r'$V_{\mathrm{out}}$ (V)')
    ax2.legend(loc='upper right', framealpha=0.9)
    ax2.set_xlim(t[0], t[-1])

    # Auto y-limits with margin
    vmin, vmax = v_out.min(), v_out.max()
    vrange = vmax - vmin if vmax > vmin else 1.0
    margin = vrange * 0.15
    ax2.set_ylim(vmin - margin, vmax + margin)

    fig.tight_layout()
    path = f"{OUT_DIR}\\{filename}"
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {path}")
    print(f"  V_out range: [{vmin:.3f}, {vmax:.3f}] V")


# --- Generate the three plots ---

make_plot(
    T_us=2000,
    title=r'$T \gg \tau$  :  Practical Integrator  ($T = 2000\,\mu$s, $\tau = 100\,\mu$s)',
    filename='Prelab-Q1-T-much-greater-tau.png',
)

make_plot(
    T_us=200,
    title=r'$T \approx \tau$  :  Practical Integrator  ($T = 200\,\mu$s, $\tau = 100\,\mu$s)',
    filename='Prelab-Q1-T-approx-tau.png',
)

make_plot(
    T_us=20,
    title=r'$T \ll \tau$  :  Practical Integrator  ($T = 20\,\mu$s, $\tau = 100\,\mu$s)',
    filename='Prelab-Q1-T-much-less-tau.png',
)

print("\nAll plots generated successfully.")
