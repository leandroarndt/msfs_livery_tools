"""Main application window"""
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from msfs_livery_tools.compression import dds
from msfs_livery_tools.package import panel_cfg
from . import styles

class MainWindow(object):
    win:tk.Tk
    
    # Toolbar
    toolbar_frame:ttk.Frame
    new_project_button:ttk.Button
    open_project_button:ttk.Button
    close_project_button:ttk.Button
    toolbar_separator:styles.Separator
    settings_button:ttk.Button
    
    # Project frame
    project_notebook:ttk.Notebook
    manifest_frame:ttk.Frame
    aircraft_frame:ttk.Frame
    panel_frame:ttk.Frame
    textures_frame:ttk.Frame
    
    # Actions frame
    actions_frame:ttk.Labelframe
    extract_textures_button:ttk.Button
    dds_json_button:ttk.Button
    texture_flags_button:ttk.Button
    aircraft_actions_separator:styles.Separator
    write_aircraft_button:ttk.Button
    panel_actions_separator:styles.Separator
    create_panel_button:ttk.Button
    copy_panel_button:ttk.Button
    registration_colors_button:ttk.Button
    package_actions_separator:styles.Separator
    crate_manifest_button:ttk.Button
    pack_livery_button:ttk.Button
    update_layout_button:ttk.Button
    
    def __init__(self):
        self.win = tk.Tk(className='MSFS Livery Tools')
        styles.init(self.win)
        
        # Toolbar
        self.toolbar_frame = ttk.Frame(self.win)
        self.toolbar_frame.pack(fill=tk.BOTH, anchor=tk.NW)
        self.new_project_button = ttk.Button(self.toolbar_frame, text='New Project')
        self.new_project_button.pack(side=tk.LEFT)
        self.open_project_button = ttk.Button(self.toolbar_frame, text='Open Project')
        self.open_project_button.pack(side=tk.LEFT)
        self.save_project_button = ttk.Button(self.toolbar_frame, text='Save project', state=tk.DISABLED)
        self.save_project_button.pack(side=tk.LEFT)
        self.toolbar_separator = styles.Separator(self.toolbar_frame, orient=tk.VERTICAL)
        self.toolbar_frame.pack(fill=tk.Y)
        self.settings_button = ttk.Button(self.toolbar_frame, text='Settings')
        self.settings_button.pack(side=tk.LEFT)
        
        # Project notebook
        self.project_notebook = ttk.Notebook(self.win)
        self.project_notebook.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.manifest_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.manifest_frame, text='Project')
        self.aircraft_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.aircraft_frame, text='Aircraft')
        self.panel_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.panel_frame, text='Panel')
        self.textures_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.textures_frame, text='Textures')
        
        # Action frame
        self.actions_frame = ttk.LabelFrame(self.win, text='Actions')
        self.actions_frame.pack(side=tk.RIGHT, expand=False, anchor=tk.N)
        #Texture section
        self.extract_textures_button = ttk.Button(self.actions_frame, text='Extract textures',
                                                    command=self.extract_textures, state=tk.DISABLED)
        self.extract_textures_button.pack(fill=tk.X)
        self.dds_json_button = ttk.Button(self.actions_frame, text='Create texture descriptors',
                                            command=self.dds_json, state=tk.DISABLED)
        self.dds_json_button.pack(fill=tk.X)
        self.texture_flags_button = ttk.Button(self.actions_frame, text='Create texture flags',
                                                command=self.create_flags, state=tk.DISABLED)
        self.texture_flags_button.pack(fill=tk.X)
        # Aircraft section
        self.aircraft_actions_separator = styles.Separator(self.actions_frame, orient=tk.HORIZONTAL)
        self.aircraft_actions_separator.pack(fill=tk.X)
        self.write_aircraft_button = ttk.Button(self.actions_frame, text='Write aircraft.cfg',
                                                command=self.write_aircraft_cfg, state=tk.DISABLED)
        self.write_aircraft_button.pack(fill=tk.X)
        # Panel section
        self.panel_actions_separator = styles.Separator(self.actions_frame, orient=tk.HORIZONTAL)
        self.panel_actions_separator.pack(fill=tk.X)
        self.create_panel_button = ttk.Button(self.actions_frame, text='Create blank panel.cfg',
                                                command=self.create_panel, state=tk.DISABLED)
        self.create_panel_button.pack(fill=tk.X)
        self.copy_panel_button = ttk.Button(self.actions_frame, text='Copy original panel.cfg',
                                                command=self.copy_panel, state=tk.DISABLED)
        self.copy_panel_button.pack(fill=tk.X)
        self.registration_colors_button = ttk.Button(self.actions_frame, text='Set registration colors',
                                                    command=self.set_registration_colors, state=tk.DISABLED)
        self.registration_colors_button.pack(fill=tk.X)
        # Package section
        self.package_actions_separator = styles.Separator(self.actions_frame, orient=tk.HORIZONTAL)
        self.package_actions_separator.pack(fill=tk.X)
        self.crate_manifest_button = ttk.Button(self.actions_frame, text='Create manifest.json',
                                                command=self.create_manifest_json, state=tk.DISABLED)
        self.crate_manifest_button.pack(fill=tk.X)
        self.pack_livery_button = ttk.Button(self.actions_frame, text='Pack livery',
                                                command=self.pack_livery, state=tk.DISABLED,
                                                style=styles.BOLD_BUTTON)
        self.pack_livery_button.pack(fill=tk.X)
        self.update_layout_button = ttk.Button(self.actions_frame, text='Update layout.json',
                                                    command=self.update_layout, state=tk.DISABLED)
        self.update_layout_button.pack(fill=tk.X)
    
    def extract_textures(self): # dds.from_gltf
        pass
    
    def dds_json(self): # package.dds_json.create_description
        pass
    
    def create_flags(self): # package.flags.create_flags
        pass
    
    def create_panel(self): # package.panel_cfg.create_empty
        pass
    
    def copy_panel(self): # package.panel_cfg.copy_original
        pass
    
    def set_registration_colors(self): # package.panel_cfg.set_registration_colors
        pass
    
    def write_aircraft_cfg(self): # package.aircraft_cfg.write_aircraft.cfg
        pass
    
    def create_manifest_json(self): # package.manifest.from_original
        pass
    
    def pack_livery(self): # Complex
        pass
    
    def update_layout(self): # package.layout.create_layout
        pass
