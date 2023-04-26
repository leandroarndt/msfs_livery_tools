"""Main application window"""
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from msfs_livery_tools.project import Project
from msfs_livery_tools.compression import dds
from msfs_livery_tools.package import panel_cfg
from . import styles, helpers

class MainWindow(object):
    project:Project
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
    # Project
    manifest_frame:ttk.Frame
    join_model_check_button:helpers.CheckButton
    origin_entry:helpers.FolderChooser
    title_entry:helpers.LabelEntry
    airplane_folder_entry:helpers.LabelEntry
    manufacturer_entry:helpers.LabelEntry
    creator_entry:helpers.LabelEntry
    version_entry:helpers.LabelEntry
    min_game_version:helpers.LabelEntry
    # Aircraft
    aircraft_frame:ttk.Frame
    # base_container_frame:helpers.FolderChooser
    suffix_entry:helpers.LabelEntry
    tail_number_entry:helpers.LabelEntry
    include_folders_label:ttk.Label
    model_check_button:helpers.CheckButton
    panel_check_button:helpers.CheckButton
    sound_check_button:helpers.CheckButton
    texture_check_button:helpers.CheckButton
    # Panel
    panel_frame:ttk.Frame
    font_color_entry:helpers.LabelEntry
    stroke_color_entry:helpers.LabelEntry
    stroke_size:helpers.LabelEntry
    # Textures
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
    manifest_actions_separator:styles.Separator
    crate_manifest_button:ttk.Button
    package_actions_separator:styles.Separator
    pack_livery_button:ttk.Button
    update_layout_button:ttk.Button
    
    def __init__(self):
        self.win = tk.Tk(className='MSFS Livery Tools')
        styles.init(self.win)
        
        # Toolbar
        self.toolbar_frame = ttk.Frame(self.win)
        self.toolbar_frame.pack(fill=tk.BOTH, anchor=tk.NW)
        self.new_project_button = ttk.Button(self.toolbar_frame, text='New Project', command=self.new_project)
        self.new_project_button.pack(side=tk.LEFT)
        self.open_project_button = ttk.Button(self.toolbar_frame, text='Open Project', command=self.open_project)
        self.open_project_button.pack(side=tk.LEFT)
        self.save_project_button = ttk.Button(self.toolbar_frame, text='Save project', command=self.save_project,
                                                state=tk.DISABLED)
        self.save_project_button.pack(side=tk.LEFT)
        self.toolbar_separator = styles.Separator(self.toolbar_frame, orient=tk.VERTICAL)
        self.toolbar_frame.pack(fill=tk.Y)
        self.settings_button = ttk.Button(self.toolbar_frame, text='Settings')
        self.settings_button.pack(side=tk.LEFT)
        
        # Project notebook
        self.project_notebook = ttk.Notebook(self.win)
        self.project_notebook.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor=tk.N)
        # Project
        self.manifest_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.manifest_frame, text='Project')
        self.join_model_check_button = helpers.CheckButton(self.manifest_frame, app=self,
                                                            property='join_model_and_textures',
                                                            text='Join model and textures',
                                                            default=True)
        self.join_model_check_button.pack(side=tk.TOP, fill=tk.X)
        self.origin_entry = helpers.FolderChooser(master=self.manifest_frame, app=self, title='Origin',
                                                    button_text='Choose…', button_command=self.choose_origin,
                                                    property='origin')
        self.origin_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.title_entry = helpers.LabelEntry(self.manifest_frame, label_text='Title: ', app=self, property='title')
        self.title_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.airplane_folder_entry = helpers.LabelEntry(self.manifest_frame, label_text='Airplane folder: ',
                                                        app=self, property='airplane_folder')
        self.airplane_folder_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.manufacturer_entry = helpers.LabelEntry(self.manifest_frame, label_text='Manufacturer: ',
                                                        app=self, property='manufacturer')
        self.manufacturer_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.creator_entry = helpers.LabelEntry(self.manifest_frame, label_text='Creator: ',
                                                app=self, property='creator')
        self.creator_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.version_entry = helpers.LabelEntry(self.manifest_frame, label_text='Version: ',
                                                app=self, property='version')
        self.version_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.min_game_version = helpers.LabelEntry(self.manifest_frame, label_text='Min. game version: ',
                                                    value='1.0.0', app=self, property='minimum_game_version')
        self.min_game_version.pack(side=tk.TOP, fill=tk.BOTH)
        # Aircraft
        self.aircraft_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.aircraft_frame, text='Aircraft')
        self.base_container_frame = helpers.FolderChooser(self.aircraft_frame, app=self, title='Base container',
                                                        button_command=self.choose_origin, button_text='Choose…',
                                                        property='base_container')
        self.base_container_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.suffix_entry = helpers.LabelEntry(self.aircraft_frame, label_text='Folder suffix: ',
                                                app=self, property='suffix')
        self.suffix_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.tail_number_entry = helpers.LabelEntry(self.aircraft_frame, label_text='Tail number: ', app=self,
                                                    property='tail_number')
        self.tail_number_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.include_folders_label = ttk.Label(self.aircraft_frame, text='Include the following folders:')
        self.include_folders_label.pack(side=tk.TOP, fill=tk.BOTH)
        self.model_check_button = helpers.CheckButton(self.aircraft_frame, app=self, property='include_model',
                                                        text='Model', state=tk.DISABLED)
        self.model_check_button.pack(side=tk.TOP, fill=tk.BOTH)
        self.panel_check_button = helpers.CheckButton(self.aircraft_frame, app=self, property='include_panel',
                                                        text='Panel', state=tk.DISABLED)
        self.panel_check_button.pack(side=tk.TOP, fill=tk.BOTH)
        self.sound_check_button = helpers.CheckButton(self.aircraft_frame, app=self, property='include_sound',
                                                        text='Sound', state=tk.DISABLED)
        self.sound_check_button.pack(side=tk.TOP, fill=tk.BOTH)
        self.texture_check_button = helpers.CheckButton(self.aircraft_frame, app=self, property='include_texture',
                                                        text='Texture',state=tk.DISABLED, default=True)
        self.texture_check_button.pack(side=tk.TOP, fill=tk.BOTH)
        self.panel_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.panel_frame, text='Registration number')
        self.font_color_entry = helpers.LabelEntry(self.panel_frame, label_text='Font color: ', app=self,
                                                    property='registration_font_color')
        self.font_color_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.stroke_color_entry = helpers.LabelEntry(self.panel_frame, label_text='Stroke color', app=self,
                                                        property='registration_stroke_color')
        self.stroke_color_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.stroke_size = helpers.LabelEntry(self.panel_frame, label_text='Stroke size', app=self,
                                                property='registration_stroke_size')
        self.stroke_size.pack(side=tk.TOP, fill=tk.BOTH)
        # Textures
        # self.textures_frame = ttk.Frame(self.project_notebook)
        # self.project_notebook.add(self.textures_frame, text='Textures')
        
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
        # Manifest section
        self.manifest_actions_separator = styles.Separator(self.actions_frame, orient=tk.HORIZONTAL)
        self.manifest_actions_separator.pack(fill=tk.X)
        self.crate_manifest_button = ttk.Button(self.actions_frame, text='Create manifest.json',
                                                command=self.create_manifest_json, state=tk.DISABLED)
        self.crate_manifest_button.pack(fill=tk.X)
        # Package section
        self.package_actions_separator = styles.Separator(self.actions_frame, orient=tk.HORIZONTAL)
        self.package_actions_separator.pack(fill=tk.X)
        self.pack_livery_button = ttk.Button(self.actions_frame, text='Pack livery',
                                                command=self.pack_livery, state=tk.DISABLED,
                                                style=styles.BOLD_BUTTON)
        self.pack_livery_button.pack(fill=tk.X)
        self.update_layout_button = ttk.Button(self.actions_frame, text='Update layout.json',
                                                    command=self.update_layout, state=tk.DISABLED)
        self.update_layout_button.pack(fill=tk.X)
    
    def enable_children(self, parent):
        for key, child in parent.children.items():
            if hasattr(child, 'state'):
                try:
                    child['state'] = tk.NORMAL
                except tk.TclError:
                    pass
            if hasattr(child, 'children'):
                self.enable_children(child)
    
    # Toolbar methods
    def new_project(self):
        path = filedialog.askdirectory(mustexist=False)
        if not path:
            return
        if Path(path, 'livery.ini').exists():
            if messagebox.askokcancel('Project exists!',
                f'Project "{Path(path, "livery.ini")}" already exists! Erase it?'):
                shutil.rmtree(path)
            else:
                return
        self.project = Project(path, self.join_model_var.get())
        self.enable_children(self.win)
    
    def open_project(self):
        path = filedialog.askdirectory(mustexist=True)
        if not path:
            return
        if not Path(path, 'livery.ini').is_file():
            if messagebox.askretrycancel('Project not found!',
                                    f'No project found at {path}!'):
                self.open_project()
            else:
                return
        self.project = Project(path)
        self.populate(self.win)
        self.enable_children(self.win)
    
    def populate(self, parent):
        for key, child in parent.children.items():
            if hasattr(child, 'load'):
                child.load()
            if hasattr(child, 'children'):
                self.populate(child)
    
    def save_project(self):
        self.project.save()
    
    # Project methods
    def choose_origin(self):
        folder = filedialog.askdirectory(mustexist=True)
        if Path(folder).is_dir():
            self.origin_entry.value.set(folder)
            self.origin_entry.update_project()
            self.origin_entry.load()
            self.base_container_frame.load()
    
    # Action methods
    
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
