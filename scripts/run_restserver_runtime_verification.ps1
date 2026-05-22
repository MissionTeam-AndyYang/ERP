param(
    [string]$Python = "backend\.venv\Scripts\python.exe",
    [string]$EnvFile = "restserver\package\config\.env.example",
    [switch]$InstallRequirements,
    [switch]$RequireDb
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Python)) {
    throw "Python executable not found: $Python"
}

if ($InstallRequirements) {
    & $Python -m pip install -r restserver\package\requirements.txt
}

$env:PYTHONPATH = "restserver"

$argsList = @("scripts\verify_restserver_runtime.py", "--env-file", $EnvFile)
if ($RequireDb) {
    $argsList += "--require-db"
}

& $Python @argsList
