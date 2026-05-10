#Requires -Version 5.1
<#
.SYNOPSIS
    Installs scalify-cli on Windows.
.DESCRIPTION
    Downloads the latest scalify-cli release from GitHub and installs it to
    %LOCALAPPDATA%\Programs\scalify-cli, then adds that directory to the
    current user's PATH if it is not already present.
.EXAMPLE
    irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.ps1 | iex
#>
$ErrorActionPreference = "Stop"

$Repo       = "Simple-Scalable-Solutions/scalify-cli"
$Binary     = "scalify-cli"
$InstallDir = if ($env:INSTALL_DIR) { $env:INSTALL_DIR } else { "$env:LOCALAPPDATA\Programs\scalify-cli" }

# Fetch latest release tag from GitHub API
$ApiUrl  = "https://api.github.com/repos/$Repo/releases/latest"
$Release = Invoke-RestMethod -Uri $ApiUrl -Headers @{ "User-Agent" = "scalify-cli-installer" }
$Version = $Release.tag_name.TrimStart("v")

# Detect CPU architecture
$Arch = if ([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture -eq "Arm64") { "arm64" } else { "amd64" }

$Filename = "${Binary}_${Version}_windows_${Arch}.zip"
$Url      = "https://github.com/$Repo/releases/download/v$Version/$Filename"

Write-Host "Installing $Binary v$Version (windows/$Arch)..."

$Tmp = Join-Path $env:TEMP "scalify-install-$(New-Guid)"
New-Item -ItemType Directory -Path $Tmp | Out-Null

try {
    $ZipPath = Join-Path $Tmp $Filename
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath

    Expand-Archive -Path $ZipPath -DestinationPath $Tmp

    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir | Out-Null
    }

    Copy-Item (Join-Path $Tmp "$Binary.exe") (Join-Path $InstallDir "$Binary.exe") -Force

    # Add install dir to the current user's PATH if not already present
    $UserPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
    if ($UserPath -notlike "*$InstallDir*") {
        [System.Environment]::SetEnvironmentVariable("PATH", "$UserPath;$InstallDir", "User")
        Write-Host "Added $InstallDir to your PATH."
        Write-Host "Restart your terminal for PATH changes to take effect."
    }

    Write-Host ""
    Write-Host "Installed to $InstallDir\$Binary.exe"
    Write-Host ""
    Write-Host "Next: set your API token"
    Write-Host "  $Binary auth set-token YOUR_TOKEN_HERE"
} finally {
    Remove-Item $Tmp -Recurse -Force -ErrorAction SilentlyContinue
}
