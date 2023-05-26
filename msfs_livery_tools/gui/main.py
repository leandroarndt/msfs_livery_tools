"""Main application window"""
import shutil, time, threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from idlelib.tooltip import Hovertip
from pathlib import Path, PureWindowsPath
from queue import Queue, Empty
import webbrowser
from msfs_livery_tools.project import Project
from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.package import panel_cfg
from msfs_livery_tools.vfs import VFS
from msfs_livery_tools.gltf import uv_map
from . import styles, helpers, settings, actions, about, splash, package_scanner
import __main__

def needs_texconv(func):
    def wrapper(*args, **kwargs):
        texconv = Path(AppSettings().texconv_path)
        if not texconv:
            messagebox.showerror(title='Texconv path not set',
                message='"Texconv.exe" path has not been set. Please inform it at "Edit"->"Settings".')
            return
        if not texconv.is_file():
            messagebox.showerror(title='Texconv not found',
                message=f'"Texconv.exe" could not be found at "{texconv}". Please correct it at application settings.')
            return
        return func(*args, **kwargs)
    return wrapper

class MainWindow(object):
    project:Project = None
    app_settings:AppSettings
    project_modified:bool = False
    vfs:VFS
    vfs_queue:Queue
    gui_disabled:bool = False
    
    # Main window
    win:tk.Tk
    agent:actions.Agent
    
    # Menu
    menu:tk.Menu
    file_menu:tk.Menu
    recent_menu:tk.Menu
    edit_menu:tk.Menu
    tools_menu:tk.Menu
    help_menu:tk.Menu
    
    # Toolbar
    toolbar_frame:ttk.Frame
    new_project_image:tk.PhotoImage
    new_project_button:ttk.Button
    new_project_tip:Hovertip
    open_project_image:tk.PhotoImage
    open_project_button:ttk.Button
    open_project_tip:Hovertip
    save_project_image:tk.PhotoImage
    save_project_button:ttk.Button
    save_project_tip:Hovertip
    toolbar_separator:styles.Separator
    settings_image:tk.PhotoImage
    settings_button:ttk.Button
    settings_tip:Hovertip
    
    # Main frame
    middle_frame:ttk.Frame
    
    # Project frame
    project_notebook:ttk.Notebook
    # Project
    manifest_frame:ttk.Frame
    join_model_check_button:helpers.CheckButton
    origin_entry:helpers.PathChooser
    title_entry:helpers.LabelEntry
    display_name_entry:helpers.LabelEntry
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
    convert_dds_file_button:ttk.Button
    compress_textures_button:ttk.Button
    dds_json_button:ttk.Button
    texture_flags_button:ttk.Button
    texture_cfg_button:ttk.Button
    thumbnail_separator:styles.Separator
    thumbnail_placeholder_button:ttk.Button
    thumbnail_resize_button:ttk.Button
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
    progress_text:tk.StringVar
    progress_label:ttk.Label
    
    def __init__(self):
        self.app_settings = AppSettings()
        self.project_modified = False
        
        # Main window
        self.win = tk.Tk()
        self.win.withdraw()
        styles.init(self.win)
        self.set_title()
        self.win.iconbitmap(Path(__main__.RESOURCES_DIR, 'msfs livery tools.ico'))
        self.win.protocol('WM_DELETE_WINDOW', self.on_close)
        
        # Splash Screen
        splash_window = splash.Splash(self.win)
        
        # Load packages onto VFS
        self.vfs_queue = Queue()
        scanner = package_scanner.Scanner(self, self.vfs_queue, splash_window)
        scanner.start()
        
        # Menu
        self.menu = tk.Menu(self.win)
        self.win.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='New…', command=self.new_project, underline=0, accelerator='Ctrl+N')
        self.win.bind_all('<Control-n>', lambda event: self.new_project())
        self.file_menu.add_command(label='Open…', command=self.open_project, underline=0, accelerator='Ctrl+O')
        self.win.bind_all('<Control-o>', lambda event: self.open_project())
        self.file_menu.add_command(label='Save', command=self.save_project, underline=0, accelerator='Ctrl+S', state=tk.DISABLED)
        self.win.bind_all('<Control-s>', lambda event: self.save_project())
        self.recent_menu = self.build_recent_menu()
        self.file_menu.add_cascade(label='Open recent', underline=5, menu=self.recent_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.on_close, accelerator='Ctrl+Q')
        self.win.bind_all('<Control-q>', self.on_close)
        self.menu.add_cascade(label='File', underline=0, menu=self.file_menu)
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label='Settings', command=self.settings, underline=0)
        self.edit_menu.add_command(label='Reload MSFS packages', command=self.reload_vfs, underline=0)
        self.menu.add_cascade(label='Edit', underline=0, menu=self.edit_menu)
        self.tools_menu = tk.Menu(self.menu, tearoff=0)
        self.tools_menu.add_command(label='Create texture UV map…', command=self.create_uv_map, underline=15)
        self.menu.add_cascade(label='Tools', underline=0, menu=self.tools_menu)
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label='Online manual',
            command = lambda: webbrowser.open('https://github.com/leandroarndt/msfs_livery_tools/wiki'),
            underline=7)
        self.help_menu.add_command(label='About', underline=0, command=self.about)
        self.help_menu.add_command(label='@fswt', underline=1,
                                    command=lambda: webbrowser.open(__main__.YOUTUBE))
        self.help_menu.add_separator()
        self.help_menu.add_command(label='Download texconv', underline=9,
                                    command=lambda: webbrowser.open(helpers.TEXCONV_URL))
        self.menu.add_cascade(label='Help', underline=0, menu=self.help_menu)
        
        # Toolbar
        self.toolbar_frame = ttk.Frame(self.win)
        self.toolbar_frame.pack(fill=tk.BOTH, anchor=tk.NW)
        self.new_project_image = tk.PhotoImage(file=__main__.RESOURCES_DIR / 'button_New project.png')
        self.new_project_button = ttk.Button(self.toolbar_frame, image=self.new_project_image,
                                            command=self.new_project)
        self.new_project_button.pack(side=tk.LEFT)
        self.new_project_tip = Hovertip(self.new_project_button, 'New project', 500)
        self.open_project_image = tk.PhotoImage(file=__main__.RESOURCES_DIR / 'button_Open project.png')
        self.open_project_button = ttk.Button(self.toolbar_frame, image=self.open_project_image,
                                            command=self.open_project)
        self.open_project_button.pack(side=tk.LEFT)
        self.open_project_tip = Hovertip(self.open_project_button, 'Open project', 500)
        self.save_project_image =tk.PhotoImage(file=__main__.RESOURCES_DIR / 'button_Save project.png')
        self.save_project_button = ttk.Button(self.toolbar_frame, image=self.save_project_image,
                                                command=self.save_project,
                                                state=tk.DISABLED)
        self.save_project_button.pack(side=tk.LEFT)
        self.save_project_tip = Hovertip(self.save_project_button, 'Save project', 500)
        self.toolbar_separator = styles.Separator(self.toolbar_frame, orient=tk.VERTICAL)
        self.toolbar_frame.pack(fill=tk.Y)
        self.settings_image = tk.PhotoImage(file=__main__.RESOURCES_DIR / 'button_Settings.png')
        self.settings_button = ttk.Button(self.toolbar_frame, image=self.settings_image,
                                            command=self.settings)
        self.settings_button.pack(side=tk.LEFT)
        self.settings_tip = Hovertip(self.settings_button, 'Application settings', 500)
        
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
                                                            default=False)
        self.join_model_check_button.pack(side=tk.TOP, fill=tk.X)
        self.origin_entry = helpers.PathChooser(master=self.manifest_frame, app=self, title='Origin',
                                                    button_text='Choose…', button_command=self.choose_origin,
                                                    property='origin')
        self.origin_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.title_entry = helpers.LabelEntry(self.manifest_frame, label_text='Title: ',
                                                app=self, property='title')
        self.title_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.display_name_entry = helpers.LabelEntry(self.manifest_frame, label_text='Display name: ',
                                                    app=self, property='display_name')
        self.display_name_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.airplane_folder_entry = helpers.LabelEntry(self.manifest_frame, label_text='Airplane folder (unique): ',
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
                                                        button_command=self.choose_base_container, button_text='Choose…',
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
        self.convert_dds_file_button = ttk.Button(self.actions_frame, text='Convert DDS file',
                                                    command=self.convert_dds_file, state=tk.DISABLED)
        self.convert_dds_file_button.pack(fill=tk.X)
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
        # Thumbnails section
        self.thumbnail_separator = styles.Separator(self.actions_frame, orient=tk.HORIZONTAL)
        self.thumbnail_separator.pack(fill=tk.X)
        self.thumbnail_placeholder_button = ttk.Button(self.actions_frame, text='Add placeholder thumbnail',
                                                    command=lambda: self.agent.copy_thumbnail_placeholder(),
                                                    state=tk.DISABLED)
        self.thumbnail_placeholder_button.pack(fill=tk.X)
        self.thumbnail_resize_button = ttk.Button(self.actions_frame, text='Resize thumbnail',
                                                    command=lambda: self.agent.resize_thumbnail(),
                                                    state=tk.DISABLED)
        self.thumbnail_resize_button.pack(fill=tk.X)
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
                                                    command=self.update_layout, state=tk.NORMAL)
        self.update_layout_button.pack(fill=tk.X)
        
        # Progress bar
        self.bottom_frame = ttk.Frame(self.win)
        self.bottom_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.progress_bar = ttk.Progressbar(self.bottom_frame, mode='determinate', orient=tk.HORIZONTAL,
                                            maximum=100, value=0)
        self.progress_bar.pack(fill=tk.X, side=tk.BOTTOM, anchor=tk.S)
        self.agent = actions.Agent(self.progress_bar)
        self.progress_text = tk.StringVar(self.win, '')
        # Not packed until used
        self.progress_label = ttk.Label(self.bottom_frame, textvariable=self.progress_text)
        
        # Close splash window
        while self.monitor_scanner(scanner, splash_window):
            time.sleep(1/30)
        splash_window.win.destroy()
        self.win.deiconify()
    
    # Monitor VFS scanner
    def monitor_scanner(self, scanner:package_scanner.Scanner, splash_window:splash.Splash|None=None):
        if scanner.is_alive():
            if not splash_window:
                if self.progress_bar['mode'] != 'indeterminate':
                    self.progress_bar.config(mode='indeterminate')
                    self.progress_bar.start()
                    self.progress_label.pack(fill=tk.X)
            
            current = ''
            try:
                current = self.vfs_queue.get(block=False)
                if splash_window and current:
                    splash_window.action_var.set(current)
                elif current:
                    self.progress_text.set(current)
            except Empty:
                pass
            
            if splash_window:
                splash_window.win.update()
            else:
                self.win.update()
            return True
        else:
            if splash_window:
                splash_window.win.destroy()
            else:
                self.progress_text.set('')
                self.progress_label.pack_forget()
                self.progress_bar.stop()
                self.progress_bar['mode'] = 'determinate'
        return False
    
    # Interface methods
    
    def set_title(self):
        if self.project is None:
            self.win.title('MSFS Livery Tools')
        else:
            self.win.title(f'MSFS Livery Tools - {Path(self.project.file).parent.name}')
    
    def set_children_state(self, parent, state:str=tk.NORMAL):
        for key, child in parent.children.items():
            if hasattr(child, 'state'):
                try:
                    child['state'] = state
                except tk.TclError:
                    pass
            if hasattr(child, 'children'):
                self.set_children_state(child, state)
        if parent == self.win:
            if state == tk.NORMAL:
                self.gui_disabled = False
                self.menu.entryconfig(0, state=tk.NORMAL)
                self.menu.entryconfig(1, state=tk.NORMAL)
                self.menu.entryconfig(2, state=tk.NORMAL)
                if not self.project_modified:
                    self.file_menu.entryconfig(2, state=tk.DISABLED)
                    self.save_project_button.config(state=tk.DISABLED)
            elif state == tk.DISABLED:
                self.gui_disabled = True
                self.menu.entryconfig(0, state=tk.DISABLED)
                self.menu.entryconfig(1, state=tk.DISABLED)
                self.menu.entryconfig(2, state=tk.DISABLED)
            self.win.update()
    
    # Menu/Toolbar methods
    def new_project(self):
        if self.gui_disabled:
            return
        path = filedialog.askdirectory(mustexist=False, title='Select project folder')
        if not path:
            return
        
        if self.project_modified:
            answer = messagebox.askyesnocancel('New project', 'Save current project before creating another one?')
            if answer:
                self.save_project()
            elif answer is None:
                return
        
        if Path(path, 'livery.ini').exists():
            if messagebox.askokcancel('Project exists!',
                f'Project "{Path(path, "livery.ini")}" already exists! Erase it?'):
                shutil.rmtree(path)
            else:
                return
        
        try:
            self.project.close() # Deletes the old project's dicionary entry at Project class
        except AttributeError: # There is no open project
            pass
        self.project = Project(path, self.join_model_check_button.value.get())
        self.set_children_state(self.win, tk.NORMAL)
        self.project_modified = False
        self.agent.project = self.project
        self.set_title()
        
        # Rebuild recent files menu
        self.app_settings.recent_files = path
        self.app_settings.save()
        self.recent_menu = self.build_recent_menu()
        self.file_menu.entryconfigure(3, menu=self.recent_menu)
        self.file_menu.entryconfig(3, state=tk.NORMAL)
        
        # Reset entries
        self.populate(self.project_notebook)
    
    def open_project(self, path:str|None=None):
        if self.gui_disabled:
            return
        if not path:
            path = filedialog.askdirectory(mustexist=True, title='Select project folder')
            if not path:
                return
            if not Path(path, 'livery.ini').is_file():
                if messagebox.askretrycancel('Project not found!',
                                        f'No project found at {path}!'):
                    self.open_project()
                else:
                    return
        
        if self.project_modified:
            answer = messagebox.askyesnocancel('Open project', 'Save current project before opening another one?')
            if answer:
                self.save_project()
            elif answer is None:
                return
        
        try:
            self.project.close() # Deletes the old project's dicionary entry at Project class
        except AttributeError: # There is no open project
            pass
        self.project = Project(path)
        self.populate(self.project_notebook)
        self.set_children_state(self.win, tk.NORMAL)
        self.project_modified = False
        self.agent.project = self.project
        
        # Rebuild recent files menu
        self.app_settings.recent_files = path
        self.app_settings.save()
        self.recent_menu = self.build_recent_menu()
        self.file_menu.entryconfigure(3, menu=self.recent_menu)
        self.file_menu.entryconfig(3, state=tk.NORMAL)
        self.set_title()
    
    def populate(self, parent):
        for child in parent.children.values():
            if hasattr(child, 'load'):
                child.load()
            if hasattr(child, 'children'):
                self.populate(child)
    
    def save_project(self):
        if self.gui_disabled:
            return
        self.project.save()
        self.project_modified = False
        self.save_project_button.config(state=tk.DISABLED)
        self.file_menu.entryconfigure(2, state=tk.DISABLED)
    
    def create_opener(self, file):
        return lambda: self.open_project(file)
    
    def build_recent_menu(self)->tk.Menu:
        menu = tk.Menu(self.file_menu)
        recent = self.app_settings.recent_files
        if len(recent) == 0:
            menu.add_command(label='(Empty)', state=tk.DISABLED)
            self.file_menu.entryconfigure(2, state=tk.DISABLED)
            return menu
        n = 0
        for file in recent:
            n += 1
            menu.add_command(label=f'{n} {PureWindowsPath(file)}', underline=0,
                            command=self.create_opener(file))
        return menu
    
    def settings(self):
        settings_window = settings.SettingsWindow(self.win)
        settings_window.win.wait_window(settings_window.master)
    
    def reload_vfs(self):
        self.set_children_state(self.win, state=tk.DISABLED)
        self.progress_label.config(state=tk.NORMAL)
        self.progress_text.set('Reloading MSFS packages…')
        scanner = package_scanner.Scanner(self, self.vfs_queue, new_vfs=False)
        scanner.start()
        
        while self.monitor_scanner(scanner):
            time.sleep(1/30)
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def create_uv_map(self):
        self.set_children_state(self.win, state=tk.DISABLED)
        
        dest = filedialog.askdirectory(mustexist=True, title='Choose texture map destination path')
        if not dest:
            return
        texture_file = filedialog.askopenfilename(defaultextension='*.DDS *.png', filetypes=(
            ('Texture files', '*.DDS *.png'),
            ('Compressed texture', '*.DDS'),
            ('PNG image', '*.png'),
        ), title='Choose texture file')
        if not texture_file:
            return
        model_file = filedialog.askopenfilename(defaultextension='*.gltf', filetypes=(
            ('glTF model', '*.gltf'),
        ), title='Choose model file')
        if not model_file:
            return
        
        self.progress_bar['mode'] = 'indeterminate'
        self.progress_bar.start(30 // 1000)
        thread = threading.Thread(target=uv_map.draw_uv_layers_for_texture, kwargs={
            'dest': dest,
            'texture_file': texture_file,
            'model_file': model_file,
        })
        thread.start()
        while thread.is_alive():
            # For some reason, update() freezes and update_idletasks() does not work
            # self.win.update_idletasks()
            # self.progress_bar.update_idletasks()
            time.sleep(1/30)
        self.progress_bar.stop()
        self.progress_bar['mode'] = 'determinate'
        
        if messagebox.askyesno(
            title='Done creating UV maps',
            message='Texture maps created. Open destination folder?'
        ):
            webbrowser.open('file:///' + dest)
        
        self.set_children_state(self.win, tk.NORMAL)
    
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
    
    def choose_base_container(self):
        folder = filedialog.askdirectory(mustexist=True)
        if Path(folder).is_dir():
            self.base_container_frame.value.set(folder)
            self.base_container_frame.update_project()
            self.base_container_frame.load()
            self.origin_entry.load()
    
    # Action methods
    def wait_agent(self):
        if self.agent.running:
            self.win.after(100, self.wait_agent)
        else:
            self.set_children_state(self.win, tk.NORMAL)
    
    @needs_texconv
    def extract_textures(self):
        self.set_children_state(self.win, tk.DISABLED)
        
        path = filedialog.askopenfilename(defaultextension='*.gltf', filetypes=(
            ('glTF models', '*.gltf'),
        ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
        title='Choose glTF model to extract textures')
        if path:
            try:
                self.agent.extract_textures(path, self.vfs)
            except ValueError:
                messagebox.showerror(title='Error extracting textures',
                                    message=f'Could not extract textures from "{path}".')
        
        self.wait_agent()
    
    @needs_texconv
    def convert_dds_file(self):
        self.set_children_state(self.win, tk.DISABLED)
        
        path = filedialog.askopenfilenames(defaultextension='*.dds', filetypes=(
            ('DDS texture', '*.dds'),
        ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
        title='Choose DDS file to extract')
        if  path:
            for file in path:
                try:
                    self.agent.convert_dds_file(file)
                except FileNotFoundError:
                    messagebox.showerror(title='File not found',
                                        message=f'Could not find file "{Path(file).name}".')
                except Exception as e:
                    messagebox.showerror(title='Could not convert DDS file',
                                        message=f'Could not extract "{Path(file).name}": "{str(e)}"')
        
        self.set_children_state(self.win, tk.NORMAL)
    
    @needs_texconv
    def compress_textures(self):
        self.set_children_state(self.win, tk.DISABLED)
        
        self.agent.compress_textures()
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def dds_json(self):
        self.set_children_state(self.win, tk.DISABLED)
        
        self.agent.create_dds_descriptors()
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def create_flags(self): # package.flags.create_flags
        pass
    
    def create_texture_cfg(self):
        self.set_children_state(self.win, tk.DISABLED)
        
        path = filedialog.askopenfilename(defaultextension='texture.cfg', filetypes=(
            ('Texture configuration', 'texture.cfg'),
        ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
        title='Choose original texture configuration file')
        if path:
            self.agent.create_texture_cfg(path)
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def write_aircraft_cfg(self): # package.aircraft_cfg.write_aircraft.cfg
        self.set_children_state(self.win, tk.DISABLED)
        
        if self.base_container_frame.value.get() == helpers.NOT_SET:
            path = filedialog.askopenfilename(defaultextension='aircraft.cfg', filetypes=(
                ('Aircraft configuration', 'aircraft.cfg'),
            ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
            title='Choose original aircraft configuration file')
            if not path:
                self.set_children_state(self.win, tk.NORMAL)
                return
            self.agent.create_aircraft_cfg(path)
            self.origin_entry.load()
            self.base_container_frame.load()
        else:
            try:
                self.agent.create_aircraft_cfg()
            except actions.ConfigurationError as e:
                messagebox.showerror(title='Configuration error', message=str(e))
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def create_panel(self): # package.panel_cfg.create_empty
        self.set_children_state(self.win, tk.DISABLED)
        self.win.update()
        
        self.agent.create_empty_panel()
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def copy_panel(self): # package.panel_cfg.copy_original
        self.set_children_state(self.win, tk.DISABLED)
        
        path = filedialog.askopenfilename(defaultextension='panel.cfg', filetypes=(
            ('Panel configuration', 'panel.cfg'),
        ), initialdir=Path(self.origin_entry.value.get(), 'SimObjects', 'Airplanes', self.base_container_frame.value.get()[3:]),
        title='Choose original panel configuration file')
        if path:
            self.agent.copy_panel(path)
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def set_registration_colors(self): # package.panel_cfg.set_registration_colors
        self.set_children_state(self.win, tk.DISABLED)
        
        try:
            self.agent.set_registration_colors()
        except actions.ConfigurationError as e:
            messagebox.showerror('Configuration error', str(e))
        except panel_cfg.RegistrationWarning as e:
            messagebox.showwarning('Review "panel.cfg"!', str(e))
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def create_manifest_json(self): # package.manifest.from_original
        self.set_children_state(self.win, tk.DISABLED)
        
        if self.base_container_frame.value.get() == helpers.NOT_SET:
            path = filedialog.askopenfilename(defaultextension='manifest.json', filetypes=(
                ('Manifest files', 'manifest.json'),
            ), initialdir=Path(self.origin_entry.value.get()),
            title='Choose original aircraft manifest file')
            if not path:
                self.set_children_state(self.win, tk.NORMAL)
                return
            self.agent.create_manifest(path)
            self.origin_entry.load()
            self.base_container_frame.load()
        else:
            try:
                self.agent.create_manifest()
            except actions.ConfigurationError as e:
                messagebox.showerror(title='Configuration error', message=str(e))
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def pack_livery(self): # Complex
        if not self.app_settings.texconv_path:
            proceed = messagebox.askokcancel(title='Texconv path not configured',
                message='Path to "texconv.exe" was not set. You won\'t be able to compress textures to DDS. Proceed?')
            if not proceed:
                return
        elif not Path(self.app_settings.texconv_path).is_file():
            proceed = messagebox.askokcancel(title='Texconv path improperly configured',
                message=f'"Texconv.exe" could not be found at "{self.app_settings.texconv_path}". You won\'t be able to compress textures to DDS. Proceed?')
            if not proceed:
                return
        
        try:
            self.project.airplane_folder
        except KeyError:
            messagebox.showerror(title='Airplane folder not set',
                message='Please, configure an airplane folder before proceeding.')
            return
        
        # Prepare window
        self.set_children_state(self.win, tk.DISABLED)
        
        # Ask path
        path = filedialog.askdirectory(mustexist=False, title='Choose package folder')
        if not path:
            self.set_children_state(self.win, tk.NORMAL)
            return
        
        # Tries to discover if there will be airplane folder overlap
        try:
            if self.project.airplane_folder in self.vfs['simobjects']['airplanes']:
                if not str(self.vfs['simobjects']['airplanes'][self.project.airplane_folder.lower()]['aircraft.cfg']\
                    .real_path()).startswith(str(PureWindowsPath(path))):
                        if not messagebox.askokcancel('WARNING', f'Airplane folder \
{self.project.airplane_folder} conflicts with existing package at "\
{self.vfs["simobjects"]["airplanes"][self.project.airplane_folder]["aircraft.cfg"].real_path().parent.parent.parent.parent}\
"! Proceed?'):
                            self.set_children_state(self.win, tk.NORMAL)
                            return
        except (KeyError):
            pass
        
        # Do things
        self.agent.package(path)
        self.wait_agent()
        
        # Uh oh!
        if self.agent.error:
            messagebox.showerror(title='Configuration error', message=str(self.agent.error))
        self.agent.error = None
    
    def update_layout(self): # package.layout.create_layout
        self.set_children_state(self.win, tk.DISABLED)
        
        path = filedialog.askopenfilename(defaultextension='layout.json', filetypes=(
            ('Package layout', 'layout.json'),
        ), title='Choose layout file to update')
        if not path:
            self.set_children_state(self.win, tk.NORMAL)
            return
        self.agent.update_layout(path)
        
        self.set_children_state(self.win, tk.NORMAL)
    
    def on_close(self, event=None):
        if self.project_modified:
            answer = messagebox.askyesnocancel('Quit', 'Save project before exit?')
            if answer:
                self.save_project()
            elif answer is None:
                return
        self.win.destroy()
