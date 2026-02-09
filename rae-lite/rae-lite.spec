# PyInstaller spec file for RAE-Lite
# Usage: pyinstaller rae-lite.spec

import sys
from pathlib import Path
import site

block_cipher = None

rae_core_src = str(Path('../rae-core/rae_core').absolute())
models_src = str(Path('../models').absolute())

# Include rae_core source code
datas_list = [(rae_core_src, 'rae_core')]

# Include models directory if it exists
if Path(models_src).exists():
    datas_list.append((models_src, 'models'))

a = Analysis(
    ['rae_lite/main.py'],
    pathex=['../rae-core', '../rae_adapters'], # Add to path for analysis
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        'rae_core',
        'rae_core.engine',
        'rae_adapters.sqlite',
        'rae_adapters.sqlite.storage',
        'rae_adapters.sqlite.vector',
        'rae_adapters.sqlite.graph',
        'rae_core.layers',
        'rae_core.layers.working',
        'rae_core.layers.longterm',
        'rae_core.layers.sensory',
        'rae_core.layers.reflective',
        'rae_core.search',
        'rae_core.search.engine',
        'rae_core.search.strategies',
        'rae_core.search.strategies.vector',
        'rae_core.search.strategies.sparse',
        'rae_core.search.strategies.fulltext',
        'rae_core.search.strategies.graph',
        'rae_core.embedding',
        'rae_core.embedding.native',
        'fastapi',
        'uvicorn',
        'pystray',
        'PIL',
        'structlog',
        'aiosqlite',
        'numpy',
        'nicegui',
        'pypdf',
        'onnxruntime',
        'tokenizers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'scipy',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RAE-Lite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Console enabled for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RAE-Lite',
)

# macOS .app bundle (optional, requires COLLECT output usually wrapped differently or just ONEFILE)
# For onedir on macOS, you typically just distribute the folder or wrap it in a DMG.
# Keeping the BUNDLE block for reference, but it might need adjustment for onedir.
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='RAE-Lite.app',
        icon='assets/icon.icns',
        bundle_identifier='com.rae.lite',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
        },
    )
