assert_columns <- function(data, columns, label) {
  absent <- setdiff(columns, names(data))
  if (length(absent) > 0) stop(label, " is missing: ", paste(absent, collapse = ", "))
  invisible(data)
}

hc3_tidy <- function(model, exponentiate = FALSE) {
  test <- lmtest::coeftest(model, vcov. = sandwich::vcovHC(model, type = "HC3"))
  out <- tibble::tibble(
    term = rownames(test), estimate = test[, 1], std.error = test[, 2],
    statistic = test[, 3], p.value = test[, 4]
  )
  critical <- stats::qt(0.975, df = stats::df.residual(model))
  out$conf.low <- out$estimate - critical * out$std.error
  out$conf.high <- out$estimate + critical * out$std.error
  if (exponentiate) out[c("estimate", "conf.low", "conf.high")] <- exp(out[c("estimate", "conf.low", "conf.high")])
  out
}

robust_glm_tidy <- function(model, exponentiate = TRUE) {
  test <- lmtest::coeftest(model, vcov. = sandwich::vcovHC(model, type = "HC3"))
  out <- tibble::tibble(
    term = rownames(test), estimate = test[, 1], std.error = test[, 2],
    statistic = test[, 3], p.value = test[, 4],
    conf.low = test[, 1] - 1.96 * test[, 2],
    conf.high = test[, 1] + 1.96 * test[, 2]
  )
  if (exponentiate) out[c("estimate", "conf.low", "conf.high")] <- exp(out[c("estimate", "conf.low", "conf.high")])
  out
}

hedges_g_av <- function(pre, post) {
  keep <- stats::complete.cases(pre, post)
  pre <- pre[keep]
  post <- post[keep]
  n <- length(pre)
  raw <- mean(post - pre) / sqrt((stats::var(pre) + stats::var(post)) / 2)
  correction <- 1 - 3 / (4 * (2 * n - 2) - 1)
  correction * raw
}

bootstrap_g_av <- function(pre, post, repetitions = 5000, seed = 2026) {
  keep <- stats::complete.cases(pre, post)
  values <- data.frame(pre = pre[keep], post = post[keep])
  set.seed(seed)
  fit <- boot::boot(values, function(d, i) hedges_g_av(d$pre[i], d$post[i]), R = repetitions)
  interval <- boot::boot.ci(fit, type = "perc")$percent[4:5]
  c(estimate = fit$t0, conf.low = interval[1], conf.high = interval[2], n = nrow(values))
}

between_change_g <- function(pre, post, group) {
  keep <- stats::complete.cases(pre, post, group)
  data <- data.frame(pre = pre[keep], post = post[keep], group = droplevels(factor(group[keep])))
  if (nlevels(data$group) != 2L) stop("The between-condition effect requires two groups")
  split_data <- split(data, data$group)
  n1 <- nrow(split_data[[1]])
  n2 <- nrow(split_data[[2]])
  change_1 <- mean(split_data[[1]]$post - split_data[[1]]$pre)
  change_2 <- mean(split_data[[2]]$post - split_data[[2]]$pre)
  pooled_baseline <- sqrt(((n1 - 1) * stats::var(split_data[[1]]$pre) + (n2 - 1) * stats::var(split_data[[2]]$pre)) / (n1 + n2 - 2))
  correction <- 1 - 3 / (4 * (n1 + n2) - 9)
  correction * (change_2 - change_1) / pooled_baseline
}

bootstrap_between_change_g <- function(pre, post, group, repetitions = 5000, seed = 2026) {
  keep <- stats::complete.cases(pre, post, group)
  data <- data.frame(pre = pre[keep], post = post[keep], group = factor(group[keep]))
  groups <- levels(data$group)
  set.seed(seed)
  estimates <- replicate(repetitions, {
    sampled <- dplyr::bind_rows(lapply(groups, function(value) {
      subset <- data[data$group == value, , drop = FALSE]
      subset[sample.int(nrow(subset), replace = TRUE), , drop = FALSE]
    }))
    between_change_g(sampled$pre, sampled$post, sampled$group)
  })
  c(
    estimate = between_change_g(data$pre, data$post, data$group),
    conf.low = unname(stats::quantile(estimates, 0.025)),
    conf.high = unname(stats::quantile(estimates, 0.975)), n = nrow(data)
  )
}

write_result <- function(data, path) {
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  readr::write_csv(data, path, na = "")
  invisible(data)
}
