#!/bin/bash

set -e

# Store current directory and change to backend directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
ORIGINAL_DIR="$(pwd)"
cd "$BACKEND_DIR"

# Use native Go environment variables for Windows compatibility
GOROOT=$(go env GOROOT)
GOPATH=$(go env GOPATH)
export GOROOT GOPATH
export PATH="$GOROOT/bin:$GOPATH/bin:$PATH"

# Install golangci-lint if not already installed
if ! command -v golangci-lint &> /dev/null; then
    echo "Installing golangci-lint..."
    GO111MODULE=on go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
fi

# Install gofumpt with explicit path check
if ! command -v gofumpt >/dev/null; then
    echo "Installing gofumpt..."
    GO111MODULE=on go install mvdan.cc/gofumpt@latest
fi

# Cross-platform file processing
echo "Running gofumpt..."
gofumpt -l -w .

# Run golangci-lint with Windows-compatible path
echo "Running golangci-lint..."
golangci-lint run --fix ./...

# Return to original directory
cd "$ORIGINAL_DIR"

echo "Linting and formatting completed!" 