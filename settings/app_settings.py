"""Deals with application settings."""
import configparser
from pathlib import Path

class AppSettings(object):
    _config_parser:configparser.ConfigParser = None
    file:Path
    
    @property
    def texconv_path(self)->str:
        return __class__._config_parser['GENERAL']['texconv_path']
    
    @texconv_path.setter
    def texconv_path(self, path:str):
        __class__._config_parser['GENERAL']['texconv_path'] = path
    
    def __init__(self, *args, **kwargs):
        self.file = Path(Path.home(), '.msfs_livery_tools.cfg')
        if __class__._config_parser is None:
            __class__._config_parser = configparser.ConfigParser()
        __class__._config_parser.read(self.file)
        if 'GENERAL' not in __class__._config_parser.sections():
            __class__._config_parser.add_section('GENERAL')
            self.save()
        
    def save(self, *args, **kwargs):
        with open(self.file, 'w') as f:
            __class__._config_parser.write(f, *args, **kwargs)
