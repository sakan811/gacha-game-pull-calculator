#!/bin/bash

set -e

# Store current directory and change to backend directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
ORIGINAL_DIR="$(pwd)"
cd "$BACKEND_DIR"

# Set up GOPATH and add the binary directory to PATH
GOPATH=${GOPATH:-$(go env GOPATH)}
export PATH=$GOPATH/bin:$PATH

# Install golangci-lint if not already installed
if ! command -v golangci-lint &> /dev/null; then
    echo "Installing golangci-lint..."
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
fi

# Install gofumpt if not already installed
if ! command -v gofumpt &> /dev/null; then
    echo "Installing gofumpt..."
    go install mvdan.cc/gofumpt@latest
fi

# Run gofumpt to format the code
echo "Running gofumpt..."
gofumpt -l -w .

# Run golangci-lint
echo "Running golangci-lint..."
golangci-lint run --fix

# Return to original directory
cd "$ORIGINAL_DIR"

echo "Linting and formatting completed!" 