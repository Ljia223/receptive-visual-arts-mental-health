scripts <- c(
  "R/00_setup.R", "R/01_get_open_data.R", "R/02_trupp_analysis.R",
  "R/03_castellotti_analysis.R", "R/04_hearts_analysis.R",
  "R/05_cross_dataset_integration.R", "R/06_make_figures.R"
)
for (script in scripts) {
  message("Running ", script)
  source(script, local = globalenv())
}
message("Workflow completed successfully")
