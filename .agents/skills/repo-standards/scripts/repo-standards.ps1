<#
.SYNOPSIS
  Run the repo-standards check/apply script.
#>
[CmdletBinding()]
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Remaining)
$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$pyArgs = @()
foreach ($arg in $Remaining) {
    switch ($arg) {
        '-Check' { $pyArgs += '--check' }
        '-Apply' { $pyArgs += '--apply' }
        '-Yes' { $pyArgs += '--yes' }
        '-AllowSharedCheckout' { $pyArgs += '--allow-shared-checkout' }
        default { $pyArgs += $arg }
    }
}

$python = "py"
$launchers = @('py', 'python', 'python3')
foreach ($l in $launchers) {
    if (Get-Command $l -ErrorAction SilentlyContinue) {
        $python = $l
        break
    }
}

if ($python -eq 'py') {
    & py -3 "$scriptDir\repo_standards.py" @pyArgs
} else {
    & $python "$scriptDir\repo_standards.py" @pyArgs
}
exit $LASTEXITCODE
