[CmdletBinding()]
param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
    git submodule update --init --recursive
    if ($LASTEXITCODE -ne 0) { throw 'Engine checkout failed.' }
    & $Python external/WebEngine/tools/setup_windows.py
    if ($LASTEXITCODE -ne 0) { throw 'Engine dependency setup failed. Python 3.12+ is required.' }
} finally { Pop-Location }
