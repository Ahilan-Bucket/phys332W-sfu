# PHYS 382 Advanced Lab — Lab Setup and Session Workflow

## A. Folder Structure Template

For each new lab, create this structure in the git repo:

```
Lab{N}-{Name}/
├── Analysis/
│   └── figures/          ← date subfolders created per session (YYYY-MM-DD/)
├── Data/                 ← date subfolders created per session (YYYY-MM-DD/)
├── Notes/
│   └── References/       ← lab-specific reference papers
└── Drafts/               ← old submission briefs, scans
```

And in the Personal folder (outside git):

```
Personal/Notebook/Lab{N}/
├── DocsNFile/            ← active .md, .docx, .tex files
│   └── Docs/
└── Archive/              ← superseded versions
```

---

## B. Lab 3: Chaotic Circuits — Schedule

*From Lab Script Section 4: "Suggested Timeline"*

| Lab Period | Tasks | Pre-lab Due |
|-----------|-------|-------------|
| **1** | Complete most of Part I (4 op amp experiments) | — |
| **2** | Hand in Pre-lab Q1; build and test nonlinear element D(x) | **Pre-lab Q1** |
| **3** | Build full jerk circuit; observe chaos | — |
| **4** | Hand in Pre-lab Q2; take data to compare with simulation | **Pre-lab Q2** |
| **5** | Better data; phase portraits, bifurcation diagrams, power spectra; advanced measurements (Feigenbaum delta, return map) | — |
| **6** | Complete data set and analysis | — |
| **7-8** | Additional data collection, analysis, projects | **Pre-lab Q3** (before Period 4) |

### Pre-lab Questions Summary

- **Q1** (due end of Period 1 / start of Period 2): Derive ODE for practical integrator, solve, sketch 3 regimes, explain R2 purpose
- **Q2** (due start of Period 4): Apply Part I to derive Eqs. 2-6 from Kiers et al. for the full circuit
- **Q3** (due start of Period 4): Numerically solve the jerk ODE. Find periodic, bifurcating, and chaotic solutions. Determine max amplitudes.

---

## C. Documentation Requirements

*From Lab Script Section 5: "Items to include in your documentation"*

### Required Figures

- Circuit diagrams (with all component values and power connections)
- Nonlinear element test (D(x) I-V curve)
- Raw data waveforms — simulated AND measured
- Maxima plot — simulated AND measured
- Phase portraits — simulated AND measured
- Bifurcation diagram — simulated AND measured (need peak-finding algorithm; check for noise artifacts)
- Power spectral densities

### Advanced Project Ideas

- **Feigenbaum constant:** delta_n = (A_n - A_{n-1}) / (A_{n+1} - A_n), extrapolate to n -> infinity, expect delta ~ 4.7
- **Return maps:** x_{n+1} vs x_n in chaotic regime (Lorenz map); look for unstable limit cycle
- **Second-return map:** x_{n+2} vs x_n for period-2 analysis
- **Largest Lyapunov exponent:** real indicator of chaos (Strogatz Section 10.5)
- **Feigenbaum alpha ~ 2.5:** width scaling of bifurcation branches (Strogatz Section 10.6)
- **U-sequence:** order of periodic windows (period-3, period-5, etc.) beyond primary cascade
- **3D phase portrait:** plot (x, x-dot, x-ddot) — trajectories don't cross in full 3D (they DO cross in 2D projections)
- **Audio chaos:** swap 1 nF for 10 nF capacitors, connect audio amplifier to hear chaos

---

## D. New Lab Setup Checklist

1. Create folder tree in git repo: `Lab{N}-{Name}/` with Analysis/, Data/, Notes/References/, Drafts/
2. Add `.gitkeep` files in empty directories
3. Create Personal folders: `Personal/Notebook/Lab{N}/DocsNFile/Docs/`, `Archive/`
4. Read lab script, extract schedule and documentation requirements into this README
5. Write Session 1 `.md` notebook (self-sufficient — can follow in lab without lab script)
6. Generate `.docx` via notebook generator
7. Copy `.md` to `DocsNFile/` for reference
8. Update MEMORY.md with new lab entry

---

## E. New Session Workflow

**Before each new session:**

1. Create `Data/YYYY-MM-DD/` subfolder for raw data (oscilloscope saves, photos)
2. Create `Analysis/figures/YYYY-MM-DD/` subfolder for analysis output
3. **Read the last session's .docx** — note what was completed, what's pending, any issues
4. **Check lab script schedule** (Section B above) — determine what's planned for this lab period
5. **Write `Lab{N}-Session{M}-Notebook.md`** covering:
   - Anything missed or incomplete from previous session
   - All tasks for current lab period from the schedule
   - Self-sufficient procedure: student can follow step-by-step without opening the lab script
   - All relevant formulas, component values, circuit descriptions with derivations
   - CC markers for data to fill in during lab
   - References to lab script page numbers for circuit diagrams
6. Generate .docx:
   ```bash
   python Personal/NotebookGenerator/generate_notebook_v5.py \
       "path/to/Lab{N}-Session{M}-Notebook.md" \
       "Personal/Notebook/Lab{N}/DocsNFile/Lab{N}-Session{M}-Notebook.docx" \
       --start-page N
   ```
7. Copy `.md` to `DocsNFile/`
8. Edit on iPad in Word: paste oscilloscope screenshots, fill CC markers

---

## F. Naming Conventions

- **No spaces in filenames** — use hyphens (critical for Git)
- **Dates:** YYYY-MM-DD (ISO 8601) for data/analysis subfolders
- **Notebook files:** `Lab{N}-Session{M}-Notebook.md` / `.docx`
- **Versioned files:** `Lab{N}-Session{M}-Notebook-v{V}.docx`
- **Merged submissions:** `Lab{N}-Sessions{A}-{B}-FINAL-v{V}.docx`
- **TOC files:** `Lab{N}-TOC-Sessions{A}-{B}.md`
- **Submission briefs:** `Lab{N}-Week{W}-Submission-Brief.tex` / `.pdf`
- **Final PDFs:** numbered prefix for submission order (`1Lab{N}-...`, `2Lab{N}-...`)

---

## G. Notebook Generator Quick Reference

**Location:** `Personal/NotebookGenerator/generate_notebook_v5.py`

**Usage:**
```bash
python Personal/NotebookGenerator/generate_notebook_v5.py input.md output.docx [--start-page N] [--font path.ttf]
```

**Critical Rules:**
1. **NEVER regenerate .docx after images are pasted** — destroys image relationships (silent failure: 17 MB -> 9 MB)
2. **Close Word before running any script** — python-docx silently drops images from locked files
3. **TOC pages shift page numbers** — after adding N TOC pages, all content page numbers shift by +N
4. **Session boundary detection:** match "Session [N]" title text, NOT keywords (keywords appear in multiple sessions)
5. **Keep intermediate versions** until final is verified, then archive

**Markdown features:** `**bold**`, `*italic*`, `==yellow==`, `++green++`, `!!red!!`, `$math$`, `$$display math$$`, `(CC marker)`, `![Caption](image.png)`, `<!-- Table N: Caption -->`

---

## H. Submission Workflow

1. Generate individual session .docx files
2. Edit on iPad (paste images, fill CC markers)
3. Merge sessions if needed (insert_session scripts)
4. Add TOC pages (add_toc scripts) — recalculate page numbers after!
5. Create submission brief: `.tex` with tcolorbox, booktabs, fancyhdr style
6. Export to PDF, number files for submission order
7. Archive superseded versions to `Personal/Notebook/Lab{N}/Archive/`
