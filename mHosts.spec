# -*- mode: python -*-

block_cipher = None

datas = [
    (r'.\icons',r'icons'),
    (r'.\mHosts.json','.'),
    (r'.\icons\aliyun.png',r'icons'),
    (r'.\icons\chrome.png',r'icons'),
    (r'.\icons\common.png',r'icons'),
    (r'.\icons\database.png',r'icons'),
    (r'.\icons\edge.png',r'icons'),
    (r'.\icons\firefox.png',r'icons'),
    (r'.\icons\java.png',r'icons'),
    (r'.\icons\linux.png',r'icons'),
    (r'.\icons\logo.ico',r'icons'),
    (r'.\icons\logo.png',r'icons'),
    (r'.\icons\mac.png',r'icons'),
    (r'.\icons\mysql.png',r'icons'),
    (r'.\icons\postgresql.png',r'icons'),
    (r'.\icons\python.png',r'icons'),
    (r'.\icons\qq.png',r'icons'),
    (r'.\icons\server.png',r'icons'),
    (r'.\icons\table.png',r'icons'),
    (r'.\icons\user.png',r'icons'),
    (r'.\icons\wechat.png',r'icons'),
    (r'.\icons\win32.png',r'icons')
]

a = Analysis(
    ['mHosts.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='mHosts',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=False ,
    icon='icons\\logo.ico'
)
