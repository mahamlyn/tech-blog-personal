[CmdletBinding()]
param(
    [switch]$KeepVenv
)

# Stops the site and removes environment files that can be recreated (.venv, __pycache__, pid and log files).
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvDir = Join-Path $ProjectRoot '.venv'
$PidFile = Join-Path $PSScriptRoot '.site.pid'

if (Test-Path $PidFile) {
    $siteId = [int](Get-Content $PidFile)
    if (Get-Process -Id $siteId -ErrorAction SilentlyContinue) {
        # /T also ends the Flask reloader's child process.
        taskkill /PID $siteId /T /F | Out-Null
        Write-Host "Stopped site (PID $siteId)."
    }
}

# Anything else still running from the venv would block its removal.
Get-CimInstance Win32_Process |
    Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($VenvDir, [StringComparison]::OrdinalIgnoreCase) } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

foreach ($file in '.site.pid', '.site.log', '.site.err.log') {
    Remove-Item (Join-Path $PSScriptRoot $file) -Force -ErrorAction SilentlyContinue
}

Get-ChildItem -Path $ProjectRoot -Recurse -Directory -Filter '__pycache__' -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "$VenvDir*" } |
    ForEach-Object { Remove-Item $_.FullName -Recurse -Force }

if ($KeepVenv) {
    Write-Host 'Kept .venv.'
} elseif (Test-Path $VenvDir) {
    Remove-Item $VenvDir -Recurse -Force
    Write-Host 'Removed .venv.'
}

Write-Host 'Done. If this terminal had the venv activated, run "deactivate".'
