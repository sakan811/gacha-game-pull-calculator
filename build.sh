#!/bin/bash

# Set output directory
APP_DIR="hsr-warp-calculator-app"

# Create app directory and necessary subdirectories
mkdir -p "$APP_DIR"/{windows,macos-intel,macos-silicon}
mkdir -p backend/embedded/dist

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Build backend with embedded files
cd backend

# Build for Windows (amd64)
GOOS=windows GOARCH=amd64 go build -o "../$APP_DIR/windows/hsrbannercalc.exe"

# Build for macOS (Intel)
GOOS=darwin GOARCH=amd64 go build -o "../$APP_DIR/macos-intel/hsrbannercalc.app"

# Build for macOS (Apple Silicon)
GOOS=darwin GOARCH=arm64 go build -o "../$APP_DIR/macos-silicon/hsrbannercalc.app"

# Create a universal binary for macOS (combines Intel and Apple Silicon)
if command -v lipo &> /dev/null && [[ "$OSTYPE" == "darwin"* ]]; then
    mkdir -p "../$APP_DIR/macos-universal"
    lipo -create \
        "../$APP_DIR/macos-intel/hsrbannercalc.app" \
        "../$APP_DIR/macos-silicon/hsrbannercalc.app" \
        -output "../$APP_DIR/macos-universal/hsrbannercalc.app"
    echo "Created universal macOS binary"
fi

cd ..

echo "Build complete! Check the $APP_DIR directory for platform-specific builds:"
echo "- Windows (64-bit): $APP_DIR/windows/"
echo "- macOS (Intel): $APP_DIR/macos-intel/"
echo "- macOS (Apple Silicon): $APP_DIR/macos-silicon/"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "- macOS (Universal): $APP_DIR/macos-universal/"
fi 