# Reproducibility guide

## Required software

- R 4.4.2
- Python 3.12 only for the optional independent validation workflow
- Internet access for the Trupp GitHub repository and Castellotti Zenodo record

## Primary workflow

1. Download the HEartS Dryad archive from https://doi.org/10.5061/dryad.3r2280gdj.
2. Rename the archive to `doi_10_5061_dryad_3r2280gdj__v20210226.zip` and place it in `data/raw/`.
3. Open R in the repository root.
4. Install the packages listed in `DESCRIPTION`.
5. Run `source("R/run_all.R")`.
6. Compare generated files with `data/derived/`, `results/tables/`, and `results/figures/`.

## Validation checkpoints

- Trupp has 84 participants and 168 pre-post rows, with 40 participants in the art condition and 44 in the active cultural comparison.
- Castellotti has 92 participants with paired STAI-S observations.
- HEartS has 5,338 records.
- HEartS exposure counts are 1,813 none, 2,117 infrequent, 1,220 regular, and 188 weekly or daily.
- The fully adjusted MHC-SF contrasts against no attendance are 1.07, 3.59, and 9.87 points for increasing attendance categories.
- Every negative acute anxiety change denotes lower post-exposure anxiety.

## Independent verification

The script `validation/hearts_reference_analysis.py` implements the HEartS models using matrix operations and heteroskedasticity-consistent covariance estimation in Python. It is retained as an implementation-independent check and is not the primary reported workflow.

## Traceability

Each output table includes the outcome, model, contrast, estimate, confidence interval, and analysis role. Figure-generating scripts read saved estimates rather than manually entered labels. The file `MANIFEST.sha256` records checksums for the release bundle.
