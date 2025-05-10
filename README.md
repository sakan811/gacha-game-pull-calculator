# Gacha Game Pull Probability Calculator

A web-based calculator that helps you estimate the probability of obtaining 5-star characters in various Gacha games.

## Supported Games

- Honkai: Star Rail
- Genshin Impact
- Zenless Zone Zero

## Technical Notes

- Rate-increase assumption: 7% for all banners across supported games
- Data sources:
  - [HoYoLAB Article](https://www.hoyolab.com/article/497840)
  - [Star Rail Station](https://starrailstation.com/en/warp#global)
  - [Paimon.moe](https://paimon.moe/wish/tally?id=300077)
  - [ZZZ RNG](https://zzz.rng.moe/en/tracker/global#3001)

## Build Status

[![Go Backend Tests](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/go-test.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/go-test.yml)
[![Frontend Tests](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-warp-calculator/actions/workflows/frontend-test.yml)
[![Docker Build](https://github.com/sakan811/gacha-game-pull-calculator/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/gacha-game-pull-calculator/actions/workflows/docker-build.yml)

## Quick Start Guide

### Docker Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sakan811/gacha-game-pull-calculator.git
   cd gacha-game-pull-calculator
   ```

2. Download the [docker-compose.yml](./docker-compose.yml) file from the repository:

3. Open a terminal in the directory containing the file

4. Run:

   ```bash
   docker-compose up -d
   ```

5. Visit [http://localhost:5173](http://localhost:5173) in your browser

## Statistics Visualization

View detailed probability statistics and visualizations [here](https://public.tableau.com/views/GachaPullAnalysis/HoyoverseGames-GachaPullAnalysis?:language=th-TH&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link).

## Application Flow Documentation

View the application architecture and flow diagrams [here](/docs/FLOW.md).

## Running Statistics Script

### Prerequisites

- [UV Package Manager](https://docs.astral.sh/uv/getting-started/installation/)

### Setup and Execution

1. Navigate to stats directory:

   ```bash
   git clone https://github.com/sakan811/gacha-game-pull-calculator.git
   cd stats
   ```

2. Set up Python environment:

   ```bash
   uv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   uv sync
   ```

4. Run the script:

   ```bash
   python runner.py
   ```
