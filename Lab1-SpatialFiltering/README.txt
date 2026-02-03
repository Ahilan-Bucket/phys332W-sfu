Lab 1 - Spatial Filtering
Description: Lab experiment on Spatial Filtering.
Purpose: To study Fourier optics and spatial filtering techniques.
Date: Jan 2026

Collaborators:
- Ahilan Kumaresan
- Nathan Unrhu

Requirements:
- Python 3
- Jupyter Notebook
- LaTeX (for PDF generation) - (For Ahilan's Local)

Directory Structure:
├── Analysis/
│   ├── Model Function Fit.ipynb
│   ├── Session2_PreLabQuestions.ipynb
│   ├── Session2_PreLabQuestions_Corrected.ipynb
│   ├── Session2_new.ipynb
│   ├── Session3_Final_summary.ipynb
│   ├── Session3_Untitled-1.ipynb
│   ├── Session4_AnalysisAssignment1.ipynb
│   └── Session4_Pre-lab_Question_3.ipynb
├── Data/
│   ├── 2026-01-08/
│   │   └── (Empty)
│   ├── 2026-01-15/
│   │   └── 2026-01-15_SF_S3_Fourier_image.tiff
│   ├── 2026-01-20/
│   │   ├── 1_10thPupil.tiff
│   │   ├── 2_10thPupil.tiff
│   │   ├── Fourier01.tiff
│   │   ├── newCentreil.tiff
│   │   └── smallestPupil01.tiff
│   ├── 2026-01-22/
│   │   ├── 12lpmm-forrier.tiff
│   │   ├── 12lpmm-image.tiff
│   │   ├── 16lpmm-forrier.tiff
│   │   ├── 16lpmm-image.tiff
│   │   ├── 26-50lpmm-forrier.tiff
│   │   ├── 26-50lpmm-image.tiff
│   │   ├── 26lpmm-forrier.tiff
│   │   ├── 26lpmm-image.tiff
│   │   ├── 50lpmm-forrier.tiff
│   │   ├── 50lpmm-image.tiff
│   │   ├── Inital-State-diffraction-pattern.tiff
│   │   ├── Screenshot 2026-01-22 160302.png
│   │   ├── corrected-iris-position.tiff
│   │   ├── corrected-state-diffraction-pattern.tiff
│   │   ├── fersnel-frindges-issue.tiff
│   │   ├── focusing-defects.tiff
│   │   ├── pair.png
│   │   └── zeroth-order-image.tiff
│   ├── 2026-01-27/
│   │   ├── RonchiFouerie-A.tiff
│   │   ├── RonchiFouerie-A2.tiff
│   │   ├── RonchiFouerie-B.tiff
│   │   ├── RonchiFouerie-D.tiff
│   │   ├── RonchiFouerie-E.tiff
│   │   ├── RonchiFouerie-F.tiff
│   │   ├── RonchiFouerie-J.tiff
│   │   ├── RonchiFouerie-K.tiff
│   │   ├── RonchiFouerie-K2.tiff
│   │   ├── RonchiFouerie01.tiff
│   │   ├── RonchiFouerieBlovked-ve1to1.tiff
│   │   ├── RonchiFoueriedefault.tiff
│   │   ├── RonchiReal-A.tiff
│   │   ├── RonchiReal-A2.tiff
│   │   ├── RonchiReal-B.tiff
│   │   ├── RonchiReal-D.tiff
│   │   ├── RonchiReal-E.tiff
│   │   ├── RonchiReal-F.tiff
│   │   ├── RonchiReal-J.tiff
│   │   ├── RonchiReal-K.tiff
│   │   ├── RonchiReal-K2.tiff
│   │   ├── RonchiReal-ve1to1.tiff
│   │   ├── RonchiReal01.tiff
│   │   ├── RonchiRealDefault.tiff
│   │   ├── RonchiRealblocked-ve1to1.tiff
│   │   ├── Screenshot 2026-01-22 161117.png
│   │   ├── Screenshot 2026-01-22 161145.png
│   │   ├── Screenshot 2026-01-27 150541.png
│   │   ├── Screenshot 2026-01-27 150551.png
│   │   ├── Screenshot 2026-01-27 162855.png
│   │   ├── Screenshot 2026-01-27 162905.png
│   │   └── Screenshot 2026-01-27 162912.png
│   └── 2026-01-29/
│       ├── BrightField-a-Fourier.tiff
│       ├── BrightField-a-Real.tiff
│       ├── DarkField-c-Fourier.tiff
│       ├── DarkField-c-Real.tiff
│       ├── FocusedFourier.tiff
│       ├── FocusedReal.tiff
│       ├── PhaseContract-b-Fourier.tiff
│       ├── PhaseContract-b-Real.tiff
│       ├── RonchiFourier-a.tiff
│       ├── RonchiFourier-b.tiff
│       ├── RonchiFourier-c.tiff
│       ├── RonchiFourier-d.tiff
│       ├── RonchiFourier-e.tiff
│       ├── RonchiFourier-f.tiff
│       ├── RonchiFourier-h.tiff
│       ├── RonchiFourier-h2.tiff
│       ├── RonchiFourier-i.tiff
│       ├── RonchiFourier-j.tiff
│       ├── RonchiFourier-k-m3.tiff
│       ├── RonchiFourier-k-m5.tiff
│       ├── RonchiReal-a.tiff
│       ├── RonchiReal-b.tiff
│       ├── RonchiReal-c.tiff
│       ├── RonchiReal-d.tiff
│       ├── RonchiReal-e.tiff
│       ├── RonchiReal-f.tiff
│       ├── RonchiReal-h.tiff
│       ├── RonchiReal-h2.tiff
│       ├── RonchiReal-i.tiff
│       ├── RonchiReal-j.tiff
│       ├── RonchiReal-k-m3.tiff
│       ├── RonchiReal-k-m5.tiff
│       ├── Schlieren-d-Fourier.tiff
│       ├── Schlieren-d-Real.tiff
│       ├── initalReal.tiff
│       └── initialFourier.tiff
├── Notes/
│   ├── AhilanPersonal/
│   │   ├── Session2_PreLabQuestions.html
│   │   ├── Session2_PreLabQuestions.pdf
│   │   ├── Session3_Lab_notebook_compressed_withPlots.pdf
│   │   ├── Session4_AnalysisAssignment1.pdf
│   │   ├── Session4_AnalysisAssignment1_old.pdf
│   │   ├── Session4_Pre-lab_Question_3.pdf
│   │   ├── Session5_Notebook1.docx
│   │   ├── Session6_Lab_1_Session_6.pdf
│   │   ├── Session6_Lab_1_Session_6_v2.pdf
│   │   └── Session6_Notebook_preview.pdf
│   ├── LabNotebook/
│   │   ├── Lab1-W2-Snapshot-1.pdf
│   │   ├── Lab1-W3-SnapShot-2.pdf
│   │   └── LiveNotebookLink.txt
│   ├── Reference/
│   │   ├── 1979-Buckman+Woolley-Spatial filtering with a photographic replica-JPhysE.pdf
│   │   └── spatial_filtering.pdf
│   └── Session4_Notes/
│       ├── 1-10th-pupil-field-iris.tiff
│       ├── 2-10th-pupil-field-iris.tiff
│       ├── 2026-01-20-descriptive-title.txt
│       ├── Error-changing-exposure.png
│       ├── Fourier-Image-Pinhole.tiff
│       ├── Fourier01.tiff
│       ├── LabView-Setup-Screenshot.png
│       ├── Screenshot 2026-01-20 150818 full screen.png
│       ├── ShowingtheLines10lp_per_mm_Real01.tiff
│       ├── diffraction-pattern-secondary-rail-01.tiff
│       ├── new-diffraction-pattern.tiff
│       └── smallestPupil-field-iris.tiff
├── SF-B2-MaskData.xlsx
├── SF-Chi2-FitAnalysis.xlsx
├── SF-Chi2Python.pdf
├── SF-DataAnalysis.pdf
└── Untitled.ipynb
