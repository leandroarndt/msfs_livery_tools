from pathlib import Path
from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.vfs import VFS
from tkinter import ttk
from threading import Thread

class Scanner(Thread):
    progress_bar_mode:str = 'indeterminate'
    
    def __init__(self, parent, queue, splash=None, new_vfs=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.settings = AppSettings()
        self.splash = splash
        self.queue = queue
        self.new_vfs = new_vfs
    
    def run(self):
        if self.new_vfs:
            self.parent.vfs = VFS.new(self.settings.msfs_package_path,
                                        include_all=self.settings.scan_all_folders,
                                        queue=self.queue, depth=self.settings.scan_depth)
        else:
            self.parent.vfs.package_folder = Path(self.settings.msfs_package_path)
            self.parent.vfs.scan(queue=self.queue, include_all=self.settings.scan_all_folders, depth=self.settings.scan_depth)
