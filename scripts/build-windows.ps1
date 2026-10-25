[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    cmake --preset windows
    if ($LASTEXITCODE -ne 0) { throw 'CMake configuration failed.' }
    cmake --build --preset windows-release
    if ($LASTEXITCODE -ne 0) { throw 'Windows build failed.' }
} finally { Pop-Location }
