# -*- coding: utf-8 -*-
"""Plot UltraFeedback per-metric round dynamics for PIRO and IRL baseline."""
from pathlib import Path
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-nwpu")

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 7.8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.65,
    "xtick.major.width": 0.55,
    "ytick.major.width": 0.55,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "legend.frameon": False,
})

metrics = [
    "Writing", "Roleplay", "Reasoning", "Math",
    "Coding", "Extraction", "STEM", "Humanities",
]
rounds = np.array([1, 2, 3])

irl = {
    "Writing": [6.65, 6.58, 6.60],
    "Roleplay": [6.03, 5.85, 5.97],
    "Reasoning": [6.53, 6.48, 6.21],
    "Math": [9.60, 9.12, 9.50],
    "Coding": [7.92, 7.48, 7.20],
    "Extraction": [7.75, 7.75, 7.82],
    "STEM": [7.88, 7.82, 7.85],
    "Humanities": [7.30, 6.97, 6.70],
}
piro = {
    "Writing": [6.22, 6.45, 6.50],
    "Roleplay": [5.95, 6.40, 6.33],
    "Reasoning": [7.05, 7.73, 6.85],
    "Math": [9.18, 9.15, 9.25],
    "Coding": [7.58, 7.40, 7.66],
    "Extraction": [7.98, 7.87, 8.18],
    "STEM": [7.95, 8.18, 7.97],
    "Humanities": [6.72, 7.08, 6.90],
}
# Best score for each metric across all reported methods/checkpoints in Table 4-5.
best = {
    "Writing": 6.90,
    "Roleplay": 6.40,
    "Reasoning": 7.73,
    "Math": 9.62,
    "Coding": 8.18,
    "Extraction": 8.18,
    "STEM": 8.18,
    "Humanities": 7.30,
}

colors = {
    "PIRO": "#D95F59",       # muted coral
    "IRL baseline": "#4C78A8",  # slate blue
    "Best": "#7A7A7A",
}

fig, axes = plt.subplots(2, 4, figsize=(6.75, 4.05), sharex=True)
axes = axes.ravel()

for ax, metric in zip(axes, metrics):
    y_irl = np.asarray(irl[metric])
    y_piro = np.asarray(piro[metric])
    y_best = best[metric]
    values = np.r_[y_irl, y_piro, y_best]
    span = max(values.max() - values.min(), 0.35)
    ymin = values.min() - 0.18 * span
    ymax = values.max() + 0.22 * span

    ax.axhline(y_best, color=colors["Best"], lw=0.85, ls=(0, (2.2, 2.2)), zorder=1)
    ax.plot(rounds, y_irl, color=colors["IRL baseline"], lw=1.45, marker="o", ms=3.2,
            mfc="white", mec=colors["IRL baseline"], mew=0.9, zorder=3)
    ax.plot(rounds, y_piro, color=colors["PIRO"], lw=1.55, marker="o", ms=3.4,
            mfc=colors["PIRO"], mec="white", mew=0.55, zorder=4)

    ax.set_title(metric, fontsize=8.4, fontweight="bold", pad=3.0)
    ax.set_xlim(0.82, 3.18)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([1, 2, 3])
    ax.grid(axis="y", color="#E6E6E6", lw=0.55)
    ax.tick_params(labelsize=7.0, pad=1.5)


    yticks = ax.get_yticks()
    if len(yticks) > 4:
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(4))

for ax in axes[::4]:
    ax.set_ylabel("Score", fontsize=7.6, labelpad=2.5)
for ax in axes[4:]:
    ax.set_xlabel("Round", fontsize=7.6, labelpad=2.0)

handles = [
    mpl.lines.Line2D([0], [0], color=colors["PIRO"], lw=1.6, marker="o", ms=3.5, label="PIRO"),
    mpl.lines.Line2D([0], [0], color=colors["IRL baseline"], lw=1.5, marker="o", ms=3.3,
                     mfc="white", label="IRL baseline"),
    mpl.lines.Line2D([0], [0], color=colors["Best"], lw=0.9, ls=(0, (2.2, 2.2)),
                     label="Best score"),
]
fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.02),
           fontsize=7.8, handlelength=2.0, columnspacing=1.7)

fig.subplots_adjust(left=0.065, right=0.995, bottom=0.105, top=0.88, wspace=0.32, hspace=0.47)

out = Path("figures/uf_round_metrics")
fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
fig.savefig(out.with_suffix(".svg"), bbox_inches="tight")
fig.savefig(out.with_suffix(".png"), dpi=600, bbox_inches="tight")
plt.close(fig)
