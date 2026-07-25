<#
.SYNOPSIS
  Scaffold or validate .agents/plugins/marketplace.json.
#>
[CmdletBinding()]
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Remaining)
$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$python = $null
foreach ($l in @('py', 'python', 'python3')) {
    if (Get-Command $l -ErrorAction SilentlyContinue) {
        $python = $l
        break
    }
}
if (-not $python) {
    throw "No Python interpreter found"
}

if ($python -eq 'py') {
    & py -3 "$scriptDir\scaffold_marketplace_json.py" @Remaining
} else {
    & $python "$scriptDir\scaffold_marketplace_json.py" @Remaining
}
exit $LASTEXITCODE
