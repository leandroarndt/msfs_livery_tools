from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from msfs_livery_tools.project import Project
from msfs_livery_tools.package import flags, dds_json
from msfs_livery_tools.gui.styles import FRAME_PADDING

class FlagsJSONFrame(ttk.Frame):
    project:Project
    descriptor:dds_json.Descriptor
    flags_file:flags.Flags
    texture_list:list
    texture:str = ''
    descriptor_modified:bool = False
    flags_modified:bool = False
    chooser_frame:ttk.Frame
    chooser_label:ttk.Label
    texture_chooser:ttk.Combobox
    refresh_button:ttk.Button
    
    # .DDS.json
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
    json_others_label:ttk.Label
    json_others_var:tk.StringVar
    json_others_entry:ttk.Entry
    save_json_button:ttk.Button
    
    # .flags
    flags_frame:ttk.LabelFrame
    no_reduce_var:tk.BooleanVar
    no_reduce_check:ttk.Checkbutton
    quality_high_var:tk.BooleanVar
    quality_high_check:ttk.Checkbutton
    precomputed_inverse_average_var:tk.BooleanVar
    precomputed_inverse_average_check:ttk.Checkbutton
    alpha_preservation_var:tk.BooleanVar
    alpha_preservation_check:ttk.Checkbutton
    flags_others_label:ttk.Label
    flags_others_var:tk.StringVar
    flags_others_entry:ttk.Entry
    save_flags_button:ttk.Button
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Chooser
        self.chooser_frame = ttk.Frame(self)
        self.chooser_frame.pack(side=tk.TOP, fill=tk.X)
        self.chooser_label = ttk.Label(self.chooser_frame, text='Choose texture: ')
        self.chooser_label.pack(side=tk.LEFT)
        self.refresh_button = ttk.Button(
            self.chooser_frame,
            text='Refresh',
            command=self.scan_textures,
            state=tk.DISABLED
        )
        self.refresh_button.pack(side=tk.RIGHT)
        self.texture_chooser = ttk.Combobox(self.chooser_frame, state=tk.DISABLED)
        self.texture_chooser.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.texture_chooser.bind('<<ComboboxSelected>>', self.chosen)
        
        # Descriptor
        self.json_frame = ttk.Labelframe(self, text='JSON descriptor', padding=FRAME_PADDING)
        self.json_frame.pack(fill=tk.X)
        self.compressed_var = tk.BooleanVar(self)
        self.compressed_check = ttk.Checkbutton(
            self.json_frame, text='Compressed',
            state=tk.DISABLED,
            variable=self.compressed_var,
            command=self.modified_json
        )
        self.compressed_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.mipmap_var = tk.BooleanVar(self)
        self.mipmap_check = ttk.Checkbutton(
            self.json_frame, text='MIP map',
            state=tk.DISABLED,
            variable=self.mipmap_var,
            command=self.modified_json
        )
        self.mipmap_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.normal_map_var = tk.BooleanVar(self)
        self.normal_map_check = ttk.Checkbutton(
            self.json_frame, text='Normal map',
            state=tk.DISABLED,
            variable=self.normal_map_var,
            command=self.modified_json
        )
        self.normal_map_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.no_gamma_var = tk.BooleanVar(self)
        self.no_gamma_check = ttk.Checkbutton(
            self.json_frame,
            text='No gamma correction',
            state=tk.DISABLED,
            variable=self.no_gamma_var,
            command=self.modified_json
        )
        self.no_gamma_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.composite_var = tk.BooleanVar(self)
        self.composite_check = ttk.Checkbutton(
            self.json_frame,
            text='Composite texture',
            state=tk.DISABLED,
            variable=self.composite_var,
            command=self.modified_json
        )
        self.composite_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.high_quality_var = tk.BooleanVar(self)
        self.high_quality_check = ttk.Checkbutton(
            self.json_frame,
            text='High Quality',
            state=tk.DISABLED,
            variable=self.high_quality_var,
            command=self.modified_json
        )
        self.high_quality_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.json_others_label = ttk.Label(self.json_frame, text='Other (comma separated): ')
        self.json_others_label.pack(side=tk.TOP, anchor=tk.W)
        self.json_others_var = tk.StringVar(self)
        self.json_others_var.trace_add('write', self.modified_json)
        self.json_others_entry = ttk.Entry(
            self.json_frame,
            textvariable=self.json_others_var,
            state=tk.DISABLED
        )
        self.json_others_entry.pack(side=tk.TOP, fill=tk.X)
        self.save_json_button = ttk.Button(
            self.json_frame,
            text='Save texture descriptor',
            command=self.save_json,
            state=tk.DISABLED
        )
        self.save_json_button.pack(side=tk.TOP, fill=tk.X)
        
        # Flags
        self.flags_frame = ttk.LabelFrame(self, text='".flags" file', padding=FRAME_PADDING)
        self.flags_frame.pack(fill=tk.X)
        self.no_reduce_var = tk.BooleanVar(self)
        self.no_reduce_check = ttk.Checkbutton(
            self.flags_frame,
            text='No reduce',
            state=tk.DISABLED,
            variable=self.no_reduce_var,
            command=self.modified_flags
        )
        self.no_reduce_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.quality_high_var = tk.BooleanVar(self)
        self.quality_high_check = ttk.Checkbutton(
            self.flags_frame, text='Quality high',
            state=tk.DISABLED,
            variable=self.quality_high_var,
            command=self.modified_flags
        )
        self.quality_high_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.precomputed_inverse_average_var = tk.BooleanVar(self)
        self.precomputed_inverse_average_check = ttk.Checkbutton(
            self.flags_frame,
            text='Precomputed inverse avarage',
            state=tk.DISABLED,
            variable=self.precomputed_inverse_average_var,
            command=self.modified_flags
        )
        self.precomputed_inverse_average_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.alpha_preservation_var = tk.BooleanVar(self)
        self.alpha_preservation_check = ttk.Checkbutton(
            self.flags_frame,
            text='Alpha preservation',
            variable=self.alpha_preservation_var,
            state=tk.DISABLED,
            command=self.modified_flags
        )
        self.alpha_preservation_check.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.flags_others_label = ttk.Label(self.flags_frame, text='Other (comma separated): ')
        self.flags_others_label.pack(side=tk.TOP, anchor=tk.W)
        self.flags_others_var = tk.StringVar(self)
        self.flags_others_entry = ttk.Entry(
            self.flags_frame,
            textvariable=self.flags_others_var,
            state=tk.DISABLED
        )
        self.flags_others_var.trace_add('write', self.modified_flags)
        self.flags_others_entry.pack(side=tk.TOP, fill=tk.X)
        self.save_flags_button = ttk.Button(
            self.flags_frame,
            text='Save ".flags" file',
            command=self.save_flags,
            state=tk.DISABLED
        )
        self.save_flags_button.pack(side=tk.TOP, fill=tk.X)
    
    def set_state(self, state:str):
        for child in self.json_frame.children.values():
            child['state'] = state
        for child in self.flags_frame.children.values():
            child['state'] = state
    
    def scan_textures(self, project:Project|None=None):
        if project:
            self.project = project
        elif self.project:
            if not self.modified_alert():
                return
        else:
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
        self.save_flags_button['state'] = tk.DISABLED
        self.descriptor = None
        self.flags_file = None
        
        self.descriptor_modified = False
        self.flags_modified = False
    
    def chosen(self, event):
        if not self.modified_alert():
            self.texture_chooser.set(self.texture)
            return
        self.texture = self.texture_chooser.get()
        
        # Descriptor
        try:
            self.descriptor = dds_json.Descriptor.open((self.project.get_texture_dir() / self.texture).with_suffix('.dds.json'))
            print(f'Opened descriptor "{self.descriptor.file.name}"')
        except FileNotFoundError:
            self.descriptor = dds_json.Descriptor.for_texture(self.project.get_texture_dir() / self.texture)
            print(f'Created descriptor object for "{self.texture}"')
        
        self.compressed_var.set(dds_json.Descriptor.COMPRESSED in self.descriptor.flags)
        self.mipmap_var.set(dds_json.Descriptor.MIPMAP in self.descriptor.flags)
        self.normal_map_var.set(dds_json.Descriptor.NORMAL_MAP in self.descriptor.flags)
        self.no_gamma_var.set(dds_json.Descriptor.NO_GAMMA in self.descriptor.flags)
        self.composite_var.set(dds_json.Descriptor.COMPOSITE in self.descriptor.flags)
        self.high_quality_var.set(dds_json.Descriptor.HIGH_QUALITY in self.descriptor.flags)
        
        self.json_others_var.set('')
        for flag in self.descriptor.flags:
            if flag not in (
                dds_json.Descriptor.COMPRESSED,
                dds_json.Descriptor.MIPMAP,
                dds_json.Descriptor.NORMAL_MAP,
                dds_json.Descriptor.NO_GAMMA,
                dds_json.Descriptor.COMPOSITE,
                dds_json.Descriptor.HIGH_QUALITY,
            ):
                if self.json_others_var.get():
                    self.json_others_var.set(','.join([self.json_others_var.get(), flag]))
                else:
                    self.json_others_var.set(flag)
        
        # Flags
        try:
            self.flags_file = flags.Flags.open((self.project.get_texture_dir() / self.texture).with_suffix('.dds.flags'))
            print(f'Opened ".flags" file "{self.flags_file.file.name}".')
        except FileNotFoundError:
            self.flags_file= flags.Flags([], (self.project.get_texture_dir() / self.texture).with_suffix('.dds.flags'))
            print(f'Created flags object for "{self.texture}".')
        
        self.no_reduce_var.set(flags.Flags.NO_REDUCE in self.flags_file.flags)
        self.quality_high_var.set(flags.Flags.QUALITY_HIGH in self.flags_file.flags)
        self.precomputed_inverse_average_var.set(flags.Flags.PRECOMPUTED_INVERSE_AVERAGE in self.flags_file.flags)
        self.alpha_preservation_var.set(flags.Flags.ALPHA_PRESERVATION in self.flags_file.flags)
        
        self.flags_others_var.set('')
        for flag in self.flags_file.flags:
            if flag not in(
                flags.Flags.NO_REDUCE,
                flags.Flags.QUALITY_HIGH,
                flags.Flags.PRECOMPUTED_INVERSE_AVERAGE,
                flags.Flags.ALPHA_PRESERVATION,
            ):
                if self.flags_others_var.get():
                    self.flags_others_var.set(','.join(self.flags_others_var.get(), flag))
                else:
                    self.flags_others_var.set(flag)
        
        # GUI state
        self.set_state(tk.NORMAL)
        self.save_json_button['state'] = tk.DISABLED
        self.save_flags_button['state'] = tk.DISABLED
        
        self.descriptor_modified = False
        self.flags_modified = False
    
    def modified_json(self, *args, **kwargs):
        self.save_json_button['state'] = tk.NORMAL
        self.descriptor_modified = True
    
    def save_json(self):
        self.descriptor.flags = set()
        if self.compressed_var.get():
            self.descriptor.flags.add(dds_json.Descriptor.COMPRESSED)
        if self.mipmap_var.get():
            self.descriptor.flags.add(dds_json.Descriptor.MIPMAP)
        if self.normal_map_var.get():
            self.descriptor.flags.add(dds_json.Descriptor.NORMAL_MAP)
        if self.no_gamma_var.get():
            self.descriptor.flags.add(dds_json.Descriptor.NO_GAMMA)
        if self.composite_var.get():
            self.descriptor.flags.add(dds_json.Descriptor.COMPOSITE)
        if self.high_quality_var.get():
            self.descriptor.flags.add(dds_json.Descriptor.HIGH_QUALITY)
        for extra in self.json_others_var.get().split(','):
            if extra.strip(' "\''):
                self.descriptor.flags.add(extra.strip(' "\''))
        
        self.descriptor.save()
        self.descriptor_modified = False
        self.save_json_button['state'] = tk.DISABLED
    
    def modified_flags(self, *args, **kwargs):
        self.save_flags_button['state'] = tk.NORMAL
        self.flags_modified = True
    
    def save_flags(self):
        self.flags_file.flags = set()
        if self.no_reduce_var.get():
            self.flags_file.flags.add(flags.Flags.NO_REDUCE)
        if self.quality_high_var.get():
            self.flags_file.flags.add(flags.Flags.QUALITY_HIGH)
        if self.precomputed_inverse_average_var.get():
            self.flags_file.flags.add(flags.Flags.PRECOMPUTED_INVERSE_AVERAGE)
        if self.alpha_preservation_var.get():
            self.flags_file.flags.add(flags.Flags.ALPHA_PRESERVATION)
        for extra in self.flags_others_var.get().split(','):
            if extra.strip(' "\''):
                self.flags_file.flags.add(extra.strip(' "\''))
        
        self.flags_file.save()
        self.flags_modified = False
        self.save_flags_button['state'] = tk.DISABLED
    
    def modified_alert(self)->bool:
        """Checks for modified descriptor and flags, asks to save and returns whether to proceed or not.
        """
        
        if self.descriptor_modified or self.flags_modified:
            if self.descriptor_modified and self.flags_modified:
                message = 'Descriptor and ".flags" file modified. Save changes?'
            elif self.descriptor_modified:
                message = 'Descriptor (".dds.json") modified. Save changes?'
            elif self.flags_modified:
                message = '".Flags" file modified. Save changes?'
                
            answer = messagebox.askyesnocancel(title='Save changes?', message=message)
            if answer is None:
                return False
            if answer == True:
                if self.descriptor_modified:
                    self.save_json()
                if self.flags_modified:
                    self.save_flags()
            return True
        return True
