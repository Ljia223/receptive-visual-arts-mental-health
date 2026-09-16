trupp_url <- paste0(
  "https://raw.githubusercontent.com/giacomobignardi/",
  "Trupp-online-art-wellbeing/3e3fc8af1a892a9a13cadd89f840394958ff4bda/",
  "03_outputs/processedData/03_df_pre_post.csv"
)
trupp_path <- "data/raw/trupp/03_df_pre_post.csv"
if (!file.exists(trupp_path)) download.file(trupp_url, trupp_path, mode = "wb", quiet = FALSE)

zenodo_base <- "https://zenodo.org/api/records/16412669/files/"
castellotti_files <- c(
  "AnxietyState_STAI-S.xlsx", "AnxietyTrait_STAI-T.xlsx", "ArtExpertise.xlsx",
  "ArtPreferences.xlsx", "Compassion_CLS-H-SF.xlsx", "Curiosity_CEI-II.xlsx",
  "Empathy_IRI.xlsx", "OpennessToExperience_BFAS.xlsx", "Post-visitQuestionnaire.xlsx",
  "VAIAK.xlsx", "VisitTime.xlsx"
)
for (filename in castellotti_files) {
  destination <- file.path("data/raw/castellotti", filename)
  if (!file.exists(destination)) {
    url <- paste0(zenodo_base, utils::URLencode(filename, reserved = TRUE), "/content")
    download.file(url, destination, mode = "wb", quiet = FALSE)
  }
}

hearts_path <- "data/raw/doi_10_5061_dryad_3r2280gdj__v20210226.zip"
if (!file.exists(hearts_path)) {
  stop("Download the HEartS archive from https://doi.org/10.5061/dryad.3r2280gdj and place it at ", hearts_path)
}
