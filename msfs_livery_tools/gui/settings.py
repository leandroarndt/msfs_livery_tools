import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.gui import helpers

class SettingsWindow(object):
    win:tk.Tk
    settings:AppSettings
    project:AppSettings # This name is used by GUI helpers
    frame:ttk.Frame
    texconv_frame:helpers.PathChooser
    master:object
    ok_button:ttk.Button
    cancel_button:ttk.Button
    
    def __init__(self, master):
        self.master = master
        self.win = tk.Toplevel(self.master)
        self.win.transient(self.master)
        self.win.title('MSFS Livery Tools settings')
        self.settings = AppSettings()
        self.project = self.settings
        self.frame = ttk.Frame(self.win)
        self.frame.pack(padx=5, pady=5)
        self.texconv_frame = helpers.PathChooser(self.frame, self,
                                                property='texconv_path',
                                                button_command=self.choose_texconv_path,
                                                title='Texconv.exe path', state=tk.NORMAL)
        self.texconv_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=5)
        self.texconv_frame.load()
        self.ok_button = ttk.Button(self.frame, command=self.ok_command, text='Ok')
        self.ok_button.pack(side=tk.RIGHT)
        self.cancel_button = ttk.Button(self.frame, command=self.cancel_command, text='Cancel')
        self.cancel_button.pack(side=tk.RIGHT)
        self.win.grab_set()
    
    def choose_texconv_path(self):
        path = filedialog.askopenfilename(title='Select textconv.exe path', filetypes=(
                                                ('Texconv executable', 'texconv.exe'),
                                            ))
        if Path(path).is_file():
            self.texconv_frame.value.set(path)
    
    def ok_command(self):
        self.settings.texconv_path = self.texconv_frame.value.get()
        self.settings.save()
        self.win.grab_release()
        self.win.destroy()
    
    def cancel_command(self):
        self.win.grab_release()
        self.win.destroy()
