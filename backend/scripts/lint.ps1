$ErrorActionPreference = "Stop"

# Store current directory and change to backend directory
$SCRIPT_DIR = $PSScriptRoot
$BACKEND_DIR = (Get-Item $SCRIPT_DIR).Parent.FullName
$ORIGINAL_DIR = $PWD.Path

Set-Location $BACKEND_DIR

# Set Go environment variables
$env:GOROOT = (go env GOROOT)
$env:GOPATH = (go env GOPATH)
$env:Path = "$($env:GOROOT)/bin;$($env:GOPATH)/bin;$($env:Path)"

# Verify Go version compatibility
$goVersion = (go version) -replace '^go version go(\d+\.\d+).*','$1'
if ([version]$goVersion -lt [version]"1.24") {
    Write-Error "Go version 1.24+ required (found $goVersion). Please update Go SDK."
    exit 1
}

# Install golangci-lint if missing
if (-not (Get-Command golangci-lint -ErrorAction SilentlyContinue)) {
    Write-Host "Installing golangci-lint..."
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
}
else {
    # Force reinstall with current Go version
    Write-Host "Reinstalling golangci-lint for Go $goVersion..."
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
}

# Install gofumpt if missing
if (-not (Get-Command gofumpt -ErrorAction SilentlyContinue)) {
    Write-Host "Installing gofumpt..."
    go install mvdan.cc/gofumpt@latest
}

# Run formatting tools
Write-Host "Running gofumpt..."
$goFiles = Get-ChildItem -Recurse -Filter *.go | 
    Where-Object { $_.FullName -notmatch '\\vendor\\' -and $_.FullName -notmatch '\\.git\\' } |
    Select-Object -ExpandProperty FullName
gofumpt -l -w @goFiles

Write-Host "Running golangci-lint..."
go clean -modcache
go mod tidy
golangci-lint run --fix --go=1.24 ./...

# Return to original directory
Set-Location $ORIGINAL_DIR

Write-Host "Linting and formatting completed!" 