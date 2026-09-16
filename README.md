# Receptive Visual Arts Engagement and Mental Health

This repository contains the reproducible analytical materials for the study Receptive Visual Arts Engagement and Mental Health Promotion: Multi-Dataset Evidence From Immediate Anxiety Change and Population-Level Well-Being.

The project integrates three independent open datasets without pooling participant records. Trupp 2022 supplies a comparative online pre-post design, Castellotti 2025 supplies an ecologically grounded in-person pre-post design, and HEartS 2019 supplies population-level cross-sectional evidence. The analytical strategy is cross-design evidence triangulation rather than a single causal model.

## Repository contents

- `R/00_setup.R` verifies the software environment and creates output directories.
- `R/01_get_open_data.R` downloads the Trupp and Castellotti source files and locates the HEartS archive.
- `R/02_trupp_analysis.R` estimates online pre-post anxiety changes, the condition-by-time contrast, baseline-adjusted differences, and appraisal associations.
- `R/03_castellotti_analysis.R` estimates in-person pre-post anxiety change and tests the prespecified trait-anxiety models.
- `R/04_hearts_analysis.R` reconstructs the HEartS exposure, fits the three adjustment sets, and runs dose-response, secondary-outcome, interaction, and sensitivity analyses.
- `R/05_cross_dataset_integration.R` harmonizes acute effect directions and creates the evidence-triangulation table.
- `R/06_make_figures.R` creates the manuscript figures from saved estimates.
- `R/run_all.R` executes the complete workflow in order.
- `config/variable_mapping.csv` documents the construct-to-variable mapping.
- `data/raw/README.md` records the permanent source locations and expected filenames.
- `data/derived/` contains non-identifying estimates used for verification and figure production.
- `results/tables/` contains machine-readable manuscript tables.
- `results/figures/` contains the publication-ready PDF figures.
- `results/machine-readable/` contains structured model output.
- `docs/analysis_decisions.md` records the analysis hierarchy and interpretive boundaries.
- `docs/reproducibility.md` provides a complete reproduction procedure.
- `validation/` contains independent Python scripts used to verify HEartS estimates and regenerate figures.

## Data sources

The repository does not redistribute participant-level source data. The source materials remain under their original licenses and repository terms.

- Trupp 2022 article DOI: https://doi.org/10.3389/fpsyg.2022.782033
- Trupp processed data and original code: https://github.com/giacomobignardi/Trupp-online-art-wellbeing
- Castellotti 2025 dataset DOI: https://doi.org/10.5281/zenodo.16412669
- Castellotti 2025 article DOI: https://doi.org/10.1371/journal.pone.0332321
- HEartS 2019 dataset DOI: https://doi.org/10.5061/dryad.3r2280gdj

The data-acquisition script downloads the openly accessible Trupp and Castellotti files. Dryad supplies HEartS as an archive; place the downloaded archive in `data/raw/` using the filename documented in `data/raw/README.md`.

## Software

The primary workflow uses R 4.4.2. Required packages are declared in `DESCRIPTION` and checked by `R/00_setup.R`. The independent HEartS verification workflow uses Python 3.12 with pandas, NumPy, SciPy, and openpyxl.

## Reproduction

Clone or download the repository, install R 4.4.2, place the HEartS archive in `data/raw/`, and run the following command from the repository root.

```r
source("R/run_all.R")
```

The workflow downloads the other public source files, validates required variables and sample sizes, writes derived results, and recreates the tables and figures. It stops with an informative error if a source file or required variable is unavailable.

## Direction of anxiety effects

Every anxiety change score is defined as post-exposure minus pre-exposure. Negative estimates therefore indicate lower anxiety after exposure. The standardized within-group estimate is Hedges g based on the average pre-post standard deviation. The online between-condition estimate is the standardized difference in change between visual art and active cultural content.

## Interpretive boundaries

The Trupp condition-by-time contrast is the primary estimate of online visual-art specificity. Within-group pre-post change alone is not treated as an art-specific causal effect. Castellotti has no concurrent control condition, so its estimates describe change during an exhibition visit. The HEartS analysis is cross-sectional and does not establish temporal order or long-term protection. Trait anxiety is not presented as a robust moderator because its unadjusted interaction does not persist after adjustment for baseline state anxiety.

## License and citation

Original code in this repository is released under the MIT License. Source datasets retain their original licenses. Cite the source datasets and articles when reusing their data, and use `CITATION.cff` to cite this analytical repository.

## Contact

Questions and reproducibility reports can be submitted through the repository issue tracker.
