trupp <- readr::read_csv("data/derived/trupp_within_group_effects.csv", show_col_types = FALSE)
castellotti <- readr::read_csv("data/derived/castellotti_within_group_effect.csv", show_col_types = FALSE)

acute <- dplyr::bind_rows(trupp, castellotti) |>
  dplyr::mutate(direction = dplyr::if_else(estimate < 0, "lower anxiety", "higher anxiety"))

triangulation <- tibble::tribble(
  ~claim, ~trupp_2022, ~castellotti_2025, ~hearts_2019, ~assessment,
  "Immediate anxiety was lower after exposure", "Supported within both conditions", "Supported", "Not measured", "Direction converged across acute settings",
  "Visual art outperformed active cultural content", "Not supported by the interaction contrast", "No control condition", "Not an acute comparison", "No evidence of art-specific superiority",
  "Habitual attendance was associated with positive mental health", "Not measured", "Not measured", "Supported for MHC-SF", "Supported by one population dataset",
  "Habitual attendance was associated with lower depressive symptoms", "Not measured", "Not measured", "Not supported", "No convergent evidence",
  "Trait anxiety robustly moderated acute change", "Not tested", "Not supported after baseline adjustment", "Not an acute moderator", "Not supported"
)

write_result(acute, "data/derived/acute_standardized_effects.csv")
write_result(triangulation, "results/tables/evidence_triangulation.csv")
