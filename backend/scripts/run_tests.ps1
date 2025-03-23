#! /usr/bin/env pwsh

$ErrorActionPreference = "Stop"

Write-Host "Running Go tests..."
Set-Location (Join-Path $PSScriptRoot "..") -ErrorAction Stop

try {
    go test -v -cover ./...
}
catch {
    Write-Error "Tests failed with error: $_"
    exit 2
}

if ($LASTEXITCODE -ne 0) {
    Write-Error "Tests failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "Tests completed successfully"
exit 0 