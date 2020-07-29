# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
block_cipher = None

a = Analysis(['phenotrex_gui/__init__.py'],
             binaries=[],
             pathex=[Path(SPECPATH).resolve().absolute()],
             datas=[('./phenotrex_gui/ui/*.ui', 'phenotrex_gui/ui')],
             hiddenimports=['sklearn.neighbors._typedefs', 'scipy.special.cython_special', 'sklearn.utils._cython_blas', 'sklearn.neighbors._quad_tree', 'sklearn.tree._utils'],
             hookspath=['./hooks'],
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
          [],
          exclude_binaries=True,
          name='phenotrex-gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='phenotrex-gui')
