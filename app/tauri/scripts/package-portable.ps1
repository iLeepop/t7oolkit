# Package a portable Windows zip from a --no-bundle Tauri build.
# Usage: .\scripts\package-portable.ps1

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$ReleaseDir = Join-Path $Root "src-tauri/target/release"
$OutDir = Join-Path $Root "dist/release"
$ConfPath = Join-Path $Root "src-tauri/tauri.conf.json"

$Config = Get-Content $ConfPath -Raw | ConvertFrom-Json
$Version = $Config.version
$ProductName = $Config.productName

$ExeName = "$ProductName.exe"
$ExePath = Join-Path $ReleaseDir $ExeName

if (-not (Test-Path $ExePath)) {
    throw "Expected executable not found: $ExePath (run 'npm run build:portable' first)"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$Staging = Join-Path $OutDir "portable-staging"
if (Test-Path $Staging) {
    Remove-Item -Recurse -Force $Staging
}
New-Item -ItemType Directory -Force -Path $Staging | Out-Null

Copy-Item $ExePath $Staging

$LoaderDll = Join-Path $ReleaseDir "WebView2Loader.dll"
if (Test-Path $LoaderDll) {
    Copy-Item $LoaderDll $Staging
}

$ZipPath = Join-Path $OutDir "$ProductName-$Version-windows-portable.zip"
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath
}

Compress-Archive -Path (Join-Path $Staging "*") -DestinationPath $ZipPath
Remove-Item -Recurse -Force $Staging

Write-Host "Portable package: $ZipPath"
