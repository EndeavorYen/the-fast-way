#Requires -Version 5.1
param(
    [Parameter(Position = 0)]
    [ValidateSet('grok', 'claude', 'cursor', 'hermes', 'all')]
    [string]$Platform = 'all',
    [switch]$SkipLeaves
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillSrc = Join-Path $RepoRoot 'SKILL.md'
$ReadmeSrc = Join-Path $RepoRoot 'README.md'
$RefsSrc = Join-Path $RepoRoot 'references'
if (-not (Test-Path -LiteralPath $SkillSrc)) {
    throw "SKILL.md not found at $SkillSrc"
}
if ($env:THE_FAST_WAY_SKIP_LEAVES -eq '1') {
    $SkipLeaves = $true
}

$LeafRepos = @(
    @{ Name = 'gentle-grill-me'; Url = 'https://github.com/EndeavorYen/gentle-grill-me.git' },
    @{ Name = 'musk-algorithm-skill'; Url = 'https://github.com/EndeavorYen/musk-algorithm-skill.git' },
    @{ Name = 'just-ten-more'; Url = 'https://github.com/EndeavorYen/just-ten-more.git' }
)

function Get-UserHome {
    if ($env:USERPROFILE) { return $env:USERPROFILE }
    return $HOME
}

function Get-Dest([string]$Name) {
    $homeDir = Get-UserHome
    switch ($Name) {
        'grok' {
            $root = if ($env:GROK_HOME) { $env:GROK_HOME } else { Join-Path $homeDir '.grok' }
            return (Join-Path $root 'skills\the-fast-way')
        }
        'hermes' {
            $root = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { Join-Path $homeDir '.hermes' }
            return (Join-Path $root 'skills\the-fast-way')
        }
        'claude' { return (Join-Path $homeDir '.claude\skills\the-fast-way') }
        'cursor' { return (Join-Path $homeDir '.cursor\skills\the-fast-way') }
        default { throw "Unknown platform $Name" }
    }
}

function Install-To([string]$Name) {
    $dest = Get-Dest $Name
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Force -LiteralPath $SkillSrc -Destination (Join-Path $dest 'SKILL.md')
    if (Test-Path -LiteralPath $ReadmeSrc) {
        Copy-Item -Force -LiteralPath $ReadmeSrc -Destination (Join-Path $dest 'README.md')
    }
    if (Test-Path -LiteralPath $RefsSrc) {
        $refsDest = Join-Path $dest 'references'
        if (Test-Path -LiteralPath $refsDest) {
            Remove-Item -LiteralPath $refsDest -Recurse -Force
        }
        Copy-Item -Recurse -LiteralPath $RefsSrc -Destination $refsDest
    }
    Write-Output "Installed $Name -> $dest"
}

function Install-Leaves([string]$LeafPlatform) {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        throw "git is required to install leaf skills from GitHub"
    }
    $tmpRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("the-fast-way-leaves-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null
    try {
        foreach ($repo in $LeafRepos) {
            $cloneDest = Join-Path $tmpRoot $repo.Name
            Write-Output "Cloning $($repo.Url)"
            & git clone --depth 1 $repo.Url $cloneDest
            if ($LASTEXITCODE -ne 0) {
                throw "git clone failed: $($repo.Url)"
            }
            $installer = Join-Path $cloneDest 'scripts\install.ps1'
            if (-not (Test-Path -LiteralPath $installer)) {
                throw "missing scripts/install.ps1 in $($repo.Name)"
            }
            Write-Output "Installing leaf $($repo.Name) for $LeafPlatform"
            & powershell -NoProfile -ExecutionPolicy Bypass -File $installer $LeafPlatform
            if ($LASTEXITCODE -ne 0) {
                if ($LeafPlatform -eq 'hermes') {
                    Write-Output "Skip $($repo.Name) on hermes: leaf installer rejected the platform"
                    continue
                }
                throw "leaf install failed: $($repo.Name) $LeafPlatform"
            }
        }
    }
    finally {
        Remove-Item -Recurse -Force $tmpRoot -ErrorAction SilentlyContinue
    }
}

$targets = if ($Platform -eq 'all') { @('grok', 'claude', 'cursor', 'hermes') } else { @($Platform) }
foreach ($t in $targets) { Install-To $t }
if (-not $SkipLeaves) {
    Install-Leaves $Platform
}
