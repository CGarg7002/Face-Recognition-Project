# -*- mode: python ; coding: utf-8 -*-
import os

# NEW: Import PyInstaller's utility
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files('dlib') + collect_data_files('face_recognition_models'),
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
