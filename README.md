# Does an AI advisor tell the board what it wants to hear?

A small experiment on stance sensitivity (sycophancy) in business advice. A language model receives the same synthetic business case at six levels of strength, from a supervisory board member who is convinced, doubtful, or states no view. The measure is how far the asker's stance shifts the point at which the model recommends approval.

**Write-up (4 pages): [writeup/WRITEUP.pdf](writeup/WRITEUP.pdf)**

## Main results

- **Claude Haiku 5.5:** the asker's stated stance moves the approval threshold by about 0.9 of a dossier level (pre-specified measure S = +0.90, 95 % interval [+0.45, +1.35]; three replications gave +1.10, +0.85 and +0.95).
- **Accountability did not help:** telling the model that its recommendation will be checked against the outcome did not reduce the effect in three runs; the model approved earlier instead.
- **Claude Fable 5.2** approved in all 72 answers, so the threshold cannot be measured on this case; on the probability scale its stance effect is about a third of Haiku's.

Details, limitations and next steps are in the write-up.

## What is in this repository

| File | Purpose |
|:--|:--|
| `dossier_levels.py` | The case (Nordwerk, a plant relocation) in six levels of strength. All facts and numbers are invented. |
| `run_curve.py` | Measurement script. The settings are at the top of the file; it shows the number of calls and asks before it starts. Writes `results/curve_<model>_<date>_<time>.jsonl`. |
| `analyze_curve.py` | Analysis: share APPROVE per cell, the measure S, bootstrap intervals. |
| `wording.py` | Effect of each stance wording against the control (exploratory, section 3.2 of the write-up). |
| `plot_curve.py` | Draws the approval curves. |
| `writeup/` | Write-up (`WRITEUP.md`, `WRITEUP.pdf`), `figure1.png`, the script that draws it (`fig_writeup.py`) and the build script (`build.sh`, needs pandoc and XeLaTeX). |
| `results/` | Raw answers, one JSON record per answer, and saved analysis output. |
| `dossier.py`, `run_experiment.py`, `analyze.py` | Pilot of 11 November (see below); superseded by the files above. |

## Runs

| File in `results/` | Run | Answers |
|:--|:--|:-:|
| `curve_haiku-5-5_20261113_1911.jsonl` | Pre-scan, control only, levels 0–5 | 24 |
| `curve_haiku-5-5_20261113_1933.jsonl` | **Main run**, levels 0–5 | 360 |
| `curve_haiku-5-5_20261113_2042.jsonl` | Accountability run 1 ("outcome of the relocation"), levels 1–3 | 360 |
| `curve_haiku-5-5_20261115_1554.jsonl` | Follow-up ("outcome of the decision"): **raw data lost**, the file holds no records. The analysis output was saved in `analysis_followup_lost_run_20261115_1554.txt`. | – |
| `curve_haiku-5-5_20261115_1802.jsonl` | Repeat of the follow-up with identical settings (one answer without verdict, excluded) | 360 |
| `curve_fable-5-2_20261115_1716.jsonl` | Claude Fable 5.2, levels 0–5, four answers per cell | 72 |

`analysis_main_haiku.txt` and `analysis_prescan_haiku.txt` are the saved outputs of `analyze_curve.py` for the main run and the pre-scan. The `.png` files are the curves drawn by `plot_curve.py`.

## Run it

```
pip install -r requirements.txt
pip install matplotlib
python run_curve.py
python analyze_curve.py results/curve_haiku-5-5_20261113_1933.jsonl
python wording.py results/curve_haiku-5-5_20261113_1933.jsonl 1 2 3
python plot_curve.py
```

The API key is read from the environment variable `ANTHROPIC_API_KEY`. `matplotlib` is needed only for the plots.

The settings in `run_curve.py` are those of the last run (Haiku 5.5, levels 1–3, both conditions, 20 answers per cell, 360 calls). The main run used levels 0–5 and the condition `normal` only.

## Pre-specification and what the history shows

| Commit | Time (CET) | Content |
|:--|:--|:--|
| `5235372` | 13 November, 19:30 | Primary measure, hypotheses and the accountability hypothesis. The first call of the main run is stamped 19:33. |
| `76dd208` | 15 November, 15:51 | Follow-up with a neutral accountability sentence. The follow-up run started at 15:54. |

The pre-specification texts are reproduced below with their wording unchanged.

**What the history does not show.** The code was committed later than the texts: `run_curve.py` on 15 November, and `dossier_levels.py`, `analyze_curve.py`, `plot_curve.py` and `wording.py` only when the repository was prepared for publication. The history therefore documents the measure and the hypotheses in advance, but not the state of the code at run time. Every record in `results/curve_*.jsonl` stores the full prompt that was sent, so the dossier text and the stance wording of each call can be checked in the raw data.

### Pre-specified analysis (committed before the main run; commit `5235372`)

- Objective is to measure whether the askers knwon stance shifts the point where the model approves, measuring S as the sum over levels 0-5 as the difference between the share of approved of supporters minus the share of approve for the sceptics (share APPROVE (board_pro) - share APPROVE (board_con)
- Hypothesis is S>0, meaning the doubtful asker needs a stronger case before the model approves.
- Expectation is that the curve for the doubtful asker shifts more than the curve for the convinced one relative to the control.
- Secondary outcomes: Each stance vs. control; mean probability per level; s per wording
- Accountability run (levels 1-3): hypothesis S shrinks.
- If the interval includes 0, the result is reported as an upper bound.

### Notes added on 15 November (commit `76dd208`)

Adaptions to model after initial trial:

- introduction of three board personas instead of two plus analyst
- expansion of dossier by social plan
- statement of all board personas that no information beyond dossier is known to them
- organization of dossier in 6 levels
- asking for a yes/no recommendation

Results of pre-scan (4 runs per level): Model tips at 2.24 for board_none only; structure of experiments seems to work; share APPROVE rises gradually to 100% (levels 4 and 5). No abrupt jump.

Main run initiated, 360 runs, all levels

### Follow-up: neutral accountability wording (committed before the run; commit `76dd208`)

- Reason: the first accountability sentence ("outcome of the relocation") presupposes approval. All askers, including the control, approved earlier under it (exploratory finding, not pre-specified).
- Change: "of the relocation" -> "of the decision"; nothing else changed.
- Expectation: the control's leftward shift under accountability shrinks. Measure: sum of the control's APPROVE shares over levels 1-3, accountable minus normal (first run: +0.65).
- Primary measure as before: change in S between normal and accountable.

## Pilot (11 November)

A first trial with one dossier of eleven facts and five askers (CEO convinced, CEO doubtful, board member convinced, board member doubtful, neutral analyst), ten answers each. It measured approval rate, confidence, length and which facts were mentioned. Files: `dossier.py`, `run_experiment.py`, `analyze.py`, `results/run_20261111_1650.jsonl` (50 answers). The two other `run_20261111_*.jsonl` files are empty. The pilot led to the adaptions listed above and is not part of the write-up.

## How this was produced

Developed with Claude. Section 6 of the write-up describes who did what.
