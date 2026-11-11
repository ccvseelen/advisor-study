# Does an AI advisor tell the board what it wants to hear?

*Working draft – rewrite in your own words before the repository goes public.*

## Question

When a language model advises on a consequential business decision, does its assessment depend on who is asking and what that person already believes? We separate two effects that are usually mixed up:

- **Role:** a CEO and a supervisory board member legitimately need different kinds of help.
- **Stance:** whether the asker is already convinced or doubtful should not change the model's verdict on the same evidence.

## Design (pilot)

- One synthetic case: relocation of a component plant, with a dossier of eleven facts (five in favour, five against, one neutral). All numbers are invented.
- Five askers: CEO convinced, CEO doubtful, board member convinced, board member doubtful, neutral analyst (2 × 2 plus control).
- Each asker gets the same dossier and question; the model summarises the key considerations and ends with a verdict (approve or reject) and a confidence from 0 to 100.
- Repeated runs, conditions interleaved; every answer is stored in `results/`.

Measured: approval rate, confidence, length, and which facts are mentioned.

## Run it

```
pip install -r requirements.txt
python run_experiment.py
python analyze.py
```

The API key is read from the environment variable `ANTHROPIC_API_KEY`.

## Status

Pilot. Keyword counting is a crude first measure; a blind second-model rating of framing is planned.

## Note

Developed with assistance from Claude.
