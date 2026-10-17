[CmdletBinding()]
param(
    [switch]$FailOnUnavailable,
    [string]$ReportPath
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$results = [System.Collections.Generic.List[object]]::new()

function Add-Result {
    param(
        [string]$Name,
        [string]$Status,
        [string]$Command,
        [string]$Detail
    )

    $results.Add([pscustomobject]@{
        Name = $Name
        Status = $Status
        Command = $Command
        Detail = $Detail
    })
}

function Invoke-ExternalCheck {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$Arguments,
        [string]$WorkingDirectory,
        [string]$CommandText
    )

    if (-not (Get-Command $FilePath -ErrorAction SilentlyContinue) -and -not (Test-Path -LiteralPath $FilePath)) {
        Add-Result $Name 'UNAVAILABLE' $CommandText "Executable not found: $FilePath"
        return
    }

    $output = ''
    $exitCode = 1
    $previousErrorActionPreference = $ErrorActionPreference
    Push-Location $WorkingDirectory
    try {
        # Native tools may emit informational warnings on stderr (for example,
        # Git's LF/CRLF advisory). Treat the process exit code as authoritative
        # while still capturing output for genuine failures.
        $ErrorActionPreference = 'Continue'
        $output = (& $FilePath @Arguments 2>&1 | Out-String).Trim()
        $exitCode = $LASTEXITCODE
    }
    catch {
        $output = $_.Exception.Message
        $exitCode = 1
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
        Pop-Location
    }

    if ($exitCode -eq 0) {
        Add-Result $Name 'PASS' $CommandText 'Completed successfully.'
    }
    else {
        Write-Output "[$Name] FAIL (exit $exitCode)"
        if ($output) {
            Write-Output $output
        }
        Add-Result $Name 'FAIL' $CommandText "Exited with code $exitCode. See terminal output for diagnostics."
    }
}

Write-Output "CF-02 quality checks: $repoRoot"

$git = Get-Command git.exe -ErrorAction SilentlyContinue
if ($git) {
    Invoke-ExternalCheck 'git-diff-check' $git.Source @('diff', '--check', '--', '.') $repoRoot 'git diff --check -- .'
}
else {
    Add-Result 'git-diff-check' 'UNAVAILABLE' 'git diff --check -- .' 'Git executable not found.'
}

$npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
$nodeModules = Join-Path $repoRoot 'node_modules'
if (-not $npm) {
    Add-Result 'frontend-lint' 'UNAVAILABLE' 'npm.cmd run lint' 'npm.cmd not found; no runtime substitution attempted.'
    Add-Result 'frontend-build' 'UNAVAILABLE' 'npm.cmd run build' 'npm.cmd not found; no runtime substitution attempted.'
}
elseif (-not (Test-Path -LiteralPath $nodeModules)) {
    Add-Result 'frontend-lint' 'UNAVAILABLE' 'npm.cmd run lint' 'node_modules is absent; npm ci was not run by this check.'
    Add-Result 'frontend-build' 'UNAVAILABLE' 'npm.cmd run build' 'node_modules is absent; npm ci was not run by this check.'
}
else {
    $eslintBinary = Join-Path $nodeModules '.bin\eslint.cmd'
    $nextBinary = Join-Path $nodeModules '.bin\next.cmd'
    if (-not (Test-Path -LiteralPath $eslintBinary)) {
        Add-Result 'frontend-lint' 'UNAVAILABLE' 'npm.cmd run lint' 'eslint is absent from node_modules; npm ci was not run by this check.'
    }
    else {
        Invoke-ExternalCheck 'frontend-lint' $npm.Source @('run', 'lint') $repoRoot 'npm.cmd run lint'
    }
    if (-not (Test-Path -LiteralPath $nextBinary)) {
        Add-Result 'frontend-build' 'UNAVAILABLE' 'npm.cmd run build' 'next is absent from node_modules; npm ci was not run by this check.'
    }
    else {
        Invoke-ExternalCheck 'frontend-build' $npm.Source @('run', 'build') $repoRoot 'npm.cmd run build'
    }
}

$backendPython = Join-Path $repoRoot 'backend\.venv\Scripts\python.exe'
$backendRoot = Join-Path $repoRoot 'backend'
if (-not (Test-Path -LiteralPath $backendPython)) {
    Add-Result 'backend-ruff' 'UNAVAILABLE' 'backend\.venv\Scripts\python.exe -m ruff check app tests alembic' 'backend/.venv is absent; global Python was not used.'
    Add-Result 'backend-pytest' 'UNAVAILABLE' 'backend\.venv\Scripts\python.exe -m pytest -p no:cacheprovider' 'backend/.venv is absent; global Python was not used.'
}
else {
    Invoke-ExternalCheck 'backend-ruff' $backendPython @('-m', 'ruff', 'check', 'app', 'tests', 'alembic') $backendRoot 'backend\.venv\Scripts\python.exe -m ruff check app tests alembic'
    Invoke-ExternalCheck 'backend-pytest' $backendPython @('-m', 'pytest', '-p', 'no:cacheprovider') $backendRoot 'backend\.venv\Scripts\python.exe -m pytest -p no:cacheprovider'
}

$passCount = @($results | Where-Object Status -eq 'PASS').Count
$failCount = @($results | Where-Object Status -eq 'FAIL').Count
$unavailableCount = @($results | Where-Object Status -eq 'UNAVAILABLE').Count

Write-Output "Summary: PASS=$passCount FAIL=$failCount UNAVAILABLE=$unavailableCount"
$results | Format-Table Name, Status, Command -AutoSize | Out-String | Write-Output

if ($ReportPath) {
    $reportFile = if ([System.IO.Path]::IsPathRooted($ReportPath)) { $ReportPath } else { Join-Path $repoRoot $ReportPath }
    $reportDirectory = Split-Path -Parent $reportFile
    New-Item -ItemType Directory -Force -Path $reportDirectory | Out-Null
    $reportLines = [System.Collections.Generic.List[string]]::new()
    $reportLines.Add('# CF-02 Offline Verification Report')
    $reportLines.Add('')
    $reportLines.Add("Generated: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK')")
    $reportLines.Add('Scope: isolated static/offline checks for this FM02 repository checkout.')
    $reportLines.Add('')
    $reportLines.Add('| Check | Status | Command | Detail |')
    $reportLines.Add('| --- | --- | --- | --- |')
    foreach ($result in $results) {
        $safeDetail = $result.Detail.Replace('|', '\|')
        $commandCell = '`' + $result.Command + '`'
        $reportLines.Add("| $($result.Name) | $($result.Status) | $commandCell | $safeDetail |")
    }
    $reportLines.Add('')
    $reportLines.Add("Summary: PASS=$passCount; FAIL=$failCount; UNAVAILABLE=$unavailableCount.")
    $reportLines.Add('')
    $reportLines.Add('No dependency installation, global runtime change, database/migration execution, application-code edit, or evidence rewrite is performed by this entry point.')
    Set-Content -LiteralPath $reportFile -Value ($reportLines -join [Environment]::NewLine) -Encoding utf8
    Write-Output "Report written: $reportFile"
}

if ($failCount -gt 0) {
    exit 1
}
if ($FailOnUnavailable -and $unavailableCount -gt 0) {
    exit 2
}
exit 0
