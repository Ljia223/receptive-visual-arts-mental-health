import json
import os
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data/raw/doi_10_5061_dryad_3r2280gdj__v20210226.zip"
OUT = "/tmp/hearts33"
os.makedirs(OUT, exist_ok=True)
with zipfile.ZipFile(ZIP) as archive:
    member = next(name for name in archive.namelist() if name.endswith("Dataset.xlsx"))
    archive.extract(member, OUT)
df = pd.read_excel(os.path.join(OUT, member))
df["exp4"] = pd.cut(df["rart8"], [-1, 0, 2, 4, 6], labels=[0, 1, 2, 3]).astype(int)
df["anyexp"] = (df["rart8"] > 0).astype(int)
df["ethnic6"] = pd.cut(df["ethnicgroups"], [0, 4, 8, 13, 16, 17, 18], labels=[1, 2, 3, 4, 5, 6]).astype(int)
df["other_receptive"] = df["rartscore"] - df["anyexp"]

def design(data, exposure="exp4", model=3, other_arts=False, exposure_categorical=True):
    parts = [np.ones((len(data), 1))]
    names = ["Intercept"]
    def add_numeric(var):
        parts.append(data[[var]].to_numpy(float))
        names.append(var)
    def add_cat(var):
        fixed_levels = {
            "exp4": [0, 1, 2, 3], "anyexp": [0, 1], "rart8": list(range(7)),
            "agecat": list(range(1, 8)), "ethnic6": list(range(1, 7)),
            "educ4": list(range(1, 5)), "srh3": list(range(1, 4)),
            "mild": list(range(4)), "mod": list(range(4)), "vig": list(range(4)),
            "partnerclose3": list(range(1, 4)),
        }
        observed = fixed_levels.get(var, sorted(data[var].unique()))
        for value in observed[1:]:
            parts.append((data[var].to_numpy() == value).astype(float)[:, None])
            names.append(f"{var}[{value}]")
    if exposure_categorical:
        add_cat(exposure)
    else:
        add_numeric(exposure)
    add_cat("agecat")
    add_cat("ethnic6")
    if model >= 2:
        add_cat("educ4")
        add_numeric("artprofbin")
    if model >= 3:
        add_cat("srh3")
        add_cat("mild")
        add_cat("mod")
        add_cat("vig")
        add_cat("partnerclose3")
    if other_arts:
        add_numeric("other_receptive")
        add_numeric("partscore")
    return np.hstack(parts), names

def ols_fit(y, X, names):
    n, k = X.shape
    xtx_inv = np.linalg.pinv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    resid = y - X @ beta
    h = np.sum((X @ xtx_inv) * X, axis=1)
    adj = resid / np.maximum(1 - h, 1e-8)
    meat = X.T @ (X * (adj ** 2)[:, None])
    cov = xtx_inv @ meat @ xtx_inv
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    tval = beta / se
    p = 2 * stats.t.sf(np.abs(tval), n - k)
    crit = stats.t.ppf(0.975, n - k)
    return {"beta": beta, "cov": cov, "se": se, "p": p, "lo": beta-crit*se, "hi": beta+crit*se, "names": names}

def poisson_fit(y, X, names):
    beta = np.zeros(X.shape[1])
    for _ in range(200):
        eta = np.clip(X @ beta, -20, 20)
        mu = np.exp(eta)
        z = eta + (y - mu) / mu
        new = np.linalg.pinv(X.T @ (X * mu[:, None])) @ (X.T @ (mu * z))
        if np.max(np.abs(new - beta)) < 1e-10:
            beta = new
            break
        beta = new
    mu = np.exp(np.clip(X @ beta, -20, 20))
    bread = np.linalg.pinv(X.T @ (X * mu[:, None]))
    h = mu * np.sum((X @ bread) * X, axis=1)
    score = (y - mu) / np.maximum(1 - h, 1e-8)
    meat = X.T @ (X * (score ** 2)[:, None])
    cov = bread @ meat @ bread
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    p = 2 * stats.norm.sf(np.abs(beta / se))
    return {"beta": beta, "cov": cov, "se": se, "p": p, "lo": beta-1.96*se, "hi": beta+1.96*se, "names": names}

def term(res, name, exponentiate=False):
    i = res["names"].index(name)
    vals = [res[x][i] for x in ["beta", "se", "lo", "hi", "p"]]
    out = dict(zip(["estimate", "se", "lo", "hi", "p"], map(float, vals)))
    if exponentiate:
        out["estimate"], out["lo"], out["hi"] = map(float, np.exp([out["estimate"], out["lo"], out["hi"]]))
    return out

def exposure_terms(res, exposure="exp4", levels=(1, 2, 3), exponentiate=False):
    return {str(level): term(res, f"{exposure}[{level}]", exponentiate) for level in levels}

def marginal(res, exposure, levels, model=3, other_arts=False, poisson=False):
    out = {}
    for level in levels:
        new = df.copy()
        new[exposure] = level
        X, names = design(new, exposure, model, other_arts, True)
        assert names == res["names"]
        if poisson:
            mu = np.exp(np.clip(X @ res["beta"], -20, 20))
            est = mu.mean()
            grad = (X * mu[:, None]).mean(axis=0)
        else:
            grad = X.mean(axis=0)
            est = grad @ res["beta"]
        se = np.sqrt(grad @ res["cov"] @ grad)
        out[str(level)] = {"estimate": float(est), "lo": float(est-1.96*se), "hi": float(est+1.96*se)}
    return out

def wald(res, constraints):
    R = np.zeros((len(constraints), len(res["names"])))
    for row, mapping in enumerate(constraints):
        for name, value in mapping.items():
            R[row, res["names"].index(name)] = value
    rb = R @ res["beta"]
    V = R @ res["cov"] @ R.T
    stat = float(rb @ np.linalg.pinv(V) @ rb)
    return {"chi2": stat, "df": len(constraints), "p": float(stats.chi2.sf(stat, len(constraints)))}

results = {"n": int(len(df))}
results["distribution"] = {str(k): {"n": int(v), "pct": float(100*v/len(df))} for k, v in df.exp4.value_counts().sort_index().items()}
desc = {}
for g, s in df.groupby("exp4"):
    desc[str(g)] = {
        "age18_35": float(100*s.agecat.isin([1,2]).mean()),
        "age56plus": float(100*s.agecat.isin([5,6,7]).mean()),
        "degree": float(100*(s.educ4==1).mean()),
        "arts_prof": float(100*(s.artprofbin==1).mean()),
        "no_partner": float(100*(s.partnerclose3==1).mean()),
        "close_partner": float(100*(s.partnerclose3==3).mean()),
        "good_health": float(100*(s.srh3==1).mean()),
        "mhc": float(s.mhcscore.mean()), "cesd": float(s.cesdscore.mean()),
        "case": float(100*s.cesdbin3.mean()), "ucla": float(s.ucla3score.mean()),
        "djg": float(s.djgscore.mean()), "social": float(s.soconscore2.mean()),
    }
results["descriptive"] = desc

models = {}
for outcome in ["mhcscore", "cesdscore"]:
    models[outcome] = {}
    for m in [1,2,3]:
        X,names = design(df, model=m)
        res = ols_fit(df[outcome].to_numpy(float), X, names)
        models[outcome][f"m{m}"] = exposure_terms(res)
        if m == 3:
            models[outcome]["marginal"] = marginal(res, "exp4", [0,1,2,3])
models["cesdbin3"] = {}
for m in [1,2,3]:
    X,names = design(df, model=m)
    res = poisson_fit(df.cesdbin3.to_numpy(float), X, names)
    models["cesdbin3"][f"m{m}"] = exposure_terms(res, exponentiate=True)
    if m == 3:
        models["cesdbin3"]["marginal"] = marginal(res, "exp4", [0,1,2,3], poisson=True)
results["models"] = models

trend = {}
for outcome in ["mhcscore", "cesdscore", "ucla3score", "djgscore", "soconscore2"]:
    X,names = design(df, model=3, exposure_categorical=False)
    lin = ols_fit(df[outcome].to_numpy(float), X, names)
    X,names = design(df, model=3)
    cat = ols_fit(df[outcome].to_numpy(float), X, names)
    nonlinear = wald(cat, [{"exp4[2]":1, "exp4[1]":-2}, {"exp4[3]":1, "exp4[1]":-3}])
    trend[outcome] = {"linear": term(lin, "exp4"), "nonlinear": nonlinear, "categorical": exposure_terms(cat), "marginal": marginal(cat, "exp4", [0,1,2,3])}
results["trend_secondary"] = trend

def interaction_design(group):
    X,names = design(df, model=3)
    for e in [1,2,3]:
        for level in sorted(df[group].unique())[1:]:
            X = np.column_stack([X, ((df.exp4==e)&(df[group]==level)).astype(float)])
            names.append(f"exp4[{e}]:{group}[{level}]")
    return X,names

interactions = {}
for outcome in ["mhcscore", "cesdscore", "cesdbin3"]:
    interactions[outcome] = {}
    for group in ["educ4", "partnerclose3"]:
        X,names = interaction_design(group)
        if outcome == "cesdbin3":
            res = poisson_fit(df[outcome].to_numpy(float), X, names)
        else:
            res = ols_fit(df[outcome].to_numpy(float), X, names)
        iterms = [n for n in names if ":" in n]
        interactions[outcome][group] = wald(res, [{name:1} for name in iterms])
        contrasts = {}
        for level in sorted(df[group].unique()):
            contrasts[str(level)] = {}
            for e in [1,2,3]:
                mapping = {f"exp4[{e}]": 1}
                if level != sorted(df[group].unique())[0]:
                    mapping[f"exp4[{e}]:{group}[{level}]"] = 1
                R = np.zeros(len(names))
                for name,value in mapping.items(): R[names.index(name)] = value
                est = float(R @ res["beta"])
                se = float(np.sqrt(R @ res["cov"] @ R))
                if outcome == "cesdbin3":
                    contrasts[str(level)][str(e)] = {"estimate": float(np.exp(est)), "lo": float(np.exp(est-1.96*se)), "hi": float(np.exp(est+1.96*se))}
                else:
                    contrasts[str(level)][str(e)] = {"estimate": est, "lo": est-1.96*se, "hi": est+1.96*se}
        interactions[outcome][group]["contrasts"] = contrasts
results["interactions"] = interactions

sens = {}
for outcome in ["mhcscore", "cesdscore"]:
    X,names = design(df, model=3, other_arts=True)
    other = ols_fit(df[outcome].to_numpy(float), X, names)
    X,names = design(df, exposure="anyexp", model=3)
    anyres = ols_fit(df[outcome].to_numpy(float), X, names)
    X,names = design(df, exposure="rart8", model=3)
    seven = ols_fit(df[outcome].to_numpy(float), X, names)
    sens[outcome] = {"other_arts": exposure_terms(other), "any": term(anyres, "anyexp[1]"), "seven": exposure_terms(seven, "rart8", range(1,7))}
X,names = design(df, model=3, other_arts=True)
otherp = poisson_fit(df.cesdbin3.to_numpy(float), X, names)
sens["cesdbin3"] = {"other_arts": exposure_terms(otherp, exponentiate=True)}
results["sensitivity"] = sens

with open(ROOT / "results/machine-readable/hearts_model_results.json", "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2)
print(json.dumps(results, indent=2))
