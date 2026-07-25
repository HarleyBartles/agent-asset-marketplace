#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ScriptDir = (Resolve-Path $PSScriptRoot).Path
$scripts = @('scaffold-repo-guide-policy', 'scaffold-guides', 'scaffold-review', 'scaffold-contributing', 'scaffold-ci-preflight', 'scaffold-gitignore')

foreach ($name in $scripts) {
    Write-Host "==> running ${name}"
    & "${ScriptDir}/${name}.ps1" @args
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
