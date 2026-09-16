import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/figures/Figure_1_cross_design_framework.pdf"


def box(ax, x, y, w, h, face, edge, title, lines, title_size=11.5, body_size=9.1):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.25,
        edgecolor=edge,
        facecolor=face,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h - 0.055, title,
        ha="center", va="top", fontsize=title_size,
        fontweight="bold", color="#17324D", zorder=3,
    )
    ax.text(
        x + 0.025, y + h - 0.115, "\n".join(lines),
        ha="left", va="top", fontsize=body_size,
        color="#263645", linespacing=1.35, zorder=3,
    )
    return patch


def arrow(ax, start, end, color="#667987", lw=1.35):
    ax.add_patch(FancyArrowPatch(
        start, end,
        arrowstyle="-|>", mutation_scale=13,
        linewidth=lw, color=color,
        connectionstyle="arc3,rad=0", zorder=1,
    ))


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, ax = plt.subplots(figsize=(13.1, 7.6))
fig.patch.set_facecolor("white")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.text(
    0.5, 0.965, "Harmonized Cross-Design Analytical Framework",
    ha="center", va="top", fontsize=16.2, fontweight="bold", color="#17324D"
)
ax.text(
    0.5, 0.925,
    "Three independent open datasets are analyzed separately and integrated through evidence triangulation",
    ha="center", va="top", fontsize=10.2, color="#526575"
)

cols = [0.035, 0.3525, 0.67]
w = 0.295
h = 0.38
y = 0.49

box(
    ax, cols[0], y, w, h, "#EAF2F8", "#5B8DB8", "Trupp 2022",
    [
        "Online quasi-randomized pre-post study",
        "N = 84 adults",
        "",
        "Exposure",
        "Digital visual art viewing",
        "",
        "Comparator",
        "Active non-art cultural content",
        "",
        "Primary estimand",
        "Time by Condition anxiety contrast",
    ],
)

box(
    ax, cols[1], y, w, h, "#EDF5F1", "#6B9B83", "Castellotti 2025",
    [
        "In-person uncontrolled field study",
        "N = 92 adults",
        "",
        "Exposure",
        "Guided immersive exhibition visit",
        "",
        "Temporal structure",
        "Pre-visit and post-visit assessment",
        "",
        "Primary estimand",
        "Standardized within-person anxiety change",
    ],
)

box(
    ax, cols[2], y, w, h, "#F4F0F7", "#8C75A5", "HEartS 2019",
    [
        "Cross-sectional online survey",
        "N = 5,338 UK adults",
        "",
        "Exposure",
        "12-month visual-arts attendance frequency",
        "",
        "Outcomes",
        "Well-being, depression, loneliness,",
        "and social connectedness",
        "",
        "Primary estimand",
        "Covariate-adjusted frequency associations",
    ],
)

band_y = 0.34
band_h = 0.09
band = FancyBboxPatch(
    (0.08, band_y), 0.84, band_h,
    boxstyle="round,pad=0.01,rounding_size=0.015",
    linewidth=1.25, edgecolor="#78909C", facecolor="#F3F6F8", zorder=2,
)
ax.add_patch(band)
ax.text(
    0.5, band_y + band_h * 0.68,
    "Construct-level harmonization with dataset-specific analysis",
    ha="center", va="center", fontsize=11.4, fontweight="bold", color="#274456"
)
ax.text(
    0.5, band_y + band_h * 0.30,
    "No individual-level pooling  |  Common effect direction  |  Design-specific estimands and uncertainty",
    ha="center", va="center", fontsize=9.2, color="#526575"
)

for c in cols:
    arrow(ax, (c + w / 2, y), (c + w / 2, band_y + band_h), color="#718491")

tri_y = 0.155
tri_h = 0.125
tri = FancyBboxPatch(
    (0.14, tri_y), 0.72, tri_h,
    boxstyle="round,pad=0.012,rounding_size=0.018",
    linewidth=1.45, edgecolor="#315B78", facecolor="#DFEAF1", zorder=2,
)
ax.add_patch(tri)
ax.text(
    0.5, tri_y + tri_h * 0.72, "Cross-design evidence triangulation",
    ha="center", va="center", fontsize=12.6, fontweight="bold", color="#17324D"
)
ax.text(
    0.5, tri_y + tri_h * 0.36,
    "Direction  |  Magnitude  |  Precision  |  Robustness  |  Design-specific limitations",
    ha="center", va="center", fontsize=9.8, color="#314D60"
)
arrow(ax, (0.5, band_y), (0.5, tri_y + tri_h), color="#536F80", lw=1.55)

ax.text(
    0.5, 0.075,
    "Integrated inference on immediate anxiety change, art specificity, and habitual visual-arts engagement",
    ha="center", va="center", fontsize=10.8, fontweight="bold", color="#334E60"
)
arrow(ax, (0.5, tri_y), (0.5, 0.102), color="#536F80", lw=1.45)

plt.subplots_adjust(left=0.015, right=0.985, top=0.985, bottom=0.025)
fig.savefig(OUT, format="pdf", bbox_inches="tight", pad_inches=0.08)
plt.close(fig)
