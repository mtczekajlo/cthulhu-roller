# Cthulhu Roller

**Cthulhu Roller** is a Call of Cthulhu RPG 7E dice roller bot for Discord.

## Installation

Needs environment variable `DISCORD_TOKEN` to be set.

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

### Systemd installation

```bash
sudo apt install -y libsystemd-dev
```

```bash
./install-service
```

## Usage

Created for simplicity. Rolls a d100 with optional bonus or penalty dice, and optional threshold for determining levels of success or failure.

```text
/croll [[number=1][die type]]...[[score][threshold]]

Test roll:
    <number>t  Threshold to determine success or failure
    <number>b  Bonus dice
    <number>p  Penalty dice
Die roll:
    <number>d/k<number>+/-<number>  Custom dice with optional modifier

Examples:
    /croll
    Result: 36
    Rolls: [ 30 ] [ 6 ]

    /croll 60t
    Hard Success! (1/2)
    Result: 24
    Threshold: 60/30/12
    Rolls: [ 20 ] [ 4 ]

    /croll b
    Result: 35
    Bonus dice: 1
    Rolls: [ 70 ] [ 30 ] [ 5 ]

    /croll 2p70t
    Failure
    Result: 74
    Threshold: 70/35/14
    Penalty dice: 2
    Rolls: [ 70 ] [ 50 ] [ 00 ] [ 4 ]

    /croll d10
    Result: 8
    Rolling 1d10
    Rolls: [ 8 ]

    /croll 2k6+2
    Result: 9
    Rolling 2d6+2
    Rolls: [ 5 ] [ 2 ]
```
