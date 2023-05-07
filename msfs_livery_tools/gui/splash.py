import tkinter as tk
from tkinter import ttk
from pathlib import Path
import __main__

class Splash(object):
    win:tk.Toplevel
    frame:ttk.Frame
    splash_image:tk.PhotoImage
    splash_label:ttk.Label
    action_var:tk.StringVar
    action_label:ttk.Label
    progress_bar:ttk.Progressbar
    
    def __init__(self, master):
        self.win = tk.Toplevel(master, padx=0, pady=0)
        self.win.title = 'MSFS Livery Tools'
        self.win.iconbitmap(Path(__main__.RESOURCES_DIR, 'msfs livery tools.ico'))
        self.win.overrideredirect(True)
        
        # Layout
        self.frame = ttk.Frame(self.win, padding=0)
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.splash_image = tk.PhotoImage(file=__main__.RESOURCES_DIR / 'splash.png')
        self.splash_label = ttk.Label(self.frame, image=self.splash_image, padding=0)
        self.splash_label.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)
        self.action_var = tk.StringVar(self.frame, 'Loading MSFS Livery Tools…')
        self.action_label = ttk.Label(self.frame, textvariable=self.action_var)
        self.action_label.pack(fill=tk.X)
        self.progress_bar = ttk.Progressbar(self.frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X)
        
        # Positioning
        self.win.update()
        geometry, pos = self.win.geometry().split('+', 1)
        width, height = geometry.split('x')
        x = self.win.winfo_screenwidth() // 2 - int(width) // 2
        y = self.win.winfo_screenheight() // 2 - int(height) // 2
        self.win.geometry(f'{width}x{height}+{x}+{y}')
        self.progress_bar.start()
