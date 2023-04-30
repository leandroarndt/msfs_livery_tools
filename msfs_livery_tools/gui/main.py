"""Main application window"""
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import webbrowser
from msfs_livery_tools.project import Project
from msfs_livery_tools.compression import dds
from msfs_livery_tools.package import panel_cfg
from . import styles, helpers, settings, actions, about
import __main__

class MainWindow(object):
    project:Project
    win:tk.Tk
    agent:actions.Agent
    
    # Menu
    menu:tk.Menu
    file_menu:tk.Menu
    help_menu:tk.Menu
    
    # Toolbar
    toolbar_frame:ttk.Frame
    new_project_button:ttk.Button
    open_project_button:ttk.Button
    close_project_button:ttk.Button
    toolbar_separator:styles.Separator
    settings_button:ttk.Button
    
    # Main frame
    middle_frame:ttk.Frame
    
    # Project frame
    project_notebook:ttk.Notebook
    # Project
    manifest_frame:ttk.Frame
    join_model_check_button:helpers.CheckButton
    origin_entry:helpers.PathChooser
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
    compress_textures_button:ttk.Button
    dds_json_button:ttk.Button
    texture_flags_button:ttk.Button
    texture_cfg_button:ttk.Button
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
    
    # Progress bar
    bottom_frame:ttk.Frame
    progress_bar:ttk.Progressbar
    
    def __init__(self):
        self.win = tk.Tk(className='MSFS Livery Tools')
        styles.init(self.win)
        
        # Menu
        self.menu = tk.Menu(self.win)
        self.win.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.file_menu.add_command(label='New…', command=self.new_project, underline=0, accelerator='Ctrl+N')
        self.win.bind_all('<Control-n>', lambda event: self.new_project())
        self.file_menu.add_command(label='Open…', command=self.open_project, underline=0, accelerator='Ctrl+O')
        self.win.bind_all('<Control-o>', lambda event: self.open_project())
        self.file_menu.add_command(label='Save', command=self.save_project, underline=0, accelerator='Ctrl+S', state=tk.DISABLED)
        self.win.bind_all('<Control-s>', lambda event: self.save_project())
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.win.destroy, accelerator='Ctrl+Q')
        self.win.bind_all('<Control-q>', lambda event: self.win.destroy())
        self.menu.add_cascade(label='File', underline=0, menu=self.file_menu)
        self.menu.add_command(label='Settings', command=self.settings, underline=0)
        self.help_menu = tk.Menu(self.menu)
        self.help_menu.add_command(label='Manual',
            command = lambda: webbrowser.open('https://github.com/leandroarndt/msfs_livery_tools/wiki'),
            underline=0)
        self.help_menu.add_command(label='About', underline=0, command=self.about)
        self.help_menu.add_command(label='@fswt', underline=1,
                                    command=lambda: webbrowser.open(__main__.YOUTUBE))
        self.menu.add_cascade(label='Help', underline=0, menu=self.help_menu)
        
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
        self.settings_button = ttk.Button(self.toolbar_frame, text='Settings', command=self.settings)
        self.settings_button.pack(side=tk.LEFT)
        
        # Main Frame
        self.middle_frame = ttk.Frame(self.win)
        self.middle_frame.pack(fill=tk.BOTH)
        
        # Project notebook
        self.project_notebook = ttk.Notebook(self.middle_frame)
        self.project_notebook.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor=tk.N)
        # Project
        self.manifest_frame = ttk.Frame(self.project_notebook)
        self.project_notebook.add(self.manifest_frame, text='Project')
        self.join_model_check_button = helpers.CheckButton(self.manifest_frame, app=self,
                                                            property='join_model_and_textures',
                                                            text='Join model and textures',
                                                            default=True)
        self.join_model_check_button.pack(side=tk.TOP, fill=tk.X)
        self.origin_entry = helpers.PathChooser(master=self.manifest_frame, app=self, title='Origin',
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
        self.base_container_frame = helpers.PathChooser(self.aircraft_frame, app=self, title='Base container',
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
        self.actions_frame = ttk.LabelFrame(self.middle_frame, text='Actions')
        self.actions_frame.pack(side=tk.RIGHT, expand=False, anchor=tk.N)
        #Texture section
        self.extract_textures_button = ttk.Button(self.actions_frame, text='Extract textures',
                                                    command=self.extract_textures, state=tk.DISABLED)
        self.extract_textures_button.pack(fill=tk.X)
        self.compress_textures_button = ttk.Button(self.actions_frame, text='Compress textures',
                                                    command=self.compress_textures, state=tk.DISABLED)
        self.compress_textures_button.pack(fill=tk.X)
        self.dds_json_button = ttk.Button(self.actions_frame, text='Create texture descriptors',
                                            command=self.dds_json, state=tk.DISABLED)
        self.dds_json_button.pack(fill=tk.X)
        self.texture_cfg_button = ttk.Button(self.actions_frame, text='Create texture.cfg',
                                            command=self.create_texture_cfg, state=tk.DISABLED)
        self.texture_cfg_button.pack(fill=tk.X)
        # self.texture_flags_button = ttk.Button(self.actions_frame, text='Create texture flags',
        #                                         command=self.create_flags, state=tk.DISABLED)
        # self.texture_flags_button.pack(fill=tk.X)
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
        
        # Progress bar
        self.bottom_frame = ttk.Frame(self.win)
        self.bottom_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.progress_bar = ttk.Progressbar(self.bottom_frame, mode='determinate', orient=tk.HORIZONTAL,
                                            maximum=100, value=0)
        self.progress_bar.pack(fill=tk.X, side=tk.BOTTOM, anchor=tk.S)
        self.agent = actions.Agent(self.progress_bar)
    
    # Interface methods
    
    def set_children_state(self, parent, state:str=tk.NORMAL):
        for key, child in parent.children.items():
            if hasattr(child, 'state'):
                try:
                    child['state'] = state
                except tk.TclError:
                    pass
            if hasattr(child, 'children'):
                self.set_children_state(child)
    
    # Menu/Toolbar methods
    def new_project(self):
        path = filedialog.askdirectory(mustexist=False, title='Select project folder')
        if not path:
            return
        if Path(path, 'livery.ini').exists():
            if messagebox.askokcancel('Project exists!',
                f'Project "{Path(path, "livery.ini")}" already exists! Erase it?'):
                shutil.rmtree(path)
            else:
                return
        self.project = Project(path, self.join_model_check_button.value.get())
        self.set_children_state(self.win)
        self.file_menu.entryconfigure(3, state=tk.NORMAL)
        self.agent.project = self.project
    
    def open_project(self):
        path = filedialog.askdirectory(mustexist=True, title='Select project folder')
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
        self.set_children_state(self.win)
        self.file_menu.entryconfigure(3, state=tk.NORMAL)
        self.agent.project = self.project
    
    def populate(self, parent):
        for key, child in parent.children.items():
            if hasattr(child, 'load'):
                child.load()
            if hasattr(child, 'children'):
                self.populate(child)
    
    def save_project(self):
        self.project.save()
    
    def settings(self):
        settings_window = settings.SettingsWindow(self.win)
        settings_window.win.wait_window(settings_window.master)
    
    def about(self):
        about_window = about.About(self.win)
        about_window.win.wait_window(about_window.master)
    
    # Project methods
    def choose_origin(self):
        folder = filedialog.askdirectory(mustexist=True)
        if Path(folder).is_dir():
            self.origin_entry.value.set(folder)
            self.origin_entry.update_project()
            self.origin_entry.load()
            self.base_container_frame.load()
    
    # Action methods
    def wait_agent(self):
        if self.agent.running:
            self.win.after(100, self.wait_agent)
        else:
            self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def extract_textures(self):
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        path = filedialog.askopenfilename(defaultextension='*.gltf', filetypes=(
            ('glTF models', '*.gltf'),
        ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
        title='Choose glTF model to extract textures')
        if path:
            try:
                self.agent.extract_textures(path)
            except ValueError:
                messagebox.showerror(title='Error extracting textures',
                                    message=f'Could not extract textures from "{path}".')
        
        self.wait_agent()
    
    def compress_textures(self):
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        self.agent.compress_textures()
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def dds_json(self):
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        self.agent.create_dds_descriptors()
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def create_flags(self): # package.flags.create_flags
        pass
    
    def create_texture_cfg(self):
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        path = filedialog.askopenfilename(defaultextension='texture.cfg', filetypes=(
            ('Texture configuration', 'texture.cfg'),
        ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
        title='Choose original texture configuration file')
        if path:
            self.agent.create_texture_cfg(path)
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def write_aircraft_cfg(self): # package.aircraft_cfg.write_aircraft.cfg
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        if self.base_container_frame.value.get() == helpers.NOT_SET:
            path = filedialog.askopenfilename(defaultextension='aircraft.cfg', filetypes=(
                ('Aircraft configuration', 'aircraft.cfg'),
            ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
            title='Choose original aircraft configuration file')
            if not path:
                return
            self.agent.create_aircraft_cfg(path)
            self.origin_entry.load()
            self.base_container_frame.load()
        else:
            try:
                self.agent.create_aircraft_cfg()
            except actions.ConfigurationError as e:
                messagebox.showerror(title='Configuration error', message=str(e))
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def create_panel(self): # package.panel_cfg.create_empty
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        self.agent.create_empty_panel()
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def copy_panel(self): # package.panel_cfg.copy_original
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        path = filedialog.askopenfilename(defaultextension='panel.cfg', filetypes=(
            ('Panel configuration', 'panel.cfg'),
        ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
        title='Choose original panel configuration file')
        self.agent.copy_panel(path)
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def set_registration_colors(self): # package.panel_cfg.set_registration_colors
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        try:
            self.agent.set_registration_colors()
        except actions.ConfigurationError as e:
            messagebox.showerror('Configuration error', str(e))
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def create_manifest_json(self): # package.manifest.from_original
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        if self.base_container_frame.value.get() == helpers.NOT_SET:
            path = filedialog.askopenfilename(defaultextension='manifest.json', filetypes=(
                ('Manifest files', 'manifest.json'),
            ), initialdir=Path(self.origin_entry.value.get()),
            title='Choose original aircraft manifest file')
            if not path:
                self.set_children_state(self.actions_frame, tk.NORMAL)
                return
            self.agent.create_manifest(path)
            self.origin_entry.load()
            self.base_container_frame.load()
        else:
            try:
                self.agent.create_manifest()
            except actions.ConfigurationError as e:
                messagebox.showerror(title='Configuration error', message=str(e))
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
    
    def pack_livery(self): # Complex
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        path = filedialog.askdirectory(mustexist=True, title='Choose package folder')
        if not path:
            self.set_children_state(self.actions_frame, tk.NORMAL)
            return
        self.agent.package(path)
        
        self.wait_agent()
        
        if self.agent.error:
            messagebox.showerror(title='Configuration error', message=str(self.agent.error))
        self.agent.error = None
    
    def update_layout(self): # package.layout.create_layout
        self.set_children_state(self.actions_frame, tk.DISABLED)
        self.win.update()
        
        path = filedialog.askopenfilename(defaultextension='layout.json', filetypes=(
            ('Package layout', 'layout.json'),
        ), title='Choose layout file to update')
        if not path:
            return
        self.agent.update_layout(path)
        
        self.set_children_state(self.actions_frame, tk.NORMAL)
