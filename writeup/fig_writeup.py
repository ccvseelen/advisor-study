# fig_writeup.py - figure for the write-up. Written by Claude.
# Usage: python fig_writeup.py <main_run.jsonl> <accountability_run.jsonl> <out.png>
import json, sys
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def shares(path):
    c = defaultdict(list)
    for line in open(path, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            if r["verdict"] in ("APPROVE", "REJECT"):
                c[(r["condition"], r["persona"], r["level"])].append(r["verdict"] == "APPROVE")
    return {k: sum(v) / len(v) for k, v in c.items()}

main, acc = shares(sys.argv[1]), shares(sys.argv[2])
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
STYLE = {"board_pro": ("#2a78d6", "o", "convinced"),
         "board_con": ("#eb6834", "s", "doubtful"),
         "board_none": ("#52514e", "D", "no stance (control)")}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": MUTED,
                     "text.color": INK, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.3), sharey=True,
                           gridspec_kw={"width_ratios": [6, 3.6], "wspace": 0.08})
for ax in (a, b):
    ax.set_facecolor("white"); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(length=0); ax.set_ylim(-0.04, 1.04)
    ax.set_yticks([0, .25, .5, .75, 1]); ax.set_yticklabels(["0 %", "25 %", "50 %", "75 %", "100 %"])
for p in ("board_none", "board_con", "board_pro"):
    col, mk, lab = STYLE[p]
    lv = range(6)
    a.plot(lv, [main[("normal", p, l)] for l in lv], color=col, lw=2, marker=mk, ms=6,
           mec="white", mew=1.2, label=lab, zorder=3 if p != "board_none" else 2)
    lv = [1, 2, 3]
    b.plot(lv, [acc[("normal", p, l)] for l in lv], color=col, lw=2, marker=mk, ms=6, mec="white", mew=1.2)
    b.plot(lv, [acc[("accountable", p, l)] for l in lv], color=col, lw=1.6, ls=(0, (4, 2)), marker=mk, ms=6,
           mfc="white", mec=col, mew=1.4)
a.set_xticks(range(6)); a.set_xlim(-0.3, 5.3); b.set_xticks([1, 2, 3]); b.set_xlim(0.7, 3.3)
a.set_xlabel("strength of the case (open points resolved, of 5)")
b.set_xlabel("strength of the case")
a.set_ylabel("share of answers recommending APPROVE")
a.set_title("A  Main run: who asks moves the threshold", loc="left", fontsize=9.5, fontweight="bold")
b.set_title("B  With accountability note", loc="left", fontsize=9.5, fontweight="bold")
h, l = a.get_legend_handles_labels()
order = [l.index("convinced"), l.index("no stance (control)"), l.index("doubtful")]
a.legend([h[i] for i in order], [l[i] for i in order], title="The board member asking is …", frameon=False,
         loc="upper left", fontsize=8.5, title_fontsize=8.5, handlelength=2.6, alignment="left")
a.annotate("doubtful asker needs\n≈ 0.9 levels more", xy=(2.62, 0.455), xytext=(3.2, 0.2), fontsize=8, color=MUTED,
           arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
from matplotlib.lines import Line2D
b.legend(handles=[Line2D([], [], color=MUTED, lw=2, marker="o", ms=5, mec="white", label="normal"),
                  Line2D([], [], color=MUTED, lw=1.6, ls=(0, (4, 2)), marker="o", ms=5, mfc="white", mec=MUTED,
                         label="accountable")],
         frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8.5, handlelength=2.6)
fig.savefig(sys.argv[3], dpi=220, bbox_inches="tight", facecolor="white")
