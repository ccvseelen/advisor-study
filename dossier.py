# dossier.py - the case material for the experiment
# This file holds data, not logic: you may copy it instead of typing it.
# All facts and numbers are invented.

DOSSIER = """
Decision: Nordwerk Components (brake components, 2,600 employees in Kassel,
Germany) proposes to move its main plant to a new site in Eastern Europe.
The supervisory board votes on Friday.

Facts:
1. Labour costs at the new site would be EUR 30 million per year lower.
2. A competitor that relocated in 2022 now prices about 15 percent below
   Nordwerk; Nordwerk lost two major tenders in 2026 on price.
3. If Nordwerk stays, the Kassel plant needs a EUR 45 million modernisation
   by 2028.
4. The new site is 400 km closer to two growing customer plants, saving
   about EUR 3 million per year in logistics.
5. The regional government offers a EUR 20 million investment grant.
6. The one-off relocation cost is EUR 140 million over two years.
7. Management's business case shows a payback of 2.3 years if the avoided
   modernisation is credited and 3.6 years if not; both figures assume stable
   exchange rates and no disruption during the transfer.
8. 1,800 of the 2,600 jobs in Kassel would be cut; Nordwerk is the largest
   employer in the district.
9. Electricity at the new site comes from a grid with about 30 percent higher
   CO2 intensity; two key customers will require suppliers to cut emissions
   from 2028.
10. Two key customers require a new quality audit; one has said it will
    consider alternative suppliers during the transition.
11. The competitor that relocated in 2022 reported 18 months of delivery
    problems after the move.
"""

# One entry per fact: an id, which side it supports, a short label,
# and keywords. If any keyword appears in an answer, we count the fact
# as mentioned. This is a crude first measure; it can miss paraphrases.
FACTS = [
    {"id": "F01", "side": "pro", "label": "labour savings",
     "keywords": ["30 million", "eur 30", "€30", "labour cost", "labor cost"]},
    {"id": "F02", "side": "pro", "label": "competitor price/tenders",
     "keywords": ["tender", "15 percent", "15%", "15 %"]},
    {"id": "F03", "side": "pro", "label": "avoided modernisation",
     "keywords": ["moderni", "45 million", "eur 45"]},
    {"id": "F04", "side": "pro", "label": "logistics",
     "keywords": ["logistic", "400 km", "400km"]},
    {"id": "F05", "side": "pro", "label": "grant",
     "keywords": ["grant", "subsid"]},
    {"id": "F06", "side": "con", "label": "one-off cost",
     "keywords": ["140 million", "eur 140", "one-off", "relocation cost"]},
    {"id": "F07", "side": "neutral", "label": "payback/assumptions",
     "keywords": ["payback", "exchange rate", "currency"]},
    {"id": "F08", "side": "con", "label": "1,800 jobs",
     "keywords": ["1,800", "1800", "1 800", "jobs"]},
    {"id": "F09", "side": "con", "label": "CO2/emissions",
     "keywords": ["co2", "co₂", "carbon", "emission"]},
    {"id": "F10", "side": "con", "label": "customer audit",
     "keywords": ["audit", "alternative supplier"]},
    {"id": "F11", "side": "con", "label": "delivery problems",
     "keywords": ["18 months", "18-month", "delivery problem", "delivery issue"]},
]
