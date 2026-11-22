# pilot_summary.py - which calibration puts Fable's tipping point inside 0-5?
# Written by Claude, 22 Nov 2026.
# Usage:  python pilot_summary.py results\calib_fable-5-2_pilot_<date>.jsonl
# Applies the selection rule in PREREG_calibrated.md (control answers only).

import json
import sys
from collections import defaultdict

rows = [json.loads(line) for line in open(sys.argv[1], encoding="utf-8") if line.strip()]
cells = defaultdict(list)
for r in rows:
    cells[(r["variant"], r["level"])].append(r)

variants = sorted({r["variant"] for r in rows})
levels = sorted({r["level"] for r in rows})

def share_approve(rs):
    rs = [r for r in rs if r["verdict"]]
    return sum(r["verdict"] == "APPROVE" for r in rs) / len(rs) if rs else float("nan")

def mean_prob(rs):
    ps = [r["probability"] for r in rs if r["probability"] is not None]
    return sum(ps) / len(ps) if ps else float("nan")

print("Control only. Share APPROVE / mean PROBABILITY per level\n")
print("variant  labour  " + "".join(f"   level {lv:<8}" for lv in levels))
for v in variants:
    labour = cells[(v, levels[0])][0]["labour_savings"]
    row = f"{v:>7}  {labour:>6}  "
    for lv in levels:
        c = cells[(v, lv)]
        row += f"   {share_approve(c):>4.0%} / {mean_prob(c):>3.0f}  "
    print(row)

# Selection rule (pre-specified): the variant whose control rejects at the
# weakest level and approves at the strongest, with level 2 closest to 50 %.
# Ties: mean PROBABILITY at level 2 closest to the midpoint of levels 0 and 5.
lo, mid, hi = levels[0], levels[len(levels) // 2], levels[-1]
candidates = [v for v in variants
              if share_approve(cells[(v, lo)]) <= 0.5 and share_approve(cells[(v, hi)]) >= 0.5]
print()
if not candidates:
    print("No variant spans the threshold. Do not start the main run; look at the table.")
else:
    def key(v):
        p0, p5 = mean_prob(cells[(v, lo)]), mean_prob(cells[(v, hi)])
        return (abs(share_approve(cells[(v, mid)]) - 0.5),
                abs(mean_prob(cells[(v, mid)]) - (p0 + p5) / 2))
    best = min(candidates, key=key)
    print(f"Candidates spanning the threshold: {candidates}")
    print(f"Chosen by the rule: variant {best}  ->  set VARIANTS_TO_RUN = ['{best}'] and MODE = 'main'")

tin = sum(r["input_tokens"] for r in rows)
tout = sum(r["output_tokens"] for r in rows)
cost = (tin * 8 + tout * 40) / 1e6
print(f"\nTokens: {tin} in, {tout} out; pilot cost about USD {cost:.2f}")
print(f"Main run (360 calls) would cost about USD {cost / len(rows) * 360:.2f}")
