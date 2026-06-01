$ErrorActionPreference = "Stop"

$AppRoot = Split-Path -Parent $PSScriptRoot
Set-Location $AppRoot

python scripts/build.py @args
