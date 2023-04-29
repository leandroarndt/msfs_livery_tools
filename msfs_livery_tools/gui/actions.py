from pathlib import Path
from msfs_livery_tools.project import Project
from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.compression import dds

class Agent(object):
    project:Project
    settings:AppSettings
    
    def __init__(self):
        self.settings = AppSettings()
    
    def extract_textures(self, gltf:str|Path):
        original_suffix = Path(gltf).parent.suffix
        texture_dir = Path(gltf).parent.parent / Path('texture', original_suffix)
        if self.project.join_model_and_textures:
            output_dir = Path(self.project.file).parent / 'model'
        else:
            output_dir = Path(self.project.file).parent / 'texture'
        try:
            dds.from_glft(gltf, texture_dir, output_dir, self.settings.texconv_path)
        except:
            raise ValueError
