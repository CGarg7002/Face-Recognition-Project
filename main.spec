# -*- mode: python ; coding: utf-8 -*-
import os
import dlib

# Dynamically find the path to dlib's data files
dlib_data_path = os.path.join(dlib.__path__[0], '*.*')

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[(dlib_data_path, 'dlib')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
