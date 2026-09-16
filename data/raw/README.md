# Source data placement

Participant-level source data are not redistributed in this repository.

## Trupp 2022

Source repository: https://github.com/giacomobignardi/Trupp-online-art-wellbeing

The acquisition script downloads `03_df_pre_post.csv` from source commit `3e3fc8af1a892a9a13cadd89f840394958ff4bda` and saves it as `data/raw/trupp/03_df_pre_post.csv`.

## Castellotti 2025

Dataset DOI: https://doi.org/10.5281/zenodo.16412669

The acquisition script downloads all eleven Excel workbooks into `data/raw/castellotti/`. The primary analysis uses `AnxietyState_STAI-S.xlsx`, `AnxietyTrait_STAI-T.xlsx`, `ArtPreferences.xlsx`, `Curiosity_CEI-II.xlsx`, `OpennessToExperience_BFAS.xlsx`, `Post-visitQuestionnaire.xlsx`, and `VisitTime.xlsx`.

## HEartS 2019

Dataset DOI: https://doi.org/10.5061/dryad.3r2280gdj

Download the Dryad package and place it at:

`data/raw/doi_10_5061_dryad_3r2280gdj__v20210226.zip`

The archive must contain `HEartS_Survey_2019_Dataset.xlsx`, `HEartS_Survey_2019_Variables.xlsx`, `HEartS_Survey_2019_Syntax.md`, and `HEartS_Survey_2019.pdf`. The analysis extracts the dataset into a temporary directory and never changes the source archive.
