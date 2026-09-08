[CmdletBinding()]
param(
    [switch]$Run,
    [switch]$Preflight,
    [string]$Scenario
)

$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
$evals = Join-Path $repo 'evals'
$scenarios = Join-Path $repo 'tests\pressure\workflow-contracts\quorum\scenarios'
$quorumBin = Join-Path $repo 'tests\pressure\workflow-contracts\quorum\bin'
$windowsProfile = if ($env:USERPROFILE) { $env:USERPROFILE } else { throw 'USERPROFILE is unset' }
$exam = Get-Content -Raw (Join-Path $PSScriptRoot 'exam.json') | ConvertFrom-Json

if ($Run -and $Preflight) {
    throw '-Run and -Preflight are mutually exclusive'
}

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

function Invoke-WslScript([string]$Script) {
    $start = [System.Diagnostics.ProcessStartInfo]::new()
    $start.FileName = 'wsl.exe'
    $start.UseShellExecute = $false
    $start.RedirectStandardInput = $true
    $graderAuthNames = @('CLAUDE_CODE_OAUTH_TOKEN', 'ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_API_KEY')
    $graderPattern = '^(' + (($graderAuthNames | ForEach-Object { [regex]::Escape($_) }) -join '|') + ')(?:/.*)?$'
    $wslEnv = @($start.Environment['WSLENV'] -split ':' | Where-Object { $_ -and $_ -notmatch $graderPattern })
    $start.Environment['WSLENV'] = (@($wslEnv) + $graderAuthNames) -join ':'
    [void]$start.ArgumentList.Add('-e')
    [void]$start.ArgumentList.Add('bash')
    [void]$start.ArgumentList.Add('-s')

    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $start
    [void]$process.Start()
    $process.StandardInput.Write($Script.Replace("`r`n", "`n"))
    $process.StandardInput.Close()
    $process.WaitForExit()
    return $process.ExitCode
}

$evalsWsl = Convert-ToWslPath $evals
$repoWsl = Convert-ToWslPath $repo
$gitDir = (& git -C $repo rev-parse --absolute-git-dir).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($gitDir)) {
    throw "git could not resolve the worktree git directory for $repo"
}
$gitDirWsl = Convert-ToWslPath $gitDir
$scenariosWsl = Convert-ToWslPath $scenarios
$quorumBinWsl = Convert-ToWslPath $quorumBin
$desktopAuthWsl = Convert-ToWslPath (Join-Path $windowsProfile '.codex')

if (-not $Run -and -not $Preflight) {
    $command = "set -euo pipefail`ncd $(Quote-Bash $evalsWsl)`nexec npx --yes bun run src/cli/index.ts check --scenarios-root $(Quote-Bash $scenariosWsl)`n"
    exit (Invoke-WslScript $command)
}

$selected = if ([string]::IsNullOrWhiteSpace($Scenario)) {
    @($exam.scenarios)
} elseif ($exam.scenarios -contains $Scenario) {
    @($Scenario)
} else {
    throw "Unknown MARK-373 scenario: $Scenario"
}
$scenarioArgs = ($selected | ForEach-Object { Quote-Bash ([string]$_) }) -join ' '

$commandParts = @(
    'set -euo pipefail',
    "repo=$(Quote-Bash $repoWsl)",
    "repo_git_dir=$(Quote-Bash $gitDirWsl)",
    "evals=$(Quote-Bash $evalsWsl)",
    "scenarios=$(Quote-Bash $scenariosWsl)",
    "quorum_bin=$(Quote-Bash $quorumBinWsl)",
    "desktop_auth=$(Quote-Bash $desktopAuthWsl)",
    'export PATH="$quorum_bin:$PATH"',
    'if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}${ANTHROPIC_AUTH_TOKEN:-}${ANTHROPIC_API_KEY:-}" ]; then printf ''%s\n'' ''MARK-373 preflight: Quorum requires an Anthropic grader credential'' >&2; exit 3; fi',
    'test -z "$(git --git-dir="$repo_git_dir" --work-tree="$repo" status --porcelain)"',
    'evidence_head=$(git --git-dir="$repo_git_dir" --work-tree="$repo" rev-parse HEAD)',
    'auth_runtime=$(mktemp -d)',
    'preflight_runtime=$(mktemp -d)',
    'trap ''rm -rf "$auth_runtime" "$preflight_runtime"'' EXIT',
    'install -d -m 700 "$auth_runtime"',
    'install -m 600 "$desktop_auth/auth.json" "$auth_runtime/auth.json"',
    'export CODEX_AUTH_HOME="$auth_runtime"',
    'mkdir -p "$preflight_runtime/home" "$preflight_runtime/codex"',
    'install -m 600 "$auth_runtime/auth.json" "$preflight_runtime/codex/auth.json"',
    'mcp_json=$(HOME="$preflight_runtime/home" CODEX_HOME="$preflight_runtime/codex" codex mcp list --json -c features.apps=false)',
    'test "$(printf ''%s'' "$mcp_json" | tr -d ''[:space:]'')" = ''[]''',
    'plugin_json=$(HOME="$preflight_runtime/home" CODEX_HOME="$preflight_runtime/codex" codex plugin list --json -c features.plugins=false)',
    'plugin_compact=$(printf ''%s'' "$plugin_json" | tr -d ''[:space:]'')',
    'case "$plugin_compact" in *''"installed":[]''*''"available":[]''*) ;; *) printf ''%s\n'' ''MARK-373 preflight: external plugin inventory is not empty'' >&2; exit 2 ;; esac',
    'cd "$evals"'
)

if ($Preflight) {
    $commandParts += 'printf ''MARK-373 preflight-ready head=%s\n'' "$evidence_head"'
} else {
    $commandParts += 'mkdir -p "results/mark373/$evidence_head"'
    $commandParts += ('for scenario in {0}; do npx --yes bun run src/cli/index.ts run "$scenario" --coding-agent codex --credential codex_sub --scenarios-root "$scenarios" --out-root results/mark373/"$evidence_head" --effort medium --no-superpowers; done' -f $scenarioArgs)
}

exit (Invoke-WslScript (($commandParts -join "`n") + "`n"))
