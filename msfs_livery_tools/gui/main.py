"""Main application window"""
from tkinter import *
from tkinter import ttk
from ..settings import AppSettings

class MainWindow(object):
    win:Tk
    
    # Toolbar
    toolbar_frame:ttk.Frame
    new_project_button:ttk.Button
    open_project_button:ttk.Button
    close_project_button:ttk.Button
    toolbar_separator:ttk.Separator
    settings_button:ttk.Button
    
    # Project frame
    project_notebook:ttk.Notebook
    manifest_frame:ttk.Frame
    aircraft_frame:ttk.Frame
    panel_frame:ttk.Frame
    textures_frame:ttk.Frame
    
    # Actions frame
    actions_frame:ttk.Labelframe
    copy_textures_button:ttk.Button
    
    def __init__(self):
        self.win = Tk(className='MSFS Livery Tools')
        
        # Toolbar
        self.toolbar_frame = ttk.Frame(self.win)
        self.toolbar_frame.pack(fill=BOTH, anchor=NW)
        self.new_project_button = ttk.Button(self.toolbar_frame, text='New Project')
        self.new_project_button.pack(side=LEFT)
        self.open_project_button = ttk.Button(self.toolbar_frame, text='Open Project')
        self.open_project_button.pack(side=LEFT)
        self.close_project_button = ttk.Button(self.toolbar_frame, text='Close project', state=DISABLED)
        self.close_project_button.pack(side=LEFT)
        self.toolbar_separator = ttk.Separator(self.toolbar_frame, orient=VERTICAL)
        self.toolbar_frame.pack(fill=Y)
        self.settings_button = ttk.Button(self.toolbar_frame, text='Settings')
        self.settings_button.pack(side=LEFT)
        
        # Project notebook
        self.project_notebook = ttk.Notebook(self.win)
        self.project_notebook.pack(side=LEFT, expand=True, fill=BOTH)
        self.manifest_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.manifest_frame, text='Project manifest')
        self.aircraft_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.aircraft_frame, text='Aircraft')
        self.panel_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.panel_frame, text='Panel')
        self.textures_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.textures_frame, text='Textures')
        
        # Action frame
        self.actions_frame = ttk.LabelFrame(self.win, text='Actions')
        self.actions_frame.pack(side=RIGHT, expand=False, anchor=N)
        self.copy_textures_button = ttk.Button(self.actions_frame, text='Copy textures', state=DISABLED)
        self.copy_textures_button.pack(expand=True)
