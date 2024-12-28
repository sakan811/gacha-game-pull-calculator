#!/bin/bash

# Set output directory
APP_DIR="hsr-warp-calculator-app"

# Create app directory and necessary subdirectories
mkdir -p "$APP_DIR"
mkdir -p backend/embedded/dist

# Determine OS and set binary name
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    BINARY_NAME="hsrbannercalc.exe"
else
    BINARY_NAME="hsrbannercalc"
fi

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Build backend with embedded files
cd backend
GOOS=windows go build -o "../$APP_DIR/windows/$BINARY_NAME"
GOOS=linux go build -o "../$APP_DIR/linux/$BINARY_NAME"
GOOS=darwin go build -o "../$APP_DIR/macos/$BINARY_NAME"
cd ..

echo "Build complete! Check the $APP_DIR directory for platform-specific builds." 