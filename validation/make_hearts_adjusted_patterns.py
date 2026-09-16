import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
with open(ROOT / "results/machine-readable/hearts_model_results.json", encoding="utf-8") as stream:
    results = json.load(stream)

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 9.2,
    "axes.titlesize": 10.2,
    "axes.labelsize": 9.2,
    "xtick.labelsize": 8.2,
    "ytick.labelsize": 8.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.linewidth": 0.75,
})

labels = ["None", "One-off or\n1--2 yearly", "Every few months\nor monthly", "Weekly or\ndaily"]
x = np.arange(4)
color = "#3E687D"
line_color = "#9BB3BF"

panels = [
    ("A", "Mental well-being", "MHC-SF score", results["models"]["mhcscore"]["marginal"], "estimate", False),
    ("B", "Depressive symptoms", "CES-D score", results["models"]["cesdscore"]["marginal"], "estimate", False),
    ("C", "Elevated depressive symptoms", "Adjusted prevalence", results["models"]["cesdbin3"]["marginal"], "estimate", True),
    ("D", "UCLA loneliness", "UCLA three-item score", results["trend_secondary"]["ucla3score"]["marginal"], "estimate", False),
    ("E", "De Jong Gierveld loneliness", "De Jong Gierveld score", results["trend_secondary"]["djgscore"]["marginal"], "estimate", False),
    ("F", "Social connectedness", "Social connectedness score", results["trend_secondary"]["soconscore2"]["marginal"], "estimate", False),
]

fig, axes = plt.subplots(2, 3, figsize=(12.2, 6.5), constrained_layout=False)
for ax, (letter, title, ylabel, values, key, proportion) in zip(axes.flat, panels):
    y = np.array([values[str(i)][key] for i in range(4)])
    lo = np.array([values[str(i)]["lo"] for i in range(4)])
    hi = np.array([values[str(i)]["hi"] for i in range(4)])
    ax.plot(x, y, color=line_color, linewidth=1.4, zorder=1)
    ax.errorbar(
        x, y, yerr=np.vstack([y-lo, hi-y]), fmt="o", markersize=5.8,
        markerfacecolor=color, markeredgecolor="white", markeredgewidth=0.7,
        ecolor=color, elinewidth=1.15, capsize=3.2, capthick=1.0, zorder=3,
    )
    ax.set_title(title, pad=8, fontweight="semibold")
    ax.text(-0.15, 1.08, letter, transform=ax.transAxes, fontsize=11.5, fontweight="bold", va="top")
    ax.set_ylabel(ylabel)
    ax.set_xticks(x, labels)
    ax.grid(axis="y", color="#D9DEE2", linewidth=0.65, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#7A858C")
    ax.spines["bottom"].set_color("#7A858C")
    ax.tick_params(axis="x", length=0, pad=6)
    ax.tick_params(axis="y", colors="#31373B")
    span = max(hi) - min(lo)
    pad = max(span * 0.16, 0.08 if not proportion else 0.015)
    ax.set_ylim(min(lo)-pad, max(hi)+pad)
    if proportion:
        ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(1.0, decimals=0))

fig.supxlabel("Visual-arts attendance during the preceding 12 months", y=0.035, fontsize=10)
fig.subplots_adjust(left=0.075, right=0.985, top=0.92, bottom=0.15, wspace=0.34, hspace=0.47)

output = ROOT / "results/figures/Figure_3_HEartS_adjusted_patterns.pdf"
fig.savefig(output, format="pdf", bbox_inches="tight", pad_inches=0.04)
fig.savefig(ROOT / "results/figures/Figure_3_HEartS_adjusted_patterns.png", dpi=240, bbox_inches="tight", pad_inches=0.04)
plt.close(fig)
print(output)
