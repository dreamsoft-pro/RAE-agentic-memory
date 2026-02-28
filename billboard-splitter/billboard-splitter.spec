# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Zasoby własne pakietu (jeśli masz podpakiet 'billboard_splitter' z assetami)
datas = collect_data_files('billboard_splitter')

# Pliki projektu, które chcesz dołączyć
datas += [
    ('settings.json', '.'),
    ('profiles.json', '.'),
    ('input/billboard3.pdf', 'input'),
    ('poppler/bin', 'poppler/bin'),
    ('icons/billboard_icon.ico', 'icons'),
]

# Tkinter/Pillow – dopisz, jeśli używasz Pillow
datas += collect_data_files('tkinter')
hiddenimports = []
hiddenimports += collect_submodules('tkinter')

# Jeśli w GUI używasz Pillow, odkomentuj:
# datas += collect_data_files('PIL')
# hiddenimports += collect_submodules('PIL')

a = Analysis(
    ['main.pyw'],             # ← jeśli masz 'main.py', zmień tutaj na 'main.py'
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='billboard-splitter',          # nazwa exe i folderu w dist/
    icon='icons/billboard_icon.ico',    # zmień/usuń, jeśli nie masz
    console=False,                      # ← bez konsoli (no-blink)
    debug=False,
    upx=True,
    disable_windowed_traceback=False,
)

# ONEDIR – generuje folder dist/billboard-splitter/ z zawartością
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='billboard-splitter',
)
