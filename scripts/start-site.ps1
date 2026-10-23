[CmdletBinding()]
param(
    [int]$Port = 5001,
    [switch]$NoBrowser
)

# Creates the virtual environment if needed, installs dependencies and starts the site in the background.
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvDir = Join-Path $ProjectRoot '.venv'
$VenvPython = Join-Path $VenvDir 'Scripts\python.exe'
$Requirements = Join-Path $ProjectRoot 'requirements.txt'
$Stamp = Join-Path $VenvDir '.requirements.hash'
$PidFile = Join-Path $PSScriptRoot '.site.pid'
$LogFile = Join-Path $PSScriptRoot '.site.log'
$ErrFile = Join-Path $PSScriptRoot '.site.err.log'
$Url = "http://127.0.0.1:$Port"

if (Test-Path $PidFile) {
    $existing = Get-Process -Id ([int](Get-Content $PidFile)) -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Site already running at $Url (PID $($existing.Id)). Use stop-site.ps1 to stop it."
        exit 0
    }
    Remove-Item $PidFile -Force
}

if (-not (Test-Path $VenvPython)) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { throw 'Python was not found on PATH.' }
    Write-Host 'Creating virtual environment...'
    & $python.Source -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the virtual environment.' }
}

$hash = (Get-FileHash $Requirements -Algorithm SHA256).Hash
if (-not (Test-Path $Stamp) -or (Get-Content $Stamp -Raw).Trim() -ne $hash) {
    Write-Host 'Installing dependencies...'
    & $VenvPython -m pip install --quiet -r $Requirements
    if ($LASTEXITCODE -ne 0) { throw 'pip install failed.' }
    Set-Content -Path $Stamp -Value $hash
}

if (-not (Test-Path (Join-Path $ProjectRoot 'static\css\pygments.css'))) {
    & $VenvPython (Join-Path $PSScriptRoot 'generate_pygments_css.py') | Out-Null
}

$env:PORT = $Port
$process = Start-Process -FilePath $VenvPython -ArgumentList 'app.py' -WorkingDirectory $ProjectRoot `
    -WindowStyle Hidden -PassThru -RedirectStandardOutput $LogFile -RedirectStandardError $ErrFile
Set-Content -Path $PidFile -Value $process.Id

$ready = $false
for ($i = 0; $i -lt 30 -and -not $ready; $i++) {
    if ($process.HasExited) { break }
    try {
        Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 | Out-Null
        $ready = $true
    } catch {
        Start-Sleep -Milliseconds 500
    }
}

if (-not $ready) {
    Write-Warning "The site did not start. See $ErrFile"
    exit 1
}

Write-Host "Site running at $Url (PID $($process.Id))"
if (-not $NoBrowser) { Start-Process $Url }
