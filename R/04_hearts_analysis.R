archive <- "data/raw/doi_10_5061_dryad_3r2280gdj__v20210226.zip"
archive_listing <- utils::unzip(archive, list = TRUE)
dataset_member <- archive_listing$Name[stringr::str_detect(archive_listing$Name, "HEartS_Survey_2019_Dataset\\.xlsx$")]
if (length(dataset_member) != 1L) stop("The HEartS archive does not contain exactly one survey dataset workbook")
temporary_directory <- tempfile("hearts_")
dir.create(temporary_directory)
utils::unzip(archive, files = dataset_member, exdir = temporary_directory)
hearts <- readxl::read_excel(file.path(temporary_directory, dataset_member))

required <- c(
  "rart8", "rartscore", "partscore", "mhcscore", "cesdscore", "cesdbin3",
  "ucla3score", "djgscore", "soconscore2", "agecat", "ethnicgroups", "educ4",
  "artprofbin", "srh3", "mild", "mod", "vig", "partnerclose3"
)
assert_columns(hearts, required, "HEartS data")
stopifnot(nrow(hearts) == 5338L)

hearts <- hearts |>
  dplyr::mutate(
    visual_arts_frequency = cut(
      rart8, breaks = c(-Inf, 0, 2, 4, Inf),
      labels = c("None", "Infrequent", "Regular", "Weekly or daily"), right = TRUE
    ),
    visual_arts_frequency = stats::relevel(visual_arts_frequency, ref = "None"),
    visual_arts_order = as.integer(visual_arts_frequency) - 1L,
    any_visual_arts = factor(ifelse(rart8 > 0, "Any", "None"), levels = c("None", "Any")),
    ethnicity6 = cut(
      ethnicgroups, breaks = c(0, 4, 8, 13, 16, 17, 18),
      labels = c("Group 1", "Group 2", "Group 3", "Group 4", "Group 5", "Group 6")
    ),
    age_category = factor(agecat), education4 = factor(educ4),
    self_rated_health = factor(srh3), mild_activity = factor(mild),
    moderate_activity = factor(mod), vigorous_activity = factor(vig),
    partner_closeness = factor(partnerclose3), arts_professional = artprofbin,
    other_receptive_arts = rartscore - as.integer(rart8 > 0)
  )

covariates <- list(
  model_1 = c("age_category", "ethnicity6"),
  model_2 = c("age_category", "ethnicity6", "education4", "arts_professional"),
  model_3 = c(
    "age_category", "ethnicity6", "education4", "arts_professional",
    "self_rated_health", "mild_activity", "moderate_activity", "vigorous_activity",
    "partner_closeness"
  )
)

fit_hearts <- function(outcome, model_name, poisson = FALSE, exposure = "visual_arts_frequency", extra = character()) {
  formula <- stats::reformulate(c(exposure, covariates[[model_name]], extra), response = outcome)
  if (poisson) {
    model <- stats::glm(formula, family = stats::poisson(link = "log"), data = hearts)
    table <- robust_glm_tidy(model, exponentiate = TRUE)
  } else {
    model <- stats::lm(formula, data = hearts)
    table <- hc3_tidy(model)
  }
  list(model = model, table = table)
}

primary <- purrr::map_dfr(names(covariates), function(model_name) {
  purrr::map_dfr(c("mhcscore", "cesdscore", "cesdbin3"), function(outcome) {
    fit <- fit_hearts(outcome, model_name, poisson = outcome == "cesdbin3")
    fit$table |>
      dplyr::filter(stringr::str_starts(term, "visual_arts_frequency")) |>
      dplyr::mutate(outcome = outcome, model = model_name, .before = 1)
  })
})

secondary_outcomes <- c("ucla3score", "djgscore", "soconscore2")
secondary <- purrr::map_dfr(secondary_outcomes, function(outcome) {
  fit_hearts(outcome, "model_3")$table |>
    dplyr::filter(stringr::str_starts(term, "visual_arts_frequency")) |>
    dplyr::mutate(outcome = outcome, model = "model_3", .before = 1)
})

trend <- purrr::map_dfr(c("mhcscore", "cesdscore", secondary_outcomes), function(outcome) {
  formula <- stats::reformulate(c("visual_arts_order", covariates$model_3), response = outcome)
  hc3_tidy(stats::lm(formula, data = hearts)) |>
    dplyr::filter(term == "visual_arts_order") |>
    dplyr::mutate(outcome = outcome, .before = 1)
})

model3_mhc <- fit_hearts("mhcscore", "model_3")$model
model3_cesd <- fit_hearts("cesdscore", "model_3")$model
model3_case <- fit_hearts("cesdbin3", "model_3", poisson = TRUE)$model

marginal <- dplyr::bind_rows(
  as.data.frame(emmeans::emmeans(model3_mhc, ~ visual_arts_frequency, vcov. = sandwich::vcovHC(model3_mhc, type = "HC3"))) |>
    dplyr::transmute(outcome = "MHC-SF", category = visual_arts_frequency, estimate = emmean, std.error = SE, conf.low = lower.CL, conf.high = upper.CL),
  as.data.frame(emmeans::emmeans(model3_cesd, ~ visual_arts_frequency, vcov. = sandwich::vcovHC(model3_cesd, type = "HC3"))) |>
    dplyr::transmute(outcome = "CES-D", category = visual_arts_frequency, estimate = emmean, std.error = SE, conf.low = lower.CL, conf.high = upper.CL)
)

distribution <- hearts |>
  dplyr::count(visual_arts_frequency, name = "n") |>
  dplyr::mutate(percent = 100 * n / sum(n))

sensitivity <- dplyr::bind_rows(
  fit_hearts("mhcscore", "model_3", exposure = "any_visual_arts")$table |>
    dplyr::filter(term == "any_visual_artsAny") |>
    dplyr::mutate(outcome = "mhcscore", analysis = "any versus none"),
  fit_hearts("cesdscore", "model_3", exposure = "any_visual_arts")$table |>
    dplyr::filter(term == "any_visual_artsAny") |>
    dplyr::mutate(outcome = "cesdscore", analysis = "any versus none"),
  fit_hearts("mhcscore", "model_3", extra = c("other_receptive_arts", "partscore"))$table |>
    dplyr::filter(stringr::str_starts(term, "visual_arts_frequency")) |>
    dplyr::mutate(outcome = "mhcscore", analysis = "adjusted for other arts")
)

write_result(distribution, "results/tables/hearts_exposure_distribution.csv")
write_result(primary, "results/tables/hearts_primary_models.csv")
write_result(secondary, "results/tables/hearts_secondary_outcomes.csv")
write_result(trend, "results/tables/hearts_ordered_trends.csv")
write_result(marginal, "data/derived/hearts_adjusted_marginal_estimates.csv")
write_result(sensitivity, "results/tables/hearts_sensitivity_models.csv")
saveRDS(hearts, "data/processed/hearts_analysis.rds")
