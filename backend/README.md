# Gacha Game Pull Calculator Backend

A backend service for calculating gacha pull probabilities in various gacha games. This API provides probability calculations for different banner types in games like Honkai: Star Rail, Genshin Impact, and Zenless Zone Zero, with support for more games in the future.

## Features

- Probability calculations for multiple gacha systems:
  - 5-star character/item drop rates
  - Pity system mechanics
  - Rate-up guarantee mechanics
- Support for multiple games (currently):
  - Honkai: Star Rail
  - Genshin Impact
  - Zenless Zone Zero
- Easily extendable for additional games
- Visualization data endpoints for probability charts

## Prerequisites

- Go 1.24 or later
- Docker (optional, for containerized deployment)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/sakan811/gacha-game-pull-calculator.git
cd gacha-game-pull-calculator
```

2. Run with Docker (recommended):

```bash
docker pull sakanbeer88/gacha-pull-calculator-backend:latest
docker run -p 8080:8080 sakanbeer88/gacha-pull-calculator-backend:latest
```

3. For local development:

```bash
cd backend
go mod download
go run cmd/main.go
```

The API will be available at `http://0.0.0.0:8080/api`

## API Endpoints

### Honkai: Star Rail

- `POST /api/star_rail/standard`
  - Calculate standard banner probabilities
- `POST /api/star_rail/limited`
  - Calculate limited character banner probabilities
- `POST /api/star_rail/light_cone`
  - Calculate light cone banner probabilities

### Genshin Impact

- `POST /api/genshin/standard`
  - Calculate standard banner probabilities
- `POST /api/genshin/limited`
  - Calculate limited character banner probabilities
- `POST /api/genshin/weapon`
  - Calculate weapon banner probabilities

### Zenless Zone Zero

- `POST /api/zenless/standard`
  - Calculate standard banner probabilities
- `POST /api/zenless/limited`
  - Calculate limited banner probabilities
- `POST /api/zenless/w_engine`
  - Calculate W-Engine banner probabilities
- `POST /api/zenless/bangboo`
  - Calculate Bangboo banner probabilities

### Visualization

- `POST /api/visualization`
  - Get data for probability visualization charts

### Request Format

```json
{
  "current_pity": 0,
  "planned_pulls": 90,
  "guaranteed": false
}
```

### Response Format

```json
{
  "total_5_star_probability": 0.8,
  "character_probability": 0.6,
  "rate_up_probability": 0.5,
  "light_cone_probability": 0.2,
  "standard_char_probability": 0.1
}
```

## Project Structure

```
backend/
├── cmd/            # Application entry point
├── config/         # Configuration management
├── internal/       # Internal packages
│   ├── api/        # API handlers and models
│   │   ├── handlers/  # HTTP request handlers
│   │   ├── models/    # Request/response structures
│   │   └── services/  # API services
│   ├── domain/     # Core business logic
│   ├── service/    # Business service layer
│   ├── middleware/ # HTTP middleware
│   ├── constants/  # Application constants
│   ├── errors/     # Error handling
│   └── web/        # Web-related utilities
└── scripts/       # Utility scripts
```

## Development

### Running Tests

```bash
go test ./...
```