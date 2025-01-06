#!/bin/bash

# Set output directory
APP_DIR="hsr-warp-calculator-app"

# Create app directory and necessary subdirectories step by step
mkdir -p "$APP_DIR/windows"

# Create macOS Intel directories
mkdir -p "$APP_DIR/macos-intel"
mkdir -p "$APP_DIR/macos-intel/HSRBannerCalc.app"
mkdir -p "$APP_DIR/macos-intel/HSRBannerCalc.app/Contents"
mkdir -p "$APP_DIR/macos-intel/HSRBannerCalc.app/Contents/MacOS"
mkdir -p "$APP_DIR/macos-intel/HSRBannerCalc.app/Contents/Resources"

# Create macOS Silicon directories
mkdir -p "$APP_DIR/macos-silicon"
mkdir -p "$APP_DIR/macos-silicon/HSRBannerCalc.app"
mkdir -p "$APP_DIR/macos-silicon/HSRBannerCalc.app/Contents"
mkdir -p "$APP_DIR/macos-silicon/HSRBannerCalc.app/Contents/MacOS"
mkdir -p "$APP_DIR/macos-silicon/HSRBannerCalc.app/Contents/Resources"

# Create backend directory
mkdir -p backend/internal/web/embedded/dist

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Build backend with embedded files
cd backend

# Build for Windows (amd64)
GOOS=windows GOARCH=amd64 go build -o "../$APP_DIR/windows/hsrbannercalc.exe" ./cmd/main.go

# Build for macOS (Intel)
GOOS=darwin GOARCH=amd64 go build -o "../$APP_DIR/macos-intel/HSRBannerCalc.app/Contents/MacOS/hsrbannercalc" ./cmd/main.go

# Create Info.plist for Intel
mkdir -p "../$APP_DIR/macos-intel/HSRBannerCalc.app/Contents"
cat > "../$APP_DIR/macos-intel/HSRBannerCalc.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>hsrbannercalc</string>
    <key>CFBundleIdentifier</key>
    <string>com.hsrbannercalc</string>
    <key>CFBundleName</key>
    <string>HSR Banner Calculator</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>
EOF

# Build for macOS (Apple Silicon)
GOOS=darwin GOARCH=arm64 go build -o "../$APP_DIR/macos-silicon/HSRBannerCalc.app/Contents/MacOS/hsrbannercalc" ./cmd/main.go

# Create Info.plist for Apple Silicon
mkdir -p "../$APP_DIR/macos-silicon/HSRBannerCalc.app/Contents"
cat > "../$APP_DIR/macos-silicon/HSRBannerCalc.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>hsrbannercalc</string>
    <key>CFBundleIdentifier</key>
    <string>com.hsrbannercalc</string>
    <key>CFBundleName</key>
    <string>HSR Banner Calculator</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
</dict>
</plist>
EOF

cd ..

echo "Build complete! Check the $APP_DIR directory for platform-specific builds:"
echo "- Windows (64-bit): $APP_DIR/windows/"
echo "- macOS (Intel): $APP_DIR/macos-intel/"
echo "- macOS (Apple Silicon): $APP_DIR/macos-silicon/"