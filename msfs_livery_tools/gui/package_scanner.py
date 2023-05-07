from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.vfs import VFS
from tkinter import ttk
from threading import Thread

class Scanner(Thread):
    progress_bar_mode:str = 'indeterminate'
    
    def __init__(self, parent, splash=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.settings = AppSettings()
        self.splash = splash
    
    def run(self):
        self.parent.vfs = VFS.new(self.settings.msfs_package_path)
