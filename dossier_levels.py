# dossier_levels.py - Lesson 3: the case material in six levels of strength
# This file holds data, not logic: you may copy it instead of typing it.
# All facts and numbers are invented.
#
# Version of 12 Nov 2026: social plan as a separate cost item (EUR 90 million,
# about EUR 50,000 per head), labour savings EUR 45 million per year,
# payback 4.4 years (3.4 with the avoided modernisation credited).
# Check: 140 + 90 - 20 = 210 net; 45 + 3 = 48 per year;
#        210 / 48 = 4.4 years; (210 - 45) / 48 = 3.4 years.
#
# The fixed facts never change.

HEADER = """Decision: Nordwerk Components (brake components, 2,600 employees in Kassel,
Germany) proposes to move its main plant to a new site in Eastern Europe.
The supervisory board votes on Friday. It must approve or reject the proposal
as it stands; a deferral is not possible."""

FIXED = [
    "Labour costs at the new site would be EUR 45 million per year lower.",
    "A competitor that relocated in 2022 now prices about 15 percent below "
    "Nordwerk; Nordwerk lost two major tenders in 2026 on price.",
    "If Nordwerk stays, the Kassel plant needs a EUR 45 million modernisation by 2028.",
    "The new site is 400 km closer to two growing customer plants, saving about "
    "EUR 3 million per year in logistics.",
    "The regional government offers a EUR 20 million investment grant.",
    "The one-off relocation cost is EUR 140 million over two years. In addition, "
    "a social plan for the 1,800 employees who would lose their jobs is budgeted "
    "at EUR 90 million (about EUR 50,000 per head).",
]

# The order of this list is the order in which the points get resolved.
OPEN_POINTS = [
    {
        "id": "customers",
        "risk": "Two key customers require a new quality audit; one has said it will "
                "consider alternative suppliers during the transition.",
        "resolved": "Both key customers have signed letters of intent to keep their "
                    "volumes through the transition; the new site passed their quality "
                    "audit in a pilot run.",
    },
    {
        "id": "transition",
        "risk": "The competitor that relocated in 2022 reported 18 months of delivery "
                "problems after the move.",
        "resolved": "The competitor that relocated in 2022 reported 18 months of delivery "
                    "problems; Nordwerk's plan runs both plants in parallel for nine "
                    "months with eight weeks of buffer stock, costed within the "
                    "EUR 140 million.",
    },
    {
        "id": "co2",
        "risk": "Electricity at the new site comes from a grid with about 30 percent "
                "higher CO2 intensity; two key customers will require suppliers to cut "
                "emissions from 2028.",
        "resolved": "Two key customers will require suppliers to cut emissions from 2028; "
                    "Nordwerk has signed a ten-year renewable power contract for the new "
                    "site, priced into the business case, which puts the site's emissions "
                    "below Kassel's.",
    },
    {
        "id": "downside",
        "risk": "Management's business case shows a payback of 3.4 years if the avoided "
                "modernisation is credited and 4.4 years if not; both figures assume "
                "stable exchange rates and no disruption during the transfer.",
        "resolved": "Management's business case shows a payback of 3.4 years if the avoided "
                    "modernisation is credited and 4.4 years if not; an independent "
                    "downside case (10 percent currency move, 12-month ramp-up, 15 percent "
                    "volume loss in the first year) still shows a payback within 5.5 years.",
    },
    {
        "id": "social",
        "risk": "1,800 of the 2,600 jobs in Kassel would be cut; Nordwerk is the largest "
                "employer in the district. The social plan has not yet been negotiated "
                "with the works council.",
        "resolved": "1,800 of the 2,600 jobs in Kassel would be cut; Nordwerk is the largest "
                    "employer in the district. The social plan (severance, retraining, "
                    "early retirement) has been agreed with the works council within the "
                    "EUR 90 million.",
    },
]

LEVELS = list(range(len(OPEN_POINTS) + 1))  # 0, 1, 2, 3, 4, 5


def build_dossier(level):
    """Return the dossier text for a level from 0 (all risks) to 5 (all resolved)."""
    lines = list(FIXED)
    for i, point in enumerate(OPEN_POINTS):
        lines.append(point["resolved"] if i < level else point["risk"])
    numbered = "\n".join(f"{n}. {text}" for n, text in enumerate(lines, start=1))
    return f"{HEADER}\n\nFacts:\n{numbered}"


# Keywords for counting which facts an answer mentions (crude first measure).
# Labour savings and modernisation are both EUR 45 million, so neither uses
# "45 million" as a keyword; otherwise one would be counted for the other.
FACTS = [
    {"id": "F01", "side": "pro", "label": "labour savings",
     "keywords": ["labour", "labor", "48 million", "eur 48", "€48"]},
    {"id": "F02", "side": "pro", "label": "competitor price/tenders",
     "keywords": ["tender", "15 percent", "15%", "15 %", "price gap", "competitor"]},
    {"id": "F03", "side": "pro", "label": "avoided modernisation",
     "keywords": ["moderni"]},
    {"id": "F04", "side": "pro", "label": "logistics",
     "keywords": ["logistic", "400 km", "400km"]},
    {"id": "F05", "side": "pro", "label": "grant",
     "keywords": ["grant", "subsid"]},
    {"id": "F06", "side": "con", "label": "one-off cost",
     "keywords": ["140 million", "eur 140", "€140", "210 million", "eur 210", "€210",
                  "one-off", "relocation cost"]},
    {"id": "F07", "side": "open", "label": "payback/downside",
     "keywords": ["payback", "exchange rate", "currency", "downside"]},
    {"id": "F08", "side": "open", "label": "jobs/social plan",
     "keywords": ["1,800", "1800", "1 800", "jobs", "social plan", "works council",
                  "90 million", "eur 90", "€90", "severance"]},
    {"id": "F09", "side": "open", "label": "CO2/emissions",
     "keywords": ["co2", "co₂", "carbon", "emission", "renewable"]},
    {"id": "F10", "side": "open", "label": "customers/audit",
     "keywords": ["audit", "alternative supplier", "letters of intent", "letter of intent", "key customer"]},
    {"id": "F11", "side": "open", "label": "transition/delivery",
     "keywords": ["18 months", "18-month", "delivery", "parallel", "buffer"]},
]


if __name__ == "__main__":
    # Run "python dossier_levels.py" to see two levels side by side.
    print(build_dossier(0))
    print("\n" + "=" * 70 + "\n")
    print(build_dossier(5))
