# analyze.py - Lesson 2: summarise a results file
# Run:  python analyze.py                      (newest file in "results")
#  or:  python analyze.py results\run_....jsonl  (a specific file)

import json
import sys
from pathlib import Path

from dossier import FACTS


def load(path):
    """Read a JSONL file: one JSON record per line."""
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def mean(values):
    return sum(values) / len(values) if values else float("nan")


if len(sys.argv) > 1:
    path = Path(sys.argv[1])
else:
    path = sorted(Path("results").glob("run_*.jsonl"))[-1]

records = load(path)
print(f"File: {path}  ({len(records)} answers)\n")

# Group the records by persona; the order follows the file.
groups = {}
for r in records:
    groups.setdefault(r["persona"], []).append(r)

# Table 1: verdict, confidence, length
print(f"{'persona':<12}{'n':>4}{'approve':>10}{'conf.':>8}{'words':>8}{'no verdict':>12}{'thinking':>10}")
for name, rs in groups.items():
    with_verdict = [r for r in rs if r["verdict"]]
    approve_rate = mean([1 if r["verdict"] == "APPROVE" else 0 for r in with_verdict])
    confidence = mean([r["confidence"] for r in rs if r["confidence"] is not None])
    words = mean([r["words"] for r in rs])
    missing = len(rs) - len(with_verdict)
    thinking = mean([1 if r["thinking"] else 0 for r in rs])
    print(f"{name:<12}{len(rs):>4}{approve_rate:>10.0%}{confidence:>8.0f}{words:>8.0f}{missing:>12}{thinking:>10.0%}")

# Table 2: how often each fact is mentioned, per persona
print(f"\n{'fact':<28}{'side':<9}" + "".join(f"{name:>11}" for name in groups))
for fact in FACTS:
    row = f"{fact['label']:<28}{fact['side']:<9}"
    for name, rs in groups.items():
        share = mean([1 if r["facts"][fact["id"]] else 0 for r in rs])
        row += f"{share:>11.0%}"
    print(row)

truncated = sum(1 for r in records if r["stop_reason"] == "max_tokens")
if truncated:
    print(f"\nWarning: {truncated} answers were cut off at max_tokens.")