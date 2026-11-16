# plot_curve.py - Lesson 3 (version 2): draw the approval curves
# Needs matplotlib:  python -m pip install matplotlib
# Run:  python plot_curve.py                 (all curve_*.jsonl files in "results")
#  or:  python plot_curve.py results\curve_....jsonl
# Draws the 'normal' condition only; writes results\curve_<model>.png

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt

from analyze_curve import approve, fit_logistic, load, mean

COLORS = {"board_pro": "#2a78d6", "board_con": "#d4691c", "board_none": "#6b6b6b"}
LABELS = {"board_pro": "board member, convinced",
          "board_con": "board member, doubtful",
          "board_none": "board member, no stance (control)"}

paths = [Path(p) for p in sys.argv[1:]] or sorted(Path("results").glob("curve_*.jsonl"))
records = [r for r in load(paths) if r["verdict"] is not None and r["condition"] == "normal"]

for model in sorted({r["model"] for r in records}):
    rs = [r for r in records if r["model"] == model]
    levels = sorted({r["level"] for r in rs})
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for persona in [p for p in COLORS if any(r["persona"] == p for r in rs)]:
        own = [r for r in rs if r["persona"] == persona]
        color = COLORS[persona]
        # measured share APPROVE per level, as dots
        shares = [mean([approve(r) for r in own if r["level"] == lv]) for lv in levels]
        ax.plot(levels, shares, "o", color=color, label=LABELS[persona])
        # fitted logistic curve, as a line
        a, b = fit_logistic([(r["level"], approve(r)) for r in own])
        xs = [levels[0] + i * (levels[-1] - levels[0]) / 100 for i in range(101)]
        ax.plot(xs, [1 / (1 + math.exp(-max(-30, min(30, a + b * x)))) for x in xs], "-", color=color)
    ax.axhline(0.5, color="#bbbbbb", linewidth=0.8, linestyle=":")
    ax.set_xlabel("strength of the case (open points resolved)")
    ax.set_ylabel("share of answers recommending APPROVE")
    ax.set_xticks(levels)
    ax.set_ylim(-0.03, 1.03)
    ax.set_title(f"Where does the advice tip? ({model})")
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = Path("results") / f"curve_{model.replace('claude-', '')}.png"
    fig.savefig(out, dpi=150)
    print(f"Saved {out}")
