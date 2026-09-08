[CmdletBinding()]
param(
    [switch]$Run,
    [string]$Scenario
)

$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
$evals = Join-Path $repo 'evals'
$scenarios = Join-Path $repo 'tests\pressure\workflow-contracts\quorum\scenarios'
$superpowers = Join-Path $repo 'codex-marketplace\plugins\superpowers-plus'
$windowsProfile = if ($env:USERPROFILE) { $env:USERPROFILE } else { throw 'USERPROFILE is unset' }

function Convert-ToWslPath([string]$Path) {
    $normalized = $Path.Replace('\', '/')
    $converted = (& wsl.exe wslpath -a -- $normalized).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($converted)) {
        throw "wslpath failed for $Path"
    }
    return $converted
}

function Quote-Bash([string]$Value) {
    $quote = [char]39
    $escapedQuote = [string]$quote + [char]92 + [char]$quote + [char]92 + [char]$quote
    return [string]$quote + $Value.Replace([string]$quote, $escapedQuote) + [string]$quote
}

$evalsWsl = Convert-ToWslPath $evals
$scenariosWsl = Convert-ToWslPath $scenarios
$superpowersWsl = Convert-ToWslPath $superpowers
$authHomeWsl = Convert-ToWslPath (Join-Path $windowsProfile '.codex')

$commandParts = @(
    "cd $(Quote-Bash $evalsWsl)",
    "export CODEX_AUTH_HOME=$(Quote-Bash $authHomeWsl)",
    "export SUPERPOWERS_ROOT=$(Quote-Bash $superpowersWsl)"
)

if ($Run) {
    $scenarioArg = if ([string]::IsNullOrWhiteSpace($Scenario)) { '' } else { " --scenarios $(Quote-Bash $Scenario)" }
    $commandParts += "exec npx --yes bun run src/cli/index.ts run-all --coding-agents codex --credentials codex_sub --scenarios-root $(Quote-Bash $scenariosWsl) --jobs 1$scenarioArg --out-root results/mark373"
} else {
    $commandParts += "exec npx --yes bun run src/cli/index.ts check --scenarios-root $(Quote-Bash $scenariosWsl)"
}

& wsl.exe bash -lc ($commandParts -join '; ')
exit $LASTEXITCODE
