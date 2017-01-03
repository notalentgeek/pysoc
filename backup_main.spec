# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/notalentgeek/Downloads/project-commitment/pc-ut-bachelor-thesis-2016/deliverable-programming/sociometric-client-python'],
             binaries=None,
             datas=[('./cascade-face-front-default.xml', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
