acute <- readr::read_csv("data/derived/acute_standardized_effects.csv", show_col_types = FALSE) |>
  dplyr::mutate(label = dplyr::case_when(
    dataset == "Trupp 2022" & group == "art" ~ "Online visual art",
    dataset == "Trupp 2022" & group == "non_art" ~ "Active cultural content",
    dataset == "Trupp 2022" ~ "Online between-condition contrast",
    TRUE ~ "In-person exhibition"
  )) |>
  dplyr::mutate(label = factor(label, levels = rev(c(
    "Online visual art", "Active cultural content", "Online between-condition contrast", "In-person exhibition"
  ))))

forest <- ggplot2::ggplot(acute, ggplot2::aes(estimate, label)) +
  ggplot2::geom_vline(xintercept = 0, linewidth = 0.5, color = "grey55") +
  ggplot2::geom_errorbarh(ggplot2::aes(xmin = conf.low, xmax = conf.high), height = 0.12, linewidth = 0.65) +
  ggplot2::geom_point(size = 2.5, color = "#176B87") +
  ggplot2::labs(x = "Standardized anxiety change", y = NULL) +
  ggplot2::theme_classic(base_size = 11)
ggplot2::ggsave("results/figures/Figure_2_standardized_anxiety_change.pdf", forest, width = 8.2, height = 4.5)

marginal <- readr::read_csv("data/derived/hearts_adjusted_marginal_estimates.csv", show_col_types = FALSE) |>
  dplyr::mutate(category = factor(category, levels = c("None", "Infrequent", "Regular", "Weekly or daily")))
dose <- ggplot2::ggplot(marginal, ggplot2::aes(category, estimate, group = outcome, color = outcome)) +
  ggplot2::geom_line(linewidth = 0.7) +
  ggplot2::geom_point(size = 2.3) +
  ggplot2::geom_errorbar(ggplot2::aes(ymin = conf.low, ymax = conf.high), width = 0.12) +
  ggplot2::facet_wrap(~ outcome, scales = "free_y") +
  ggplot2::scale_color_manual(values = c("MHC-SF" = "#176B87", "CES-D" = "#B24C63"), guide = "none") +
  ggplot2::labs(x = "Visual-arts attendance", y = "Adjusted marginal estimate") +
  ggplot2::theme_classic(base_size = 11) +
  ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 20, hjust = 1))
ggplot2::ggsave("results/figures/Figure_3_HEartS_adjusted_patterns.pdf", dose, width = 9.4, height = 4.8)
