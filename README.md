# Cthulhu Roller

**Cthulhu Roller** is a Call of Cthulhu RPG 7E dice roller bot for Discord.

## Installation

<https://github.com/pyenv/pyenv>

<https://github.com/python-poetry/poetry>

```bash
curl https://pyenv.run | bash
pyenv install 3.11
pyenv local 3.11
pip install poetry
poetry env use 3.11
poetry install
source .env
poetry run python cthulhu_roller.py
```

## Usage

Created for simplicity. Rolls a d100 with optional bonus or penalty dice, and optional threshold for determining levels of success or failure.

```text
/croll [[number=1][die type]]...[[score][threshold]]

Die Types:
    b: Bonus dice (can't be chained with Penalty)
    p: Penalty dice (can't be chained with Bonus)
    t: Threshold to determine success/fail. Score is required if a threshold is set.

Examples:
    /croll
    36

    /croll 60t
    Hard Success: 24

    /croll b
    70/30 + 5 = 35

    /croll 2p70t
    Failure: 0/50/70 + 4 = 74
```

## Notes

Needs environmental variable DISCORD_TOKEN to be set if you want to run this yourself. See `.env.example` for a Linux/OSX method.
