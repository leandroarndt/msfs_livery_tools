from pathlib import Path
import tkinter as tk
from tkinter import ttk
from msfs_livery_tools.project import Project
from msfs_livery_tools.package import flags, dds_json
from msfs_livery_tools.gui.styles import FRAME_PADDING

class FlagsJSONFrame(ttk.Frame):
    project:Project
    descriptor:dds_json.Descriptor
    texture_list:list
    chooser_frame:ttk.Frame
    chooser_label:ttk.Label
    texture_chooser:ttk.Combobox
    refresh_button:ttk.Button
    
    # .DDS.json
    json_modified:bool = False
    json_frame:ttk.LabelFrame
    compressed_var:tk.BooleanVar
    compressed_check:ttk.Checkbutton
    mipmap_var:tk.BooleanVar
    mipmap_check:ttk.Checkbutton
    normal_map_var:tk.BooleanVar
    normal_map_check:ttk.Checkbutton
    no_gamma_var:tk.BooleanVar
    no_gamma_check:ttk.Checkbutton
    composite_var:tk.BooleanVar
    composite_check:ttk.Checkbutton
    high_quality_var:tk.BooleanVar
    high_quality_check:ttk.Checkbutton
    json_others_var:tk.StringVar
    json_others_entry:ttk.Entry
    save_json_button:ttk.Button
    
    # .flags
    flags_frame:ttk.LabelFrame
    no_reduce_check:ttk.Checkbutton
    quality_high_check:ttk.Checkbutton
    precomputed_inverse_average_check:ttk.Checkbutton
    flags_others:ttk.Entry
    save_flags_button:ttk.Button
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Chooser
        self.chooser_frame = ttk.Frame(self)
        self.chooser_frame.pack(side=tk.TOP, fill=tk.X)
        self.chooser_label = ttk.Label(self.chooser_frame, text='Choose texture: ')
        self.chooser_label.pack(side=tk.LEFT)
        self.refresh_button = ttk.Button(self.chooser_frame, text='Refresh', command=self.scan_textures, state=tk.DISABLED)
        self.refresh_button.pack(side=tk.RIGHT)
        self.texture_chooser = ttk.Combobox(self.chooser_frame, state=tk.DISABLED)
        self.texture_chooser.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.texture_chooser.bind('<<ComboboxSelected>>', self.chosen)
        
        # Descriptor
        self.json_frame = ttk.Labelframe(self, text='JSON descriptor', padding=FRAME_PADDING)
        self.json_frame.pack(fill=tk.X)
        self.compressed_var = tk.BooleanVar(self)
        self.compressed_check = ttk.Checkbutton(self.json_frame, text='Compressed', state=tk.DISABLED, variable=self.compressed_var, command=self.modified_json)
        self.compressed_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.mipmap_var = tk.BooleanVar(self)
        self.mipmap_check = ttk.Checkbutton(self.json_frame, text='MIP map', state=tk.DISABLED, variable=self.mipmap_var, command=self.modified_json)
        self.mipmap_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.normal_map_var = tk.BooleanVar(self)
        self.normal_map_check = ttk.Checkbutton(self.json_frame, text='Normal map', state=tk.DISABLED, variable=self.normal_map_var, command=self.modified_json)
        self.normal_map_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.no_gamma_var = tk.BooleanVar(self)
        self.no_gamma_check = ttk.Checkbutton(self.json_frame, text='No gamma correction', state=tk.DISABLED, variable=self.no_gamma_var, command=self.modified_json)
        self.no_gamma_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.composite_var = tk.BooleanVar(self)
        self.composite_check = ttk.Checkbutton(self.json_frame, text='Composite texture', state=tk.DISABLED, variable=self.composite_var, command=self.modified_json)
        self.composite_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.high_quality_var = tk.BooleanVar(self)
        self.high_quality_check = ttk.Checkbutton(self.json_frame, text='High Quality', state=tk.DISABLED, variable=self.high_quality_var, command=self.modified_json)
        self.high_quality_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.json_others_label = ttk.Label(self.json_frame, text='Other (comma separated): ')
        self.json_others_label.pack(side=tk.TOP, anchor=tk.W)
        self.json_others_var = tk.StringVar(self)
        self.json_others_var.trace_add('write', self.modified_json)
        self.json_others_entry = ttk.Entry(self.json_frame, textvariable=self.json_others_var, state=tk.DISABLED)
        self.json_others_entry.pack(side=tk.TOP, fill=tk.X)
        self.save_json_button = ttk.Button(self.json_frame, text='Save texture descriptor', command=self.save_json, state=tk.DISABLED)
        self.save_json_button.pack(side=tk.TOP, fill=tk.X)
    
    def set_state(self, state:str):
        for child in self.json_frame.children.values():
            child['state'] = state
    
    def scan_textures(self, project:Project|None=None):
        if project:
            self.project = project
        if not self.project:
            return
        self.texture_chooser.set('')
        texture_folder = self.project.get_texture_dir()
        file_list = list(texture_folder.glob('*.png')) + list(texture_folder.glob('*.dds'))
        self.texture_list = set()
        for file in file_list:
            self.texture_list.add(file.with_suffix('.DDS').name)
        self.texture_list = list(self.texture_list)
        self.texture_list.sort()
        self.texture_chooser['values'] = tuple(self.texture_list)
        
        # Disable entries
        self.set_state(tk.DISABLED)
        self.save_json_button['state'] = tk.DISABLED
        self.descriptor = None
    
    def chosen(self, event):
        texture = self.texture_chooser.get()
        try:
            self.descriptor = dds_json.Descriptor.open((self.project.get_texture_dir() / texture).with_suffix('.dds.json'))
            print(f'Opened descriptor "{self.descriptor.file.name}"')
        except FileNotFoundError:
            self.descriptor = dds_json.Descriptor.for_texture(self.project.get_texture_dir() / texture)
            print(f'Creating descriptor "{self.descriptor.file.name}"')
        
        self.compressed_var.set(dds_json.Descriptor.COMPRESSED in self.descriptor.flags)
        self.mipmap_var.set(dds_json.Descriptor.MIPMAP in self.descriptor.flags)
        self.normal_map_var.set(dds_json.Descriptor.NORMAL_MAP in self.descriptor.flags)
        self.no_gamma_var.set(dds_json.Descriptor.NO_GAMMA in self.descriptor.flags)
        self.composite_var.set(dds_json.Descriptor.COMPOSITE in self.descriptor.flags)
        self.high_quality_var.set(dds_json.Descriptor.HIGH_QUALITY in self.descriptor.flags)
        
        self.set_state(tk.NORMAL)
        self.save_json_button['state'] = tk.DISABLED
    
    def modified_json(self, *args, **kwargs):
        self.json_modified = True
        self.save_json_button['state'] = tk.NORMAL
    
    def save_json(self):
        self.descriptor.flags = []
        if self.compressed_var.get():
            self.descriptor.flags.append(dds_json.Descriptor.COMPRESSED)
        if self.mipmap_var.get():
            self.descriptor.flags.append(dds_json.Descriptor.MIPMAP)
        if self.normal_map_var.get():
            self.descriptor.flags.append(dds_json.Descriptor.NORMAL_MAP)
        if self.no_gamma_var.get():
            self.descriptor.flags.append(dds_json.Descriptor.NO_GAMMA)
        if self.composite_var.get():
            self.descriptor.flags.append(dds_json.Descriptor.COMPOSITE)
        if self.high_quality_var.get():
            self.descriptor.flags.append(dds_json.Descriptor.HIGH_QUALITY)
        for extra in self.json_others_var.get().split(','):
            self.descriptor.flags.append(extra.strip(' "\''))
        
        self.descriptor.save()
        self.json_modified = False
        self.save_json_button['state'] = tk.DISABLED
