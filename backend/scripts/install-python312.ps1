# Install Python 3.12+ for ChitraBazar (Django 6 requires Python >= 3.12)
# Run in PowerShell:  Set-ExecutionPolicy -Scope Process Bypass; .\scripts\install-python312.ps1

$ErrorActionPreference = "Stop"
$PyVersion = "3.12.10"
$PyRoot = "$env:LOCALAPPDATA\Programs\Python\Python312"
$Installer = "$env:TEMP\python-$PyVersion-amd64.exe"
$EmbedZip = "$env:TEMP\python-$PyVersion-embed-amd64.zip"

function Test-Python312 {
    if (Test-Path "$PyRoot\python.exe") {
        & "$PyRoot\python.exe" --version
        return $true
    }
    $py312 = & py -3.12 --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Found: $py312"
        return $true
    }
    return $false
}

Write-Host "=== ChitraBazar: Python $PyVersion installer ===" -ForegroundColor Cyan

if (Test-Python312) {
    Write-Host "Python 3.12 already installed. Skipping download." -ForegroundColor Green
    py -0p
    exit 0
}

Write-Host "Downloading official installer..."
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$PyVersion/python-$PyVersion-amd64.exe" `
    -OutFile $Installer -UseBasicParsing

Write-Host "Installing (per-user, no global launcher — avoids error 1603)..."
# Include_launcher=0 avoids conflict with existing Python 3.11 py launcher
$proc = Start-Process -FilePath $Installer -ArgumentList @(
    "/quiet",
    "InstallAllUsers=0",
    "PrependPath=1",
    "Include_test=0",
    "Include_launcher=0",
    "SimpleInstall=1"
) -Wait -PassThru

if ($proc.ExitCode -ne 0) {
    Write-Warning "MSI installer exited with $($proc.ExitCode). Trying embeddable package..."
    if (-not (Test-Path $PyRoot)) { New-Item -ItemType Directory -Path $PyRoot -Force | Out-Null }
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$PyVersion/python-$PyVersion-embed-amd64.zip" `
        -OutFile $EmbedZip -UseBasicParsing
    Expand-Archive -Path $EmbedZip -DestinationPath $PyRoot -Force
    $pth = Join-Path $PyRoot "python312._pth"
    (Get-Content $pth) -replace '#import site', 'import site' | Set-Content $pth
    $getPip = "$env:TEMP\get-pip.py"
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getPip -UseBasicParsing
    & "$PyRoot\python.exe" $getPip
}

Write-Host ""
Write-Host "Installed versions:" -ForegroundColor Green
py -0p 2>$null
if (Test-Path "$PyRoot\python.exe") {
    & "$PyRoot\python.exe" --version
}

Write-Host ""
Write-Host "Recreate project venv (optional):" -ForegroundColor Yellow
Write-Host "  cd $PSScriptRoot\.."
Write-Host "  py -3.12 -m venv .venv --clear"
Write-Host "  .\.venv\Scripts\pip install -r requirements.txt"
