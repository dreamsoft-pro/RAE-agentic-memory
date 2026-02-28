# ScreenWatcher Edge Client Build Script

Write-Host "Cleaning up previous builds..."
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }

$PYINSTALLER = ".\venv\Scripts\pyinstaller.exe"
$TESSERACT_DATA = "C:\cloud\screenwatcher_project\tesseract\bin;tesseract_bin"

Write-Host "Building sw_agent.exe..."
& $PYINSTALLER --onefile --name sw_agent --distpath ./dist/edge_client --add-data $TESSERACT_DATA edge_client/main.py

Write-Host "Building sw_configurator.exe..."
& $PYINSTALLER --onefile --windowed --name sw_configurator --distpath ./dist/edge_client --add-data $TESSERACT_DATA edge_client/configurator.py

Write-Host "Build complete! Files are in ./dist/edge_client"