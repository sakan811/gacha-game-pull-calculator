# Gacha Game Pull Probability Calculator

This is a simple calculator to help you estimate the probability of getting a 5-star character in Gacha Games.

Supporting Games:

- Honkai: Star Rail
- Genshin Impact
- Zenless Zone Zero

## Status

[![Go Backend Tests](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/go-test.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/go-test.yml)

[![Frontend Tests](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/frontend-test.yml)

[![Binary Tests](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/binary-test.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/binary-test.yml)

## How to Use the Calculator

1. Download the executable file from the [hsr-warp-calculator-app](./hsr-warp-calculator-app/) folder depending on your operating system.
    - [Windows](./hsr-warp-calculator-app/windows/hsrbannercalc.exe)
    - [MacOS Intel](./hsr-warp-calculator-app/macos-intel/HSRBannerCalc.app/Contents/MacOS/hsrbannercalc)
    - [MacOS Apple Silicon](./hsr-warp-calculator-app/macos-silicon/HSRBannerCalc.app/Contents/MacOS/hsrbannercalc)
2. Run the executable file.
3. Navigate to the <http://localhost:5173> in your browser.

## Disclaimer

Assumes that the rate-increase is 7% for all banners in Genshin Impact, Honkai Star Rail, and Zenless Zone Zero.

## General Guidelines

- **Current Pity** is the number of pulls you have done without getting a 5-star character.
- **Planned Pulls** is the number of pulls you plan to do.

## Probability Statistics Visualizations

[Click here](/docs/VISUAL.md) to view the visualizations.

Reference:

<https://www.hoyolab.com/article/497840>

<https://starrailstation.com/en/warp#global>

<https://paimon.moe/wish/tally?id=300077>

<https://zzz.rng.moe/en/tracker/global#3001>

## How to run the statistics script

1. Install [Python](https://www.python.org/downloads/) on your machine.
2. Install [UV](https://docs.astral.sh/uv/getting-started/installation/), a Python package manager.
3. Navigate to the `stats` folder.
   - `cd stats`
4. Create a virtual environment.
   - `uv venv`
5. Activate the virtual environment.
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
6. Install the requirements.
   - `uv pip install -r requirements.txt`
7. Run the `stats_main.py` file.
   - `python stats_main.py`
