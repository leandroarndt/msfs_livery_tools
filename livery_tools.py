from pathlib import Path
from msfs_livery_tools.gui import main

RESOURCES_DIR:Path = (Path(__file__).parent / 'resources').absolute()
URL = 'https://github.com/leandroarndt/msfs_livery_tools'
ABOUT = 'MSFS Livery Tools automates all bureaucratic tasks of MSFS 2020 livery creation.'
COPYRIGHT = (Path(__file__).parent / 'LICENSE').read_text()
YOUTUBE = 'https://youtube.com/@fswt'
VERSION = 0
SUBVERSION = 1

if __name__ == '__main__':
    app = main.MainWindow()
    app.win.mainloop()