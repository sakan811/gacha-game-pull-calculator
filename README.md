# Gacha Game Pull Probability Calculator

This is a simple calculator to help you estimate the probability of getting a 5-star character in Gacha Games.

Supporting Games:

- Honkai: Star Rail
- Genshin Impact
- Zenless Zone Zero

## Status

[![Go Backend Tests](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/go-test.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/go-test.yml)

[![Frontend Tests](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/frontend-test.yml)

[![Docker Build](https://github.com/sakan811/gacha-game-pull-calculator/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/gacha-game-pull-calculator/actions/workflows/docker-build.yml)

## How to Use the Calculator

1. Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your system.
2. Download the [docker-compose.yml](./docker-compose.yml) file from this repository.
3. Place the `docker-compose.yml` in any directory of your choice.
4. Run the following command to start the application:

   ```bash
   docker-compose up -d
   ```

5. Navigate to <http://localhost:5173> in your browser to access the calculator.
6. When you're done, you can stop the application with:

   ```bash
   docker-compose down
   ```

## Disclaimer

Assumes that the rate-increase is 7% for all banners in Genshin Impact, Honkai Star Rail, and Zenless Zone Zero.

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
