"""Project configuration manager"""
from pathlib import Path
import configparser, ast

class Project(object):
    """Project handler with tools to create its structure."""
    
    _config:configparser.ConfigParser
    _parsers:dict[configparser.ConfigParser] = {}
    file:Path
    
    def __delattr__(self, name):
        attributes = {
            'join_model_and_textures': ('PROJECT', 'join_model_and_textures'),
            'origin': ('PROJECT', 'origin'),
            'base_container': ('AIRCRAFT', 'base_container'),
            'title': ('PROJECT', 'title'),
            'display_name': ('PROJECT', 'display_name'),
            'airplane_folder': ('PROJECT', 'airplane_folder'),
            'manufacturer': ('PROJECT', 'manufacturer'),
            'creator': ('PROJECT', 'creator'),
            'version': ('PROJECT', 'version'),
            'minimum_game_version': ('PROJECT', 'minimum_game_version'),
            'suffix': ('AIRCRAFT', 'suffix'),
            'tail_number': ('AIRCRAFT', 'tail_number'),
            'include_model': ('AIRCRAFT', 'model'),
            'include_panel': ('AIRCRAFT', 'panel'),
            'include_sound': ('AIRCRAFT', 'sound'),
            'include_texture': ('AIRCRAFT', 'texture'),
            'registration_font_color': ('PANEL', 'font_color'),
            'registration_stroke_color': ('PANEL', 'stroke_color'),
            'registration_stroke_size': ('PANEL', 'stroke_size'),
        }
        for property, location in attributes.items():
            if property == name:
                try:
                    remove = __class__._parsers[self.file.as_posix()].remove_option(location[0], location[1])
                    if not remove:
                        raise configparser.NoOptionError(location[1], location[0])
                except (configparser.NoOptionError, configparser.NoSectionError):
                    raise AttributeError(f'"{self} has no attribute "{name}" or it has not been set.')
    
    # General settings
    @property
    def join_model_and_textures(self)->bool:
        return True if __class__._parsers[self.file.as_posix()]['PROJECT']['join_model_and_textures'] == 'True' else False
    
    @join_model_and_textures.setter
    def join_model_and_textures(self, value:bool):
        __class__._parsers[self.file.as_posix()]['PROJECT']['join_model_and_textures'] = str(value)
    
    @property
    def origin(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['origin']
    
    @origin.setter
    def origin(self, path:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['origin'] = str(path) # Avoid Path objects
        try: # Tries to get the first subdirectory at SimObjects\Airplanes
            container_path = Path(path) / 'SimObjects' / 'Airplanes'
            for subdir in container_path.glob('*/'):
                container = f'..\{subdir.name}'
                break
        except:
            container = Path(path).name.split('-')
            try:
                container.remove('aircraft')
                container = f'..\{"_".join(container)}'
            except ValueError: # 'aircraft' not in origin name
                pass
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['base_container'] = container
        
    @property
    def base_container(self)->str:
        return __class__._parsers[self.file.as_posix()]['AIRCRAFT']['base_container']
    
    @base_container.setter
    def base_container(self, path:str):
        if str(path).startswith('..\\'):
            __class__._parsers[self.file.as_posix()]['AIRCRAFT']['base_container'] = str(path)    
            __class__._parsers[self.file.as_posix()]['PROJECT']['origin'] = Path(path).absolute.parent.parent.parent
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['base_container'] = f'..\{str(Path(path).name)}' # Avoid Path objects
        __class__._parsers[self.file.as_posix()]['PROJECT']['origin'] = str(Path(path).parent.parent.parent)
    
    @property
    def title(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['title']
    
    @title.setter
    def title(self, value:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['title'] = value

    @property
    def display_name(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['display_name']
    
    @display_name.setter
    def display_name(self, value:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['display_name'] = value
    
    @property
    def airplane_folder(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['airplane_folder']
    
    @airplane_folder.setter
    def airplane_folder(self, value:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['airplane_folder'] = value
    
    @property
    def manufacturer(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['manufacturer']
    
    @manufacturer.setter
    def manufacturer(self, value:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['manufacturer'] = value
    
    @property
    def creator(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['creator']
    
    @creator.setter
    def creator(self, value:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['creator'] = value
    
    @property
    def version(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['version']
    
    @version.setter
    def version(self, value:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['version'] = value
    
    @property
    def minimum_game_version(self)->str:
        return __class__._parsers[self.file.as_posix()]['PROJECT']['minimum_game_version']
    
    @minimum_game_version.setter
    def minimum_game_version(self, value:str):
        __class__._parsers[self.file.as_posix()]['PROJECT']['minimum_game_version'] = value
    
    # Aircraft.cfg specific settings
    @property
    def suffix(self)->str:
        return __class__._parsers[self.file.as_posix()]['AIRCRAFT']['suffix']
    
    @suffix.setter
    def suffix(self, value:str):
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['suffix'] = value
    
    @property
    def tail_number(self)->str:
        return __class__._parsers[self.file.as_posix()]['AIRCRAFT']['tail_number']
    
    @tail_number.setter
    def tail_number(self, value:str):
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['tail_number'] = value
    
    # Which folders to use at the package
    @property
    def include_model(self)->bool:
        try:
            return True if __class__._parsers[self.file.as_posix()]['AIRCRAFT']['model'] == 'True' else False
        except KeyError:
            return False
    
    @include_model.setter
    def include_model(self, value:bool):
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['model'] = str(value)
    
    @property
    def include_panel(self)->bool:
        try:
            return True if __class__._parsers[self.file.as_posix()]['AIRCRAFT']['panel'] == 'True' else False
        except KeyError:
            return False
    
    @include_panel.setter
    def include_panel(self, value:bool):
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['panel'] = str(value)
    
    @property
    def include_sound(self)->bool:
        try:
            return True if __class__._parsers[self.file.as_posix()]['AIRCRAFT']['sound'] == 'True' else False
        except KeyError:
            return False
    
    @include_sound.setter
    def include_sound(self, value:bool):
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['sound'] = str(value)
    
    @property
    def include_texture(self)->bool:
        try:
            return True if __class__._parsers[self.file.as_posix()]['AIRCRAFT']['texture'] == 'True' else False
        except KeyError:
            return True
    
    @include_texture.setter
    def include_texture(self, value:bool):
        __class__._parsers[self.file.as_posix()]['AIRCRAFT']['texture'] = str(value)
    
    # External registration settings (panel.cfg)
    @property
    def registration_font_color(self)->str:
        return __class__._parsers[self.file.as_posix()]['PANEL']['font_color']
    
    @registration_font_color.setter
    def registration_font_color(self, value:str):
        __class__._parsers[self.file.as_posix()]['PANEL']['font_color'] = value
    
    @property
    def registration_stroke_color(self)->str:
        return __class__._parsers[self.file.as_posix()]['PANEL']['stroke_color']
    
    @registration_stroke_color.setter
    def registration_stroke_color(self, value:str):
        __class__._parsers[self.file.as_posix()]['PANEL']['stroke_color'] = value
    
    @property
    def registration_stroke_size(self)->int:
        return int(__class__._parsers[self.file.as_posix()]['PANEL']['stroke_size'])
    
    @registration_stroke_size.setter
    def registration_stroke_size(self, value:int):
        __class__._parsers[self.file.as_posix()]['PANEL']['stroke_size'] = str(value)
    
    #TODO: Maybe a texture class?
    def texture(self, name:str, property:str, value=None, delete=False)->str:
        """Access to texture properties.

        Args:
            name (str): texture name.
            property (str): property being accessed.
            value (_type_, optional): if provided, set value to the string representation
                of this argument. Defaults to None.
            delete (bool, optional): delete property.
        
        Return: property value.
        """
        key = f'{name}_{property}'
        if value is not None:
            __class__._parsers[self.file.as_posix()]['TEXTURES'][key] = str(value)
        
        # Return list:
        if __class__._parsers[self.file.as_posix()]['TEXTURES'][key].startswith('[') and \
            __class__._parsers[self.file.as_posix()]['TEXTURES'][key].endswith(']'):
                return ast.literal_eval(__class__._parsers[self.file.as_posix()]['TEXTURES'][key])
        
        # Return string:
        return __class__._parsers[self.file.as_posix()]['TEXTURES'][key]
    
    def __init__(self, project_path:str, join_model_and_textures=False):
        """Project handler with tools to create its structure.

        Args:
            project_path (str): path to project directory.
            join_model_and_textures (bool, optional): whether to create only one
                directory with both model and texture files. Defaults to True.
        """
        self.file = Path(project_path, 'livery.ini')
        if Path(project_path, 'livery.ini').as_posix() not in __class__._parsers:
            if self.file not in __class__._parsers:
                __class__._parsers[self.file.as_posix()] = configparser.ConfigParser()
            if self.file.is_file():
                __class__._parsers[self.file.as_posix()].read(self.file, encoding='utf-8')
            else:
                __class__._parsers[self.file.as_posix()]['PROJECT'] = {
                    'join_model_and_textures': join_model_and_textures
                }
                __class__._parsers[self.file.as_posix()]['AIRCRAFT'] = {}
                __class__._parsers[self.file.as_posix()]['PANEL'] = {}
                __class__._parsers[self.file.as_posix()]['TEXTURES'] = {}
                Path(project_path).mkdir(exist_ok=True)
                self.create_structure()
                self.save()
    
    def save(self):
        with open(self.file, 'w') as f:
            __class__._parsers[self.file.as_posix()].write(f)
    
    def close(self):
        del __class__._parsers[self.file.as_posix()]
    
    def create_structure(self):
        Path(self.file.parent, 'panel').mkdir(exist_ok=True)
        Path(self.file.parent, 'sound').mkdir(exist_ok=True)
        Path(self.file.parent, 'model').mkdir(exist_ok=True)
        if not self.join_model_and_textures:
            Path(self.file.parent, 'texture').mkdir(exist_ok=True)
