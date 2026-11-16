# wording.py - effect of each stance wording against the no-stance control.
# Written by Claude. Usage:
#   python wording.py results\<file>.jsonl            (all levels in the file)
#   python wording.py results\<file>.jsonl 1 2 3      (only these levels)
# For each condition in the file: share APPROVE of stance wording i minus the
# share APPROVE of the whole control (all four control wordings pooled),
# summed over the levels; 95 % interval by bootstrap within cells.
import json
import random
import sys
from collections import defaultdict

rows = [json.loads(line) for line in open(sys.argv[1], encoding="utf-8") if line.strip()]
LEVELS = [int(x) for x in sys.argv[2:]] or sorted({r["level"] for r in rows})
CONDITIONS = sorted({r["condition"] for r in rows}, key=lambda c: (c != "normal", c))
STANCES = ["board_pro", "board_con"]

cells = defaultdict(list)          # (condition, persona, wording, level) -> list of 0/1
for r in rows:
    if r["verdict"] in ("APPROVE", "REJECT"):
        cells[(r["condition"], r["persona"], r["wording"], r["level"])].append(
            1 if r["verdict"] == "APPROVE" else 0)

def share(xs):
    return sum(xs) / len(xs)

def sample(key, rng):
    """The answers of one cell; with rng, a bootstrap resample of them."""
    if key[0] == "control":
        _, cond, level = key
        xs = [x for w in range(1, 5) for x in cells[(cond, "board_none", w, level)]]
    else:
        xs = cells[key]
    return [rng.choice(xs) for _ in xs] if rng else xs

def effect(persona, wording, conds, rng=None):
    """Sum over levels of (wording minus control), averaged over the conditions."""
    total = 0.0
    for c in conds:
        total += sum(share(sample((c, persona, wording, lv), rng))
                     - share(sample(("control", c, lv), rng)) for lv in LEVELS)
    return total / len(conds)

rng = random.Random(1)
groups = [([c], c) for c in CONDITIONS]
if len(CONDITIONS) > 1:
    groups.append((CONDITIONS, "mean of conditions"))
print(f"File: {sys.argv[1]}   levels: {LEVELS}")
for conds, label in groups:
    print(f"\n== {label} ==  wording minus pooled control, summed over levels")
    for p in STANCES:
        for w in range(1, 5):
            est = effect(p, w, conds)
            boot = sorted(effect(p, w, conds, rng) for _ in range(2000))
            n = sum(len(cells[(c, p, w, LEVELS[0])]) for c in conds)
            print(f"  {p:10s} wording {w}: {est:+.2f}  [{boot[50]:+.2f}, {boot[1949]:+.2f}]"
                  f"  (n = {n} per level)")

print("\nShare APPROVE per wording and level  (" + " | ".join(CONDITIONS) + ")")
for p in STANCES + ["board_none"]:
    for w in range(1, 5):
        parts = [" ".join(f"{share(cells[(c, p, w, lv)]):.1f}" for lv in LEVELS)
                 for c in CONDITIONS]
        print(f"  {p:10s} wording {w}: " + " | ".join(parts))
