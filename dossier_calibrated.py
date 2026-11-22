# dossier_calibrated.py - the Nordwerk case with weaker economics, so that
# Claude Fable 5.2's approval threshold falls inside levels 0-5.
# Written by Claude, 22 Nov 2026.
#
# Only ONE parameter changes: the annual labour savings. Everything that
# follows from it (payback figures, downside case) is recalculated with the
# same arithmetic as in dossier_levels.py:
#   net investment   = 140 + 90 - 20 = EUR 210 million   (unchanged)
#   annual benefit   = labour savings + 3 logistics
#   payback          = 210 / benefit
#   payback credited = (210 - 45) / benefit   (avoided modernisation credited)
#   downside case    = payback x 1.25, rounded to half a year
#                      (the original: 4.4 -> "within 5.5 years")
# All other facts, open points and their order are taken unchanged from
# dossier_levels.py. Variant "base" reproduces the original dossier exactly;
# the check at the bottom of this file confirms that.

import dossier_levels as original

NET_INVESTMENT = 140 + 90 - 20      # EUR million
MODERNISATION = 45                  # EUR million, avoided if Nordwerk moves
LOGISTICS = 3                       # EUR million per year

# labour savings in EUR million per year
VARIANTS = {"base": 45, "A": 35, "B": 28, "C": 22, "D": 15}


def figures(variant):
    """Payback (plain), payback (credited) and downside bound for a variant."""
    benefit = VARIANTS[variant] + LOGISTICS
    plain = round(NET_INVESTMENT / benefit, 1)
    credited = round((NET_INVESTMENT - MODERNISATION) / benefit, 1)
    downside = round(NET_INVESTMENT / benefit * 1.25 * 2) / 2
    return plain, credited, downside


def years(x):
    """4.4 -> '4.4', 7.0 -> '7'."""
    return f"{x:g}"


def fixed_facts(variant):
    facts = list(original.FIXED)
    facts[0] = (f"Labour costs at the new site would be EUR {VARIANTS[variant]} "
                f"million per year lower.")
    return facts


def open_points(variant):
    plain, credited, downside = figures(variant)
    points = [dict(p) for p in original.OPEN_POINTS]
    head = (f"Management's business case shows a payback of {years(credited)} years if the "
            f"avoided modernisation is credited and {years(plain)} years if not; ")
    for p in points:
        if p["id"] == "downside":
            p["risk"] = head + ("both figures assume stable exchange rates and no "
                                "disruption during the transfer.")
            p["resolved"] = head + ("an independent downside case (10 percent currency "
                                    "move, 12-month ramp-up, 15 percent volume loss in the "
                                    f"first year) still shows a payback within "
                                    f"{years(downside)} years.")
    return points


def build_dossier(level, variant):
    """Dossier text for a level (0-5) and a calibration variant."""
    lines = fixed_facts(variant)
    for i, point in enumerate(open_points(variant)):
        lines.append(point["resolved"] if i < level else point["risk"])
    numbered = "\n".join(f"{n}. {text}" for n, text in enumerate(lines, start=1))
    return f"{original.HEADER}\n\nFacts:\n{numbered}"


FACTS = original.FACTS   # keyword lists for the crude fact count (unchanged)

# Safety check: variant "base" must give exactly the original dossier.
for _level in original.LEVELS:
    assert build_dossier(_level, "base") == original.build_dossier(_level), \
        f"variant 'base' differs from dossier_levels.py at level {_level}"


if __name__ == "__main__":
    # Run "python dossier_calibrated.py" to see the figures and one dossier.
    print("variant  labour  payback  credited  downside")
    for v in VARIANTS:
        p, c, d = figures(v)
        print(f"{v:>7}  {VARIANTS[v]:>6}  {p:>7}  {c:>8}  {d:>8}")
    print("\nCheck passed: variant 'base' equals the original dossier.\n")
    print(build_dossier(0, "B"))
