#Requires -Version 5.1
<#
.SYNOPSIS
    Installs the Scalify CLI skill for Claude Code on Windows.
.EXAMPLE
    irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.ps1 | iex
#>
$ErrorActionPreference = "Stop"

$SkillDir = Join-Path $env:USERPROFILE ".claude\skills\scalify-cli"
$SkillUrl = "https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/skills/scalify-cli/SKILL.md"

Write-Host "Installing Scalify CLI skill for Claude Code..."

if (-not (Test-Path $SkillDir)) {
    New-Item -ItemType Directory -Path $SkillDir | Out-Null
}

Invoke-WebRequest -Uri $SkillUrl -OutFile (Join-Path $SkillDir "SKILL.md")

Write-Host "Skill installed to $SkillDir\SKILL.md"
Write-Host "Restart Claude Code (or start a new session) for the skill to take effect."
