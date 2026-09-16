# Computational environment

The primary analysis target is R 4.4.2. Package dependencies are declared in the repository `DESCRIPTION` file and are checked before analysis begins.

The independent validation target is Python 3.12 with the packages listed in `requirements-validation.txt`.

The fixed random seed is 2026 for bootstrap procedures. Linear models use HC3 heteroskedasticity-consistent standard errors. Modified Poisson models use a log link and HC3 robust covariance estimation. All tests are two sided and confidence intervals use a 95 percent level.
