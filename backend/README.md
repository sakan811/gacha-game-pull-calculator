# Honkai: Star Rail Warp Calculator Backend

This is the backend service for the Honkai: Star Rail Warp Calculator. It provides probability calculations for different types of banners in Honkai: Star Rail, Genshin Impact, and Zenless Zone Zero.

## Features

- Probability calculations for:
  - Standard banners
  - Limited character banners
  - Light cone/weapon banners
- Support for multiple games:
  - Honkai: Star Rail
  - Genshin Impact
  - Zenless Zone Zero
- Pity system calculations
- Rate-up probability calculations

## Prerequisites

- Go 1.21 or later
- Docker (optional, for containerized deployment)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/honkai-star-rail-warp-calculator.git
cd honkai-star-rail-warp-calculator
```

2. Run with Docker Compose (recommended):

```bash
docker-compose up
```

This will start both the frontend and backend services:

- Frontend will be available at <http://localhost:5173>
- Backend API will be available at <http://localhost:8080>

3. For local development without Docker:

```bash
cd backend
go mod download
go run cmd/main.go
```

## API Endpoints

### Honkai: Star Rail

- `POST /api/star-rail/standard`
  - Calculate standard banner probabilities
- `POST /api/star-rail/limited`
  - Calculate limited banner probabilities
- `POST /api/star-rail/light-cone`
  - Calculate light cone banner probabilities

### Genshin Impact

- `POST /api/genshin/standard`
  - Calculate standard banner probabilities
- `POST /api/genshin/limited`
  - Calculate limited banner probabilities
- `POST /api/genshin/weapon`
  - Calculate weapon banner probabilities

### Zenless Zone Zero

- `POST /api/zenless/standard`
  - Calculate standard banner probabilities
- `POST /api/zenless/limited`
  - Calculate limited banner probabilities
- `POST /api/zenless/w-engine`
  - Calculate W-Engine banner probabilities
- `POST /api/zenless/bangboo`
  - Calculate Bangboo banner probabilities

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
  "base_probability": 0.5,
  "rate_up_probability": 0.25
}
```

## Development

### Project Structure

```
backend/
├── cmd/            # Application entry point
├── config/         # Configuration management
├── internal/       # Internal packages
│   ├── api/       # API handlers and models
│   ├── domain/    # Core business logic
│   ├── service/   # Business service layer
│   ├── middleware/# HTTP middleware
│   ├── constants/ # Application constants
│   └── errors/    # Error handling
└── scripts/       # Utility scripts
```

### Running Tests

```bash
go test ./...
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
