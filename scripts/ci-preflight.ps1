# `agent-asset-marketplace` preflight script.
# This is a repo-owned mirror of the CI pipeline in
# `.github/workflows/marketplace-validation.yml`. It is read-only and prints
# the repair command for any failing check.
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path "$ScriptDir/.."

$pythonCmd = $null
$pythonArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = 'py'
    $pythonArgs += '-3'
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = 'python'
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = 'python3'
} else {
    throw 'No Python interpreter found'
}

$pyPrefix = "$pythonCmd"
if ($pythonArgs.Count -gt 0) {
    $pyPrefix += " $($pythonArgs -join ' ')"
}

function Invoke-Python($extraArgs) {
    & $pythonCmd @($pythonArgs + $extraArgs)
}

function Test-GitRef($ref) {
    git rev-parse --verify $ref 2>&1 | Out-Null
    return $LASTEXITCODE -eq 0
}

$ChangedFrom = $null
for ($i = 0; $i -lt $args.Count; $i++) {
    if ($args[$i] -in @('--check', '-Check')) { continue }
    if ($args[$i] -eq '--changed-from') {
        $i++
        $ChangedFrom = $args[$i]
    } else {
        throw "unknown arg: $($args[$i])"
    }
}

$base = 'HEAD'
if ($ChangedFrom) {
    if (Test-GitRef($ChangedFrom)) {
        $base = $ChangedFrom
    } else {
        Write-Warning "$ChangedFrom not found, falling back to HEAD"
        $base = 'HEAD'
    }
} elseif (Test-GitRef('origin/main')) {
    $base = 'origin/main...HEAD'
} else {
    Write-Warning 'origin/main not found, linting all tracked Python files'
    $base = 'HEAD'
}

Write-Host '==> Lint changed Python files'
$files = if ($base -eq 'HEAD') {
    (git ls-files '*.py').Split("`n") | Where-Object { $_.Trim() -ne '' }
} else {
    (git diff --name-only --diff-filter=ACMR $base).Split("`n") | Where-Object { $_ -match '\.py$' } | Where-Object { $_.Trim() -ne '' }
}
if ($files) {
    $ruffArgs = @('-m', 'ruff', 'check') + @($files)
    Invoke-Python $ruffArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Fix lint: $pyPrefix -m ruff check --fix <files> && $pyPrefix -m ruff format <files>"
    }
}

Write-Host '==> Repo standards'
& .agents/skills/repo-standards/scripts/repo-standards.ps1 --check
if ($LASTEXITCODE -ne 0) {
    throw "Fix repo standards: $pyPrefix .agents/skills/repo-standards/scripts/repo_standards.py --apply --yes"
}

Write-Host '==> Validate agent mesh'
& .agents/skills/generating-agent-mesh/scripts/validate-agent-mesh.ps1 --check
if ($LASTEXITCODE -ne 0) {
    throw "Fix agent mesh: $pyPrefix .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py"
}

foreach ($phase in @('inventory', 'heal', 'project', 'index', 'catalog', 'validate')) {
    Write-Host "==> Marketplace $phase"
    Invoke-Python @('tools/rebuild_marketplace.py', '--phase', $phase, '--check')
    if ($LASTEXITCODE -ne 0) {
        throw "Fix marketplace: $pyPrefix tools/rebuild_marketplace.py"
    }
}

Write-Host 'All preflight checks passed.'
