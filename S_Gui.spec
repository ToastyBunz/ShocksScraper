# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/jashu/git/ShocksScraper/S_Gui.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/jashu/git/ShocksScraper/Lib/site-packages/customtkinter', 'customtkinter/'), ('C:/Users/jashu/git/ShocksScraper/Lib/site-packages/seleniumwire', 'seleniumwire/'), ('C:/Users/jashu/git/ShocksScraper/images', 'images/'), ('C:/Users/jashu/git/ShocksScraper/Lib/site-packages/certifi', 'certifi/')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='S_Gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\jashu\\git\\ShocksScraper\\images\\Excel-Logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='S_Gui',
)
