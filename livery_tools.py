from pathlib import Path
from msfs_livery_tools.gui import main

try:
    RESOURCES_DIR:Path = (Path(__file__).parent / 'resources').absolute()
    COPYRIGHT = (Path(__file__).parent / 'LICENSE').read_text()
except NameError: # Executing from py2exe version
    import sys
    RESOURCES_DIR:Path = (Path(sys.executable).parent / 'resources').absolute()
    COPYRIGHT = (Path(sys.executable).parent / 'LICENSE').read_text()
URL = 'https://github.com/leandroarndt/msfs_livery_tools'
ABOUT = 'MSFS Livery Tools automates all bureaucratic tasks of MSFS 2020 livery creation.'
YOUTUBE = 'https://youtube.com/@fswt'
VERSION = 1
SUBVERSION = 3

if __name__ == '__main__':
    app = main.MainWindow()
    app.win.mainloop()