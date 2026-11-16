# analyze_curve.py - Lesson 3 (version 2): tipping-point analysis
# Run:  python analyze_curve.py                 (all curve_*.jsonl files in "results")
#  or:  python analyze_curve.py results\curve_....jsonl

import json
import math
import random
import sys
from pathlib import Path

BOOTSTRAP_ROUNDS = 2000
STANCES = ("board_pro", "board_con")


def load(paths):
    records = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    record["file"] = path.name     # remember where each answer came from
                    records.append(record)
    for r in records:                     # files from version 1 lack these fields
        r.setdefault("condition", "normal")
        r.setdefault("wording", 1)
    return records


def mean(values):
    return sum(values) / len(values) if values else float("nan")


def approve(r):
    return 1 if r["verdict"] == "APPROVE" else 0


# --- primary measure: sum of approval differences (Spearman-Kaerber) ---

def cells_of(rs, persona, levels):
    """Dict level -> list of 0/1 outcomes for one persona."""
    return {lv: [approve(r) for r in rs if r["persona"] == persona and r["level"] == lv]
            for lv in levels}


def shift_sum(cells_a, cells_b, levels):
    """S = sum over levels of (share APPROVE of a - share APPROVE of b), in levels."""
    return sum(mean(cells_a[lv]) - mean(cells_b[lv]) for lv in levels)


def bootstrap_shift(cells_a, cells_b, levels, rng):
    """Resample within each cell, recompute S; return the bootstrap values (unsorted)."""
    values = []
    for _ in range(BOOTSTRAP_ROUNDS):
        s = 0.0
        for lv in levels:
            a, b = cells_a[lv], cells_b[lv]
            s += mean([rng.choice(a) for _ in a]) - mean([rng.choice(b) for _ in b])
        values.append(s)
    return values


def interval(values):
    """Middle 95 percent of the bootstrap values."""
    ordered = sorted(values)
    n = len(ordered)
    return ordered[int(0.025 * n)], ordered[int(0.975 * n) - 1]


def report_shift(label, est, lo, hi):
    print(f"  {label:<44} S = {est:+.2f}  95% interval [{lo:+.2f}, {hi:+.2f}]")
    if lo > 0 or hi < 0:
        print(f"  {'':<44} -> the interval excludes 0")
    else:
        print(f"  {'':<44} -> no effect shown; the shift is at most {max(abs(lo), abs(hi)):.2f} levels")


# --- secondary: logistic fit, used for the figure ---

def fit_logistic(points, steps=30, ridge=0.01):
    """Fit p(x) = 1 / (1 + exp(-(a + b*x))) to (x, y) points with y in {0, 1}.
    Newton's method on the log-likelihood; the small ridge term keeps a and b
    finite when the data are perfectly separated. Returns (a, b)."""
    a, b = 0.0, 0.0
    for _ in range(steps):
        ga, gb = -ridge * a, -ridge * b          # gradient
        haa, hab, hbb = ridge, 0.0, ridge        # minus the Hessian
        for x, y in points:
            p = 1 / (1 + math.exp(-max(-30, min(30, a + b * x))))
            w = p * (1 - p)
            ga += y - p
            gb += (y - p) * x
            haa += w
            hab += w * x
            hbb += w * x * x
        det = haa * hbb - hab * hab
        if det <= 0:
            break
        da = (hbb * ga - hab * gb) / det        # Newton step: solve the 2x2 system
        db = (haa * gb - hab * ga) / det
        step = max(1.0, math.hypot(da, db) / 5)  # damping: no huge jumps
        a += da / step
        b += db / step
    return a, b


def tipping_point(points):
    """Level at which the fitted approval probability is 50 percent, or None."""
    a, b = fit_logistic(points)
    return None if b <= 0.05 else -a / b


# --- main part ---

def main():
    rng = random.Random(1)  # fixed seed: the same data always give the same intervals
    paths = [Path(p) for p in sys.argv[1:]] or sorted(Path("results").glob("curve_*.jsonl"))
    all_records = load(paths)
    print("Files:", ", ".join(str(p) for p in paths))

    for model in sorted({r["model"] for r in all_records}):
        for condition in sorted({r["condition"] for r in all_records if r["model"] == model}):
            group = [r for r in all_records if r["model"] == model and r["condition"] == condition]
            rs = [r for r in group if r["verdict"] is not None]
            personas = [p for p in ("board_pro", "board_con", "board_none", "neutral")
                        if any(r["persona"] == p for r in group)]
            levels = sorted({r["level"] for r in group})
            print(f"\n=== {model}, condition '{condition}': {len(group)} answers ===")

            def cell(persona, level, data=rs):
                return [r for r in data if r["persona"] == persona and r["level"] == level]

            print("\nShare APPROVE  (answers with verdict / without)")
            print(f"{'level':<7}" + "".join(f"{p:>18}" for p in personas))
            for lv in levels:
                row = f"{lv:<7}"
                for p in personas:
                    c = cell(p, lv)
                    missing = len(cell(p, lv, group)) - len(c)
                    row += f"{mean([approve(r) for r in c]):>10.0%} ({len(c):>2}/{missing})"
                print(row)

            print("\nMean PROBABILITY (0-100)")
            print(f"{'level':<7}" + "".join(f"{p:>18}" for p in personas))
            for lv in levels:
                row = f"{lv:<7}"
                for p in personas:
                    probs = [r["probability"] for r in cell(p, lv) if r["probability"] is not None]
                    row += f"{mean(probs):>18.0f}"
                print(row)

            # Primary measure
            if all(p in personas for p in STANCES):
                print("\nPrimary measure: sum of approval differences over the measured levels")
                pro, con = cells_of(rs, "board_pro", levels), cells_of(rs, "board_con", levels)
                if any(not pro[lv] or not con[lv] for lv in levels):
                    print("  (some cells are empty; measure skipped)")
                else:
                    boot = bootstrap_shift(pro, con, levels, rng)
                    report_shift("board_pro minus board_con", shift_sum(pro, con, levels), *interval(boot))
                    if "board_none" in personas:
                        none = cells_of(rs, "board_none", levels)
                        for p, cells in (("board_pro", pro), ("board_con", con)):
                            b2 = bootstrap_shift(cells, none, levels, rng)
                            report_shift(f"{p} minus control", shift_sum(cells, none, levels), *interval(b2))
                    print("  Positive S: the convinced asker gets approval earlier than the doubtful one.")

                    # Same measure per wording (5 runs per cell each: rough, but shows consistency)
                    wordings = sorted({r["wording"] for r in rs})
                    if len(wordings) > 1:
                        print("\n  Per wording (pro wording i against con wording i):")
                        for w in wordings:
                            sub = [r for r in rs if r["wording"] == w]
                            pw, cw = cells_of(sub, "board_pro", levels), cells_of(sub, "board_con", levels)
                            if all(pw[lv] and cw[lv] for lv in levels):
                                print(f"    wording {w}: S = {shift_sum(pw, cw, levels):+.2f}")

                    if "board_none" in personas:
                        ctrl = [mean(none[lv]) for lv in levels]
                        if levels[0] == 0 and levels[-1] == 5 and (ctrl[0] > 0.2 or ctrl[-1] < 0.8):
                            print("\n  Warning: the control does not run from near 0 to near 1;"
                                  " S then underestimates the shift.")

            # Secondary: fitted tipping points (for the figure)
            print("\nFitted tipping point (level at 50 % APPROVE; for the figure, not the test)")
            for p in personas:
                t = tipping_point([(r["level"], approve(r)) for r in rs if r["persona"] == p])
                print(f"  {p:<12} {'   -' if t is None else f'{t:5.2f}'}")

            ctrl_name = "board_none" if "board_none" in personas else personas[-1]
            undecided = [lv for lv in levels if 0.15 <= mean([approve(r) for r in cell(ctrl_name, lv)]) <= 0.85]
            print(f"\nLevels where the control '{ctrl_name}' is undecided (15-85 % APPROVE): {undecided or 'none'}")

            print(f"Mean words: {mean([r['words'] for r in group]):.0f}; "
                  f"cut off at max_tokens: {sum(1 for r in group if r['stop_reason'] == 'max_tokens')}; "
                  f"tokens {sum(r['input_tokens'] for r in group)} in, "
                  f"{sum(r['output_tokens'] for r in group)} out")

        # Accountability: compare the shift between conditions on the same levels
        conds = {r["condition"] for r in all_records if r["model"] == model}
        if {"normal", "accountable"} <= conds:
            acc = [r for r in all_records if r["model"] == model and r["condition"] == "accountable"
                   and r["verdict"] is not None]
            # compare only with 'normal' answers measured in the same run (same files)
            acc_files = {r["file"] for r in acc}
            nor = [r for r in all_records if r["model"] == model and r["condition"] == "normal"
                   and r["verdict"] is not None and r["file"] in acc_files]
            levels = sorted({r["level"] for r in acc})
            print(f"\n=== {model}: accountability, levels {levels} ===")
            results = {}
            for name, data in (("normal", nor), ("accountable", acc)):
                pro, con = cells_of(data, "board_pro", levels), cells_of(data, "board_con", levels)
                if any(not pro[lv] or not con[lv] for lv in levels):
                    print(f"  {name}: some cells are empty; skipped")
                    continue
                boot = bootstrap_shift(pro, con, levels, rng)
                results[name] = (shift_sum(pro, con, levels), boot)
                report_shift(f"{name}: board_pro minus board_con", results[name][0], *interval(boot))
            if len(results) == 2:
                # the two bootstrap series are independent, so pairing them in order is valid
                diff = [b - a for a, b in zip(results["normal"][1], results["accountable"][1])]
                report_shift("change in S (accountable minus normal)",
                             results["accountable"][0] - results["normal"][0], *interval(diff))
                print("  Negative change: accountability shrinks the stance effect.")
            for name, data in (("normal", nor), ("accountable", acc)):
                probs = [r["probability"] for r in data if r["probability"] is not None and r["level"] in levels]
                print(f"  mean PROBABILITY on these levels, {name}: {mean(probs):.0f}")


# Run main() only when the file is started directly, not when another
# script imports its functions (plot_curve.py does that).
if __name__ == "__main__":
    main()
