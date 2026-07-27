<#
.SYNOPSIS
  Optional CI preflight extra: run ruff on changed Python files.
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Remaining
)

$ErrorActionPreference = 'Stop'

$ScriptDir = (Resolve-Path $PSScriptRoot).Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir '..')).Path

$ChangedFrom = $null
for ($i = 0; $i -lt $Remaining.Count; $i++) {
    switch ($Remaining[$i]) {
        '--changed-from' {
            $i++
            $ChangedFrom = $Remaining[$i]
        }
        '--check' {
            # ruff check is read-only; no action needed
        }
        default {
            if ($Remaining[$i]) {
                Write-Warning "Unknown argument: $($Remaining[$i])"
            }
        }
    }
}

if (-not (Get-Command ruff -ErrorAction SilentlyContinue)) {
    Write-Host "ruff not found; skipping Python lint (install with: pip install ruff==0.9.0)"
    exit 0
}

$base = if ($ChangedFrom) { $ChangedFrom } else { 'origin/main...HEAD' }
$changed = git -C $RepoRoot diff --name-only $base -- '*.py' | Where-Object { $_.Trim() }
$exitCode = 0

if (-not $changed) {
    Write-Host "No changed Python files to lint."
    exit 0
}

Push-Location $RepoRoot
try {
    ruff check @($changed)
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}
exit $exitCode
