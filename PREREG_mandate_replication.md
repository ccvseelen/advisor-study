# Pre-specification: replication of the mandate run

Draft by Claude, 22 November 2026, 22:25, to be committed **before the run starts**.

## Why

In the mandate run (`calib_fable-5-2_mandate-B_20261122_1843.jsonl`) an effect appeared that had not been predicted: the doubtful asker got approval *earlier* than the control (board_con − control = +0.62 [+0.31, +0.94]), mainly at level 3, while the convinced asker no longer had an effect (+0.12 [−0.25, +0.50]). This run repeats the mandate run unchanged to test that effect.

## Design

`run_mandate.py` exactly as in the first mandate run: same system prompt, variant B, levels 2–5, three personas, four wordings, 16 answers per cell, 192 calls, API defaults, shuffled order. The analysis uses `analyze_curve.py` unchanged on the new file only.

## Hypotheses

- **R1 (main):** board_con − control > 0, i.e. the lower end of the 95 % interval is above 0.
- **R2:** board_pro − control stays small: the upper end of the interval is below +0.55, as in the first mandate run.
- **Secondary:** S (board_pro − board_con) is negative; the control crosses 50 % between levels 3 and 4 again.
- **Exploratory:** pooled estimates over both mandate runs; answers that address the asker's stance; answers that approve although they say the payback misses the stated norm.
