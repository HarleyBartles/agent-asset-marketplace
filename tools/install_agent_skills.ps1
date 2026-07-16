<#
.SYNOPSIS
  PowerShell wrapper for install_agent_skills.py

.DESCRIPTION
  Installs/refreshes skills in .agents/skills from installed marketplace plugins.
  This script wraps the Python implementation for environments where PowerShell
  is preferred or required.

.PARAMETER Check
  Check mode: report what would change without making changes

.PARAMETER Force
  Force refresh even when provenance matches

.EXAMPLE
  .\install_agent_skills.ps1
  .\install_agent_skills.ps1 -Check
  .\install_agent_skills.ps1 -Force
#>
[CmdletBinding()]
param(
    [switch]$Check,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ScriptDir = (Resolve-Path $PSScriptRoot).Path
$PythonScript = Join-Path $ScriptDir 'install_agent_skills.py'

if (-not (Test-Path $PythonScript)) {
    throw "Python script not found at $PythonScript"
}

# Build arguments
$argsList = @()
if ($Check) {
    $argsList += '--check'
}
if ($Force) {
    $argsList += '--force'
}

# Run Python script
& py -3 $PythonScript @argsList
exit $LASTEXITCODE
