"""Deals with application settings."""
import configparser
from pathlib import Path

class AppSettings(object):
    _config_parser:configparser.ConfigParser = None
    file:Path
    
    @property
    def compress_textures_on_build(self)->bool:
        try:
            return True if __class__._config_parser['BUILD']['compress_textures'] == 'True' else False
        except KeyError:
            return True
    
    @compress_textures_on_build.setter
    def compress_textures_on_build(self, value:bool):
        __class__._config_parser['BUILD']['compress_textures'] = str(value)
    
    @property
    def texconv_path(self)->str:
        return __class__._config_parser['GENERAL']['texconv_path']
    
    @texconv_path.setter
    def texconv_path(self, path:str):
        __class__._config_parser['GENERAL']['texconv_path'] = path
    
    @property
    def recent_files(self)->list[str]:
        try:
            return __class__._config_parser['GENERAL']['recent'].split('|')
        except KeyError:
            return []
    
    @recent_files.setter
    def recent_files(self, path:str):
        try:
            recent = __class__._config_parser['GENERAL']['recent'].split('|')
            if path in recent:
                recent.remove(path)
            recent = [path] + recent
            recent = recent[:5]
            __class__._config_parser['GENERAL']['recent'] = '|'.join(recent)
        except KeyError:
            __class__._config_parser['GENERAL']['recent'] = str(path)
    
    def __init__(self, *args, **kwargs):
        self.file = Path(Path.home(), '.msfs_livery_tools.cfg')
        if __class__._config_parser is None:
            __class__._config_parser = configparser.ConfigParser()
        __class__._config_parser.read(self.file)
        for section in ('GENERAL', 'BUILD'):
            if section not in __class__._config_parser.sections():
                __class__._config_parser.add_section(section)
                self.save()
        
    def save(self, *args, **kwargs):
        with open(self.file, 'w') as f:
            __class__._config_parser.write(f, *args, **kwargs)
