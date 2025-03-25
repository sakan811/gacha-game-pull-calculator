# Gacha Game Statistics Analysis

A Python module for analyzing and processing gacha game pull statistics. This module provides statistical analysis and visualization tools for gacha game probability data.

## Features

- Statistical analysis of gacha pull data:
  - Pull distribution analysis
  - Pity system impact assessment
  - Probability calculations
- Visualization generation:
  - Distribution charts for different banner types
  - Cumulative probability graphs
  - Support for multiple games:
    - Honkai: Star Rail
    - Genshin Impact
    - Zenless Zone Zero

## Prerequisites

- Python 3.12 or later
- UV package manager
- Virtual environment (recommended)

## Setup

1. Install UV package manager: <https://docs.astral.sh/uv/getting-started/installation/>

2. Create and activate virtual environment:

```bash
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

## Module Structure

```text
stats/
├── graph/              # Generated visualization outputs
├── stats_utils/        # Core utility functions
│   ├── banner_config.py          # Banner configuration
│   ├── hsr_warp_stats.py        # HSR-specific calculations
│   ├── probability_calculator.py # Probability computations
│   └── visualization.py         # Chart generation
├── stats_main.py      # Main entry point
└── requirements.txt   # Project dependencies
```

## Usage

### Running Analysis

```bash
cd stats
python stats_main.py
```

The generated charts will be saved in the `graph/` directory, organized by game and banner type.
