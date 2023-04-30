from distutils.core import setup
from pathlib import Path
import livery_tools
import py2exe

def data_files(folder:str, patterns:list[str])->tuple:
      files = []
      path = Path(folder)
      for pattern in patterns:
            for file in path.glob(pattern):
                  files.append(file)
      return (folder, files)

py2exe.freeze(
      windows=['livery_tools.py'],
      data_files=[data_files('resources', ['*.png', '*.ico']), data_files('.', ['LICENSE'])],
      options={
            'packages': ['msfs_livery_tools',
                         'msfs_livery_tools.compression',
                         'msfs_livery_tools.gui',
                         'msfs_livery_tools.package',
                         'msfs_livery_tools.project',
                         'msfs_livery_tools.settings'],
      },
      version_info={
            'product_name': 'MSFS Livery Tools',
            'description': livery_tools.ABOUT,
            'version': f'{livery_tools.VERSION}.{livery_tools.SUBVERSION}',
      }
)