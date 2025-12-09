#!/bin/bash
# Build RAE-Lite standalone executable

set -e

echo "Building RAE-Lite..."

# Install dependencies
pip install -e ".[dev]"

# Clean previous builds
rm -rf build/ dist/

# Build with PyInstaller
pyinstaller rae-lite.spec

echo "Build complete!"
echo "Executable: dist/RAE-Lite"

# Platform-specific instructions
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS: RAE-Lite.app created in dist/"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Windows: RAE-Lite.exe created in dist/"
else
    echo "Linux: RAE-Lite created in dist/"
fi
