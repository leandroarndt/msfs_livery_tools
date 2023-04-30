import webbrowser
import tkinter as tk
from tkinter import ttk
from pathlib import PureWindowsPath
from . import styles
import __main__

class About(object):
    win:tk.Tk
    header_image:tk.PhotoImage
    master:object
    header_image:tk.PhotoImage
    header_label:ttk.Label
    about_label:ttk.Label
    copyright_title:ttk.Label
    copyright_message:ttk.Label
    button_frame:ttk.Frame
    url_button:ttk.Button
    youtube_button:ttk.Button
    close_button:ttk.Button
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        self.win = tk.Toplevel(self.master)
        self.win.title('About MSFS Livery Tools')
        self.win.resizable(False, False)
        self.header_image = tk.PhotoImage(file=PureWindowsPath(__main__.RESOURCES_DIR, 'header.png'))
        self.header_label = ttk.Label(self.win, image=self.header_image)
        self.header_label.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.about_label = ttk.Label(self.win, text=__main__.ABOUT)
        self.about_label.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.copyright_title = ttk.Label(self.win, text='Use, modification and distribution terms',
                                        style=styles.HEADING)
        self.copyright_title.pack(side=tk.TOP)
        self.copyright_message = ttk.Label(self.win, text=__main__.COPYRIGHT)
        self.copyright_message.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.button_frame = ttk.Frame(self.win, padding=5)
        self.button_frame.pack(side=tk.TOP)
        self.url_button = ttk.Button(self.button_frame, text='Open website', command=lambda: webbrowser.open(__main__.URL))
        self.url_button.pack(side=tk.LEFT)
        self.youtube_button = ttk.Button(self.button_frame, text="Open author's YouTube channel",
                                        command=lambda: webbrowser.open(__main__.YOUTUBE),
                                        style=styles.BOLD_BUTTON)
        self.youtube_button.pack(side=tk.LEFT)
        self.close_button = ttk.Button(self.button_frame, command=lambda: self.win.destroy(), text='Close')
        self.close_button.pack(side=tk.RIGHT)
        self.win.grab_set()