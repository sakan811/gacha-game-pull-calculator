# Install golangci-lint if not already installed
if (!(Get-Command golangci-lint -ErrorAction SilentlyContinue)) {
    Write-Host "Installing golangci-lint..."
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
}

# Install gofumpt if not already installed
if (!(Get-Command gofumpt -ErrorAction SilentlyContinue)) {
    Write-Host "Installing gofumpt..."
    go install mvdan.cc/gofumpt@latest
}

# Run gofumpt to format the code
Write-Host "Running gofumpt..."
gofumpt -l -w .

# Run golangci-lint
Write-Host "Running golangci-lint..."
golangci-lint run --fix

Write-Host "Linting and formatting completed!" 