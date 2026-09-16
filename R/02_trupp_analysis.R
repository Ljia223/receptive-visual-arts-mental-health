trupp <- readr::read_csv("data/raw/trupp/03_df_pre_post.csv", show_col_types = FALSE)
assert_columns(trupp, c("SubID", "condition", "block", "STAI"), "Trupp data")
stopifnot(dplyr::n_distinct(trupp$SubID) == 84L, nrow(trupp) == 168L)

trupp <- trupp |>
  dplyr::mutate(
    id = factor(SubID),
    condition = factor(condition, levels = c("non_art", "art")),
    time = factor(block, levels = c("pre", "post"))
  )

wide <- trupp |>
  dplyr::select(id, condition, time, state_anxiety = STAI) |>
  tidyr::pivot_wider(names_from = time, values_from = state_anxiety) |>
  dplyr::mutate(change = post - pre)

mixed <- lmerTest::lmer(STAI ~ time * condition + (1 | id), data = trupp, REML = FALSE)
ancova <- stats::lm(post ~ pre + condition, data = wide)
mixed_table <- broom.mixed::tidy(mixed, effects = "fixed", conf.int = TRUE)
ancova_table <- hc3_tidy(ancova)

acute <- wide |>
  dplyr::group_by(condition) |>
  dplyr::group_modify(function(.x, .y) {
    b <- bootstrap_g_av(.x$pre, .x$post)
    tibble::tibble(
      dataset = "Trupp 2022", estimate_type = "within-group post minus pre",
      group = as.character(.y$condition), n = unname(b["n"]),
      estimate = unname(b["estimate"]), conf.low = unname(b["conf.low"]),
      conf.high = unname(b["conf.high"])
    )
  })

contrast <- bootstrap_between_change_g(wide$pre, wide$post, wide$condition)
acute <- dplyr::bind_rows(
  acute,
  tibble::tibble(
    dataset = "Trupp 2022", estimate_type = "between-condition difference in change",
    group = "art minus active cultural content", n = unname(contrast["n"]),
    estimate = unname(contrast["estimate"]), conf.low = unname(contrast["conf.low"]),
    conf.high = unname(contrast["conf.high"])
  )
)

secondary_columns <- intersect(c("posMood", "negMood", "lone", "wellbeing"), names(trupp))
secondary <- purrr::map_dfr(secondary_columns, function(outcome) {
  model <- lmerTest::lmer(stats::as.formula(paste(outcome, "~ time * condition + (1 | id)")), data = trupp, REML = FALSE)
  broom.mixed::tidy(model, effects = "fixed", conf.int = TRUE) |>
    dplyr::filter(term == "timepost:conditionart") |>
    dplyr::mutate(outcome = outcome)
}) |>
  dplyr::mutate(p.holm = stats::p.adjust(p.value, method = "holm"))

appraisal <- trupp |>
  dplyr::filter(condition == "art", time == "post") |>
  dplyr::select(id, dplyr::any_of(c("experience_beautifulness", "experience_meaning"))) |>
  dplyr::left_join(wide |> dplyr::select(id, pre, change), by = "id")
appraisal_models <- purrr::map_dfr(intersect(c("experience_beautifulness", "experience_meaning"), names(appraisal)), function(variable) {
  model <- stats::lm(stats::as.formula(paste("change ~ pre +", variable)), data = appraisal)
  hc3_tidy(model) |> dplyr::filter(term == variable) |> dplyr::mutate(appraisal = variable)
})

write_result(mixed_table, "results/tables/trupp_mixed_model.csv")
write_result(ancova_table, "results/tables/trupp_ancova.csv")
write_result(secondary, "results/tables/trupp_secondary_outcomes.csv")
write_result(appraisal_models, "results/tables/trupp_appraisal_associations.csv")
write_result(acute, "data/derived/trupp_within_group_effects.csv")
