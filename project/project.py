"""Project configuration manager"""
from pathlib import Path
import configparser

class Project(object):
    """Project handler with tools to create its structure."""
    
    _config:configparser
    file:Path
    
    # General settings
    @property
    def join_model_and_textures(self):
        return self._config['PROJECT']['join_model_and_textures']
    
    @join_model_and_textures.setter
    def join_model_and_textures(self, value:str):
        self._config['PROJECT']['join_model_and_textures'] = value
    
    @property
    def origin(self):
        return self._config['PROJECT']['origin']
    
    @origin.setter
    def origin(self, path:str):
        self._config['PROJECT']['origin'] = path
        self._config['AIRCRAFT']['base_container'] = f'..\{Path(path).name}'
    
    @property
    def title(self):
        return self._config['PROJECT']['title']
    
    @title.setter
    def title(self, value:str):
        self._config['PROJECT']['title'] = value
    
    @property
    def airplane_folder(self):
        return self._config['PROJECT']['airplane_folder']
    
    @airplane_folder.setter
    def airplane_folder(self, value:str):
        self._config['PROJECT']['airplane_folder'] = value
    
    @property
    def manufacturer(self):
        return self._config['PROJECT']['manufacturer']
    
    @manufacturer.setter
    def manufacturer(self, value:str):
        self._config['PROJECT']['manufacturer'] = value
    
    @property
    def creator(self):
        return self._config['PROJECT']['creator']
    
    @manufacturer.setter
    def creator(self, value:str):
        self._config['PROJECT']['creator'] = value
    
    @property
    def version(self):
        return self._config['PROJECT']['version']
    
    @version.setter
    def version(self, value:str):
        self._config['PROJECT']['version'] = value
    
    @property
    def minimum_game_version(self):
        return self._config['PROJECT']['minimum_game_version']
    
    @minimum_game_version.setter
    def minimum_game_version(self, value:str):
        self._config['PROJECT']['minimum_game_version'] = value
    
    # Aircraft.cfg specific settings
    @property
    def suffix(self):
        return self._config['AIRCRAFT']['suffix']
    
    @suffix.setter
    def suffix(self, value:str):
        self._config['PROJECT']['suffix'] = value
    
    @property
    def suffix(self):
        return self._config['AIRCRAFT']['suffix']
    
    @suffix.setter
    def suffix(self, value:str):
        self._config['PROJECT']['suffix'] = value
    
    @property
    def tail_number(self):
        return self._config['AIRCRAFT']['tail_number']
    
    @tail_number.setter
    def tail_number(self, value:str):
        self._config['PROJECT']['tail_number'] = value
    
    # Which folders to use at the package
    @property
    def model(self):
        return self._config['AIRCRAFT']['model']
    
    @model.setter
    def model(self, value:str):
        self._config['PROJECT']['model'] = value
    
    @property
    def panel(self):
        return self._config['AIRCRAFT']['panel']
    
    @panel.setter
    def panel(self, value:str):
        self._config['PROJECT']['panel'] = value
    
    @property
    def sound(self):
        return self._config['AIRCRAFT']['sound']
    
    @sound.setter
    def sound(self, value:str):
        self._config['PROJECT']['sound'] = value
    
    @property
    def texture(self):
        return self._config['AIRCRAFT']['texture']
    
    @texture.setter
    def texture(self, value:str):
        self._config['PROJECT']['panel'] = value
    
    # External registration settings (panel.cfg)
    @property
    def font_color(self):
        return self._config['PANEL']['font_color']
    
    @font_color.setter
    def font_color(self, value:str):
        self._config['PANEL']['font_color'] = value
    
    @property
    def stroke_color(self):
        return self._config['PANEL']['stroke_color']
    
    @stroke_color.setter
    def stroke_color(self, value:str):
        self._config['PANEL']['stroke_color'] = value
    
    @property
    def stroke_size(self):
        return self._config['PANEL']['stroke_size']
    
    @stroke_size.setter
    def stroke_size(self, value:str):
        self._config['PANEL']['stroke_size'] = value
    
    # Direct access to 'TEXTURES' section
    @property
    def textures(self):
        return self._config['TEXTURES']
    
    @textures.setter
    def textures(self, value:dict):
        self._config['TEXTURES'] = value
    
    def __init__(self, project_path:str, join_model_and_textures=True):
        """Project handler with tools to create its structure.

        Args:
            project_path (str): path to project directory.
            join_model_and_textures (bool, optional): whether to create only one
                directory with both model and texture files. Defaults to True.
        """
        self.file = Path(project_path, 'livery.ini')
        self._config = configparser.ConfigParser()
        if self.file.is_file():
            self._config.read(self.file)
        else:
            self._config['PROJECT'] = {
                'join_model_and_textures': join_model_and_textures
            }
            self._config['AIRCRAFT'] = {}
            self._config['PANEL'] = {}
            self._config['TEXTURES'] = {}
            Path(project_path).mkdir(exist_ok=True)
            self.create_structure()
            self.save()
    
    def save(self):
        with open(self.file, 'w') as f:
            self._config.write(f)
    
    def create_structure(self):
        base_dir = Path(self.file).parent
        Path(self.file.parent, 'panel').mkdir(exist_ok=True)
        Path(self.file.parent, 'sound').mkdir(exist_ok=True)
        Path(self.file.parent, 'model').mkdir(exist_ok=True)
        if not self.join_model_and_textures:
            Path(self.file.parent, 'texture').mkdir(exist_ok=True)
