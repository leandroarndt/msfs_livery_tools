import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.gui import helpers
import __main__

class SettingsWindow(object):
    win:tk.Tk
    settings:AppSettings
    project:AppSettings # This name is used by GUI helpers
    settings_frame:ttk.Frame
    buttons_frame:ttk.Frame
    compress_on_build_var:tk.BooleanVar
    compress_on_build_button:ttk.Checkbutton
    texconv_frame:helpers.PathChooser
    download_texconv_button:ttk.Button
    ok_button:ttk.Button
    cancel_button:ttk.Button
    
    def __init__(self, master:tk.Tk):
        self.master = master
        self.win = tk.Toplevel(self.master)
        self.win.transient(self.master)
        self.win.title('MSFS Livery Tools settings')
        self.win.iconbitmap(Path(__main__.RESOURCES_DIR, 'msfs livery tools.ico'))
        self.settings = AppSettings()
        self.project = self.settings
        self.settings_frame = ttk.Frame(self.win)
        self.settings_frame.pack(padx=5, pady=5, fill=tk.X)
        self.compress_on_build_var = tk.BooleanVar(self.win, value=self.settings.compress_textures_on_build)
        self.compress_on_build_button = ttk.Checkbutton(self.settings_frame, command=self.set_compress_on_build,
                                                        text='Compress new or modified textures on build',
                                                        variable=self.compress_on_build_var)
        self.compress_on_build_button.pack(side=tk.TOP, fill=tk.X)
        self.texconv_frame = helpers.PathChooser(self.settings_frame, self,
                                                property='texconv_path',
                                                button_command=self.choose_texconv_path,
                                                title='Texconv.exe path', state=tk.NORMAL)
        self.texconv_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=5)
        self.texconv_frame.load()
        self.buttons_frame = ttk.Frame(self.win)
        self.buttons_frame.pack(padx=5, pady=5, fill=tk.X)
        self.ok_button = ttk.Button(self.buttons_frame, command=self.ok_command, text='Ok')
        self.ok_button.pack(side=tk.RIGHT)
        self.cancel_button = ttk.Button(self.buttons_frame, command=self.cancel_command, text='Cancel')
        self.cancel_button.pack(side=tk.RIGHT)
        self.download_texconv_button = ttk.Button(self.buttons_frame, command=self.download_texconv,
                                                text='Download texconv')
        self.download_texconv_button.pack(side=tk.LEFT)
        self.win.grab_set()
    
    def set_compress_on_build(self):
        self.settings.compress_textures_on_build = self.compress_on_build_var.get()
    
    def choose_texconv_path(self):
        path = filedialog.askopenfilename(title='Select textconv.exe path', filetypes=(
                                                ('Texconv executable', 'texconv.exe'),
                                            ))
        if Path(path).is_file():
            self.texconv_frame.value.set(path)
    
    def download_texconv(self):
        webbrowser.open(helpers.TEXCONV_URL)
    
    def ok_command(self):
        self.settings.texconv_path = self.texconv_frame.value.get()
        self.settings.save()
        self.win.grab_release()
        self.win.destroy()
    
    def cancel_command(self):
        self.win.grab_release()
        self.win.destroy()
