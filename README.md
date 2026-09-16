# Receptive Visual Arts Engagement and Mental Health

## Overview

This repository provides the reproducible analytical materials for the study entitled Receptive Visual Arts Engagement and Mental Health Promotion: Multi-Dataset Evidence From Immediate Anxiety Change and Population-Level Well-Being.

The study uses three independent open datasets to examine receptive visual arts engagement across online, in-person, and population settings. Individual-level records are analyzed separately within each dataset and are not pooled. Evidence is integrated through a harmonized cross-design triangulation framework.

## Research Objectives

The study addresses three objectives.

- Estimate immediate changes in state anxiety following online digital visual art viewing and an in-person contemporary art exhibition
- Evaluate whether online visual art produces greater anxiety reduction than active non-art cultural content and examine relevant individual differences
- Examine associations between visual-arts attendance frequency and mental well-being, depressive symptoms, loneliness, and social connectedness in the HEartS sample

## Data Sources

### Trupp 2022

The Trupp dataset contains data from an online quasi-randomized pre-post study involving 84 adults. Participants viewed either an interactive digital presentation of Claude Monet's The Water-Lily Pond or active non-art cultural content concerning Japanese food history.

The primary outcome is immediate state anxiety. Secondary outcomes include subjective well-being, positive and negative mood, loneliness, and post-exposure aesthetic evaluations.

The source data and original analytical materials are available through the public repository accompanying the original publication.

### Castellotti 2025

The Castellotti dataset contains paired observations from 92 adults who completed an individually guided immersive visit to a contemporary art exhibition. State anxiety was measured immediately before and after the visit.

The dataset also includes trait anxiety, art interest, openness, curiosity, visit duration, and post-visit evaluations of beauty, understanding, satisfaction, and related experiential qualities.

The public dataset is available from Zenodo.

https://doi.org/10.5281/zenodo.16412669

### HEartS 2019

The HEartS Survey contains cross-sectional data from 5,338 adults in the United Kingdom. The focal exposure is the reported frequency of visiting an exhibition, museum, or collection of art, photography, sculpture, or other visual arts during the preceding 12 months.

The principal outcomes are Mental Health Continuum Short Form scores and eight-item Center for Epidemiologic Studies Depression Scale scores. Secondary outcomes include UCLA loneliness, De Jong Gierveld loneliness, and social connectedness.

The public dataset, questionnaire, documentation, and original syntax are available from Dryad.

https://doi.org/10.5061/dryad.3r2280gdj

## Analytical Framework

Each dataset is analyzed independently according to its original design and measurement structure.

- Trupp 2022 provides comparative evidence concerning immediate anxiety change and visual-art specificity
- Castellotti 2025 provides ecologically grounded evidence concerning immediate anxiety change in a physical exhibition setting
- HEartS 2019 provides observational evidence concerning habitual visual-arts attendance and population mental health

Construct harmonization is conceptual rather than numerical. Brief digital viewing, an in-person exhibition visit, and annual attendance frequency are not treated as equivalent exposure doses.

## Statistical Analyses

The Trupp analysis uses baseline-adjusted analysis of covariance and a linear mixed model containing time, condition, and their interaction. The primary estimate of visual-art specificity is the Time by Condition interaction.

The Castellotti analysis uses a repeated-measures linear mixed model to estimate pre-visit to post-visit anxiety change. Trait anxiety and other participant characteristics are examined in exploratory interaction models.

The HEartS analysis uses HC3 robust linear regression for continuous outcomes and modified Poisson regression with robust standard errors for elevated depressive symptoms. Models use nested demographic, educational, health, behavioral, physical-activity, and relationship covariates available in the public release.

Standardized anxiety change is calculated as the post-exposure score minus the pre-exposure score. Negative standardized estimates therefore indicate lower anxiety after exposure.

Cross-dataset integration considers effect direction, magnitude, precision, robustness, and design-specific limitations. The datasets are not combined through individual-level pooling or a primary random-effects meta-analysis.

## Reproducibility

The core statistical analyses were conducted in R version 4.4.2. The analytical workflow uses a fixed random seed of 2026 for stochastic procedures. Bootstrap confidence intervals are based on 5,000 participant-level resamples.

The principal R packages include the following.

- lme4
- lmerTest
- pbkrtest
- emmeans
- sandwich
- lmtest
- performance
- effectsize
- boot

The analytical materials document data exclusions, legal-range checks, reverse scoring, scale construction, exposure recoding, covariate construction, model specifications, multiplicity adjustments, and sensitivity analyses.

## Data Use

Raw source data are not redistributed through this repository. Users should obtain the datasets directly from their original repositories and comply with the applicable licenses and data-use conditions.

The repository contains no names, contact information, precise addresses, or other direct personal identifiers. No attempt should be made to reidentify participants or link released records to external individual-level information.

## Interpretation Boundaries

The online active-control comparison does not establish a visual-art-specific anxiety effect when the between-condition contrast is compatible with no difference.

The in-person exhibition study has no independent comparison condition and therefore supports visit-associated change rather than a causal effect attributable exclusively to visual art.

The HEartS survey is cross-sectional and based on a non-probability online sample. Its estimates represent adjusted associations within the released sample and should not be interpreted as nationally representative or causal effects.

Receptive visual arts engagement is evaluated as a potentially accessible cultural resource for mental health promotion and not as a substitute for clinical assessment or treatment.

## Citation

Users of the analytical materials should cite the original Trupp, Castellotti, and HEartS publications and the corresponding data repositories.
