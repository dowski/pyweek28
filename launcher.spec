# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['launcher.py'],
             pathex=['C:\\Users\\Christian\\PycharmProjects\\pyweek28'],
             binaries=[],
             datas=[
             ('images', 'images'),
             ('sounds', 'sounds'),
             ('fonts', 'fonts'),
             ('stackytower.py', '.'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='stackytower',
          icon='stackytower.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
