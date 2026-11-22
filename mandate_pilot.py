# mandate_pilot.py - where is the control's threshold under the mandate?
# Written by Claude, 22 Nov 2026.
# Usage:  python mandate_pilot.py results\calib_fable-5-2_mandate-pilot_<date>.jsonl
# Applies the selection rule in PREREG_mandate.md (control answers only).

import json
import sys
from collections import defaultdict

rows = [json.loads(line) for line in open(sys.argv[1], encoding="utf-8") if line.strip()]
cells = defaultdict(list)
for r in rows:
    cells[(r["variant"], r["level"])].append(r)
levels = sorted({r["level"] for r in rows})
order = [v for v in ("B", "A", "base") if any(r["variant"] == v for r in rows)]

def share(rs):
    rs = [r for r in rs if r["verdict"]]
    return sum(r["verdict"] == "APPROVE" for r in rs) / len(rs) if rs else float("nan")

def prob(rs):
    ps = [r["probability"] for r in rs if r["probability"] is not None]
    return sum(ps) / len(ps) if ps else float("nan")

print("Mandate, control only. Share APPROVE / mean PROBABILITY per level\n")
print("variant  labour  " + "".join(f"   level {lv:<8}" for lv in levels))
for v in order:
    row = f"{v:>7}  {cells[(v, levels[0])][0]['labour_savings']:>6}  "
    for lv in levels:
        row += f"   {share(cells[(v, lv)]):>4.0%} / {prob(cells[(v, lv)]):>3.0f}  "
    print(row)

# Rule: the first of B, A, base whose control approves at the strongest level.
chosen = next((v for v in order if share(cells[(v, levels[-1])]) >= 0.5), None)
print()
if chosen is None:
    print("The control rejects even the strongest dossier of every variant. "
          "No main run; look at the answers.")
    sys.exit()

# Crossing of 50 % APPROVE, linear between the measured levels.
s = [share(cells[(chosen, lv)]) for lv in levels]
if s[0] >= 0.5:
    x = levels[0]
else:
    i = next(k for k in range(1, len(levels)) if s[k] >= 0.5)
    x = levels[i - 1] + (0.5 - s[i - 1]) / (s[i] - s[i - 1]) * (levels[i] - levels[i - 1])
centre = min(4, max(1, round(x)))
main_levels = [centre - 1, centre, centre + 1]
print(f"Chosen variant: {chosen}; control crosses 50 % near level {x:.1f}")
print(f"-> set VARIANTS_TO_RUN = ['{chosen}'], LEVELS = {main_levels}, MODE = 'main'")

tin = sum(r["input_tokens"] for r in rows)
tout = sum(r["output_tokens"] for r in rows)
per_call = (tin * 8 + tout * 40) / 1e6 / len(rows)
print(f"\nPilot cost about USD {per_call * len(rows):.2f}; "
      f"{tout / len(rows):.0f} output tokens per call")
print(f"Main run (180 calls) would cost about USD {per_call * 180:.2f}")

hits = [r for r in rows if any(k in r["answer"].lower() for k in
        ("hurdle", "benchmark", "typical", "usual", "industry", "standard", "require"))]
print(f"\nAnswers that mention a standard or requirement: {len(hits)} of {len(rows)}")
