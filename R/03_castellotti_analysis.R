read_castellotti <- function(filename) {
  x <- readxl::read_excel(file.path("data/raw/castellotti", filename))
  names(x)[1] <- "id"
  x
}

state <- read_castellotti("AnxietyState_STAI-S.xlsx") |>
  dplyr::transmute(id, anxiety_pre = `STAI-S Pre-visit (score)`, anxiety_post = `STAI-S Post-visit (score)`)
trait <- read_castellotti("AnxietyTrait_STAI-T.xlsx") |>
  dplyr::transmute(id, trait_anxiety = `Anxiety Trait (STAI-T)`)
preferences <- read_castellotti("ArtPreferences.xlsx") |>
  dplyr::transmute(id, art_preference = `Art Preference`)
openness <- read_castellotti("OpennessToExperience_BFAS.xlsx") |>
  dplyr::transmute(id, openness = `OTE (BFAS)`)
curiosity <- read_castellotti("Curiosity_CEI-II.xlsx") |>
  dplyr::transmute(id, curiosity = `Curiosity (CEI-II)`)
ratings <- read_castellotti("Post-visitQuestionnaire.xlsx") |>
  dplyr::transmute(id, beauty = `5. Beauty `, understanding = `8. Understanding`, satisfaction = `24. Satisfaction`)
visit <- readxl::read_excel("data/raw/castellotti/VisitTime.xlsx") |>
  dplyr::transmute(id = sprintf("S%02d", Subject), visit_minutes = `Visit time`)

castellotti <- purrr::reduce(
  list(state, trait, preferences, openness, curiosity, ratings, visit),
  dplyr::full_join, by = "id"
) |>
  dplyr::mutate(change = anxiety_post - anxiety_pre)
stopifnot(nrow(castellotti) == 92L)

long <- castellotti |>
  dplyr::select(id, anxiety_pre, anxiety_post) |>
  tidyr::pivot_longer(c(anxiety_pre, anxiety_post), names_to = "time", values_to = "state_anxiety") |>
  dplyr::mutate(time = factor(time, levels = c("anxiety_pre", "anxiety_post")))
time_model <- lmerTest::lmer(state_anxiety ~ time + (1 | id), data = long, REML = FALSE)

trait_unadjusted <- stats::lm(change ~ scale(trait_anxiety), data = castellotti)
trait_adjusted <- stats::lm(change ~ scale(trait_anxiety) + anxiety_pre, data = castellotti)
exploratory <- purrr::map_dfr(
  c("art_preference", "openness", "curiosity", "visit_minutes", "beauty", "understanding", "satisfaction"),
  function(variable) {
    model <- stats::lm(stats::as.formula(paste("change ~ anxiety_pre + scale(", variable, ")")), data = castellotti)
    hc3_tidy(model) |>
      dplyr::filter(stringr::str_detect(term, "scale")) |>
      dplyr::mutate(variable = variable)
  }
) |>
  dplyr::mutate(p.fdr = stats::p.adjust(p.value, method = "BH"))

g <- bootstrap_g_av(castellotti$anxiety_pre, castellotti$anxiety_post)
acute <- tibble::tibble(
  dataset = "Castellotti 2025", estimate_type = "within-group post minus pre",
  group = "in-person exhibition", n = unname(g["n"]), estimate = unname(g["estimate"]),
  conf.low = unname(g["conf.low"]), conf.high = unname(g["conf.high"])
)

write_result(broom.mixed::tidy(time_model, effects = "fixed", conf.int = TRUE), "results/tables/castellotti_time_model.csv")
write_result(hc3_tidy(trait_unadjusted), "results/tables/castellotti_trait_unadjusted.csv")
write_result(hc3_tidy(trait_adjusted), "results/tables/castellotti_trait_baseline_adjusted.csv")
write_result(exploratory, "results/tables/castellotti_exploratory_associations.csv")
write_result(acute, "data/derived/castellotti_within_group_effect.csv")
saveRDS(castellotti, "data/processed/castellotti_analysis.rds")
