#!/bin/bash

set -e

echo "Running Go tests..."

cd "$(dirname "$0")/.."

go test -v -race -cover ./...

echo "Tests completed successfully" 