# Gacha Game Pull Calculator Frontend

A Vue-based web interface for visualizing gacha pull probabilities. This application provides interactive charts and probability calculations for different banner types in games like Honkai: Star Rail, Genshin Impact, and Zenless Zone Zero, with support for more games in the future.

## Features

- Interactive probability calculator for:
  - 5-star character/item drop rates
  - Pity system mechanics
  - Rate-up guarantee tracking
- Real-time chart visualizations:
  - Successful Pull Distribution chart
  - Cumulative Probability curve
- Support for multiple games (currently):
  - Honkai: Star Rail
  - Genshin Impact
  - Zenless Zone Zero
- Responsive design for all device types
- Modern UI with Tailwind CSS

## Prerequisites

- Node.js 18.x or later
- npm 9.x or later
- Docker (optional, for containerized deployment)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/sakan811/gacha-game-pull-calculator.git
cd gacha-game-pull-calculator
```

2. Run with Docker (recommended):

```bash
docker pull sakanbeer88/gacha-pull-calculator-frontend:latest
docker run -p 5173:5173 sakanbeer88/gacha-pull-calculator-frontend:latest
```

3. For local development:

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173`

## UI Components

### Calculator Form

- Game selection dropdown
- Banner type selection
- Current pity input
- Planned pulls input
- Guaranteed status toggle

### Result Display

- Overall 5-star probability
- Rate-up character probability
- Expected pulls calculation

### Chart Visualizations

- Successful Pull Distribution chart
  - Shows likelihood of getting 5-star at each pull
- Cumulative Probability chart
  - Shows aggregate probability over multiple pulls
  - Includes red dotted line at planned pulls

## Project Structure

```
frontend/
├── dist/            # Production build output
├── node_modules/    # Dependencies
├── public/          # Static assets
├── scripts/         # Build and utility scripts
├── src/
│   ├── components/  # Vue components
│   ├── tests/       # Test suites
│   ├── app.css      # Global styles
│   ├── App.vue      # Root component
│   ├── main.ts      # Application entry point
│   └── types.ts     # TypeScript type definitions
├── .dockerignore    # Docker ignore configuration
├── .gitignore       # Git ignore configuration
├── Dockerfile       # Docker build configuration
├── index.html       # Entry HTML template
├── nginx.conf       # Nginx configuration for production
├── package.json     # Project dependencies and scripts
├── tailwind.config.js # Tailwind CSS configuration
├── tsconfig.json    # TypeScript configuration
├── tsconfig.node.json # TypeScript node configuration
├── vite.config.ts   # Vite bundler configuration
└── vitest.config.ts # Vitest testing configuration
```

## Development

### Key Dependencies

- Vue 3 (Composition API)
- Chart.js 4 (Visualizations)
- Tailwind CSS (Styling)
- Vitest (Testing)

### Running Tests

```bash
npm test
```

For interactive testing:

```bash
npm run test:ui
```

### Building for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Visualization Configuration

Charts are configured with:

- X-axis starting at 0 pulls
- Red dotted line indicating total pulls input
- Responsive design for all screen sizes
- Annotations for key probability thresholds
