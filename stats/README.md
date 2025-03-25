# Gacha Game Statistics Analysis

A Python module for analyzing and processing gacha game pull statistics. This module provides statistical analysis and visualization tools for gacha game probability data, supporting multiple gacha games and banner types.

## Features

- Comprehensive statistical analysis:
  - Pull distribution analysis with pity system mechanics
  - Probability calculations for all banner types
  - Rate-up and guarantee system impact assessment
  - Expected value calculations
- Advanced visualization generation:
  - Distribution charts with detailed probability breakdowns
  - Cumulative probability graphs with pity thresholds
- Multi-game support:
  - Honkai: Star Rail
  - Genshin Impact
  - Zenless Zone Zero
- Extensible architecture for adding new games

## Prerequisites

- Python 3.12 or later
- UV package manager
- Virtual environment (recommended)

## Setup

1. Install UV package manager: <https://docs.astral.sh/uv/getting-started/installation/>

2. Create and activate virtual environment:

    ```bash
    cd stats
    uv venv
    # On Windows:
    venv\Scripts\activate
    # On Unix:
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    uv pip install -r requirements.txt
    ```

## Project Structure

```text
stats/
├── graph/                    # Generated visualization outputs
├── stats_utils/             # Core utility functions
│   ├── banner_config.py     # Banner type configurations
│   ├── hsr_warp_stats.py    # HSR-specific calculations
│   ├── probability_calculator.py  # Core probability engine
│   └── visualization.py     # Chart generation system
├── stats_main.py           # Main entry point
└── requirements.txt        # Project dependencies
```

## Usage

### Running Analysis

```bash
cd stats
python stats_main.py
```

### Output

Generated charts are saved in the `graph/` directory, organized by:

- Game type
- Banner category
- Analysis type (distribution/cumulative)

Each chart type includes:

- Distribution Charts:

  - Pull probability per roll
  - Most likely pull number with peak probability
  - Soft pity threshold markers with probability
  - Detailed probability annotations

- Cumulative Charts:

  - Cumulative probability curve
  - 50% probability threshold marker
  - Hard pity guarantee line
  - Reference markers for key probability thresholds
