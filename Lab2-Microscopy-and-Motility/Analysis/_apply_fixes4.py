"""Fix STEP 4 (displacement analysis) and STEP 5 (MSD) in Cell 3.

Changes:
  STEP 4:
    1. Sigma-clip outliers (iterative 3-sigma) before D_variance
    2. Freedman-Diaconis auto-bins + density=True histogram
    3. Fit normalized Gaussian PDF instead of raw-count Gaussian
    4. Per-segment D estimates for proper error bars (SEM)

  STEP 5:
    5. Fix lag_times offset: (arange+1)*dt instead of arange*dt

  Gaussian function:
    6. Add gaussian_pdf() alongside existing gaussian()
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

NB_PATH = r'D:\Documents\SFU\PHYS382-AdvancedLab\phys332w-sfu-GIT\phys332W-sfu\Lab2-Microscopy-and-Motility\Analysis\Lab2_Analysis_Pipeline.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

def get_src(idx):
    s = nb['cells'][idx]['source']
    return ''.join(s) if isinstance(s, list) else s

def set_src(idx, s):
    nb['cells'][idx]['source'] = s

# =====================================================================
# FIX 1: Add gaussian_pdf to Cell 2 (after existing gaussian function)
# =====================================================================
cell2 = get_src(2)

old_gaussian_block = (
    "def gaussian(x, amplitude, mean, std_dev):\n"
    "    return amplitude * np.exp(-(x - mean)**2 / (2 * std_dev**2))"
)

new_gaussian_block = (
    "def gaussian(x, amplitude, mean, std_dev):\n"
    "    return amplitude * np.exp(-(x - mean)**2 / (2 * std_dev**2))\n"
    "\n"
    "def gaussian_pdf(x, mean, std_dev):\n"
    "    \"\"\"Normalized Gaussian probability density function.\n"
    "    Use with density=True histograms so the fit area = 1.\"\"\"\n"
    "    return (1.0 / (np.sqrt(2 * np.pi) * abs(std_dev))) * np.exp(-(x - mean)**2 / (2 * std_dev**2))\n"
    "\n"
    "def sigma_clip(arr, sigma=3, max_iter=5):\n"
    "    \"\"\"Iterative sigma-clipping. Returns clipped array.\"\"\"\n"
    "    a = np.array(arr, dtype=float)\n"
    "    for _ in range(max_iter):\n"
    "        mu = np.mean(a)\n"
    "        sd = np.std(a)\n"
    "        if sd == 0:\n"
    "            break\n"
    "        mask = np.abs(a - mu) < sigma * sd\n"
    "        if mask.all():\n"
    "            break\n"
    "        a = a[mask]\n"
    "    return a"
)

if old_gaussian_block in cell2:
    cell2 = cell2.replace(old_gaussian_block, new_gaussian_block)
    print('FIX 1: Added gaussian_pdf() and sigma_clip() to Cell 2')
else:
    print('ERROR: Could not find gaussian function in Cell 2')

set_src(2, cell2)

# =====================================================================
# FIX 2: Replace STEP 4 in Cell 3
# =====================================================================
cell3 = get_src(3)

# Find the STEP 4 block boundaries
step4_start = "        # ==============================================================\n        # STEP 4: DISPLACEMENT HISTOGRAM + GAUSSIAN FIT"
step4_end = "        # ==============================================================\n        # STEP 5: MSD ANALYSIS + ALPHA EXPONENT"

idx_start = cell3.find(step4_start)
idx_end = cell3.find(step4_end)

if idx_start < 0 or idx_end < 0:
    print(f'ERROR: Could not find STEP 4 boundaries (start={idx_start}, end={idx_end})')
else:
    new_step4 = r"""        # ==============================================================
        # STEP 4: DISPLACEMENT HISTOGRAM + GAUSSIAN FIT
        # ==============================================================
        print(f'  STEP 4: Displacement analysis...')
        all_dx = []
        all_dy = []
        for seg in selected:
            all_dx.extend(np.diff(seg['x']))
            all_dy.extend(np.diff(seg['y']))

        dx_px = np.array(all_dx)
        dy_px = np.array(all_dy)
        dx_um = dx_px * PIXEL_SIZE
        dy_um = dy_px * PIXEL_SIZE
        n_steps = len(dx_px)

        # --- METHOD 1: Direct Variance (with sigma-clipping) ---
        # Tracking artifacts create outlier displacements (e.g. bead-to-bead
        # mis-links).  Iterative 3-sigma clipping removes these before
        # computing variance, so D_variance measures the THERMAL motion,
        # not the tracking noise.
        dx_clipped = sigma_clip(dx_um, sigma=3, max_iter=5)
        dy_clipped = sigma_clip(dy_um, sigma=3, max_iter=5)
        n_clipped = n_steps - len(dx_clipped) + n_steps - len(dy_clipped)
        if n_clipped > 0:
            print(f'    Sigma-clip removed {n_clipped} outlier steps '
                  f'({n_clipped/(2*n_steps)*100:.1f}%)')

        var_dx = np.var(dx_clipped)
        var_dy = np.var(dy_clipped)
        D_x_direct = var_dx / (2 * dt)
        D_y_direct = var_dy / (2 * dt)
        D_direct = (D_x_direct + D_y_direct) / 2

        # --- METHOD 2: Gaussian Fit (density-normalized) ---
        # Use Freedman-Diaconis rule for automatic bin width, and
        # density=True so histogram integrates to 1.  Fit the normalized
        # Gaussian PDF: p(x) = 1/(sqrt(2pi)*sigma) * exp(-(x-mu)^2/(2*sigma^2))
        # This makes the fit independent of bin count and sample size.
        counts_x, bin_edges_x = np.histogram(dx_um, bins='fd', density=True)
        bin_centers_x = (bin_edges_x[:-1] + bin_edges_x[1:]) / 2
        try:
            popt_x, pcov_x = curve_fit(gaussian_pdf, bin_centers_x, counts_x,
                                        p0=[0, np.std(dx_um)])
            std_x_fit = abs(popt_x[1])
        except Exception:
            std_x_fit = np.std(dx_clipped)
            popt_x = [0, std_x_fit]

        counts_y, bin_edges_y = np.histogram(dy_um, bins='fd', density=True)
        bin_centers_y = (bin_edges_y[:-1] + bin_edges_y[1:]) / 2
        try:
            popt_y, pcov_y = curve_fit(gaussian_pdf, bin_centers_y, counts_y,
                                        p0=[0, np.std(dy_um)])
            std_y_fit = abs(popt_y[1])
        except Exception:
            std_y_fit = np.std(dy_clipped)
            popt_y = [0, std_y_fit]

        D_x_fit = std_x_fit**2 / (2 * dt)
        D_y_fit = std_y_fit**2 / (2 * dt)
        D_fit = (D_x_fit + D_y_fit) / 2

        # --- Per-segment D estimates for proper error bars ---
        # Compute D for each segment individually, then take mean +/- SEM.
        seg_D_var = []
        seg_D_gau = []
        for seg in selected:
            sdx = np.diff(seg['x']) * PIXEL_SIZE
            sdy = np.diff(seg['y']) * PIXEL_SIZE
            if len(sdx) < 5:
                continue
            # Variance method (clipped)
            sdx_c = sigma_clip(sdx, sigma=3, max_iter=3)
            sdy_c = sigma_clip(sdy, sigma=3, max_iter=3)
            seg_D_x = np.var(sdx_c) / (2 * dt)
            seg_D_y = np.var(sdy_c) / (2 * dt)
            seg_D_var.append((seg_D_x + seg_D_y) / 2)
            # Gaussian method
            seg_D_gau.append((np.var(sdx) + np.var(sdy)) / (4 * dt))

        if len(seg_D_var) > 1:
            D_direct_err = np.std(seg_D_var) / np.sqrt(len(seg_D_var))
            D_fit_err = np.std(seg_D_gau) / np.sqrt(len(seg_D_gau))
        else:
            D_direct_err = abs(D_x_direct - D_y_direct) / 2
            D_fit_err = abs(D_x_fit - D_y_fit) / 2

        # --- Histogram plot ---
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        ax = axes[0]
        bw_x = bin_edges_x[1] - bin_edges_x[0]
        ax.bar(bin_centers_x, counts_x, width=bw_x,
               alpha=0.6, color='steelblue', label='Data (density)')
        x_fine = np.linspace(bin_centers_x[0], bin_centers_x[-1], 200)
        ax.plot(x_fine, gaussian_pdf(x_fine, *popt_x), 'r-', linewidth=2,
                label=f'Gaussian PDF fit\n$\\sigma$ = {std_x_fit:.4f} $\\mu$m')
        ax.set_xlabel(r'$\Delta x$ per frame ($\mu$m)')
        ax.set_ylabel('Probability density')
        ax.set_title(f'X Displacement \u2014 D_x = {D_x_fit:.4f} $\\mu$m$^2$/s')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        bw_y = bin_edges_y[1] - bin_edges_y[0]
        ax.bar(bin_centers_y, counts_y, width=bw_y,
               alpha=0.6, color='darkorange', label='Data (density)')
        y_fine = np.linspace(bin_centers_y[0], bin_centers_y[-1], 200)
        ax.plot(y_fine, gaussian_pdf(y_fine, *popt_y), 'r-', linewidth=2,
                label=f'Gaussian PDF fit\n$\\sigma$ = {std_y_fit:.4f} $\\mu$m')
        ax.set_xlabel(r'$\Delta y$ per frame ($\mu$m)')
        ax.set_ylabel('Probability density')
        ax.set_title(f'Y Displacement \u2014 D_y = {D_y_fit:.4f} $\\mu$m$^2$/s')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        fig.savefig(str(FIGURES_DIR / 'displacement_histogram.png'), dpi=300, bbox_inches='tight')
        plt.show()

"""

    cell3 = cell3[:idx_start] + new_step4 + cell3[idx_end:]
    print('FIX 2: Replaced STEP 4 with sigma-clipped variance + density-normalized Gaussian PDF')

# =====================================================================
# FIX 3: Fix lag_times in STEP 5
# =====================================================================
old_lag = "        lag_times = np.arange(max_lag) * dt"
new_lag = "        lag_times = (np.arange(max_lag) + 1) * dt  # lag 0 → 1-frame displacement"

if old_lag in cell3:
    cell3 = cell3.replace(old_lag, new_lag)
    print('FIX 3: Fixed lag_times offset (arange+1)*dt')
else:
    print('WARNING: lag_times line not found (may already be fixed)')

# Also fix the linear fit indexing — with the new lag_times, lag_times[0]
# is already 1*dt (not 0), so we fit from index 0 instead of index 1.
old_fit_slice = """        n_fit = max_lag // 4
        fit_times = lag_times[1:n_fit+1]
        fit_MSD = MSD_um[1:n_fit+1]
        fit_err = MSD_err_um[1:n_fit+1]"""

new_fit_slice = """        n_fit = max_lag // 4
        fit_times = lag_times[:n_fit]
        fit_MSD = MSD_um[:n_fit]
        fit_err = MSD_err_um[:n_fit]"""

if old_fit_slice in cell3:
    cell3 = cell3.replace(old_fit_slice, new_fit_slice)
    print('FIX 3b: Updated linear fit slice to use index 0 (lag_times already starts at dt)')
else:
    print('WARNING: linear fit slice not found')

# Fix power-law slice similarly
old_pl_slice = """        n_fit_power = max_lag // 2
        pl_t = lag_times[1:n_fit_power+1]
        pl_msd = MSD_um[1:n_fit_power+1]
        pl_err = MSD_err_um[1:n_fit_power+1]"""

new_pl_slice = """        n_fit_power = max_lag // 2
        pl_t = lag_times[:n_fit_power]
        pl_msd = MSD_um[:n_fit_power]
        pl_err = MSD_err_um[:n_fit_power]"""

if old_pl_slice in cell3:
    cell3 = cell3.replace(old_pl_slice, new_pl_slice)
    print('FIX 3c: Updated power-law fit slice')
else:
    print('WARNING: power-law fit slice not found')

# Fix the MSD plot references that used lag_times[1:]
old_plot_valid = """        valid = MSD_um[1:] > 0
        ax.errorbar(lag_times[1:][valid], MSD_um[1:][valid], yerr=MSD_err_um[1:][valid],"""
new_plot_valid = """        valid = MSD_um > 0
        ax.errorbar(lag_times[valid], MSD_um[valid], yerr=MSD_err_um[valid],"""

if old_plot_valid in cell3:
    cell3 = cell3.replace(old_plot_valid, new_plot_valid)
    print('FIX 3d: Updated log-log MSD plot indexing')
else:
    print('WARNING: MSD log-log plot valid slice not found')

# Fix reference line in log-log plot
old_ref = """        msd_at_1 = MSD_um[1] if MSD_um[1] > 0 else 1e-6
        ax.plot(ref_t, msd_at_1 * (ref_t/dt)**1"""
new_ref = """        msd_at_1 = MSD_um[0] if MSD_um[0] > 0 else 1e-6
        ax.plot(ref_t, msd_at_1 * (ref_t/dt)**1"""

if old_ref in cell3:
    cell3 = cell3.replace(old_ref, new_ref)
    print('FIX 3e: Updated reference line MSD_um[0]')
else:
    print('WARNING: reference line not found')

# Fix linear fit plot line
old_fit_line = "        fit_line_t = np.linspace(0, lag_times[n_fit], 100)"
new_fit_line = "        fit_line_t = np.linspace(0, lag_times[n_fit-1], 100)"

if old_fit_line in cell3:
    cell3 = cell3.replace(old_fit_line, new_fit_line)
    print('FIX 3f: Updated fit_line_t upper bound')
else:
    print('WARNING: fit_line_t not found')

# Fix power-law plot line
old_pl_line = "        pl_line_t = np.linspace(dt, lag_times[n_fit_power], 100)"
new_pl_line = "        pl_line_t = np.linspace(dt, lag_times[n_fit_power-1], 100)"

if old_pl_line in cell3:
    cell3 = cell3.replace(old_pl_line, new_pl_line)
    print('FIX 3g: Updated pl_line_t upper bound')
else:
    print('WARNING: pl_line_t not found')

# =====================================================================
# FIX 4: Add per-segment D_MSD for error bars (after D_msd calculation)
# =====================================================================
old_msd_result = "        D_msd = slope / 4\n        D_msd_err = slope_err / 4"
new_msd_result = """        D_msd = slope / 4
        # Per-segment MSD-slope D for error bar
        seg_D_msd = []
        for seg in selected:
            x = seg['x'].copy()
            y = seg['y'].copy()
            n_f = len(x)
            _ml = min(n_f // 2, max_lag)
            _nf = max(1, _ml // 4)
            _msd_s = np.zeros(_ml)
            for lag in range(_ml):
                dxl = x[lag+1:] - x[:n_f-lag-1]
                dyl = y[lag+1:] - y[:n_f-lag-1]
                _msd_s[lag] = np.mean(dxl**2 + dyl**2) if len(dxl) > 0 else 0
            _msd_um = _msd_s * PIXEL_SIZE**2
            _lt = (np.arange(_ml) + 1) * dt
            if _nf >= 2:
                try:
                    _c = np.polyfit(_lt[:_nf], _msd_um[:_nf], 1)
                    seg_D_msd.append(_c[0] / 4)
                except Exception:
                    pass
        if len(seg_D_msd) > 1:
            D_msd_err = np.std(seg_D_msd) / np.sqrt(len(seg_D_msd))
        else:
            D_msd_err = slope_err / 4"""

if old_msd_result in cell3:
    cell3 = cell3.replace(old_msd_result, new_msd_result)
    print('FIX 4: Added per-segment D_MSD for error bars')
else:
    print('WARNING: D_msd result block not found')

set_src(3, cell3)

# =====================================================================
# Save
# =====================================================================
with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('\nAll STEP 4/5 fixes applied and saved.')
