import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


labels = [
    "Trupp 2022  Online visual art  n = 40",
    "Trupp 2022  Active cultural control  n = 44",
    "Castellotti 2025  In-person exhibition  n = 92",
    "Trupp 2022  Art versus cultural control",
]

effects = np.array([-0.369, -0.212, -0.420, -0.114])
lower = np.array([-0.686, -0.417, -0.583, -0.416])
upper = np.array([-0.137, -0.028, -0.278, 0.167])
y = np.array([3.8, 2.8, 1.8, 0.25])

colors = ["#4F7C78", "#7B8794", "#8A708B", "#344F68"]
markers = ["s", "s", "s", "D"]

plt.rcParams.update(
    {
        "font.family": "Nimbus Sans",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 10.5,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

fig, ax = plt.subplots(figsize=(9.0, 5.2), facecolor="white")
ax.set_facecolor("white")

ax.axvspan(-0.80, 0, color="#F3F7F6", zorder=0)
ax.axvline(0, color="#59636E", linewidth=1.15, linestyle="--", zorder=1)
ax.axhline(1.03, color="#D6DADF", linewidth=0.9, zorder=1)

for i in range(len(effects)):
    ax.errorbar(
        effects[i],
        y[i],
        xerr=np.array([[effects[i] - lower[i]], [upper[i] - effects[i]]]),
        fmt=markers[i],
        color=colors[i],
        ecolor=colors[i],
        markersize=7.8 if i < 3 else 8.5,
        markeredgecolor="white",
        markeredgewidth=0.8,
        elinewidth=2.0,
        capsize=4.0,
        capthick=1.5,
        zorder=3,
    )

ax.set_yticks(y)
ax.set_yticklabels(labels, ha="right")
ax.tick_params(axis="y", length=0, pad=10)

ax.set_xlim(-0.80, 0.25)
ax.set_ylim(-0.55, 4.55)
ax.set_xticks([-0.75, -0.50, -0.25, 0, 0.25])
ax.set_xlabel("Standardized anxiety change with 95% confidence interval", labelpad=12)
ax.set_title("Standardized Anxiety Change Across Online and In-Person Settings", loc="left", pad=22, weight="semibold")

ax.text(-0.795, 4.25, "Within-condition change", color="#3D4650", fontsize=9.5, weight="semibold", va="bottom")
ax.text(-0.795, 0.65, "Between-condition contrast", color="#3D4650", fontsize=9.5, weight="semibold", va="bottom")

for yi, est, lo, hi in zip(y, effects, lower, upper):
    ax.text(
        1.035,
        yi,
        f"{est:.3f}  [{lo:.3f}, {hi:.3f}]",
        transform=ax.get_yaxis_transform(),
        ha="left",
        va="center",
        fontsize=9.2,
        color="#28323C",
        clip_on=False,
    )

ax.text(1.035, 4.25, "Effect  [95% CI]", transform=ax.get_yaxis_transform(), ha="left", va="bottom", fontsize=9.3, color="#3D4650", weight="semibold", clip_on=False)

for side in ["top", "right", "left"]:
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#8C949C")
ax.spines["bottom"].set_linewidth(0.8)
ax.grid(axis="x", color="#E5E8EB", linewidth=0.7, zorder=0)
ax.set_axisbelow(True)

fig.text(
    0.075,
    0.015,
    "Negative values indicate anxiety reduction. No pooled effect was calculated.",
    ha="left",
    va="bottom",
    fontsize=8.6,
    color="#59636E",
)

fig.subplots_adjust(left=0.41, right=0.73, top=0.84, bottom=0.20)
fig.savefig(ROOT / "results/figures/Figure_2_standardized_anxiety_change.pdf", bbox_inches="tight", facecolor="white")
fig.savefig(ROOT / "results/figures/Figure_2_standardized_anxiety_change.png", dpi=600, bbox_inches="tight", facecolor="white")
plt.close(fig)
