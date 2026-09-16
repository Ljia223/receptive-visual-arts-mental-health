required_packages <- c(
  "readr", "readxl", "dplyr", "tidyr", "purrr", "tibble", "stringr",
  "broom", "broom.mixed", "sandwich", "lmtest", "lme4", "lmerTest", "emmeans", "car",
  "effectsize", "boot", "ggplot2", "scales", "jsonlite", "openxlsx"
)

missing_packages <- required_packages[!vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing_packages) > 0) {
  stop(
    "Install the following packages before running the workflow: ",
    paste(missing_packages, collapse = ", ")
  )
}

dirs <- c(
  "data/raw/trupp", "data/raw/castellotti", "data/processed", "data/derived",
  "results/tables", "results/figures", "results/machine-readable"
)
invisible(lapply(dirs, dir.create, recursive = TRUE, showWarnings = FALSE))
options(stringsAsFactors = FALSE, contrasts = c("contr.treatment", "contr.poly"))
set.seed(2026)

source("R/utils.R")
