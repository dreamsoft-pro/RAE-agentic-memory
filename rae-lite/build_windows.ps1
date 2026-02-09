# Build RAE-Lite for Windows
# Usage: .\build_windows.ps1

$ErrorActionPreference = "Stop"

Write-Host "Building RAE-Lite for Windows..." -ForegroundColor Cyan

# 1. Check and download models
$ModelsDir = Join-Path (Get-Location) "..\models"
$NomicDir = Join-Path $ModelsDir "nomic-embed-text-v1.5"
$NomicModelPath = Join-Path $NomicDir "model.onnx"

if (-not (Test-Path $NomicDir)) {
    New-Item -ItemType Directory -Force -Path $NomicDir | Out-Null
}

if (-not (Test-Path $NomicModelPath)) {
    Write-Host "Nomic ONNX model not found. Please ensure 'models/nomic-embed-text-v1.5/model.onnx' exists." -ForegroundColor Yellow
} else {
    Write-Host "Nomic model found." -ForegroundColor Green
}

# 2. Setup Venv
Write-Host "Setting up Python virtual environment..." -ForegroundColor Cyan
if (-not (Test-Path "build_venv")) {
    python -m venv build_venv
}

.\build_venv\Scripts\Activate.ps1

# 3. Install Dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install pyinstaller fastapi uvicorn httpx numpy aiosqlite pydantic pydantic-settings structlog pystray pillow nicegui pypdf onnxruntime tokenizers
# Install rae-core in editable mode
pip install -e ../rae-core

# 3.5. Stop running instances
Write-Host "🛑 Stopping running RAE-Lite instances..." -ForegroundColor Cyan
Stop-Process -Name "RAE-Lite" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 4. Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Cyan
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

# 5. Build
Write-Host "Running PyInstaller..." -ForegroundColor Cyan
pyinstaller rae-lite.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build complete!" -ForegroundColor Green
    Write-Host "Output directory: dist\RAE-Lite" -ForegroundColor Green
    Write-Host "Run: dist\RAE-Lite\RAE-Lite.exe" -ForegroundColor Green
} else {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}
