# Run the full smoke test in PowerShell
# Usage: .\run_smoke.ps1

$python = "python"
Write-Host "Running full smoke test..."
& $python full_smoke_test.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Smoke test completed successfully. Reports are in smoke_outputs\"
} else {
    Write-Host "Smoke test failed with exit code $LASTEXITCODE"
}
