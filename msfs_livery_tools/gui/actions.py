from pathlib import Path
from tkinter import ttk
from typing import Callable
from threading import Thread
from msfs_livery_tools.project import Project
from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.compression import dds
from msfs_livery_tools.package import dds_json

class Runner(Thread):
    """Abstract thread for tasks with indeterminate length/accomplishment."""
    task:Callable
    args:list
    kwargs:dict
    
    def __init__(self, task:Callable, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        self.task(*self.args, **self.kwargs)

class Agent(object):
    project:Project
    settings:AppSettings
    progress_bar:ttk.Progressbar
    progress_bar_maximum:int
    running:bool = False
    
    def _texture_dir(self)->Path:
        if self.project.join_model_and_textures:
            return Path(self.project.file).parent / 'model'
        else:
            return Path(self.project.file).parent / 'texture'
        
    def __init__(self, progress_bar):
        self.settings = AppSettings()
        self.progress_bar = progress_bar
        self.progress_bar_maximum = self.progress_bar['maximum']
    
    def monitor(self, thread:Runner):
        if thread.is_alive():
            self.running = True
            self.progress_bar['mode'] = 'indeterminate'
            self.progress_bar.start()
            self.progress_bar.after(100, lambda: self.monitor(thread))
        else:
            self.progress_bar.stop()
            self.restore_progress_bar()
            self.running = False
    
    def prepare_progress_bar(self, maximum):
        self.progress_bar['maximum'] = maximum
        self.progress_bar['value'] = 0
        self.progress_bar['mode'] = 'determinate'
    
    def restore_progress_bar(self):
        self.progress_bar['mode'] = 'determinate'
        self.progress_bar['maximum'] = self.progress_bar_maximum
        self.progress_bar['value'] = 0
    
    def extract_textures(self, gltf:str|Path):
        original_suffix = Path(gltf).parent.suffix
        texture_dir = Path(gltf).parent.parent / Path('texture', original_suffix)
        output_dir = self._texture_dir()
        thread = Runner(dds.from_glft, gltf, texture_dir, output_dir, self.settings.texconv_path)
        thread.start()
        self.monitor(thread)
    
    def compress_textures(self):
        texture_dir = self._texture_dir()
        textures = list(texture_dir.glob('*.png'))
        self.prepare_progress_bar(len(textures))
        for file in textures:
            self.progress_bar['value'] += 1
            self.progress_bar.update()
            print(f'Compressing "{file}"…')
            dds.convert(file, texture_dir, self.settings.texconv_path)
        self.restore_progress_bar()
    
    def create_dds_descriptors(self):
        texture_dir = self._texture_dir()
        textures = list(texture_dir.glob('*.dds'))
        self.prepare_progress_bar(len(textures))
        for file in textures:
            self.progress_bar['value'] += 1
            self.progress_bar.update()
            print(f'Describing "{file}"…')
            dds_json.create_description(file)
        self.restore_progress_bar()
